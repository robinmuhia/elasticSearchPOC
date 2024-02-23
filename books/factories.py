import factory

from .models import Author, Book, Country, Genre


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    name = factory.Faker("country")


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Faker("word")


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker("name")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text")
    year = factory.Faker("year")
    rating = factory.Faker("pyfloat", left_digits=2, right_digits=1, positive=True)
    genre = factory.SubFactory(GenreFactory)
    country = factory.SubFactory(CountryFactory)
    author = factory.SubFactory(AuthorFactory)
