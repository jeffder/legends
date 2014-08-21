from django.contrib.auth.models import User
from django.db import models


class Ground(models.Model):

    name = models.CharField(max_length=20, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
