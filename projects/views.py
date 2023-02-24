from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer


# Code from CI walkthrough project
class ProjectList(APIView):
    """
    List all projects
    No Create view (post method), as profile creation handled by django signals
    """
    serializer_class = ProjectSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(
            projects,
            many=True,
            context={'request': request}
            )
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(serializer.errrors, status=HTTP_400_BAD_REQUEST)