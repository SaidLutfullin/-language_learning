import loguru
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.html import strip_tags


class Words(models.Model):
    user = models.ForeignKey("authentication.user", on_delete=models.CASCADE)
    russian_word = models.CharField("Русское слово", max_length=100)
    foreign_word = models.CharField("Иностранное слово", max_length=100)
    context = models.CharField("Контекст", max_length=200, blank=True, null=True)
    asking_date = models.DateField("Дата повторения", blank=True, null=True)
    box_number = models.IntegerField("Номер коробки", default=0)
    language = models.ForeignKey("dictionary.language", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.russian_word)

    class Meta:
        ordering = ["-pk"]

    def save(self, *args, **kwargs):
        self.russian_word = strip_tags(self.russian_word)
        self.foreign_word = strip_tags(self.foreign_word)
        self.context = strip_tags(self.context)
        super().save(*args, **kwargs)


@receiver(pre_save, sender=Words)
def clean_name(instance, **kwargs):
    if (instance.foreign_word not in instance.context) and instance.context:
        raise ValidationError("Контекст не содержит изучаемого слова")


class Language(models.Model):
    language_name = models.CharField("Язык", max_length=50)
    language_code = models.CharField("Код языка", max_length=10, default="en")

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

    def __str__(self):
        return str(self.language_name)
