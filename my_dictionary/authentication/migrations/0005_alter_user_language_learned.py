# Generated by Django 4.1.2 on 2023-02-09 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_language_words_language'),
        ('authentication', '0004_alter_user_language_learned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language_learned',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='dictionary.language'),
        ),
    ]