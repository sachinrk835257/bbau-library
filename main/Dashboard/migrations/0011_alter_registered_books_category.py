# Generated by Django 4.2.6 on 2023-12-07 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0010_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registered_books',
            name='category',
            field=models.CharField(default='Null', max_length=50, verbose_name='Category'),
        ),
    ]
