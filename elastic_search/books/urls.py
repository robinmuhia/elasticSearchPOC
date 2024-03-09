from rest_framework.routers import SimpleRouter

from elastic_search.books import views

router = SimpleRouter()

router.register("books", views.BookViewSet)

urlpatterns = router.urls
