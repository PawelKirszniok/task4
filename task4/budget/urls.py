from budget.views import BudgetViewSet, ExpenseViewSet, IncomeViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('', BudgetViewSet)

nested_router = routers.NestedDefaultRouter(router, '', lookup='budget')
nested_router.register('expenses', ExpenseViewSet, basename='budget-expenses')
nested_router.register('incomes', IncomeViewSet, basename='budget-incomes')


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(nested_router.urls)),
]