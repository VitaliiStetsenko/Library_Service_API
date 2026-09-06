from django.urls import path, include
from rest_framework import routers

from books.views import BooksViewSet

app_name = "books"

router = routers.DefaultRouter()
router.register("", BooksViewSet, basename="books")

urlpatterns = [path("", include(router.urls))]
