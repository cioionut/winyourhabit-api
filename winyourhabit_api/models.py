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

    class Meta:
        abstract = True


class ProofText(Proof):
    content = models.CharField(max_length=5000, blank=True, default='')


# class UserGroup(models.Model):


class HabitGroup(models.Model):
    title = models.CharField(max_length=500, blank=True, default='')

    description = models.CharField(max_length=500, blank=True, default='')

    users = models.ManyToManyField(User, related_name='users')
    proof_type = models.CharField(
        verbose_name='ProofType',
        max_length=10,
        choices=Proof.PROOF_TYPE_CHOICES,
        default=Proof.TEXT,
    )
    timeframe = models.FloatField(default=24*3600)

    # mapUserAutoAddTimeframe: < userId, < bool >>
    # mapUserToBetDefaultValue: < userId, float
    # betValue >
    #
    # fVoteAddMember: (votedUserId, votingUserId, bool vote)
    # fVoteRemoveMember: (votedUserId, votingUserId, bool vote)
