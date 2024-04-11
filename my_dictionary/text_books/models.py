import os

from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class TextBook(models.Model):
    def user_directory_path(self, instance=None):
        if instance:
            return os.path.join("users", str(self.owner.id), instance)
        else:
            return None

    owner = models.ForeignKey("authentication.user", on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    book_file = models.FileField(
        upload_to=user_directory_path, validators=[FileExtensionValidator(["pdf"])]
    )
    keys_file = models.FileField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["pdf"])],
    )
    preview_image = models.ImageField(upload_to=user_directory_path)
    current_page_number = models.IntegerField(default=1)
    keys_page_number = models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse("show_text_book", kwargs={"text_book_id": self.id})

    def __str__(self):
        return f"Учебник {self.name}. {self.description}"

    class Meta:
        ordering = ["-pk"]


class Exercise(models.Model):
    text_book = models.ForeignKey(TextBook, on_delete=models.CASCADE)
    date = models.DateField()
    text = models.TextField()
    page_number = models.IntegerField()
    keys_page_number = models.IntegerField()

    @property
    def miniature(self):
        return self.text[:50]

    def __str__(self):
        return f"Упражнение {self.title} из учебника {self.text_book.name}"

    class Meta:
        ordering = ["-page_number"]
