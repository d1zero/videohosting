from rest_framework.serializers import ModelSerializer, ValidationError
from authentication.models import User


class UserSerializer(ModelSerializer):

    def validate_email(self, value):
        print(value)

    @staticmethod
    def validate_username(self, value) -> str:
        print(1)
        if len(value) < 5:
            raise ValidationError(detail='Login field is too short')
        return value

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }
