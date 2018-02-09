from math import floor
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from winyourhabit_api.models import User, Proof, HabitGroup, Objective, Vote
from django.db.models import Q


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

    # def create(self, validated_data):
    #
    #     user = User.objects.create_user(
    #                 username=validated_data['username'],
    #                 email=validated_data['email'],
    #                 password=validated_data['password'],
    #                 credit=validated_data['credit'],
    #     )
    #     return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'credit', 'habit_groups')


class ProofSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(read_only=True)
    type = serializers.ChoiceField(
            required=True,
            choices=Proof.PROOF_TYPE_CHOICES,
            # validators=[UniqueValidator(queryset=User.objects.all())]
            )
    content = serializers.CharField(
        required=True,
        max_length=5000,
    )
    image = serializers.ImageField(required=False)

    def create(self, validated_data):
        proof = Proof.objects.create(**validated_data)
        proof.objective.valid = True
        proof.objective.save()
        return proof

    class Meta:
        model = Proof
        fields = '__all__'


class HabitGroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = HabitGroup
        fields = '__all__'


class ObjectiveSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # habit_group = HabitGroupSerializer()
    proof = ProofSerializer(read_only=True)

    # def perform_create(self, serializer):
    #     serializer.save(proof=self.request.proof)

    class Meta:
        model = Objective
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):

    def validate(self, data):
        try:
            objective = data['objective']
            user = data['user']
            # objective = Objective.objects.get(id=data['objective'])
            who_vote = [vote.user.id for vote in Vote.objects.filter(objective=objective.id).all()]
        except Exception as e:
            raise serializers.ValidationError(str(e))
        if user not in objective.habit_group.users.all():
            raise serializers.ValidationError('Your are not a member of this habit group')
        if user.id == objective.user.id:
            raise serializers.ValidationError('Can not vote yourself')
        if user.id in who_vote:
            raise serializers.ValidationError('You already vote')
        if objective.valid is False:
            raise serializers.ValidationError('Can not vote an invalid objective')
        return data

    def create(self, validated_data):
        vote = Vote.objects.create(**validated_data)
        # invalidate objective
        n_nvotes = Vote.objects.filter(objective=vote.objective, value=False).count()
        n_users_group = vote.objective.habit_group.users.count()
        if n_nvotes > floor(n_users_group / 2) and n_users_group > 0:
            # invalidate objective
            vote.objective.valid = False
            vote.objective.save()
            # transfer credit
            source_user = vote.objective.user
            source_user.credit -= (n_users_group - 1) * vote.objective.bet_value
            for dest_user in vote.objective.habit_group.users.all():
                if dest_user.id != source_user.id:
                    dest_user.credit += vote.objective.bet_value
                    dest_user.save()
            source_user.save()

        return vote

    class Meta:
        model = Vote
        fields = '__all__'
