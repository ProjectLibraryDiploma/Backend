from datetime import datetime

from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from Backend import settings
from book_sender.models import Category, Book, Client, Token
from book_sender.serializer import BookSerializer


def send_email_message(subject, recipient_list, html, text = "", from_email=settings.EMAIL_HOST_USER):
    msg = EmailMultiAlternatives(subject, text, from_email, recipient_list)
    msg.attach_alternative(html, "text/html")
    return msg.send()


def send_email_to_users():
    for client in Client.objects.all():
        books = Book.objects.filter(categories__client=client, is_sended=False).distinct()
        send_mail(subject="New books",
        message=str(books.all()[0].title), from_email=settings.EMAIL_HOST_USER, recipient_list=[client.email])
        for book in books.all():
            book.is_sended = True
            book.save()


def send_confirmation_link(client):
    token = Token.objects.create(client_email=client)
    context = {"email_url": "http://127.0.0.1:8000/check_email/{}".format(token.value)}
    html = get_template("email_confirmation.html").render(context)

    send_email_message(subject="Confirmation link", recipient_list=[client.email], html=html, from_email=settings.EMAIL_HOST_USER)


class HomeView(TemplateView):
    template_name = "home.html"


class GetEmailConfirmarionView(View):

    def post(self, request):
        user = Client.objects.get_or_create(email=request.POST['email'])[0]
        Token.objects.filter(client_email=user).all().delete()
        send_confirmation_link(user)
        messages.error(request, 'Посилання було відправлено на вашу email адресу')
        return redirect("home")


class ConfirmEmailView(View):

    def get(self, request, token):
        my_token = Token.objects.filter(value=token, expiration_time__gt=datetime.now())
        if my_token.exists():
            client = my_token.first().client_email
            my_token.delete()
            new_token = Token.objects.create(client_email=client)
            request.session['token'] = str(new_token.value)
            return redirect('choose_category')
        else:
            return redirect('home')


class ChooseCategoryView(TemplateView):
    template_name = "categories.html"

    def get(self, request):
        return render(request, "categories.html", {"categories": Category.objects.all()})

    def post(self, request):
        for names in request.POST:
            if names != 'csrfmiddlewaretoken' and names != 'token':
                category = Category.objects.filter(name=names)
                if category.exists():
                    Client.objects.filter(token__value=request.POST['token']).first().categories.add(category.all())
        return HttpResponse('ok')


class GetNewBooks(ViewSet):

    def create(self, request, *args, **kwargs):

        data = self.request.data
        for category in data:
            current_category = Category.objects.get_or_create(name=category)
            for category_book in data[category]:
                serializer = BookSerializer(data=category_book)
                if serializer.is_valid():
                    book_data = serializer.validated_data()
                    current_book = Book.objects.get_or_create(title=book_data['title'])[0]
                    current_book.author = book_data['author']
                    current_book.categories.add(current_category)
                    current_book.save()
        send_email_to_users()
        return Response(status=200)



