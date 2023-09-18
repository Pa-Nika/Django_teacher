from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('history', views.history, name='history'),
    path('upload', views.upload_video, name='upload_video'),
    path('online', views.online_video, name='online_video'),
]
