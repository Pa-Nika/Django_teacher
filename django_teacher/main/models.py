from django.db import models


class Video(models.Model):
    title = models.CharField('Название', max_length=80)
    video_file = models.FileField('Файл', upload_to='media/videos')
    uploaded_at = models.DateField('Дата')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
