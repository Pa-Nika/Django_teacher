import dlib
import os
from django.shortcuts import render, redirect
# from .position import position_analyzer
from .forms import VideoForm
from .models import Video


# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor("main/utils/shape_predictor_68_face_landmarks.dat")


def history(request):
    all_videos = Video.objects.all()
    sorted_videos = sorted(all_videos, key=lambda x: x.date, reverse=True)
    data = {
        'title': 'История загрузок',
        'videos': sorted_videos
    }
    return render(request, 'video/history.html', data)


def upload_video(request):
    error = ''
    form = VideoForm()
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            tmp_video = form.save()
            # my_video = form.save()
            # position = position_analyzer.PositionAnalysis(my_video.video_file.path, detector, predictor)
            # position.analyse()
            os.remove(tmp_video.video_file.path)
            return redirect('upload_video')
        else:
            error = 'Введите корректные данные'
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'video/upload_video.html', data)


def online_video(request):
    return render(request, 'video/online_video.html')