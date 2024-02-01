from rest_framework import serializers

from .models import Book,Genre,Author,Country


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer()
    country = CountrySerializer()

    class Meta:
        model = Book
        fields = "__all__"

class SearchSerializer(serializers.Serializer):
    query = serializers.CharField()