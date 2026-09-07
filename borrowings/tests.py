from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowings
from borrowings.serializers import BorrowingsListRetrieveSerializer

BORROWINGS_URL = reverse("borrowings:borrowings-list")


def detail_url(borrowing_id):
    return reverse(
        "borrowings:borrowings-detail",
        args=(borrowing_id,),
    )


def return_url(borrowing_id):
    return reverse(
        "borrowings:borrowings-return-book",
        args=(borrowing_id,),
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


def sample_borrowing(user, book, **params):
    defaults = {
        "expected_return_date": date.today() + timedelta(days=7),
        "book": book,
        "user": user,
    }
    defaults.update(params)

    return Borrowings.objects.create(**defaults)


class UnauthenticatedBorrowingsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_borrowing_list(self):
        response = self.client.get(BORROWINGS_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_borrowing_detail(self):
        user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test_password",
        )

        book = sample_book()
        borrowing = sample_borrowing(
            user=user,
            book=book,
        )

        response = self.client.get(detail_url(borrowing.id))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_create_borrowing(self):

        book = sample_book()

        payload = {
            "expected_return_date": (
                    date.today()
                    + timedelta(days=7)
            ).isoformat(),
            "book": book.id,
        }

        response = self.client.post(
            BORROWINGS_URL,
            payload,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class AuthenticatedBorrowingsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="test_password",
        )

        self.other_user = get_user_model().objects.create_user(
            email="other@test.com",
            password="test_password",
        )

        self.client.force_authenticate(self.user)

    def test_borrowing_list_only_own_borrowings(self):
        own_book = sample_book(
            title="own_book",
        )
        other_book = sample_book(
            title="other_book",
        )

        own_borrowing = sample_borrowing(
            user=self.user,
            book=own_book,
        )

        other_borrowing = sample_borrowing(
            user=self.other_user,
            book=other_book,
        )

        response = self.client.get(BORROWINGS_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        serializer = BorrowingsListRetrieveSerializer(own_borrowing)

        self.assertIn(
            serializer.data,
            response.data["results"],
        )

        self.assertNotIn(
            {**BorrowingsListRetrieveSerializer(other_borrowing).data},
            response.data["results"],
        )

    def test_borrowing_detail_own_borrowing(self):
        book = sample_book()

        borrowing = sample_borrowing(
            user=self.user,
            book=book,
        )

        response = self.client.get(detail_url(borrowing.id))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_borrowing_detail_other_user_borrowing(self):
        book = sample_book()

        borrowing = sample_borrowing(
            user=self.other_user,
            book=book,
        )

        response = self.client.get(detail_url(borrowing.id))

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_filter_by_is_active_true(self):
        active_book = sample_book(
            title="active_book",
        )
        returned_book = sample_book(
            title="returned_book",
        )

        active_borrowing = sample_borrowing(
            user=self.user,
            book=active_book,
            actual_return_date=None,
        )

        returned_borrowing = sample_borrowing(
            user=self.user,
            book=returned_book,
            actual_return_date=date.today(),
        )

        response = self.client.get(
            BORROWINGS_URL,
            {"is_active": "true"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertIn(
            BorrowingsListRetrieveSerializer(active_borrowing).data,
            response.data["results"],
        )

        self.assertNotIn(
            BorrowingsListRetrieveSerializer(returned_borrowing).data,
            response.data["results"],
        )

    def test_filter_by_is_active_false(self):
        active_book = sample_book(
            title="active_book",
        )
        returned_book = sample_book(
            title="returned_book",
        )

        active_borrowing = sample_borrowing(
            user=self.user,
            book=active_book,
            actual_return_date=None,
        )

        returned_borrowing = sample_borrowing(
            user=self.user,
            book=returned_book,
            actual_return_date=date.today(),
        )

        response = self.client.get(
            BORROWINGS_URL,
            {"is_active": "false"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertIn(
            BorrowingsListRetrieveSerializer(returned_borrowing).data,
            response.data["results"],
        )

        self.assertNotIn(
            BorrowingsListRetrieveSerializer(active_borrowing).data,
            response.data["results"],
        )

    def test_filter_by_user_id_does_not_show_other_users_borrowings(self):
        own_book = sample_book(
            title="own_book",
        )
        other_book = sample_book(
            title="other_book",
        )

        own_borrowing = sample_borrowing(
            user=self.user,
            book=own_book,
        )

        other_borrowing = sample_borrowing(
            user=self.other_user,
            book=other_book,
        )

        response = self.client.get(
            BORROWINGS_URL,
            {"user_id": self.other_user.id},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertIn(
            BorrowingsListRetrieveSerializer(own_borrowing).data,
            response.data["results"],
        )

        self.assertNotIn(
            BorrowingsListRetrieveSerializer(other_borrowing).data,
            response.data["results"],
        )

    def test_user_can_return_own_borrowing(self):
        book = sample_book(
            title="return_book",
            inventory=5,
        )

        borrowing = sample_borrowing(
            user=self.user,
            book=book,
            actual_return_date=None,
        )

        response = self.client.post(return_url(borrowing.id))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        borrowing.refresh_from_db()
        book.refresh_from_db()

        self.assertEqual(
            borrowing.actual_return_date,
            date.today(),
        )

        self.assertEqual(
            book.inventory,
            6,
        )

    def test_user_cannot_return_other_user_borrowing(self):
        book = sample_book(
            title="other_book",
            inventory=5,
        )

        borrowing = sample_borrowing(
            user=self.other_user,
            book=book,
            actual_return_date=None,
        )

        response = self.client.post(return_url(borrowing.id))

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        borrowing.refresh_from_db()
        book.refresh_from_db()

        self.assertIsNone(
            borrowing.actual_return_date,
        )

        self.assertEqual(
            book.inventory,
            5,
        )

    def test_user_cannot_return_already_returned_borrowing(self):
        book = sample_book(
            title="returned_book",
            inventory=5,
        )

        borrowing = sample_borrowing(
            user=self.user,
            book=book,
            actual_return_date=date.today(),
        )

        response = self.client.post(return_url(borrowing.id))

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        borrowing.refresh_from_db()
        book.refresh_from_db()

        self.assertEqual(
            borrowing.actual_return_date,
            date.today(),
        )

        self.assertEqual(
            book.inventory,
            5,
        )


class AdminBorrowingsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = get_user_model().objects.create_user(
            email="admin@test.com",
            password="admin_password",
            is_staff=True,
        )

        self.user_1 = get_user_model().objects.create_user(
            email="user1@test.com",
            password="password",
        )

        self.user_2 = get_user_model().objects.create_user(
            email="user2@test.com",
            password="password",
        )

        self.client.force_authenticate(self.admin)

    def test_borrowing_list(self):
        book_1 = sample_book(
            title="book_1",
        )
        book_2 = sample_book(
            title="book_2",
        )

        borrowing_1 = sample_borrowing(
            user=self.user_1,
            book=book_1,
        )

        borrowing_2 = sample_borrowing(
            user=self.user_2,
            book=book_2,
        )

        response = self.client.get(BORROWINGS_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            2,
        )

        self.assertIn(
            BorrowingsListRetrieveSerializer(borrowing_1).data,
            response.data["results"],
        )

        self.assertIn(
            BorrowingsListRetrieveSerializer(borrowing_2).data,
            response.data["results"],
        )

    def test_filter_by_user_id(self):
        book_1 = sample_book(
            title="book_1",
        )
        book_2 = sample_book(
            title="book_2",
        )

        borrowing_1 = sample_borrowing(
            user=self.user_1,
            book=book_1,
        )

        borrowing_2 = sample_borrowing(
            user=self.user_2,
            book=book_2,
        )

        response = self.client.get(
            BORROWINGS_URL,
            {"user_id": self.user_1.id},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertIn(
            BorrowingsListRetrieveSerializer(borrowing_1).data,
            response.data["results"],
        )

        self.assertNotIn(
            BorrowingsListRetrieveSerializer(borrowing_2).data,
            response.data["results"],
        )

    def test_filter_by_is_active_true(self):
        active_book = sample_book(
            title="active_book",
        )
        returned_book = sample_book(
            title="returned_book",
        )

        active_borrowing = sample_borrowing(
            user=self.user_1,
            book=active_book,
            actual_return_date=None,
        )

        returned_borrowing = sample_borrowing(
            user=self.user_2,
            book=returned_book,
            actual_return_date=date.today(),
        )

        response = self.client.get(
            BORROWINGS_URL,
            {"is_active": "true"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertIn(
            BorrowingsListRetrieveSerializer(active_borrowing).data,
            response.data["results"],
        )

        self.assertNotIn(
            BorrowingsListRetrieveSerializer(returned_borrowing).data,
            response.data["results"],
        )

    def test_filter_by_is_active_false(self):
        active_book = sample_book(
            title="active_book",
        )
        returned_book = sample_book(
            title="returned_book",
        )

        active_borrowing = sample_borrowing(
            user=self.user_1,
            book=active_book,
            actual_return_date=None,
        )

        returned_borrowing = sample_borrowing(
            user=self.user_2,
            book=returned_book,
            actual_return_date=date.today(),
        )

        response = self.client.get(
            BORROWINGS_URL,
            {"is_active": "false"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertIn(
            BorrowingsListRetrieveSerializer(returned_borrowing).data,
            response.data["results"],
        )

        self.assertNotIn(
            BorrowingsListRetrieveSerializer(active_borrowing).data,
            response.data["results"],
        )

    def test_admin_can_return_any_borrowing(self):
        book = sample_book(
            title="admin_return_book",
            inventory=5,
        )

        borrowing = sample_borrowing(
            user=self.user_1,
            book=book,
            actual_return_date=None,
        )

        response = self.client.post(return_url(borrowing.id))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        borrowing.refresh_from_db()
        book.refresh_from_db()

        self.assertEqual(
            borrowing.actual_return_date,
            date.today(),
        )

        self.assertEqual(
            book.inventory,
            6,
        )
