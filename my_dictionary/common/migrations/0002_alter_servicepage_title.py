# Generated by Django 4.1.2 on 2023-03-15 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicepage',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Заголовок'),
        ),
    ]