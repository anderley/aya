from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DashTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "dash/view.html"