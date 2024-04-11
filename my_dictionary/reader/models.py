import os

from django.core.validators import FileExtensionValidator
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


class PDFBook(models.Model):
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    user = models.ForeignKey("authentication.user", on_delete=models.CASCADE)
    language = models.ForeignKey("dictionary.language", on_delete=models.PROTECT)

    def user_directory_path(self, instance=None):
        if instance:
            return os.path.join("users", str(self.user.id), instance)
        else:
            return None

    book_file = models.FileField(
        upload_to=user_directory_path, validators=[FileExtensionValidator(["pdf"])]
    )
    preview_image = models.ImageField(upload_to=user_directory_path)
    current_page_number = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
