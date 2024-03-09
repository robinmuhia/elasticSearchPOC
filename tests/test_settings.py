from elastic_search.config.settings import *  # noqa

ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = "django_elasticsearch_dsl.signals.RealTimeSignalProcessor"
ELASTICSEARCH_DSL = {
    "default": {
        "hosts": ["http://localhost:9200"],
    },
}
