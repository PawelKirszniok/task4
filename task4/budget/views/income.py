from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from budget.serializers.income import IncomeSerializer
from budget.models import Budget, Income
from rest_framework.response import Response


class IncomeViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = [IsAuthenticated]
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()

    def create(self, request, budget_pk=None, *args, **kwargs) -> Response:
        budget = get_object_or_404(Budget, pk=budget_pk, owner=self.request.user)
        self.request.budget = budget
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer) -> None:
        serializer.save(budget=self.request.budget)

    def get_queryset(self) -> QuerySet:
        return self.queryset.filter(
            budget=self.kwargs["budget_pk"], budget__owner=self.request.user
        )
