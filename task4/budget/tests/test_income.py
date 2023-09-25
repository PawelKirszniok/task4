from decimal import Decimal
from unittest.mock import ANY
from budget.models import Budget, Income
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


class IncomeTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.owner = User(username="test_owner", first_name="John", last_name="Smith")
        cls.owner.save()
        cls.owner_token = AccessToken.for_user(cls.owner)
        cls.viewer = User(
            username="test_viewer", first_name="Susan", last_name="Potter"
        )
        cls.viewer.save()
        cls.viewer_token = AccessToken.for_user(cls.viewer)
        cls.client = APIClient()

    def setUp(self) -> None:
        super().setUp()
        self.budget = Budget.objects.create(name="test_budget_get", owner=self.owner)
        self.budget.viewers.set([self.viewer])
        self.budget.save()

    def test_owner_create_income(self):
        data = {
            "name": "gas",
            "category": "car",
            "amount": "99.50",
        }
        response = self.client.post(
            f"/budget/{self.budget.pk}/incomes/",
            data=data,
            headers={"Authorization": f"Bearer {self.owner_token}"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"pk": ANY, **data})

        income = Income.objects.get(pk=response.json()["pk"])

        self.assertEqual(income.budget, self.budget)

    def test_viewer_create_income(self):
        data = {
            "name": "gas",
            "category": "car",
            "amount": "99.50",
        }
        response = self.client.post(
            f"/budget/{self.budget.pk}/incomes/",
            data=data,
            headers={"Authorization": f"Bearer {self.viewer_token}"},
        )

        self.assertEqual(response.status_code, 404)

    def test_owner_delete_income(self):
        income = Income.objects.create(
            budget=self.budget, name="gas", amount=Decimal("99.5"), category="car"
        )
        income.save()

        response = self.client.delete(
            f"/budget/{self.budget.pk}/incomes/{income.pk}/",
            headers={"Authorization": f"Bearer {self.owner_token}"},
        )

        self.assertEqual(response.status_code, 204)

        with self.assertRaises(Income.DoesNotExist):
            Income.objects.get(pk=income.pk)

    def test_viewer_delete_income(self):
        income = Income.objects.create(
            budget=self.budget, name="gas", amount=Decimal("99.5"), category="car"
        )
        income.save()

        response = self.client.delete(
            f"/budget/{self.budget.pk}/incomes/{income.pk}/",
            headers={"Authorization": f"Bearer {self.viewer_token}"},
        )

        self.assertEqual(response.status_code, 404)

    def test_owner_update_income(self):
        income = Income.objects.create(
            budget=self.budget, name="gas", amount=Decimal("99.5"), category="car"
        )
        income.save()

        response = self.client.patch(
            f"/budget/{self.budget.pk}/incomes/{income.pk}/",
            headers={"Authorization": f"Bearer {self.owner_token}"},
            data={"name": "premium gas"},
            content_type="application/json",
        )

        expected = {
            "pk": income.pk,
            "name": "premium gas",
            "category": "car",
            "amount": "99.50",
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_viewer_update_income(self):
        income = Income.objects.create(
            budget=self.budget, name="gas", amount=Decimal("99.5"), category="car"
        )
        income.save()

        response = self.client.patch(
            f"/budget/{self.budget.pk}/incomes/{income.pk}/",
            headers={"Authorization": f"Bearer {self.viewer_token}"},
            data={"name": "premium gas"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
