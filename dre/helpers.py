import locale
from typing import List, Dict, Any, Tuple
from itertools import groupby
from fluxo_caixa.models import FluxoCaixa
from core.models import Indicador
from datetime import date


class DREHelper:

    @staticmethod
    def _group_by_key(fluxos: List[FluxoCaixa], key_func) -> Dict:
        """Generalized function to group fluxo items by a given key."""
        fluxos.sort(key=key_func)

        return {
            key: list(group)
            for key, group in groupby(fluxos, key=key_func)
        }

    @classmethod
    def _check_competencia(cls, attr: Any, competencia: str) -> Any:
        data_competencia = getattr(attr, competencia)

        return (data_competencia.year, data_competencia.month)
        
    @classmethod
    def _group_fluxos_by_months(
        cls,
        fluxos: List[FluxoCaixa],
        competencia: str
    ) -> Dict:
        locale.setlocale(locale.LC_TIME, "pt_BR.utf8")

        return cls._group_by_key(
            fluxos, key_func=lambda x: cls._check_competencia(
                x, competencia
            )
        )

    @classmethod
    def _get_header(
        cls,
        fluxos: List[FluxoCaixa],
        competencia: str
    ) -> Tuple[List[Tuple], List[Dict]]:
        months = cls._group_fluxos_by_months(fluxos, competencia).keys()

        return months, [
            {
                "title": date(key[0], key[1], 1).strftime("%b %y"),
                "sub_title": f"Mês {idx + 1}" # noqa
            }
            for idx, key in enumerate(months)
        ]

    @classmethod
    def _calc_group(
        cls,
        months: List[Tuple],
        grouped_fluxos: Dict[str, List[FluxoCaixa]]
    ) -> List[Dict]:
        grouped_values = [
            {
                "valor": sum(
                    fluxo.valor
                    if fluxo
                    else 0
                    for fluxo in grouped_fluxos.get(month, [])
                ),
                "av": 0,
                "ah": 0
            }
            for month in months
        ] if grouped_fluxos else []
        missing_columns = len(months) - len(grouped_values)

        if missing_columns:
            grouped_values.extend(
                {
                    "valor": 0,
                    "av": 0,
                    "ah": 0
                }
                for _ in range(missing_columns)
            )

        return grouped_values

    @classmethod
    def _get_tipo_lancamentos(
        cls,
        months: List[Tuple],
        fluxos: List[FluxoCaixa],
        competencia: str
    ) -> List[Dict]:
        tipo_lancamentos_fluxos = cls._group_by_key(
            fluxos, key_func=lambda x: x.categoria.tipo_lancamento.descricao # noqa
        )
        return [
            {
                "tipo_lancamento": key,
                "meses": cls._calc_group(
                    months,
                    cls._group_by_key(
                        group, key_func=lambda x: cls._check_competencia(
                            x, competencia
                        )
                    )
                )
            }
            for key, group in tipo_lancamentos_fluxos.items()
        ]
    
    @classmethod
    def _calc_av_meses(
        cls,
        meses: List[Dict],
        receita_operacional_bruta: Dict
    ) -> None:
        for idx, mes in enumerate(meses):
            if idx > 0:
                mes["av"] = round(
                    mes["valor"] / receita_operacional_bruta["meses"][idx]["valor"], 2
                ) if (
                    len(receita_operacional_bruta["meses"]) < idx
                    and receita_operacional_bruta["meses"][idx]["valor"] > 0
                ) else 1

    @classmethod
    def _calc_av_values(cls, indicadores:List[Dict]) -> None:
        excluded_indicadores = []
        receita_operacional_bruta = [
            indicador
            for indicador in indicadores
            if indicador["indicador"] == "RECEITA OPERACIONAL BRUTA"
        ][0]

        for indicador in indicadores:
            if indicador["indicador"] not in excluded_indicadores:
                cls._calc_av_meses(indicador["meses"], receita_operacional_bruta)

                if indicador["tipo_lancamentos"]:
                    for tipo_lancamento in indicador["tipo_lancamentos"]:
                        cls._calc_av_meses(tipo_lancamento["meses"], receita_operacional_bruta)
    
    @classmethod
    def _calc_ah_meses(cls, meses: List[Dict]) -> None:
        for idx, mes in enumerate(meses):
            if idx > 0:
                mes["ah"] = round(
                    mes["valor"] / meses[idx - 1]["valor"], 2
                ) if meses[idx - 1]["valor"] > 0 else 0
    
    @classmethod
    def _calc_ah_values(cls, indicadores:List[Dict]) -> None:
        excluded_indicadores = []

        for indicador in indicadores:
            if indicador["indicador"] not in excluded_indicadores:
                cls._calc_ah_meses(indicador["meses"])

                if indicador["tipo_lancamentos"]:
                    for tipo_lancamento in indicador["tipo_lancamentos"]:
                        cls._calc_ah_meses(tipo_lancamento["meses"])

    @classmethod
    def _get_rows(
        cls,
        months: List[Tuple],
        fluxos: List[FluxoCaixa],
        indicadores: List[Indicador],
        competencia: str
    ) -> List[Dict]:
        indicador_fluxos = cls._group_by_key(
            fluxos, key_func=lambda x: x.categoria.tipo_lancamento.indicador.descricao # noqa
        )
        
        grouped_indicadores = [
            {
                "indicador": indicador.descricao,
                "meses": cls._calc_group(
                    months,
                    cls._group_by_key(
                        indicador_fluxos.get(indicador.descricao, []),
                        key_func=lambda x: cls._check_competencia(
                            x, competencia
                        )
                    )
                    if indicador.descricao != "FATURAMENTO BRUTO"
                    else
                    cls._group_by_key(
                        fluxos,
                        key_func=lambda x: cls._check_competencia(
                            x, "data_emissao"
                        )
                    )
                ),
                "tipo_lancamentos": cls._get_tipo_lancamentos(
                    months, indicador_fluxos.get(indicador.descricao, []), competencia
                ),
            }
            for indicador in indicadores
        ]

        cls._calc_av_values(grouped_indicadores)
        cls._calc_ah_values(grouped_indicadores)

        return grouped_indicadores
    
    @staticmethod
    def _get_fluxos_by_competencia(
        fluxos: List[FluxoCaixa],
        competencia: str
    ) -> List[FluxoCaixa]:
        return [
            f
            for f in fluxos
            if getattr(f, competencia) is not None
        ]        

    @staticmethod
    def get_data(
        fluxos: List[FluxoCaixa],
        indicadores: List[Indicador],
        competencia: str
    ) -> Dict:
        filtered_fluxos = DREHelper._get_fluxos_by_competencia(
            fluxos, competencia
        )
        months, header = DREHelper._get_header(
            filtered_fluxos, competencia
        )

        return {
            "header": header,
            "rows": DREHelper._get_rows(
                months, filtered_fluxos, indicadores, competencia
            )
        }
