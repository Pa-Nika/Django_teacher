from django import forms
from .models import Video
from datetime import date


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file', 'date']

        widgets = {
            "title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название файла'
            }),
            "video_file": forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Видео'
            }),
            "date": forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата встречи',
                'autocomplete': "off",
                'value': date.today().strftime('%d.%m.%Y')
            })
        }
