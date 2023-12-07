# Generated by Django 4.2.6 on 2023-11-30 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0008_alter_profile_issuedbooks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='issuedBooks',
            field=models.TextField(default='Null', verbose_name='ISSUED BOOKS'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='returnedBooks',
            field=models.TextField(default='Null', verbose_name='RETURNED BOOKS'),
        ),
    ]