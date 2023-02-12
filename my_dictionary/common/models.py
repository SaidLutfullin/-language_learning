from django.db import models


class ServicePage(models.Model):
    SERVICE_PAGE_TYPES = [
        ('user_agreement', 'Пользовательское соглашение'),
        ('privacy_policy', 'Политика конфиденциальности'),
    ]
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True, verbose_name='Текст страницы')
    page_type = models.CharField(max_length=30, verbose_name='Тип страницы', choices=SERVICE_PAGE_TYPES, unique=True)

    class Meta:
        verbose_name = 'Служебная страница'
        verbose_name_plural = 'Служебные страницы'

    def __str__(self):
        return str(self.title)