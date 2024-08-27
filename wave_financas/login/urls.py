from . import views
from django.urls import path

urlpatterns = [
    path('contas/', views.login_view, name='contas'),
]