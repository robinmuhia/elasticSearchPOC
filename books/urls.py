from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register("books", views.BookViewSet)

urlpatterns = router.urls
