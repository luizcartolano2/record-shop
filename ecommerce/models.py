""" Docstring for the models.py module.

"""
from django.db import models, transaction
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

    def get_queryset(self):
        """
        Method to get a queryset of Disc objects.
        :return: query filter by the id.
        """
        return self.__class__.objects.filter(id=self.id)

    @transaction.atomic()
    def add_disc(self, amount):
        """
        Here we add a method to add new disc's to an existing model.
        It's important to note that by call the `select_for_update`
        method we acquire a lock to the table of disc's so no other
        request will write to this entry.
        :param amount: number of disc's to be added.
        """
        obj = self.get_queryset().select_for_update().get()
        obj.amount = amount
        obj.save()

    @transaction.atomic()
    def remove_disc(self, amount):
        """
        Here we add a method to add new disc's to an existing model.
        It's important to note that by call the `select_for_update`
        method we acquire a lock to the table of disc's so no other
        request will write to this entry. Making sure we will not
        sell more discs than available.
        :param amount: number of disc's to be added.
        """
        obj = self.get_queryset().select_for_update().get()
        if amount <= obj.amount:
            obj.balance -= amount
            obj.save()
        else:
            raise transaction.TransactionManagementError


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
