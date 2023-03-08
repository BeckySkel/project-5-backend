from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from django.http import Http404
from rest_framework import status, permissions, generics
from devise.permissions import IsOwnerOrReadOnly


# Code from CI walkthrough project
class ProfileList(generics.ListAPIView):
    """
    Lists all profiles
    Creation and updates handled by django signals
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


# Code from CI walkthrough project
class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve profile and update if owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
