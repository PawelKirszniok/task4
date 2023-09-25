from django.db import models

from budget.models.budget import Budget


class Income(models.Model):
    name = models.CharField(max_length=256)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.CharField(max_length=256)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="incomes")
