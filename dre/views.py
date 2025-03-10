from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DRETemplateView(LoginRequiredMixin, TemplateView):
    template_name = "dre/view.html"
