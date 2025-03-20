from django.urls import path

from usuarios import views as auth_view

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', auth_view.CustomLoginView.as_view(), name='login'), # noqa  
    path('logout/', views.logout_view, name='logout'),
]
