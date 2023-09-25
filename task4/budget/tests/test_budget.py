from decimal import Decimal
from unittest.mock import ANY
from budget.models import Budget, Expense
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


class BudgetTestCase(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User(username="test_username", first_name="John", last_name="Smith")
        cls.user.save()
        cls.token = AccessToken.for_user(cls.user)
        cls.client = APIClient()

    def test_create_budget(self):
        response = self.client.post(
            "/budget/",
            data={"name": "test_budget"},
            headers={"Authorization": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"pk": ANY, "name": "test_budget"})

        budget = Budget.objects.get(pk=response.json()["pk"])

        self.assertEqual(budget.owner, self.user)

    def test_get_budget(self):
        budget = Budget.objects.create(name="test_budget_get", owner=self.user)
        budget.save()

        response = self.client.get(
            f"/budget/{budget.pk}/", headers={"Authorization": f"Bearer {self.token}"}
        )

        expected = {
            "expenses": {},
            "incomes": {},
            "name": "test_budget_get",
            "owner": {
                "first_name": "John",
                "is_active": True,
                "last_name": "Smith",
                "pk": self.user.pk,
                "username": "test_username",
            },
            "pk": budget.pk,
            "viewers": [],
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_update_budget(self):
        budget = Budget.objects.create(name="test_budget_before", owner=self.user)
        budget.save()

        response = self.client.patch(
            f"/budget/{budget.pk}/",
            data={"name": "updated_name"},
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.token}"},
        )

        expected = {
            "expenses": {},
            "incomes": {},
            "name": "updated_name",
            "owner": {
                "first_name": "John",
                "is_active": True,
                "last_name": "Smith",
                "pk": self.user.pk,
                "username": "test_username",
            },
            "pk": budget.pk,
            "viewers": [],
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_delete_budget(self):
        budget = Budget.objects.create(name="test_budget_delete", owner=self.user)
        budget.save()

        response = self.client.delete(
            f"/budget/{budget.pk}/", headers={"Authorization": f"Bearer {self.token}"}
        )

        self.assertEqual(response.status_code, 204)

        with self.assertRaises(Budget.DoesNotExist):
            Budget.objects.get(pk=budget.pk)

    def test_share_budget(self):
        user = User(
            username="test_other_username", first_name="Susan", last_name="Potter"
        )
        user.save()
        token = AccessToken.for_user(user)
        budget = Budget.objects.create(name="test_budget_get", owner=user)
        budget.save()

        #  self.user is not authorized
        response = self.client.get(
            f"/budget/{budget.pk}/", headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            f"/budget/{budget.pk}/share/",
            data={"share_with": [self.user.pk]},
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 204)

        #  self.user is authorized
        response = self.client.get(
            f"/budget/{budget.pk}/", headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()["viewers"]), 1)

    def test_list_endpoint(self):
        user = User(username="stephens", first_name="Stephen", last_name="Smith")
        user.save()
        token = AccessToken.for_user(user)

        budget1 = Budget.objects.create(name="cars", owner=user)
        budget1.save()

        budget2 = Budget.objects.create(name="groceries", owner=user)
        budget2.save()

        response = self.client.get(
            f"/budget/?ordering=name", headers={"Authorization": f"Bearer {token}"}
        )

        expected = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "expenses": {},
                    "incomes": {},
                    "name": "cars",
                    "owner": {
                        "first_name": "Stephen",
                        "is_active": True,
                        "last_name": "Smith",
                        "pk": user.pk,
                        "username": "stephens",
                    },
                    "pk": budget1.pk,
                    "viewers": [],
                },
                {
                    "expenses": {},
                    "incomes": {},
                    "name": "groceries",
                    "owner": {
                        "first_name": "Stephen",
                        "is_active": True,
                        "last_name": "Smith",
                        "pk": user.pk,
                        "username": "stephens",
                    },
                    "pk": budget2.pk,
                    "viewers": [],
                },
            ],
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

        #  another user does not see the results
        response = self.client.get(
            f"/budget/", headers={"Authorization": f"Bearer {self.token}"}
        )

        expected = {"count": 0, "next": None, "previous": None, "results": []}

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), expected)

    def test_filter_list_endpoint(self):
        user = User(username="stephens", first_name="Stephen", last_name="Smith")
        user.save()
        token = AccessToken.for_user(user)

        budget1 = Budget.objects.create(name="cars", owner=user)
        budget1.save()

        budget2 = Budget.objects.create(name="groceries", owner=user)
        budget2.save()

        response = self.client.get(
            f"/budget/?name=cars", headers={"Authorization": f"Bearer {token}"}
        )

        expected = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "expenses": {},
                    "incomes": {},
                    "name": "cars",
                    "owner": {
                        "first_name": "Stephen",
                        "is_active": True,
                        "last_name": "Smith",
                        "pk": user.pk,
                        "username": "stephens",
                    },
                    "pk": budget1.pk,
                    "viewers": [],
                },
            ],
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), expected)

    def test_group_line_items(self):
        budget = Budget.objects.create(name="test_grouped_budget", owner=self.user)
        budget.save()
        expense = Expense.objects.create(
            budget=budget, name="gas", amount=Decimal("99.5"), category="car"
        )
        expense.save()
        expense = Expense.objects.create(
            budget=budget, name="repair", amount=Decimal("499.5"), category="car"
        )
        expense.save()
        expense = Expense.objects.create(
            budget=budget, name="groceries", amount=Decimal("50.40"), category="food"
        )
        expense.save()

        response = self.client.get(
            f"/budget/{budget.pk}/", headers={"Authorization": f"Bearer {self.token}"}
        )

        expected = {
            "expenses": {
                "car": [
                    {"amount": "99.50", "category": "car", "name": "gas", "pk": 1},
                    {"amount": "499.50", "category": "car", "name": "repair", "pk": 2},
                ],
                "food": [
                    {
                        "amount": "50.40",
                        "category": "food",
                        "name": "groceries",
                        "pk": 3,
                    }
                ],
            },
            "incomes": {},
            "name": "test_grouped_budget",
            "owner": {
                "first_name": "John",
                "is_active": True,
                "last_name": "Smith",
                "pk": self.user.pk,
                "username": "test_username",
            },
            "pk": budget.pk,
            "viewers": [],
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)
