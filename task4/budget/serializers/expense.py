from rest_framework import serializers

from budget.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["pk", "name", "amount", "category"]
