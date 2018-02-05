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
        verbose_name='Tip',
        max_length=10,
        choices=PROOF_TYPE_CHOICES,
        default=TEXT,
    )

    class Meta:
        abstract = True


class ProofText(Proof):
    content = models.CharField(max_length=5000, blank=True, default='')
