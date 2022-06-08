from django.contrib import admin
from django.contrib.auth.models import User

from book_sender.models import Book, Category, Token, Client


admin.site.register(Token)
admin.site.register(Client)
admin.site.register(Book)
admin.site.register(Category)
# Register your models here.
