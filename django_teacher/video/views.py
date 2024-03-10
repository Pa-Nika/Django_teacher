import dlib
import plotly.express as px
from django.shortcuts import render, redirect
from .forms import VideoForm
from .models import Video
from .position import position_analyzer

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("video/static/video/face_detection_data/shape_predictor_68_face_landmarks.dat")


def history(request):
    all_videos = Video.objects.all()
    sorted_videos = sorted(all_videos, key=lambda x: x.id, reverse=True)
    data = {
        'title': 'История загрузок',
        'videos': sorted_videos
    }
    return render(request, 'video/history.html', data)


def make_chart(dataframe, form):
    final_mark = round(dataframe['mark'].mean(), 2)
    dataframe['eye_mark'] = dataframe['eye_mark'].fillna('Не распознано')
    dataframe[['eye_mark', 'hor_mark', 'ver_mark', 'square_mark']] = dataframe[['eye_mark', 'hor_mark', 'ver_mark', 'square_mark']].\
        replace(0, 'Не распознали лицо').bfill()
    dataframe[['eye_mark', 'hor_mark', 'ver_mark', 'square_mark']] = dataframe[['eye_mark', 'hor_mark', 'ver_mark', 'square_mark']].\
        replace(-1, 'Несколько лиц в кадре').bfill()
    dataframe = dataframe.rename(columns={'hor_mark': 'По-горизонтали',
                                          'ver_mark': 'По-вертикали',
                                          'square_mark': 'Крупность',
                                          'eye_mark': 'Положение глаз'})
    fig = px.line(dataframe,
                  x='duration',
                  y='mark',
                  title=f'График для {form.cleaned_data["date"]}. Итоговая оценка {final_mark}',
                  labels={'duration': 'Длительность видео', 'mark': 'Оценка'},
                  hover_data=['mark', 'По-горизонтали', 'По-вертикали', 'Крупность', 'Положение глаз'],
                  height=700,
                  width=1000
                  )
    plot_html = fig.to_html(full_html=False)
    return plot_html, final_mark


def upload_video(request):
    error = ''
    form = VideoForm()

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            my_video = form.save()
            position = position_analyzer.PositionAnalyzer(my_video.video_file.path, detector, predictor)
            plot_html, final_mark = make_chart(position.analyse(), form)
            data = {
                'form': form,
                'error': error,
                'plot_html': plot_html
            }
            return render(request, 'video/upload_video.html', data)
        else:
            error = 'Введите корректные данные'
            data = {
                'form': form,
                'error': error
            }
            return render(request, 'video/upload_video.html', data)

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'video/upload_video.html', data)


def online_video(request):
    return render(request, 'video/online_video.html')
