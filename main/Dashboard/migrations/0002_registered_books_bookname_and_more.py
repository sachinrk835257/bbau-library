# Generated by Django 5.0 on 2024-01-19 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registered_books',
            name='bookName',
            field=models.CharField(default='', max_length=255, verbose_name='Book Name'),
        ),
        migrations.AddField(
            model_name='registered_books',
            name='department',
            field=models.CharField(default='', max_length=50, verbose_name='Department'),
        ),
        migrations.AddField(
            model_name='registered_books',
            name='register_by',
            field=models.CharField(default='', max_length=50, verbose_name='book register by'),
        ),
    ]
