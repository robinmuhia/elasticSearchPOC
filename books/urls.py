from django.urls import path

from .views import BookViewSet

urlpatterns = [
    path("book/", BookViewSet.as_view()),
]
