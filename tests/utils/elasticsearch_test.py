from django.core.management import call_command


class ElasticSearchMixin:
    def create_elasticsearch_index(self):
        """Create elastic search indices."""
        call_command("search_index", "--rebuild", "-f")
