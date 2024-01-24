# Generated by Django 5.0 on 2024-01-22 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0011_alter_registered_books_bookpages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registered_books',
            name='bookContact',
            field=models.TextField(default='Null', null=True, verbose_name='Call No.'),
        ),
        migrations.AlterField(
            model_name='registered_books',
            name='bookPrice',
            field=models.CharField(default='Null', max_length=20, null=True, verbose_name='Book Price'),
        ),
        migrations.AlterField(
            model_name='registered_books',
            name='edition',
            field=models.CharField(default='Null', max_length=10, null=True, verbose_name='Edition'),
        ),
        migrations.AlterField(
            model_name='registered_books',
            name='place_and_publisher',
            field=models.TextField(default='Null', null=True, verbose_name='Place And Publisher'),
        ),
        migrations.AlterField(
            model_name='registered_books',
            name='printYear',
            field=models.CharField(default='Null', max_length=10, null=True, verbose_name='Printed Year'),
        ),
        migrations.AlterField(
            model_name='registered_books',
            name='volume',
            field=models.CharField(default='Null', max_length=10, null=True, verbose_name='Volume'),
        ),
    ]