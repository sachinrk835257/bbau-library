# Generated by Django 5.0 on 2024-01-21 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0006_registered_books_bookcontact_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issued_books',
            name='category',
        ),
        migrations.RemoveField(
            model_name='registered_books',
            name='category',
        ),
        migrations.RemoveField(
            model_name='returned_books',
            name='category',
        ),
    ]