from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from budget.serializers.user import UserSerializer, CreateUserSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'first_name', 'last_name']

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer
        return self.serializer_class

