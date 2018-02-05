from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# from django.contrib.auth.models import User
from winyourhabit_api.models import User, ProofText


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
                    validated_data['username'],
                    validated_data['email'],
                    validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'credit')


class ProofTextSerializer(serializers.ModelSerializer):

    type = serializers.ChoiceField(
            required=True,
            choices=[ProofText.TEXT],
            # validators=[UniqueValidator(queryset=User.objects.all())]
            )
    content = serializers.CharField(
        required=True,
        max_length=5000,
    )

    class Meta:
        model = ProofText
        fields = ('id', 'type', 'content')
