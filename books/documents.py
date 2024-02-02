from django_elasticsearch_dsl import Document,fields
from django_elasticsearch_dsl.registries import registry
from .models import Book,Genre,Country,Author

@registry.register_document
class BookDocument(Document):
    genre = fields.ObjectField(properties={
        'name': fields.TextField(),
    })
    country = fields.NestedField(properties={
        'name': fields.TextField(),
    })
    author = fields.NestedField(properties={
        'name': fields.TextField(),
    })
    class Index:
        name = "books"

        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Django:
        model = Book
        fields = [
        "id",
        "title", 
        "description",
        "year",
        "rating", 
        ]

        related_models = [Genre,Country,Author]

    def get_queryset(self):
        return super().get_queryset().select_related("genre", "author", "country")

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Genre):
            return BookDocument.search().filter("term", genre__name=related_instance.name)
        elif isinstance(related_instance, Country):
            return BookDocument.search().filter("term", country__name=related_instance.name)
        elif isinstance(related_instance, Author):
            return BookDocument.search().filter("term", author__name=related_instance.name)