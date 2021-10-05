from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "genre"
        ordering = ['name']
        # verbose_name='หมวดหมู่สินค้า'
        # verbose_name_plural="ข้อมูลประเภทสินค้า"

    def get_songs_by_genre(self):
        return reverse('sorted_by_genre', args=[self.name])


class Song(models.Model):
    name = models.CharField(max_length=255, unique=True)
    singer = models.CharField(max_length=255, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="songs", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'song'
        ordering = ['-created_at']

    # def get_songs_by_genre(self):
    #     return reverse('sorted_by_category', args=[self.category.singer, self.name])


class Playlist(models.Model):
    name = models.CharField(max_length=255, null=True)
    desc = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="playlists", blank=True)
    songs = models.ManyToManyField(Song)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'playlist'
        ordering = ['-created_at']

    def length_of_songs(self):
        return self.songs.all().count()

    def __str__(self):
        return self.name
