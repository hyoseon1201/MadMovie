from django.db import models


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    adult = models.BooleanField()
    title = models.CharField(max_length=200)
    views = models.IntegerField(default=0)
    original_title = models.CharField(max_length=200, null=True)
    overview = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    release_date = models.DateField()
    poster_path = models.TextField(null=True)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()