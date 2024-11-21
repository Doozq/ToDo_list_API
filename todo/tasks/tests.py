from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Task, Comment
import os
from django.core.files.uploadedfile import SimpleUploadedFile


class TaskApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        self.client.login(username="testuser", password="testpassword")

        self.url = "http://127.0.0.1:8000/api/"

        self.task_data = {
            "title": "Test Task",
            "description": "Test task description",
            "status": "новая",
        }
        self.task = Task.objects.create(**self.task_data)

    def test_get_task_list(self):
        url = self.url + "tasks/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_task_detail(self):
        url = self.url + f"tasks/{self.task.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task.title)
        self.assertEqual(response.data["status"], self.task.status)

    def test_create_task(self):
        url = self.url + "tasks/"
        data = {
            "title": "New Task",
            "description": "Description of the new task",
            "status": "в работе",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Task")
        self.assertEqual(response.data["status"], "в работе")

    def test_update_task(self):
        url = self.url + f"tasks/{self.task.id}/"
        data = {
            "title": "Updated Task Title",
            "description": "Updated description",
            "status": "отменена",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Task Title")
        self.assertEqual(response.data["status"], "отменена")

    def test_partial_update_task(self):
        url = self.url + f"tasks/{self.task.id}/"
        data = {"status": "выполнена"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "выполнена")

    def test_delete_task(self):
        url = self.url + f"tasks/{self.task.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_comment(self):
        url = self.url + f"tasks/{self.task.id}/comments/"
        data = {"text": "Comment"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "Comment")
        self.assertEqual(response.data["task"], self.task.id)

    def test_get_comments(self):
        Comment.objects.create(task=self.task, text="First comment")
        Comment.objects.create(task=self.task, text="Second comment")

        url = self.url + f"tasks/{self.task.id}/comments/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["text"], "First comment")
        self.assertEqual(response.data[1]["text"], "Second comment")

    def test_update_comment(self):
        comment = Comment.objects.create(task=self.task, text="Old comment")
        url = self.url + f"tasks/{self.task.id}/comments/{comment.id}/"
        data = {"text": "Updated comment text"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Updated comment text")

    def test_delete_comment(self):
        comment = Comment.objects.create(
            task=self.task, text="Comment to delete"
        )
        url = self.url + f"tasks/{self.task.id}/comments/{comment.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_upload_file_to_task(self):
        url = self.url + f"tasks/{self.task.id}/"

        test_file = SimpleUploadedFile(
            name="test_file.txt",
            content=b"File content",
            content_type="text/plain",
        )

        data = {
            "title": "Test Task with File",
            "description": "Task with file upload",
            "status": "новая",
            "file": test_file,
        }

        response = self.client.put(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task.refresh_from_db()
        self.assertTrue(os.path.exists(self.task.file.path))

    def test_create_task_missing_title(self):
        url = self.url + "tasks/"
        data = {"description": "Task without title", "status": "новая"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_task_invalid_status(self):
        url = self.url + "tasks/"
        data = {
            "title": "Task with invalid status",
            "description": "This task has invalid status",
            "status": "invalid_status",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)
