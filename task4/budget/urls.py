from budget.views import BudgetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', BudgetViewSet)

urlpatterns = router.urls