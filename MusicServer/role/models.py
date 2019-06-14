from django.db import models

# Create your models here.
from authority.models import Authority


class Role(models.Model):
    name=models.CharField(max_length=20)
    authorities = models.ManyToManyField(Authority)