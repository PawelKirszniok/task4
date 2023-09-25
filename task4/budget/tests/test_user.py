from decimal import Decimal
from unittest.mock import ANY
from budget.models import Budget, Income
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


class UserTestCase(TestCase):

    def test_create_user(self):
        data = {
            "username": "test_user",
            "password": "test_password",
            "email": "test@test.com"
        }
        response = self.client.post(
            "/user/", data=data
        )

        self.assertEqual(response.status_code, 201)

        User.objects.get(pk=response.json()["pk"])

    def test_list_users(self):
        user1 = User.objects.create_user(username="test1", password="test_password_1")
        user2 = User.objects.create_user(username="test2", password="test_password_2")

        response = self.client.get("/user/")

        self.assertEqual(response.status_code, 200)
        users = response.json()
        expected = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "pk": user1.pk,
                    "username": "test1",
                    "first_name": "",
                    "last_name": "",
                    "is_active": True
                },

                {
                    "pk": user2.pk,
                    "username": "test2",
                    "first_name": "",
                    "last_name": "",
                    "is_active": True
                }
            ]
        }

        self.assertEqual(users, expected)


