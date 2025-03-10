from django.urls import path

from .views import DRETemplateView

urlpatterns = [
    path('', DRETemplateView.as_view(), name='view_dre'),
]