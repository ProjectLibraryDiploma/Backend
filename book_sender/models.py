from datetime import datetime, timedelta
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _

from Backend import settings


class Category(models.Model):
    name = models.CharField("Category name", max_length=255, unique=True)
    # Add image field

    class Meta:
        verbose_name = "Caategory"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(_("Book title"), max_length=255)
    author = models.CharField(_("Author"), max_length=300)
    price = models.IntegerField(_("Price"), blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name="books", verbose_name=_("Categories"))
    is_sended = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " " + self.author


class Client(models.Model):
    email = models.EmailField(_("Email"), primary_key=True)
    categories = models.ManyToManyField(Category, related_name="client", verbose_name=_("Categories"), blank=True)
    telegram_login = models.CharField(max_length=255, blank=True)


class Token(models.Model):
    expiration_time = models.DateTimeField(blank=True)
    value = models.CharField(max_length=255, blank=True)
    client_email = models.ForeignKey(Client, on_delete=models.CASCADE)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.expiration_time = datetime.now() + timedelta(days=1)
        self.value = uuid4()
        super().save(force_insert, force_update, using, update_fields)
