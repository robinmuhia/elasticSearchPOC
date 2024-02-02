from django.core.management.base import BaseCommand
from django.db import transaction
from ...factories import CountryFactory, AuthorFactory, GenreFactory, BookFactory


class Command(BaseCommand):

    help_text = "Generate books"
    batch_size = 10000

    def add_arguments(self, parser):
        parser.add_argument(
            "no_of_books", type=int, help="no of books to generate in database"
        )

    @transaction.atomic
    def handle(self, *args, **options):

        print("Creating Books")
        CountryFactory.create_batch(194)
        print("created 194 countries")
        GenreFactory.create_batch(34)
        print("created 34 genres")
        AuthorFactory.create_batch(30)
        print("created 30 Authors ✅")
        no_of_movies = options["no_of_books"]
        self.batch_size = no_of_movies // 10
        # create books in batches of given size
        print(f"creating movies in batches of {self.batch_size}")
        for i in range(0, no_of_movies, self.batch_size):
            BookFactory.create_batch(self.batch_size)
            print(f"created {i+self.batch_size} movies ✅")
        print(f"successfully created {no_of_movies} movies ✅")
