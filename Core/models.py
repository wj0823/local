from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(blank=True, null=True)
    max_score = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="userrole")
    ROLE_CHOICES = (
        ('T', 'Teacher'),
        ('S', 'Student'),
    )
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='S')
