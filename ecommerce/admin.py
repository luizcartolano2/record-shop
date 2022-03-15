""" Docstring for the admin.py module.

"""
from django.contrib import admin
from .models import Client, Disc, Request


admin.site.register(Client)
admin.site.register(Disc)
admin.site.register(Request)
