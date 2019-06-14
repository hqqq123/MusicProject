from django.db import models

# Create your models here.
from singer.models import Singer
from type.models import Type


class Music(models.Model):
    name=models.CharField(max_length=50)
    img=models.CharField(max_length=200)
    file=models.CharField(max_length=200)
    singers=models.ManyToManyField(Singer)
    type=models.ForeignKey(Type,on_delete=models.SET_NULL,null=True)
