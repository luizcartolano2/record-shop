""" Docstring for the models.py module.

"""
from django.db import models
from django.contrib.auth.models import User


class Disc(models.Model):
    """
    Class to store the disc's information.
    """
    name = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    release_year = models.CharField(max_length=4)
    style = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)


class Client(models.Model):
    """
    Class to store the client's information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=31)
    identity = models.CharField(max_length=11)
    birth_day = models.CharField(max_length=10)


class Request(models.Model):
    """
    Class to store the request's information.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Disc = models.ForeignKey(Disc, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    operation_date = models.DateTimeField(auto_now_add=True)
