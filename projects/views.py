from rest_framework import status, permissions, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from django.http import Http404
from devise.permissions import IsOwnerOrReadOnly
from django.db.models import Count


class ProjectList(generics.ListCreateAPIView):
    """
    List projects, can create new if logged in
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProjectSerializer
    queryset = Project.objects.annotate(
        task_count=Count('tasks', distinct=True)
    ).order_by('-created_on')

    filter_backends = [
        filters.OrderingFilter
    ]

    ordering_fields = [
        'created_on',
        'updated_on',
        'task_count'
    ]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve project and edit or delete if owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProjectSerializer
    queryset = Project.objects.annotate(
        task_count=Count('tasks', distinct=True)
    )


class TaskList(generics.ListCreateAPIView):
    """
    List tasks, can create new if logged in
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    filter_backends = [
        filters.OrderingFilter
    ]

    ordering_fields = [
        'created_on',
        'updated_on',
        'due_date'
    ]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve project and edit or delete if owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
