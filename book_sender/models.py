from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField("Category name", max_length=255, primary_key=True)
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


class User(AbstractUser):
    email = models.EmailField(_("Email"), unique=True)


class UsersBooks(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_sended = models.BooleanField(default=False)
