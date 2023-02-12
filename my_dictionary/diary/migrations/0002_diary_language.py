# Generated by Django 4.1.2 on 2023-02-07 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_language_words_language'),
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diary',
            name='language',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='dictionary.language'),
            preserve_default=False,
        ),
    ]