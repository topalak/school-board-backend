from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random

class User(AbstractUser):
    TIER_CHOICES = [
        (1, 'Student'),
        (2, 'Teacher'),
        (3, 'General')
    ]

    email = models.EmailField(unique=True)
    tier = models.IntegerField(choices=TIER_CHOICES, default=1)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # Create your models here.


class VerificationCode(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

