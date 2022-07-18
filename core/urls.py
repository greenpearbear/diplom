from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegistryUser.as_view(), name='регистрация пользователя')
]
