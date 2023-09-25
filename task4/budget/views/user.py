from django.contrib.auth.models import User
from rest_framework import mixins, viewsets
from budget.serializers.user import UserSerializer, CreateUserSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer
        return self.serializer_class

