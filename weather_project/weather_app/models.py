# coding=utf-8

from django.db import models

# Create your models here.


class IP_Limited(models.Model):
    ip = models.IPAddressField
    limited = models.IntegerField
