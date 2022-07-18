from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.RegistryUser.as_view(), name='регистрация пользователя')
]
