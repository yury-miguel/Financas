from . import views
from django.urls import path


urlpatterns = [
    path('sistema/metas/', views.metas, name='metas'),
]