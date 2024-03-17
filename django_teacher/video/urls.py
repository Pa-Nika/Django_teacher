from django.urls import path
from . import views


urlpatterns = [
    path('history', views.history, name='history'),
    path('upload', views.upload_video, name='upload_video'),
    path('online', views.online_video, name='online_video')
    # path('video/feed', views.video_feed, name='video_feed'),
]
