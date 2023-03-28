from rest_framework import generics, permissions
from devise.permissions import ContributorDeletionPermission
from .models import Contributor
from .serializers import ContributorSerializer


class ContributorList(generics.ListCreateAPIView):
    """
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ContributorDetail(generics.RetrieveDestroyAPIView):
    """
    """
    permission_classes = [ContributorDeletionPermission]
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
