# Generated by Django 4.0.4 on 2022-06-10 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Category name')),
            ],
            options={
                'verbose_name': 'Caategory',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, verbose_name='Email')),
                ('telegram_login', models.CharField(blank=True, max_length=255)),
                ('categories', models.ManyToManyField(blank=True, related_name='client', to='book_sender.category', verbose_name='Categories')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiration_time', models.DateTimeField(blank=True)),
                ('value', models.CharField(blank=True, max_length=255)),
                ('client_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_sender.client')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Book title')),
                ('author', models.CharField(max_length=300, verbose_name='Author')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Price')),
                ('is_sended', models.BooleanField(default=False)),
                ('categories', models.ManyToManyField(related_name='books', to='book_sender.category', verbose_name='Categories')),
            ],
        ),
    ]
