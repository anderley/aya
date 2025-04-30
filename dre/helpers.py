import locale
from datetime import date
from itertools import groupby
from typing import List, Dict, Any, Tuple
from collections import defaultdict

from core.models import Indicador
from fluxo_caixa.models import FluxoCaixa
from estoques.models import Estoque


class DREHelper:
    VALOR = "valor"
    AV = "av"
    AH = "ah"
    MESES = "meses"
    DEFAULT_MES_DATA = {VALOR: 0, AV: 0, AH: 0}

    @staticmethod
    def _group_by_key(data: List[Any], key_func) -> Dict:
        data.sort(key=key_func)
        return {
            key: list(group)
            for key, group in groupby(data, key=key_func)
        }

    @classmethod
    def _check_competencia(
        cls, obj: Any, competencia: str
    ) -> Tuple[int, int]:
        data_competencia = getattr(obj, competencia)
        return (data_competencia.year, data_competencia.month)

    @classmethod
    def _group_fluxos_by_months(
        cls,
        fluxos: List[FluxoCaixa],
        competencia: str
    ) -> Dict:
        locale.setlocale(locale.LC_TIME, "pt_BR.utf8")

        return cls._group_by_key(
            fluxos, lambda x: cls._check_competencia(x, competencia)
        )

    @classmethod
    def _get_header(
        cls,
        fluxos: List[FluxoCaixa],
        competencia: str
    ) -> Tuple[List[Tuple], List[Dict]]:
        months = cls._group_fluxos_by_months(
            fluxos, competencia
        ).keys()
        header = [
            {
                "title": date(year, month, 1).strftime("%b %y"),
                "sub_title": f"Mês {idx + 1}"
            }
            for idx, (year, month) in enumerate(months)
        ]
        return list(months), header

    @classmethod
    def _calc_group(
        cls,
        months: List[Tuple],
        grouped_fluxos: Dict[str, List[FluxoCaixa]]
    ) -> List[Dict]:
        grouped_values = [
            {
                cls.VALOR: sum(
                    fluxo.valor
                    for fluxo in grouped_fluxos.get(month, [])
                ),
                cls.AV: 0,
                cls.AH: 0
            }
            for month in months
        ] if grouped_fluxos else []

        missing_columns = len(months) - len(grouped_values)
        grouped_values.extend(cls.DEFAULT_MES_DATA.copy() for _ in range(missing_columns))

        return grouped_values

    @classmethod
    def _get_tipo_lancamentos(
        cls,
        months: List[Tuple],
        fluxos: List[FluxoCaixa],
        competencia: str
    ) -> List[Dict]:
        tipo_lancamentos_fluxos = cls._group_by_key(
            fluxos, lambda x: x.categoria.tipo_lancamento.descricao
        )
        return [
            {
                "tipo_lancamento": key,
                cls.MESES: cls._calc_group(
                    months,
                    cls._group_by_key(
                        group, lambda x: cls._check_competencia(x, competencia)
                    )
                )
            }
            for key, group in tipo_lancamentos_fluxos.items()
        ]

    @classmethod
    def _calc_av_meses(cls, meses: List[Dict], receita_op_bruta: Dict) -> None:
        for idx, mes in enumerate(meses):
            if idx > 0:
                valor_base = receita_op_bruta[cls.MESES][idx][cls.VALOR]
                mes[cls.AV] = round(
                    mes[cls.VALOR] / valor_base,
                    2
                ) if valor_base > 0 else 1

    @classmethod
    def _calc_av_values(cls, indicadores: List[Dict]) -> None:
        receita_op_bruta = next((i for i in indicadores if i["indicador"] == "RECEITA OPERACIONAL BRUTA"), None)

        if not receita_op_bruta:
            return
        for indicador in indicadores:
            cls._calc_av_meses(
                indicador[cls.MESES], receita_op_bruta
            )
            for tipo in indicador.get("tipo_lancamentos", []):
                cls._calc_av_meses(
                    tipo[cls.MESES], receita_op_bruta
                )

    @classmethod
    def _calc_ah_meses(cls, meses: List[Dict]) -> None:
        for idx, mes in enumerate(meses):
            if idx > 0:
                prev_val = meses[idx - 1][cls.VALOR]
                mes[cls.AH] = round(
                    mes[cls.VALOR] / prev_val, 2
                ) if prev_val > 0 else 0

    @classmethod
    def _calc_ah_values(cls, indicadores: List[Dict]) -> None:
        for indicador in indicadores:
            cls._calc_ah_meses(indicador[cls.MESES])
            for tipo in indicador.get("tipo_lancamentos", []):
                cls._calc_ah_meses(tipo[cls.MESES])

    @classmethod
    def _get_indicador_by_descricao(
        cls,
        indicadores: List[Dict],
        descricao: str
    ) -> Dict:
        return next(
            (
                i
                for i in indicadores
                if i.get("indicador") == descricao
            ),
            None
        )

    @classmethod
    def _calc_estoques(
        cls,
        months: List[Tuple],
        indicadores: List[Dict],
        estoques: List[Estoque]
    ) -> None:
        estoque_inicial = cls._get_indicador_by_descricao(
            indicadores, "Estoque Inicial"
        )
        estoque_final = cls._get_indicador_by_descricao(
            indicadores, "Estoque Final"
        )
        grouped = defaultdict(list)

        for estoque in estoques:
            grouped[estoque.is_primeiro].append(estoque)

        grouped_ini = cls._group_by_key(
            grouped[True], lambda x: cls._check_competencia(x, "competencia")
        )
        grouped_fin = cls._group_by_key(
            grouped[False], lambda x: cls._check_competencia(x, "competencia")
        )

        for idx, month in enumerate(months):
            idx_prev = 0 if idx == 0 else idx - 1
            estoque_final[cls.MESES][idx][cls.VALOR] = sum(
                e.valor for e in grouped_fin.get(month, [])
            )
            estoque_inicial[cls.MESES][idx][cls.VALOR] = sum(
                e.valor for e in grouped_ini.get(month, [])
            ) + estoque_final[cls.MESES][idx_prev][cls.VALOR]

    @classmethod
    def _calc_saldo_final(cls, indicadores: List[Dict]) -> None:
        saldo_final = cls._get_indicador_by_descricao(
            indicadores, "SALDO FINAL"
        )
        resultado_liquido = cls._get_indicador_by_descricao(
            indicadores, "RESULTADO LÍQUIDO"
        )
        resultado_apos_lucro = cls._get_indicador_by_descricao(
            indicadores, "RESULTADO APÓS O LUCRO"
        )

        for idx, _ in enumerate(saldo_final[cls.MESES]):
            saldo_final[cls.MESES][idx][cls.VALOR] = (
                resultado_liquido[cls.MESES][idx][cls.VALOR] +
                resultado_apos_lucro[cls.MESES][idx][cls.VALOR]
            )

    @classmethod
    def _get_rows(
        cls,
        months: List[Tuple],
        fluxos: List[FluxoCaixa],
        indicadores: List[Indicador],
        estoques: List[Estoque],
        competencia: str
    ) -> List[Dict]:
        indicador_fluxos = cls._group_by_key(
            fluxos, lambda x: x.categoria.tipo_lancamento.indicador.descricao
        )

        grouped_indicadores = [
            {
                "indicador": indicador.descricao,
                cls.MESES: cls._calc_group(
                    months,
                    cls._group_by_key(
                        indicador_fluxos.get(indicador.descricao, []),
                        lambda x: cls._check_competencia(x, competencia)
                    ) if indicador.descricao != "FATURAMENTO BRUTO" else
                    cls._group_by_key(
                        fluxos, lambda x: cls._check_competencia(x, "data_emissao")
                    )
                ),
                "tipo_lancamentos": cls._get_tipo_lancamentos(
                    months, indicador_fluxos.get(indicador.descricao, []), competencia
                ),
            }
            for indicador in indicadores
        ]

        cls._calc_estoques(
            months, grouped_indicadores, estoques
        )
        cls._calc_saldo_final(grouped_indicadores)
        cls._calc_av_values(grouped_indicadores)
        cls._calc_ah_values(grouped_indicadores)

        return grouped_indicadores

    @staticmethod
    def _get_fluxos_by_competencia(
        fluxos: List[FluxoCaixa], competencia: str
    ) -> List[FluxoCaixa]:
        return [
            f
            for f in fluxos
            if getattr(f, competencia, None) is not None
        ]

    @staticmethod
    def get_data(
        fluxos: List[FluxoCaixa],
        indicadores: List[Indicador],
        estoques: List[Estoque],
        competencia: str
    ) -> Dict:
        filtered_fluxos = DREHelper._get_fluxos_by_competencia(
            fluxos, competencia
        )
        months, header = DREHelper._get_header(
            filtered_fluxos, competencia
        )
        rows = DREHelper._get_rows(
            months, filtered_fluxos, indicadores, estoques, competencia
        )
        return {"header": header, "rows": rows}
