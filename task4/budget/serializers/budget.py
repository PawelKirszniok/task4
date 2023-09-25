from collections import defaultdict

from rest_framework import serializers

from budget.models import Budget, Expense, Income
from budget.serializers.expense import ExpenseSerializer
from budget.serializers.income import IncomeSerializer
from budget.serializers.user import UserSerializer


class BudgetSerializer(serializers.ModelSerializer):
    incomes = serializers.SerializerMethodField(method_name="get_grouped_incomes")
    expenses = serializers.SerializerMethodField(method_name="get_grouped_expenses")
    owner = UserSerializer()
    viewers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Budget
        fields = ["pk", "incomes", "expenses", "name", "viewers", "owner"]

    def get_grouped_expenses(self, obj: Budget) -> dict:
        expenses = Expense.objects.filter(budget=obj)
        return self._group_by_category(expenses, ExpenseSerializer)

    def get_grouped_incomes(self, obj: Budget) -> dict:
        incomes = Income.objects.filter(budget=obj)
        return self._group_by_category(incomes, IncomeSerializer)

    def _group_by_category(
        self, line_items: list, item_serializer: type[serializers.Serializer]
    ) -> dict:
        grouped = defaultdict(list)
        for item in line_items:
            grouped[item.category].append(item_serializer(item).data)
        return grouped


class CreateBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["pk", "name"]


class ShareBudgetSerializer(serializers.Serializer):
    share_with = serializers.ListField(child=serializers.IntegerField())
