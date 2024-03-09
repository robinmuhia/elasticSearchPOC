from django.db import models

from elastic_search.books.mixins import GenericMixin

# Model Structure for our Movie Database


class Country(GenericMixin):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Genre(GenericMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(GenericMixin):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(GenericMixin):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="genres")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="countries")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="authors")
    year = models.IntegerField()
    rating = models.FloatField()

    def __str__(self):
        return self.title
