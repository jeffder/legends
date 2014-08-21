from django.db import models


class Ground(models.Model):

    name = models.CharField(max_length=20, null=False)

    class Meta:
        app_label = 'main'
        ordering = ['name']

    def __str__(self):
        return self.name
