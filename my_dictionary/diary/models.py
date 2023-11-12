from django.db import models
from tinymce.models import HTMLField


class Diary(models.Model):
    date = models.DateField("Дата")
    user = models.ForeignKey("authentication.user", on_delete=models.CASCADE)
    title = models.CharField("Заголовок", max_length=100, blank=True, null=True)
    text = HTMLField("Текст")
    language = models.ForeignKey("dictionary.language", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-date", "title"]
