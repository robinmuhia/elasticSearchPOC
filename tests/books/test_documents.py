import pytest
from django.test import TestCase
from model_bakery import baker

from elastic_search.books.documents import BookDocument
from elastic_search.books.models import Author, Book, Country, Genre
from tests.utils.elasticsearch_test import ElasticSearchMixin


@pytest.mark.django_db
class BookDocumentTest(TestCase, ElasticSearchMixin):
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

    def test_document_indexing(self):
        """Make sure document is properly indexed."""
        book_hits = BookDocument().search().execute()
        assert book_hits is not None
        book_hit = book_hits.hits[0]
        assert book_hit.genre.name == "action"
        assert book_hit.country.name == "Kenya"
        assert book_hit.author.name == "Dave Muhia"
        assert book_hit.title == "Edge of Tommorrow"
        assert book_hit.description == "Best movie"
        assert book_hit.year == 2014
        assert book_hit.rating == 4.2

    def test_get_queryset(self):
        queryset = BookDocument().get_queryset()
        assert len(queryset) == 1

    def test_get_instances_from_related(self):
        """Test retrieval of related models."""
        book_document = BookDocument()

        genre_instance = book_document.get_instances_from_related(self.genre)
        assert genre_instance is not None
        assert len(genre_instance) == 1
        assert genre_instance[0].title == self.book.title

        author_instance = book_document.get_instances_from_related(self.author)
        assert author_instance is not None
        assert len(author_instance) == 1
        assert author_instance[0].title == self.book.title

        country_instance = book_document.get_instances_from_related(self.country)
        assert country_instance is not None
        assert len(country_instance) == 1
        assert country_instance[0].title == self.book.title
