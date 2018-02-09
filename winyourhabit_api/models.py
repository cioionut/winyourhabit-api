from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    credit = models.FloatField(default=0.)


class Objective(models.Model):
    title = models.CharField(max_length=500, blank=False, default='')
    description = models.CharField(max_length=1024, blank=True, default='')
    start_date = models.DateTimeField(blank=False)
    valid = models.BooleanField(default=False)
    bet_value = models.FloatField(default=1.)

    user = models.ForeignKey(User, related_name='objectives', on_delete=models.CASCADE)
    habit_group = models.ForeignKey('HabitGroup', related_name='objectives',
                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.title


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
    created_date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=5000, blank=True, default='')
    image = models.ImageField(upload_to="proofs/images")
    objective = models.OneToOneField(Objective, related_name='proof', null=True, on_delete=models.CASCADE)

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

    def __str__(self):
        return self.title


class Vote(models.Model):
    value = models.BooleanField(default=True)
    user = models.ForeignKey(User, related_name='negative_votes', on_delete=models.CASCADE)
    objective = models.ForeignKey(Objective, related_name='negative_votes',
                                  on_delete=models.CASCADE)
