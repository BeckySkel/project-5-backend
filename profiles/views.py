from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from django.http import Http404
from django.db.models import Count
from rest_framework import status, permissions, generics, filters
from devise.permissions import IsOwnerOrReadOnly


# Code from CI walkthrough project
class ProfileList(generics.ListAPIView):
    """
    Lists all profiles
    Creation handled by django signals
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        created_projects_count=Count('user__projects', distinct=True),
        contrib_projects_count=Count('user__contrib_projects', distinct=True)
    ).order_by('-created_on')

    filter_backends = [
        filters.OrderingFilter
    ]

    ordering_fields = [
        'created_on',
        'created_projects_count',
        'contrib_projects_count'
    ]


# Code from CI walkthrough project
class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve profile instance and update if owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        created_projects_count=Count('user__projects', distinct=True),
        contrib_projects_count=Count('user__contrib_projects', distinct=True)
    )
