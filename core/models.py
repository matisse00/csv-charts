from django.contrib.postgres.fields import JSONField
from django.db import models


class Dataset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    data = JSONField()
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
