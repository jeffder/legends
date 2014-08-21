from django.db import models


class Season(models.Model):

    season = models.IntegerField(null=False)

    # Every season from 2008 has full data (coaches, games, tips, results,
    # ladders etc). The rest have some ladders and category winners except
    # 2006...
    has_full_data = models.BooleanField(default=True)

    # ...which has no data except the Premier.
    has_no_data = models.BooleanField(default=False)

    class Meta:
        app_label = 'main'
        ordering = ['-season']

    def __str__(self):
        return '{}'.format(self.season)
