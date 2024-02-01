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
        name = "Books"

        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Django:
        model = Book
        fields = [
        "title", 
        "description",
        "year",
        "rating", 
        ]

        related_models = [Genre,Country,Author]

    def get_queryset(self):
        return super().get_queryset().prefetch_related("genre","author","country")

