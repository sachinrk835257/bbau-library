# Generated by Django 5.0 on 2024-01-30 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0016_issued_books_semester_returned_books_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='department',
            field=models.CharField(default='', max_length=50, verbose_name='DEPARTMENT'),
        ),
    ]
