from django.contrib.auth.models import User
from django.db import models


class Budget(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_budgets"
    )
    viewers = models.ManyToManyField(User, related_name="shared_budgets")
