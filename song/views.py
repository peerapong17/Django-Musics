from django.contrib import messages
from song.models import Genre, Playlist, Song
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage


def index(request, genre=None):
    playlists = Playlist.objects.filter(user_id=request.user.id).all()
    # all_playlist = Playlist.objects.get(id=19)
    # print(all_playlist.songs.all())
    # all_songs=  Song.objects.all()
    # print(all_songs.playlist_set.all())
    if genre != None:
        genres = get_object_or_404(Genre, name=genre)

        if request.method == "POST":
            search = request.POST["search"]
            songs = genres.song_set.filter(name__contains=search)
        else:
            songs = genres.song_set.all()

        return render(request, 'song/index.html', {'songs': songs, "playlists": playlists})
    else:
        if request.method == "POST":
            search = request.POST["search"]
            songs = Song.objects.filter(name__contains=search)
        else:
            songs = Song.objects.all()

        return render(request, 'song/index.html', {'songs': songs, "playlists": playlists})


def playlistDetail(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    songs = playlist.songs.all()
    return render(request, 'playlist/playlist-detail.html', {"playlist": playlist, "songs": songs})


def createPlaylist(request):
    if request.method == "POST":
        imageFile = request.FILES["image"]
        name = request.POST["name"]
        description = request.POST["description"]

        if str(imageFile.content_type).startswith("image"):
            playlist = Playlist(
                name=name, desc=description, image=imageFile, user_id=request.user.id)
            playlist.save()
            return redirect("playlistDetail", playlist.id)
        else:
            messages.warning(
                request, "Invalid image type, please type again")
            render(request, 'playlist/create.html')

        # another way
        # if str(imageFile.content_type).startswith("image"):
        #     fs = FileSystemStorage()
        #     img_url = "playlists/" + imageFile.name
        #     fs.save(img_url, imageFile)
        #     playlist = Playlist(
        #         name=name, desc=description, image=img_url)
        #     # playlist.save()
        #     messages.success(request, "บันทึกข้อมูลเรียบร้อย")
        #     return redirect("userPlaylist")
        # else:
        #     messages.info(
        #         request, "invalid image type, please type again")
        #     render(request, 'playlist/create.html')
    return render(request, 'playlist/create.html')


def updatePlaylist(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        if request.FILES["image"] is not None:
            if str(request.FILES["image"].content_type).startswith("image"):
                fs = FileSystemStorage()
                fs.delete(str(playlist.image))
                playlist.name = name
                playlist.desc = description
                playlist.image = request.FILES["image"]
                playlist.save()
                return redirect("playlistDetail", playlist.id)
            else:
                messages.warning(
                    request, "Invalid image type, please type again")
                return redirect("updatePlaylist", playlist_id)
        else:
            playlist.name = name
            playlist.description = description
            playlist.save()

    return render(request, 'playlist/update.html', {"playlist": playlist})


@login_required(login_url='signIn')
def deletePlaylist(request, playlist_id):
    fs = FileSystemStorage()
    playlist = Playlist.objects.get(id=playlist_id)
    fs.delete(str(playlist.image))
    playlist.delete()
    return redirect('userPlaylist')


def userPlaylist(request):
    playlists = Playlist.objects.filter(user=request.user.id).all()
    return render(request, 'playlist/user-playlist.html', {'playlists': playlists})


def addSongToPlaylist(request, playlist_id=None, song_id=None):
    playlists = Playlist.objects.filter(user_id=request.user.id)
    song = Song.objects.get(id=song_id)

    if playlist_id is not None:
        if not song.playlist_set.filter(id=playlist_id):
            song.playlist_set.add(playlist_id)
            return redirect("playlistDetail", playlist_id)

        else:
            messages.warning(request, "This song already exist in your playlist")


    return render(request, "playlist/add-song.html", {"playlists": playlists, "song": song})


def deleteSongFromPlaylist(request, playlist_id=None, song_id=None):
    playlist = Playlist.objects.get(id=playlist_id)
    playlist.songs.remove(song_id)
    return redirect("playlistDetail", playlist_id)


# def searchSong(request):
#     products = Product.objects.filter(name__contains=request.GET['title'])
#     return render(request, 'index.html', {'products': products})
