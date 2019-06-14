from django.db import models

# Create your models here.
from account.models import Account
from music.models import Music


class Musiclist(models.Model):
    name = models.CharField(max_length=50)
    musics = models.ManyToManyField(Music)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

