from django.urls import path
from operadora import views

urlpatterns = [
    path('', views.home, name='home'),
]
