from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from authentication.models import User
from authentication.serializers import UserSerializer
from authentication.service import create_user, login_user, change_password


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False, url_path='register', url_name='auth-user-register')
    def register(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = create_user(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        return Response(data={'message': new_user.response})


    @action(methods=['POST'], detail=False, url_path='login', url_name='auth-user-login')
    def login(self, request) -> Response:
        # if 'email' not in request.data and 'username' not in request.data and 'password' not in request.data:
        # TODO: check email and username
        if 'password' not in request.data:
            return Response(data={'message': 'Fields password, email/login must not be empty'},
                            status=HTTP_400_BAD_REQUEST)
        data = login_user(email=request.data['email'], password=request.data['password'],
                          username=None) if 'email' in request.data else login_user(
            email=None, password=request.data['password'],
            username=request.data['username'])

        if data.error is not None:
            return Response(data={'message': data.error}, status=data.status)

        response = Response()
        response.set_cookie(key='refresh', value=data.refresh)
        response.data = {'access': data.access}
        response.status_code = data.status
        return response


    @action(methods=['GET'], detail=False, url_path='me', url_name='auth-user-data', permission_classes=[IsAuthenticated])
    def get_user_data(self, request) -> Response:
        user = request.user
        data = self.serializer_class(instance=user).data
        return Response(data)


    @action(methods=['POST'], detail=False, url_path='change-password', url_name='auth-user-change-password', permission_classes=[IsAuthenticated])
    def change_password(self, request) -> Response:

        if 'old_password' not in request.data:
            raise ParseError(detail='old_password field must not be empty')

        if 'new_password' not in request.data or len(request.data['new_password']) < 1:
            raise ParseError(detail='new_password field must not be empty')

        if 're_new_password' not in request.data or len(request.data['re_new_password']) < 1:
            raise ParseError(detail='re_new_password field must not be empty')

        result = change_password(request.user.id, request.data['old_password'],
                        request.data['new_password'], request.data['re_new_password'])

        if result.status != HTTP_200_OK and result.error != None:
            return Response(data={'error': result.error},status=result.status)

        return Response(data={'message': 'success'}, status=result.status)
