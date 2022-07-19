from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.RegistryUserView.as_view(), name='регистрация пользователя'),
    path("login", views.LoginUserView.as_view(), name='вход по логину/паролю'),
    path("profile", views.RetrieveUpdateUserView.as_view(), name='обновление и получение данных пользователей'),
    path("update_password", views.UpdatePasswordUserView.as_view(), name='изменение пароля'),
]
