from django.db import models
from django.urls import reverse
from loguru import logger
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')
    text = models.TextField(verbose_name='Текст статьи')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    is_main_page = models.BooleanField(default=False, verbose_name='Главная страница?')
    is_published = models.BooleanField(default=False, verbose_name='Опублковать?')
    preview_photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото превью')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_article', kwargs={'article_slug': self.slug})

    class Meta:
        verbose_name = 'Статьи'
        verbose_name_plural = 'Статьи'
        ordering = ['-date']

    @logger.catch
    def save(self, *args, **kwargs):
        if self.is_main_page:
            previous_main_page = Article.objects.filter(is_main_page=True).first()
            if previous_main_page is not None and previous_main_page != self:
                previous_main_page.is_main_page = False
                previous_main_page.save()
        super(Article, self).save(*args, **kwargs)


class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name='Статья', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(verbose_name='Имя', max_length=80)
    email = models.EmailField(verbose_name='E-mail', max_length=100)
    text = models.TextField('Текст (максимальная длина комментария 1000 символов)', max_length=1000)
    created = models.DateTimeField(default=timezone.now, verbose_name='Оставлен')
    active = models.BooleanField(default=True, verbose_name='Активный')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.name} прокоментировал стаьтю {self.article}'
