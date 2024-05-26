from django.db import models

from movies.models import Movie


class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    known_for_department = models.CharField(max_length=100, null=True)
    profile_path = models.TextField(null=True)
    movies = models.ManyToManyField(Movie, related_name='actors', blank=True)

    def __str__(self):
        return f"{self.name}"
