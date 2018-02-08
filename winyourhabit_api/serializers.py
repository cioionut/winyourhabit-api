from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# from django.contrib.auth.models import User
from winyourhabit_api.models import User, Proof, HabitGroup, Objective, NegativeVote


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


class ProofSerializer(serializers.ModelSerializer):

    type = serializers.ChoiceField(
            required=True,
            choices=Proof.PROOF_TYPE_CHOICES,
            # validators=[UniqueValidator(queryset=User.objects.all())]
            )
    content = serializers.CharField(
        required=True,
        max_length=5000,
    )

    class Meta:
        model = Proof
        fields = ('id', 'type', 'content', 'objective')


class HabitGroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = HabitGroup
        fields = ('title', 'description', 'users', 'proof_type', 'created_date', 'time_frame')


class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = '__all__'


class NegativeVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NegativeVote
        fields = '__all__'
