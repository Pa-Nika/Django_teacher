import dlib
from django.shortcuts import render, redirect
from .position import position_analyzer
from .forms import VideoForm


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("main/utils/shape_predictor_68_face_landmarks.dat")


def index(request):
    data = {
        'title': 'Главная страница'
    }

    return render(request, 'main/index.html', data)


def about(request):
    return render(request, 'main/about.html')


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            my_video = form.save()
            position = position_analyzer.PositionAnalysis(my_video.video_file.path, detector, predictor)
            position.analyse()
            return redirect('/upload')
    else:
        form = VideoForm()
    return render(request, 'main/upload_video.html', {'form': form})


def online_video(request):
    return render(request, 'main/online_video.html')
