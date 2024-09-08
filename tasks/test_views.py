from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from tasks.models import Task, Comment, TaskTimer
from datetime import datetime, timedelta


class TaskTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Creăm o sarcină pentru teste
        self.task = Task.objects.create(title='Test Task', description='Test Description', user=self.user)

    def test_task_list_view(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data[0])
        self.assertIn('title', response.data[0])

    def test_my_tasks_list_view(self):
        url = reverse('my-tasks-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test Task')

    def test_add_comment_to_task(self):
        url = reverse('add-comment-to-task')
        data = {'task_id': self.task.id, 'comment': 'This is a test comment'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, 'This is a test comment')

    def test_start_task_timer(self):
        url = reverse('start-task-timer', args=[self.task.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskTimer.objects.count(), 1)

    def test_stop_task_timer(self):
        timer = TaskTimer.objects.create(task=self.task, user=self.user)
        url = reverse('stop-task-timer', args=[self.task.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        timer.refresh_from_db()
        self.assertIsNotNone(timer.end_time)

    def test_add_task_timer(self):
        url = reverse('add-task-timer')
        data = {
            'task_id': self.task.id,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'duration': 30
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TaskTimer.objects.count(), 1)
        timer = TaskTimer.objects.get()
        self.assertEqual(timer.duration, timedelta(minutes=30))
