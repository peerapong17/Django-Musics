from song import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="song_list"),
    path('<str:genre>',
         views.index, name="sorted_by_genre"),
]
