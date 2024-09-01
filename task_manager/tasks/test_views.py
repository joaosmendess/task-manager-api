from django.test import TestCase
from unittest.mock import patch, MagicMock
from .models import Task
from rest_framework.test import APIClient

class TaskGoogleCalendarTests(TestCase):

    @patch('tasks.views.build')  # Mockar o método build do Google API Client
    def test_delete_task_google_calendar(self, mock_build):
        # Criar uma tarefa no banco de dados com um google_event_id falso
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            date='2024-09-01',
            time='12:00:00',
            google_event_id='fake_event_id'
        )

        # Configuração do mock
        mock_service = MagicMock()
        mock_events = mock_service.events.return_value
        mock_build.return_value = mock_service

        client = APIClient()
        response = client.delete(f'/api/tasks/{task.id}/')

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(id=task.id).exists())  # Verificar se a tarefa foi deletada
        mock_events.delete.assert_called_once_with(calendarId='primary', eventId='fake_event_id')  # Verificar se o evento foi deletado
