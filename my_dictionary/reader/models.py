from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


# Create your models here.
class ForeignBook(models.Model):
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    user = models.ForeignKey("authentication.user", on_delete=models.CASCADE)
    language = models.ForeignKey("dictionary.language", on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class ForeignBookPage(models.Model):
    page_text = HTMLField("Текст")
    foreign_book = models.ForeignKey(ForeignBook, on_delete=models.CASCADE)
