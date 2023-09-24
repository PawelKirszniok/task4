from budget.models import Budget
from budget.serializers.expense import ExpenseSerializer
from budget.serializers.income import IncomeSerializer
from budget.serializers.user import UserSerializer
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


class ShareBudgetSerializer(serializers.Serializer):
    share_with = serializers.ListField(child=serializers.IntegerField())