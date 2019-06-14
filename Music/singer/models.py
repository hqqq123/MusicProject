from django.db import models

# Create your models here.
class Singer(models.Model):
    name=models.CharField(max_length=20)
