import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


def isbn_validator(value):
    if len(str(value)) == 10 or len(str(value)) == 13:
        return value
    else:
        raise ValidationError(
            (f'{value} is not a valid ISBN number'),
            params={'value': value},
        )


class User(AbstractUser):
    pass


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Author)
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.PositiveIntegerField(null=True, blank=True, validators=[isbn_validator])
    pages = models.PositiveIntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=1000, null=True, blank=True)
    language = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title

