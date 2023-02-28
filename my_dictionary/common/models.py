from django.db import models
from tinymce.models import HTMLField


class ServicePage(models.Model):
    SERVICE_PAGE_TYPES = [
        ('user_agreement', 'Пользовательское соглашение'),
        ('privacy_policy', 'Политика конфиденциальности'),
        ('404', 'Ошибка 404'),
        ('500', 'Ошибка 500'),
        ('test_completed', 'Тренеровка завершена'),
        ('password_reset_complete', 'Пароль успешно сброшен'),
        ('password_reset_done', 'Сброс пароля по почте'),
        ('password_change_done', 'Парроль успешно изменен'),
    ]
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    text = HTMLField(blank=True, verbose_name='Текст страницы')
    page_type = models.CharField(max_length=30, verbose_name='Тип страницы',
                                 choices=SERVICE_PAGE_TYPES, unique=True)

    class Meta:
        verbose_name = 'Служебная страница'
        verbose_name_plural = 'Служебные страницы'

    def __str__(self):
        return str(self.title)
