from django.urls import path
from .views import register, login, music_detail, music_list


urlpatterns = [
    path('music/', music_list, name='music_list'),
    path('music/<int:pk>/', music_detail, name='music_detail'),
    path('signup/', register, name='register'),
    path('login/', login, name='login')
]