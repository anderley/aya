from django.urls import path

from .views import DashTemplateView

urlpatterns = [
    path('', DashTemplateView.as_view(), name='view_dash'),
]
