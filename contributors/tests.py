from django.contrib.auth.models import User
from .models import Contributor
from projects.models import Project, Task
from rest_framework import status
from rest_framework.test import APITestCase


class ContributorListViewTests(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            username='username1',
            password='password1'
            )
        user2 = User.objects.create_user(
            username='username2',
            password='password2'
            )
        user3 = User.objects.create_user(
            username='username3',
            password='password3'
            )
        Project.objects.create(creator=user1, title='Project 1')
        Project.objects.create(creator=user2, title='Project 2')

    def test_can_list_contributors(self):
        user1 = User.objects.get(username='username1')
        user2 = User.objects.get(username='username2')
        project = Project.objects.get(title='Project 1')
        Contributor.objects.create(creator=user1, user=user2, project=project)
        response = self.client.get('/contributors/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_add_contributor(self):
        self.client.login(username='username1', password='password1')
        user2 = User.objects.get(username='username2')
        project = Project.objects.get(title='Project 1')

        response = self.client.post('/contributors/', {
            'user': user2.id,
            'project': project.id
            })
        count = Contributor.objects.count()

        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_add_contributor(self):
        user1 = User.objects.get(username='username1')
        user2 = User.objects.get(username='username2')
        project = Project.objects.get(title='Project 1')

        response = self.client.post('/contributors/', {
            'creator': user1.id,
            'user': user2.id,
            'project': project.id
            })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_add_self_as_contributor(self):
        self.client.login(username='username1', password='password1')
        user1 = User.objects.get(username='username1')
        project = Project.objects.get(title='Project 1')

        response = self.client.post('/contributors/', {
            'user': user1.id,
            'project': project.id
            })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_add_contributor_to_unowned_project(self):
        self.client.login(username='username1', password='password1')
        user3 = User.objects.get(username='username3')
        project = Project.objects.get(title='Project 2')

        response = self.client.post('/contributors/', {
            'user': user3.id,
            'project': project.id
            })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
