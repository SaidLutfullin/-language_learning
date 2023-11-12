import os

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER = (("M", "мужской"), ("F", "женский"))

    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("users", str(self.pk), instance)
        return None

    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    avatar = models.ImageField(upload_to=image_upload_to, blank=True)
    about_me = models.TextField(blank=True)
    language_learned = models.ForeignKey(
        "dictionary.language", on_delete=models.PROTECT, default=1
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
