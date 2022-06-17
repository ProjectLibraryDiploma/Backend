from datetime import datetime

from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from Backend import settings
from book_sender.models import Category, Book, Client, Token
from book_sender.serializer import BookSerializer


def send_email_message(subject, recipient_list, html, text="", from_email=settings.EMAIL_HOST_USER):
    msg = EmailMultiAlternatives(subject, text, from_email, recipient_list)
    msg.attach_alternative(html, "text/html")
    return msg.send()


def send_confirmation_link(user, token):
    context = {"email_url": "http://127.0.0.1:8000/check_email/{}".format(token)}
    html = get_template("email_confirmation.html").render(context)
    send_email_message(subject="Email confirmation", recipient_list=[user.email], html=html, from_email=settings.EMAIL_HOST_USER)


def send_email_to_users():
    data = {}
    for client in Client.objects.all():
        changes = False
        for category in Category.objects.filter(client=client):
            books = Book.objects.filter(categories=category, is_sended=False).distinct()
            if books.exists():
                changes = True
                data[category.name] = books.all()

        context = {"data": data}
        html = get_template("email_books.html").render(context)
        if changes:
            send_email_message(subject="New books", recipient_list=[client.email], html=html,
                               from_email=settings.EMAIL_HOST_USER)


class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request):
        return render(request, "home.html")


class GetEmailConfirmarionView(View):

    def post(self, request):
        user = Client.objects.get_or_create(email=request.POST['email'])[0]
        Token.objects.filter(client_email=user).all().delete()
        token = Token.objects.create(client_email=user)
        send_confirmation_link(user, token.value)
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
            messages.error(request, 'Час дії посилання вичерпано. Ще раз введіть імейл')
            return redirect('home')


class ChooseCategoryView(TemplateView):
    template_name = "categories.html"

    def get(self, request):
        try:
            value = request.session['token']
        except KeyError:
            messages.error(request, 'Час дії посилання вичерпано. Ще раз введіть імейл')
            return redirect('home')
        token = Token.objects.filter(value=request.session['token'], expiration_time__gt=datetime.now())
        if token.exists():
            client = Client.objects.filter(token=token.first()).first()
            return render(
                request,
                "categories.html",
                {"categories": Category.objects.all(), "client_cateories": Category.objects.filter(client=client)}
            )
        else:
            messages.error(request, 'Час дії посилання вичерпано. Ще раз введіть імейл')
            return redirect('home')

    def post(self, request):
        try:
            value = request.session['token']
        except KeyError:
            messages.error(request, 'Час дії посилання вичерпано. Ще раз введіть імейл')
            return redirect('home')
        token = Token.objects.filter(value=request.session['token'], expiration_time__gt=datetime.now())
        if token.exists():
            client = Client.objects.filter(token=token.first()).first()
            client.categories.clear()
            for name in request.POST:
                if name != 'csrfmiddlewaretoken':
                    category = Category.objects.filter(id=name)
                    if category.exists():
                        client.categories.add(category.first())
            messages.error(request, 'Нові обрані категорії збережено')
            token.delete()
            return redirect('home')
        else:
            messages.error(request, 'Час дії посилання вичерпано. Ще раз введіть імейл')
            return redirect('home')


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
