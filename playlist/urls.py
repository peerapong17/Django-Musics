from playlist import views
from django.urls import path

urlpatterns = [
    path('user/playlist',
         views.user_playlist, name='userPlaylist'),
    path('user/playlist/<int:playlist_id>',
         views.playlist_detail, name='playlistDetail'),
    path('playlist/create/', views.create_playlist, name="createPlaylist"),
    path('playlist/delete/<int:playlist_id>',
         views.delete_playlist, name="deletePlaylist"),
    path('playlist/update/<int:playlist_id>',
         views.update_playlist, name="updatePlaylist"),
    path('playlist/add/<int:song_id>',
         views.add_song_to_playlist, name="addSong"),
    path('add-song/<int:song_id>',
         views.add_song_to_playlist, name="addSongToPlaylist"),
    path('playlist/<int:playlist_id>/delete/add/<int:song_id>',
         views.delete_song_from_playlist, name="deleteSongFromPlaylist"),
    # path('search',
    #      views.index, name="searchSong"),
]
