# Generated by Django 5.0 on 2024-01-21 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0008_alter_registered_books_purchasedate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registered_books',
            name='bookPages',
            field=models.CharField(default='Null', max_length=10, verbose_name='Book Pages'),
        ),
        migrations.AlterField(
            model_name='registered_books',
            name='bookPrice',
            field=models.CharField(default='Null', max_length=7, verbose_name='Book Price'),
        ),
        migrations.AlterField(
            model_name='registered_books',
            name='printYear',
            field=models.CharField(default='Null', max_length=10, verbose_name='Printed Year'),
        ),
    ]
