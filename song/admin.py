from django.contrib import admin
from .models import Genre, Song, Playlist


class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10


class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'singer', 'genre',
                    'image', 'created_at', 'updated_at']
    list_editable = ['singer', 'genre', 'image']
    list_per_page = 10


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'image', 'created_at', 'updated_at']
    list_editable = ['desc', 'image']
    list_per_page = 5


admin.site.register(Genre, GenreAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Playlist, PlaylistAdmin)
