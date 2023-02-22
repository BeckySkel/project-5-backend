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
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)