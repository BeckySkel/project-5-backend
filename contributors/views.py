from rest_framework import generics, permissions, filters
from devise.permissions import ContributorDeletionPermission
from .models import Contributor
from .serializers import ContributorSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ContributorList(generics.ListCreateAPIView):
    """
    Lists all contributors
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend
    ]

    filterset_fields = [
        # Contributor instances of the selected project
        'project',
        # Contributor invites sent by the selected user
        'creator__profile',
        # Contributor instances of the selected user
        'user__profile'
    ]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ContributorDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve contributor instance and update if owner
    """
    permission_classes = [ContributorDeletionPermission]
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
