from django.shortcuts import render, get_object_or_404
from playlist.models import Genre, Song, Playlist


# Create your views here.
def index(request, genre=None):
    user_playlists = Playlist.objects.filter(user_id=request.user.id)

    if genre is not None:
        genres = get_object_or_404(Genre, name=genre)

        if request.method == "POST":
            search = request.POST["search"]
            songs = genres.song_set.filter(name__contains=search)
        else:
            songs = genres.song_set.all()

    else:
        if request.method == "POST":
            search = request.POST["search"]
            songs = Song.objects.filter(name__contains=search)
        else:
            songs = Song.objects.all()

    return render(request, 'song/index.html', {'songs': songs, 'user_playlists': user_playlists})

