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


class ProjectDetailViewTest(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='username1', password='password1')
        user2 = User.objects.create_user(username='username2', password='password2')
        Project.objects.create(creator=user1, title='Project 1')
        Project.objects.create(creator=user2, title='Project 2')

    def test_can_retrieve_project_with_valid_id(self):
        title = 'Project 1'
        project1 = Project.objects.get(title=title)
        response = self.client.get(f'/projects/{project1.id}')

        self.assertEqual(response.data['title'], title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrieve_project_with_invalid_id(self):
        invalid_id = Project.objects.count() + 1
        response = self.client.get(f'/projects/{invalid_id}')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_owned_project(self):
        self.client.login(username='username1', password='password1')

        new_title = 'My Project'
        response = self.client.put(
            '/projects/1',
            {'title': new_title}
            )
        project1 = Project.objects.filter(pk=1).first()

        self.assertEqual(project1.title, new_title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_others_project(self):
        self.client.login(username='username1', password='password1')

        new_title = 'My Project'
        response = self.client.put(
            '/projects/2',
            {'title': new_title}
            )
        project2 = Project.objects.filter(pk=2).first()

        self.assertNotEqual(project2.title, new_title)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
