from song.models import Genre


def genres(request):
    genres = Genre.objects.all()
    return dict(genres=genres)