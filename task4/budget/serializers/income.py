from rest_framework import serializers

from budget.models import Income


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ["pk", "name", "amount", "category"]
