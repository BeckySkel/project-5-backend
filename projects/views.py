from rest_framework import status, permissions, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from django.http import Http404
from devise.permissions import IsOwnerOrReadOnly
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend


# Projects
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
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]

    filterset_fields = [
        # Projects that the selected user has submitted tasks to
        'tasks__creator__profile',
        # Projects the selected user created
        'creator__profile',
        # Projects the selected user is a contributor on
        'contributors__profile'
    ]

    search_fields = [
        'title',
        'description'
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


# Tasks
class TaskList(generics.ListCreateAPIView):
    """
    List tasks, can create new if logged in
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]

    filterset_fields = [
        # Tasks that the selected user created
        'creator__profile',
        # Tasks submitted to the selected user's created projects
        'project__creator__profile',
        # Tasks submitted to projects the selected user is a contributor on
        'project__contributors__profile',
        # Tasks in the selected project
        'project',
    ]

    search_fields = [
        'summary',
        'body'
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
