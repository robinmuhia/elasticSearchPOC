import copy
from abc import abstractmethod

from elasticsearch_dsl import Document, Q
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from elastic_search.books.documents import BookDocument
from elastic_search.books.models import Book
from elastic_search.books.serializers import BookSerializer


class PaginatedElasticSearchAPIView(ModelViewSet, LimitOffsetPagination):
    document_class: Document = None

    @abstractmethod
    def generate_search_query(self, search_terms_list, param_filters):
        """This method should be overridden
        and return a Q() expression."""

    @action(methods=["GET"], detail=False)
    def search(self, request: Request):
        try:
            params = copy.deepcopy(request.query_params)
            search_terms = params.pop("search", None)
            query = self.generate_search_query(
                search_terms_list=search_terms, param_filters=params
            )

            search = self.document_class.search().query(query)
            response = search.to_queryset()

            results = self.paginate_queryset(response)
            serializer = self.serializer_class(results, many=True)

            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(e, status=500)


class BookViewSet(PaginatedElasticSearchAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    document_class = BookDocument

    def generate_search_query(self, search_terms_list: list[str], param_filters: dict):
        if search_terms_list is None:
            return Q("match_all")
        search_terms = search_terms_list[0].replace("\x00", "")
        search_terms.replace(",", " ")
        search_fields = ["title", "description"]
        filter_fields = ["year", "rating"]
        query = Q("multi_match", query=search_terms, fields=search_fields, fuzziness="auto")

        wildcard_query = Q(
            "bool",
            should=[
                Q("wildcard", **{field: f"{search_terms.lower()}*"}) for field in search_fields
            ],
        )
        query = query | wildcard_query

        if len(param_filters) > 0:
            filters = []
            for field in filter_fields:
                if field in param_filters:
                    filters.append(Q("term", **{field: param_filters[field]}))
            filter_query = Q("bool", should=[query], filter=filters)
            query = query & filter_query

        return query
