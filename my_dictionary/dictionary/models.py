from django.db import models


class Words(models.Model):
    user = models.ForeignKey('authentication.user', on_delete=models.CASCADE)
    russian_word = models.CharField('Русское слово', max_length=100)
    foreign_word = models.CharField('Иностранное слово', max_length=100)
    context = models.CharField('Контекст', max_length=100)
    asking_date = models.DateField('Дата повторения', null=True, blank=True)
    box_number = models.IntegerField('Номер коробки', default=0)
    language = models.ForeignKey('dictionary.language', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.russian_word)

    class Meta:
        ordering = ['-pk']


class Language(models.Model):
    language_name = models.CharField('Язык', max_length=50)

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

    def __str__(self):
        return str(self.language_name)
