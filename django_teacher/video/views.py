import threading
from datetime import datetime

import dlib
import plotly.express as px
import os

from django.http import FileResponse, HttpResponse

from .static.stuff_to_html import constants as const
from django.shortcuts import render, redirect
from .forms import VideoForm
from .models import Video
from .upload import position_analyzer
from .online import online_video_reader, video_analysis

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("video/static/video/face_detection_data/shape_predictor_68_face_landmarks.dat")
analyzer = video_analysis.OnlineVideoAnalyzer(detector, predictor)
video_thread = None


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
    dataframe[['eye_mark', 'hor_mark', 'ver_mark', 'square_mark']] = dataframe[
        ['eye_mark', 'hor_mark', 'ver_mark', 'square_mark']]. \
        replace(0, 'Не распознали лицо').bfill()
    dataframe[['eye_mark', 'hor_mark', 'ver_mark', 'square_mark']] = dataframe[
        ['eye_mark', 'hor_mark', 'ver_mark', 'square_mark']]. \
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
            file_path = my_video.video_file.path
            os.remove(file_path)
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


def start_read_video():
    new_video_online = online_video_reader.OnlineVideoReader()
    new_video_online.read_video()


def online_video(request):
    global video_thread
    data = {
        'text_about': const.TEXT_ONLINE_VIDEO_GET
    }
    if request.method == 'GET':
        thread = threading.Thread(target=start_read_video)
        thread.start()
        return render(request, 'video/online_video.html', data)


def start_analysis_video():
    analyzer.read_video()


def online_analysis(request):
    global video_thread
    if video_thread is None or not video_thread.is_alive():
        video_thread = threading.Thread(target=start_analysis_video)
        video_thread.start()
    elif not video_thread.is_alive():
        video_thread = None  # Установка переменной video_thread в значение None после завершения потока
        video_thread = threading.Thread(target=start_analysis_video)
        video_thread.start()
    data = {
        'load_time': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        'text_about': const.TEXT_ONLINE_VIDEO_RESULTS
    }
    return render(request, 'video/online_analysis.html', data)


def safe_object():
    today = datetime.today()
    formatted_date = today.strftime("%Y-%m-%d")
    processed_data = {
        "title": f"График за {formatted_date}",
        "video_file": "онлайн",
        "date": formatted_date
    }

    # Создание экземпляра модели Video и заполнение данными
    video_object = Video.objects.create(
        title=processed_data['title'],
        video_file=processed_data['video_file'],
        date=processed_data['date']
    )

    # Сохранение объекта в базе данных
    video_object.save()


def make_chart_online(dataframe):
    final_mark = round(dataframe['mark'].mean(), 2)
    dataframe['eye_mark'] = dataframe['eye_mark'].fillna('Не распознано')
    dataframe[['eye_mark', 'hor_mark', 'ver_mark', 'square_mark']] = dataframe[
        ['eye_mark', 'hor_mark', 'ver_mark', 'square_mark']]. \
        replace(0, 'Не распознали лицо').bfill()
    dataframe[['eye_mark', 'hor_mark', 'ver_mark', 'square_mark']] = dataframe[
        ['eye_mark', 'hor_mark', 'ver_mark', 'square_mark']]. \
        replace(-1, 'Несколько лиц в кадре').bfill()

    today = datetime.today()
    formatted_date = today.strftime("%d-%m-%Y")

    dataframe = dataframe.rename(columns={'hor_mark': 'По-горизонтали',
                                          'ver_mark': 'По-вертикали',
                                          'square_mark': 'Крупность',
                                          'eye_mark': 'Положение глаз'})
    fig = px.line(dataframe,
                  x='duration',
                  y='mark',
                  title=f'График за {formatted_date}. Итоговая оценка {final_mark}',
                  labels={'duration': 'Длительность видео', 'mark': 'Оценка'},
                  hover_data=['mark', 'По-горизонтали', 'По-вертикали', 'Крупность', 'Положение глаз'],
                  height=700,
                  width=1000
                  )
    plot_html = fig.to_html(full_html=False)
    return plot_html, final_mark


def online_results(request):
    data = {
        'text_about': const.TEXT_ONLINE_VIDEO_RESULTS
    }

    if request.method == 'GET':
        if video_thread is not None or video_thread.is_alive():
            analyzer.set_stop()
            video_thread.join()
            plot_html, final_mark = make_chart_online(analyzer.get_df())
            data = {
                'plot_html': plot_html
            }
            safe_object()
        return render(request, 'video/online_results.html', data)

    if request.method == 'POST':
        file_path = "output.avi"
        if os.path.exists(file_path):
            print("Внутри")
            with open(file_path, 'rb') as f:
                file_content = f.read()
            response = HttpResponse(file_content, content_type='video/x-msvideo')
            response['Content-Disposition'] = 'attachment; filename="output.avi"'
            return response
