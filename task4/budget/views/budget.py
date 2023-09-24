from rest_framework import viewsets
from budget.models import Budget, Income, Expense
from budget.serializers.budget import BudgetSerializer, CreateBudgetSerializer
from rest_framework.permissions import IsAuthenticated


class BudgetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateBudgetSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
