# Generated by Django 4.2.6 on 2023-10-16 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0003_registered_books_register_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(default='', max_length=30, verbose_name='STUDENT NAME'),
        ),
    ]
