from unittest.mock import ANY
from budget.models import Budget
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


class BudgetTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User(username="test_username", first_name="John", last_name="Smith")
        cls.user.save()
        cls.token = AccessToken.for_user(cls.user)
        cls.client = APIClient()

    def test_create_budget(self):
        response = self.client.post(
            "/budget/", data={"name": "test_budget"}, headers={"Authorization": f"Bearer {self.token}"}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"pk": ANY, 'name': 'test_budget'})

        budget = Budget.objects.get(pk=response.json()["pk"])

        self.assertEqual(budget.owner, self.user)

    def test_get_budget(self):
        budget = Budget.objects.create(name="test_budget_get", owner=self.user)
        budget.save()

        response = self.client.get(
            f"/budget/{budget.pk}/", headers={"Authorization": f"Bearer {self.token}"}
        )

        expected = {
            'expenses': [],
            'incomes': [],
            'name': 'test_budget_get',
            'owner': {'first_name': 'John',
                      'is_active': True,
                      'last_name': 'Smith',
                      'pk': self.user.pk,
                      'username': 'test_username'},
            'pk': budget.pk,
            'viewers': []
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_update_budget(self):
        budget = Budget.objects.create(name="test_budget_before", owner=self.user)
        budget.save()

        response = self.client.patch(
            f"/budget/{budget.pk}/",
            data={"name": "updated_name"},
            content_type='application/json',
            headers={"Authorization": f"Bearer {self.token}"}
        )

        expected = {
            'expenses': [],
            'incomes': [],
            'name': 'updated_name',
            'owner': {'first_name': 'John',
                      'is_active': True,
                      'last_name': 'Smith',
                      'pk': self.user.pk,
                      'username': 'test_username'},
            'pk': budget.pk,
            'viewers': []
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_delete_budget(self):
        budget = Budget.objects.create(name="test_budget_delete", owner=self.user)
        budget.save()

        response = self.client.delete(
            f"/budget/{budget.pk}/",headers={"Authorization": f"Bearer {self.token}"}
        )

        self.assertEqual(response.status_code, 204)

        with self.assertRaises(Budget.DoesNotExist):
            Budget.objects.get(pk=budget.pk)

