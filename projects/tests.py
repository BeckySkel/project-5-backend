from django.contrib.auth.models import User
from .models import Project, Task
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

    def test_logged_in_user_can_create_project(self):
        self.client.login(username='username', password='password')

        response = self.client.post('/projects/', {'title': 'My Project'})
        count = Project.objects.count()

        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_project(self):
        response = self.client.post('/projects/', {'title': 'My Project'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProjectDetailViewTest(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            username='username1',
            password='password1'
            )
        user2 = User.objects.create_user(
            username='username2',
            password='password2'
            )
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


# Tasks
class TaskListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='username', password='password')
        user = User.objects.get(username='username')
        Project.objects.create(creator=user, title='My Project')

    def test_can_list_tasks(self):
        user = User.objects.get(username='username')
        project = Project.objects.get(title='My Project')
        Task.objects.create(
            creator=user,
            summary='summary',
            body='body',
            project=project)
        response = self.client.get('/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_task(self):
        self.client.login(username='username', password='password')
        project = Project.objects.get(title='My Project')

        response = self.client.post('/tasks/', {
            'summary': 'summary',
            'body': 'body',
            'project': project.id,
            })
        count = Task.objects.count()

        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_task(self):
        project = Project.objects.get(title='My Project')
        response = self.client.post('/tasks/', {
            'summary': 'summary',
            'body': 'body',
            'project': project.id,
            })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TaskDetailViewTest(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            username='username1',
            password='password1'
            )
        user2 = User.objects.create_user(
            username='username2',
            password='password2'
            )
        project1 = Project.objects.create(creator=user1, title='Project 1')
        project2 = Project.objects.create(creator=user2, title='Project 2')
        task1 = Task.objects.create(
            creator=user2,
            summary='summary 1',
            body='body 1',
            project=project1
        )
        task2 = Task.objects.create(
            creator=user2,
            summary='summary 2',
            body='body 2',
            project=project2
        )

    def test_can_retrieve_task_with_valid_id(self):
        summary = 'summary 1'
        task1 = Task.objects.get(summary=summary)
        response = self.client.get(f'/tasks/{task1.id}')

        self.assertEqual(response.data['summary'], summary)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrieve_task_with_invalid_id(self):
        invalid_id = Task.objects.count() + 1
        response = self.client.get(f'/tasks/{invalid_id}')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_owned_task(self):
        self.client.login(username='username1', password='password1')

        new_summary = 'new summary'
        response = self.client.patch(
            '/tasks/1',
            {'summary': new_summary}
            )
        task1 = Task.objects.filter(pk=1).first()

        self.assertEqual(task1.summary, new_summary)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_task_if_not_creator_or_contrib(self):
        self.client.login(username='username1', password='password1')

        new_summary = 'new summary'
        response = self.client.patch(
            '/tasks/2',
            {'summary': new_summary}
            )
        task2 = Task.objects.filter(pk=2).first()

        self.assertNotEqual(task2.summary, new_summary)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
