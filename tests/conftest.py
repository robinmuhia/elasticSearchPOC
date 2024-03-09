import pytest
from django.conf import settings
from elasticsearch import Elasticsearch


@pytest.fixture(autouse=True)
def clear_elasticsearch_indices():
    """
    Fixture to clear all Elasticsearch indices after each test case.
    """
    es = Elasticsearch(hosts=settings.ELASTICSEARCH_DSL["default"]["hosts"])

    indices = es.options().indices.get_alias(index="*").keys()

    for index_name in indices:
        es.options(ignore_status=[404, 400]).indices.delete(index=index_name)
    yield
