from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import update_last_login
from authentication.models import User
from authentication.dataclasses import RegisterResponse, LoginResponse, ChangePasswordResponse


def create_user(email: str, username: str, password: str) -> RegisterResponse:
    user = User.objects.create(email=email, username=username)
    user.is_active = True
    user.set_password(password)
    user.save()
    return RegisterResponse(response='success')


def login_user(email: str | None, username: str | None, password: str) -> LoginResponse:
    if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
        user = User.objects.get(email=email) if User.objects.filter(email=email).exists() else User.objects.get(
            username=username)
        if not user.check_password(password):
            return LoginResponse(error='Incorrect password', status=HTTP_401_UNAUTHORIZED, access=None, refresh=None)
        refresh = RefreshToken.for_user(user=user)
        update_last_login(sender=None, user=user)
        return LoginResponse(access=str(refresh.access_token), refresh=refresh, status=HTTP_200_OK, error=None)
    else:
        return LoginResponse(error='User not found', status=HTTP_404_NOT_FOUND, access=None, refresh=None)


def change_password(user_id: int, old_password: str, new_password: str, re_new_password: str):
    user = User.objects.get(id=user_id)

    if not user.check_password(old_password):
        return ChangePasswordResponse(error='Incorrect old_password', status=HTTP_401_UNAUTHORIZED)

    if new_password != re_new_password:
        return ChangePasswordResponse(error='New passwords does not match', status=HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return ChangePasswordResponse(error=None, status=HTTP_200_OK)