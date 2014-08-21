from django.contrib.auth.models import User
from django.db import models


class Club(models.Model):

    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=10)
    user = models.ForeignKey(User, unique=True, related_name='clubs')

    class Meta:
        app_label = 'main'
        ordering = ['name']

    def __str__(self):
        return self.name
