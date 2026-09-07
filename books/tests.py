from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer

BOOKS_URL = reverse("books:books-list")


def detail_url(book_id):
    return reverse(
        "books:books-detail",
        args=(book_id,),
    )


def sample_book(**params):
    defaults = {
        "title": "test_title",
        "author": "test_author",
        "cover": "Hard",
        "inventory": 10,
        "daily_fee": 10,
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_book_list(self):
        response = self.client.get(BOOKS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_detail(self):
        book = sample_book(
            title="not_default_title",
            author="not_default_author",
            cover="SOFT",
            inventory=5,
            daily_fee=50,
        )
        url = detail_url(book.id)

        response = self.client.get(url)
        serializer = BookSerializer(book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        payload = {
            "title": "test_title",
            "author": "not_default_author",
            "cover": "Soft",
            "inventory": 110,
            "daily_fee": 110,
        }
        response = self.client.post(BOOKS_URL, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_book(self):
        book = sample_book()
        url = detail_url(book.id)

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertTrue(Book.objects.filter(id=book.id).exists())

    def test_filter_by_title(self):

        book_with_title_1 = sample_book(title="BBBBBB")
        book_with_title_2 = sample_book(title="CCCCCC")

        response_1 = self.client.get(
            BOOKS_URL,
            {"title": "B"},
        )
        response_2 = self.client.get(
            BOOKS_URL,
            {"title": "C"},
        )

        serializer_with_title_1 = BookSerializer(book_with_title_1)
        serializer_with_title_2 = BookSerializer(book_with_title_2)

        self.assertEqual(response_1.status_code, status.HTTP_200_OK)

        self.assertIn(
            serializer_with_title_1.data,
            response_1.data["results"],
        )
        self.assertNotIn(
            serializer_with_title_1.data,
            response_2.data["results"],
        )

        self.assertIn(
            serializer_with_title_2.data,
            response_2.data["results"],
        )
        self.assertNotIn(
            serializer_with_title_2.data,
            response_1.data["results"],
        )

    def test_filter_by_author(self):

        book_with_author_1 = sample_book(title="BBBBBB", author="BBBBBB")
        book_with_author_2 = sample_book(title="CCCCCC", author="CCCCCC")

        response_1 = self.client.get(
            BOOKS_URL,
            {"author": "B"},
        )
        response_2 = self.client.get(
            BOOKS_URL,
            {"author": "C"},
        )

        serializer_with_author_1 = BookSerializer(book_with_author_1)
        serializer_with_author_2 = BookSerializer(book_with_author_2)

        self.assertEqual(response_1.status_code, status.HTTP_200_OK)

        self.assertIn(
            serializer_with_author_1.data,
            response_1.data["results"],
        )
        self.assertNotIn(
            serializer_with_author_1.data,
            response_2.data["results"],
        )

        self.assertIn(
            serializer_with_author_2.data,
            response_2.data["results"],
        )
        self.assertNotIn(
            serializer_with_author_2.data,
            response_1.data["results"],
        )


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test_password",
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "test_title",
            "author": "not_default_author",
            "cover": "Soft",
            "inventory": 110,
            "daily_fee": 110,
        }
        response = self.client.post(BOOKS_URL, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_delete_book(self):
        book = sample_book()
        url = detail_url(book.id)

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertTrue(Book.objects.filter(id=book.id).exists())


class AdminBooksApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="admin_password",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "test_title",
            "author": "not_default_author",
            "cover": "Soft",
            "inventory": 110,
            "daily_fee": 110,
        }
        response = self.client.post(BOOKS_URL, payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_delete_book(self):
        book = sample_book()
        url = detail_url(book.id)

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
