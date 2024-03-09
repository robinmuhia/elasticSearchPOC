import pytest
from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APITestCase

from elastic_search.books.models import Author, Book, Country, Genre
from tests.utils.elasticsearch_test import ElasticSearchMixin

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class BookDocumentTest(APITestCase, TestCase, ElasticSearchMixin):
    def setUp(self):
        """Set up test suite."""
        self.create_elasticsearch_index()
        self.genre = baker.make(
            Genre,
            name="action",
        )
        self.author = baker.make(Author, name="Dave Muhia")
        self.country = baker.make(Country, name="Kenya")
        self.book = baker.make(
            Book,
            title="Edge of Tommorrow",
            description="Best movie",
            year=2014,
            rating=4.2,
            author=self.author,
            genre=self.genre,
            country=self.country,
        )
        self.genre2 = baker.make(
            Genre,
            name="action",
        )
        self.author2 = baker.make(Author, name="John Connor")
        self.country2 = baker.make(Country, name="Kenya")
        self.book2 = baker.make(
            Book,
            title="Demon Slayer",
            description="Tengen Uzui is the GOAT. All your hashiras were killed.",
            year=2023,
            rating=5,
            author=self.author2,
            genre=self.genre2,
            country=self.country2,
        )

    def test_search_endpoint(self):
        """Test the search endpoint."""
        base_url = "/api/books/search/"
        # no search params
        response = self.client.get(base_url)
        assert response.status_code == 200
        assert response.data["count"] == 2
        assert response.data["results"][0]["title"] == self.book.title
        assert response.data["results"][1]["title"] == self.book2.title

        # test search
        response = self.client.get(base_url + "?search=Tommorrow")
        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["title"] == self.book.title

        # test fuzzy search on description
        response = self.client.get(base_url + "?search=kilted")
        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["title"] == self.book2.title

        # test filters
        response = self.client.get(base_url + "?search=a&year=2023")
        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["title"] == self.book2.title
