# Generated by Django 5.0 on 2024-01-21 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0007_remove_issued_books_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registered_books',
            name='purchaseDate',
            field=models.TextField(default='00-00-0000', max_length=15, verbose_name='Purchase Date'),
        ),
    ]