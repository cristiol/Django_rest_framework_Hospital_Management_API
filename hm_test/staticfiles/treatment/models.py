from django.db import models


class Treatment(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=500, default=None)

    def __str__(self):
        return self.name