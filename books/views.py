from .models import Genre,Book,Country,Author
from .serializers import GenreSerializer,BookSerializer,CountrySerializer,AuthorSerializer,SearchSerializer
import abc
from .documents import BookDocument

from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request):
        try:
            serializer = SearchSerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            query:dict = serializer.validated_data.get("query")
            if query is None:
                return HttpResponse(content="No search parameters provided",status=400)
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f"Found {response.hits.total.value} hit(s) for query: '{query}'")

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)

class GenreViewSet(PaginatedElasticSearchAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def generate_q_expression(self, query):
        return Q("bool",
                    should=[
                        Q("match", name=query),
                    ], minimum_should_match=1)


class CountryViewSet(PaginatedElasticSearchAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    def generate_q_expression(self, query):
        return Q("bool",
                    should=[
                        Q("match", name=query),
                    ], minimum_should_match=1)

class AuthorViewSet(PaginatedElasticSearchAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    def generate_q_expression(self, query):
        return Q("bool",
                    should=[
                        Q("match", name=query),
                    ], minimum_should_match=1)

class BookViewSet(PaginatedElasticSearchAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    document_class = BookDocument

    def generate_q_expression(self, query):
        try:
            int(query)
            return Q("bool", should=[
                Q("multi_match", query=query, fields=["year", "rating", "global_ranking", "length", "revenue"]),
            ])
        except ValueError:
            return Q("bool", should=[
                Q("multi_match", query=query, fields=["title", "description"], fuzziness="auto"),
            ])

