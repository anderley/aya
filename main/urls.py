from django.urls import path
from . import views
from usuarios import views as auth_view

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', auth_view.CustomLoginView.as_view(), name='login'), # noqa  
    path('logout/', views.logout_view, name='logout'),  
]
