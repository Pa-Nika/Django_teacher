from django.urls import path
from . import views


urlpatterns = [
    path('history', views.history, name='history'),
    path('upload', views.upload_video, name='upload_video'),
    path('online', views.online_video, name='online_video'),
    path('online/analysis', views.online_analysis, name='online_analysis'),
    path('online/results', views.online_results, name='online_results')
]
