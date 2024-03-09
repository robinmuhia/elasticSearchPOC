from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from elastic_search.books.models import Author, Book, Country, Genre


@registry.register_document
class BookDocument(Document):
    genre = fields.ObjectField(
        properties={
            "name": fields.TextField(),
        }
    )
    country = fields.NestedField(
        properties={
            "name": fields.TextField(),
        }
    )
    author = fields.NestedField(
        properties={
            "name": fields.TextField(),
        }
    )

    class Index:
        name = "books"

    class Django:
        model = Book
        fields = [
            "title",
            "description",
            "year",
            "rating",
        ]

        related_models = [Genre, Country, Author]

    def get_queryset(self):
        return super().get_queryset().select_related("genre", "author", "country")

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Genre):
            return related_instance.genres.all()
        elif isinstance(related_instance, Country):
            return related_instance.countries.all()
        elif isinstance(related_instance, Author):
            return related_instance.authors.all()
        else:
            return []
