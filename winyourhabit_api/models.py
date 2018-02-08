from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    credit = models.FloatField(default=0.)


class Proof(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    PROOF_TYPE_CHOICES = (
        (TEXT, 'text'),
        (IMAGE, 'image'),
    )
    type = models.CharField(
        verbose_name='ProofType',
        max_length=10,
        choices=PROOF_TYPE_CHOICES,
        default=TEXT,
    )

    content = models.CharField(max_length=5000, blank=True, default='')

    def __str__(self):
        return self.content


class HabitGroup(models.Model):
    title = models.CharField(max_length=500, blank=False, default='')
    description = models.CharField(max_length=1024, blank=True, default='')
    users = models.ManyToManyField(User, related_name='habit_groups')
    proof_type = models.CharField(
        verbose_name='ProofType',
        max_length=10,
        choices=Proof.PROOF_TYPE_CHOICES,
        default=Proof.TEXT,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    time_frame = models.IntegerField(default=1)  # numbers of days

    # mapUserAutoAddTimeframe: < userId, < bool >>
    # mapUserToBetDefaultValue: < userId, float
    # betValue >
    #
    # fVoteAddMember: (votedUserId, votingUserId, bool vote)
    # fVoteRemoveMember: (votedUserId, votingUserId, bool vote)
    def __str__(self):
        return self.title


class Objective(models.Model):
    title = models.CharField(max_length=500, blank=False, default='')
    description = models.CharField(max_length=1024, blank=True, default='')
    start_date = models.DateTimeField(blank=False)
    valid = models.BooleanField(default=False)
    bet_value = models.FloatField(default=1.)

    user = models.ForeignKey(User, related_name='objectives', on_delete=models.CASCADE)
    habit_group = models.ForeignKey(HabitGroup, related_name='objectives',
                                    on_delete=models.CASCADE)
    proof = models.OneToOneField(Proof, related_name='objective', null=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class NegativeVote(models.Model):
    user = models.ForeignKey(User, related_name='negative_votes', on_delete=models.CASCADE)
    objective = models.ForeignKey(Objective, related_name='negative_votes',
                                  on_delete=models.CASCADE)
