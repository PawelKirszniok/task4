from budget.models import Budget
from budget.serializers import ExpenseSerializer, IncomeSerializer, UserSerializer
from rest_framework import serializers


class BudgetSerializer(serializers.ModelSerializer):
    incomes = IncomeSerializer(many=True, read_only=True)
    expenses = ExpenseSerializer(many=True, read_only=True)
    owner = UserSerializer()
    viewers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Budget
        fields = ["pk", "incomes", "expenses", "name", "viewers", "owner"]


class CreateBudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = ["pk", "name"]

