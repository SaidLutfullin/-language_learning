# Generated by Django 4.1.2 on 2023-01-28 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_alter_comment_options_alter_comment_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=1000, verbose_name='Текст'),
        ),
    ]