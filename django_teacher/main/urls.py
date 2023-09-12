from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('upload', views.upload_video, name='upload_video'),
    path('online', views.online_video, name='online_video'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
