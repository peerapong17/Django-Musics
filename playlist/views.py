from django.contrib import messages
from django.core import serializers as core_serializers
from django.http import HttpResponse, JsonResponse

from playlist.models import Playlist, Song
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def playlist_detail(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    songs = playlist.songs.all()
    return render(request, 'playlist/detail.html', {"playlist": playlist, "songs": songs})


def create_playlist(request):
    if request.method == "POST":
        if not request.FILES:
            messages.warning(
                request, "Please choose an image")
        else:
            image_file = request.FILES["image"]
            name = request.POST["name"]
            description = request.POST["description"]
            if str(image_file.content_type).startswith("image"):
                playlist = Playlist(
                    name=name, desc=description, image=image_file, user_id=request.user.id)
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


def update_playlist(request, playlist_id):
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
def delete_playlist(request, playlist_id):
    fs = FileSystemStorage()
    playlist = Playlist.objects.get(id=playlist_id)
    fs.delete(str(playlist.image))
    playlist.delete()
    return redirect('userPlaylist')


def user_playlist(request):
    playlists = Playlist.objects.filter(user=request.user.id).all()
    return render(request, 'playlist/user-playlist.html', {'playlists': playlists})


def add_song_to_playlist(request, song_id=None):
    song = Song.objects.get(id=song_id)
    user_playlists = song.playlist_set.filter(user_id=request.user.id).all()
    json_decoded = core_serializers.serialize('json', user_playlists)

    if request.method == "POST":
        user_playlists = [playlist.id for playlist in song.playlist_set.filter(user_id=request.user.id).all()]
        if request.POST['selectedPlaylists'] is not "":
            selected_playlist_checkbox = request.POST['selectedPlaylists'].split(',')
            selected_playlists = [int(item) for item in selected_playlist_checkbox]
        else:
            selected_playlists = []

        if len(selected_playlists) > 0:
            for selected_playlist in selected_playlists:
                if selected_playlist in user_playlists:
                    for item in user_playlists:
                        if item not in selected_playlists:
                            # song = Song.objects.get(id=song_id)
                            song.playlist_set.remove(item)
                else:
                    # song = Song.objects.get(id=song_id)
                    song.playlist_set.add(selected_playlist)
                    # for item in user_playlists:
                    #     if item not in selected_playlists:
                    #         song.playlist_set.remove(item)
        else:
            for item in user_playlists:
                song.playlist_set.remove(item)

    return HttpResponse(json_decoded, content_type="application/json")


def delete_song_from_playlist(request, playlist_id=None, song_id=None):
    playlist = Playlist.objects.get(id=playlist_id)
    playlist.songs.remove(song_id)
    return JsonResponse("Song was deleted from your playlist", safe=False)

    # return redirect("playlistDetail", playlist_id)

# def searchSong(request):
#     products = Product.objects.filter(name__contains=request.GET['title'])
#     return render(request, 'index.html', {'products': products})
