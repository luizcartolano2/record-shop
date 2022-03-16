""" Docstring for the models.py module.

"""
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, BaseUserManager


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
            obj.amount -= amount
            obj.save()
        else:
            raise transaction.TransactionManagementError


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Class to store the client's information.
    """
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=31)
    identity = models.CharField(max_length=11)
    birth_day = models.CharField(max_length=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()


class Request(models.Model):
    """
    Class to store the request's information.
    """
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    Disc = models.ForeignKey(Disc, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    operation_date = models.DateTimeField(auto_now_add=True)
