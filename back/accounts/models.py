import os

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from movies.models import Genre

import uuid
from django.utils.deconstruct import deconstructible

@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}_{}.{}'.format(instance.id, uuid.uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)


class User(AbstractUser):
    username_validator = RegexValidator(
        regex='^[a-zA-Z0-9]*$',
        message="Username must contain only letters and numbers.",
    )

    username = models.CharField(
        max_length=15,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField(max_length=30, unique=True)
    like_genres = models.ManyToManyField(Genre, related_name='users')
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    profile_image = models.ImageField(upload_to=UploadToPathAndRename('profile_images/'), blank=True, null=True)

    def is_following(self, user):
        return self.followings.filter(id=user.id).exists()