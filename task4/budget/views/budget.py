from django.contrib.auth.models import User
from django.db.models import Q, QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from budget.models import Budget
from budget.serializers.budget import (
    BudgetSerializer,
    CreateBudgetSerializer,
    ShareBudgetSerializer,
)


class BudgetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["name", "owner", "viewers"]

    def get_queryset(self) -> QuerySet:
        if self.request.method in SAFE_METHODS:
            return Budget.objects.filter(
                Q(owner=self.request.user) | Q(viewers__in=[self.request.user])
            )
        return Budget.objects.filter(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def share(self, request, pk) -> Response:
        budget = self.get_object()
        serializer = ShareBudgetSerializer(data=request.data)

        if serializer.is_valid():
            users = User.objects.filter(pk__in=serializer.validated_data["share_with"])
            budget.viewers.set(users)
            budget.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateBudgetSerializer
        return self.serializer_class

    def perform_create(self, serializer) -> None:
        serializer.save(owner=self.request.user)
