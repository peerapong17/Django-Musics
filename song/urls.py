from song import views
from django.urls import path


urlpatterns = [
    path('', views.index, name="home"),
    path('genre/<str:genre>',
         views.index, name="sorted_by_genre"),
    path('user/playlist',
         views.userPlaylist, name='userPlaylist'),
    path('user/playlist/<int:playlist_id>',
         views.playlistDetail, name='playlistDetail'),
    path('playlist/create/', views.createPlaylist, name="createPlaylist"),
    path('playlist/delete/<int:playlist_id>',
         views.deletePlaylist, name="deletePlaylist"),
    path('playlist/update/<int:playlist_id>',
         views.updatePlaylist, name="updatePlaylist"),
     path('playlist/add/<int:song_id>',
         views.addSongToPlaylist, name="addSong"),
    path('playlist/<int:playlist_id>/add/<int:song_id>',
         views.addSongToPlaylist, name="addSongToPlaylist"),
    path('playlist/<int:playlist_id>/delete/add/<int:song_id>',
         views.deleteSongFromPlaylist, name="deleteSongFromPlaylist"),
     path('serch',
         views.index, name="searchSong"),
]
