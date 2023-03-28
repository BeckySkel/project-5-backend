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

    search_fields = [
        'user',
        'project',
        'creator'
    ]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ContributorDetail(generics.RetrieveDestroyAPIView):
    """
    """
    permission_classes = [ContributorDeletionPermission]
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
