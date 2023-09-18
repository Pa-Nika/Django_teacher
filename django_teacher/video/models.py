from django.db import models


class Video(models.Model):
    title = models.CharField('Название', max_length=80)
    video_file = models.FileField('Файл', upload_to='media/videos')
    date = models.DateField('Дата')
    user = models.CharField('Пользователь', max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
