from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import Serializer, ModelSerializer, CharField, ValidationError


class UserSerializer(ModelSerializer):
    """User Serializers"""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}, 'id': {'read_only': True}}

    def create(self, validated_data):
        """Creates user by validated data."""

        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(Serializer):
    """Auth Token Serializer"""

    email = CharField()
    password = CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validates and authenticates given user"""

        user = authenticate(
            request=self.context.get('request'),
            username=attrs.get('email'),
            password=attrs.get('password')
        )

        if not user:
            raise ValidationError(_('Unable to authenticate given credentials'),
                                  code='authentication')

        attrs['user'] = user
        return attrs
