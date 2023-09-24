from budget.models import Income
from rest_framework import serializers


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ["pk", "name", "amount", "category"]
