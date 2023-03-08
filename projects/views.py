from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from django.http import Http404
from devise.permissions import IsOwnerOrReadOnly


# Code inspired by CI walkthrough project
class ProjectList(generics.ListCreateAPIView):
    """
    List projects, can create new if logged in
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


# Code inspired by CI walkthrough project
class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve project and edit or delete if owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


# Code inspired by CI walkthrough project
class TaskList(generics.ListCreateAPIView):
    """
    List tasks, can create new if logged in
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


# Code inspired by CI walkthrough project
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve project and edit or delete if owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
