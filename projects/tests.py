from django.contrib.auth.models import User
from .models import Project
from rest_framework import status
from rest_framework.test import APITestCase


class ProjectListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='username', password='password')

    def test_can_list_projects(self):
        user = User.objects.get(username='username')
        Project.objects.create(creator=user, title='My Project')
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='username', password='password')
        response = self.client.post('/projects/', {'title': 'My Project'})
        count = Project.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_post(self):
        response = self.client.post('/projects/', {'title': 'My Project'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
