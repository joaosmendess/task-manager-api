from rest_framework import viewsets
from googleapiclient.discovery import build
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle


SCOPES = ['https://www.googleapis.com/auth/calendar']

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        task = serializer.save()

        # Criar evento no Google Calendar
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                
        service = build('calendar', 'v3', credentials=creds)

        event = {
            'summary': task.title,
            'description': task.description,
            'start': {
                'dateTime': f'{task.date}T{task.time}',
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': f'{task.date}T{task.time}',
                'timeZone': 'America/Sao_Paulo',
            },
        }

        service.events().insert(calendarId='primary', body=event).execute()


def google_calendar_auth(request):
    creds = None
    # O arquivo token.pickle armazena as credenciais do usuário
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Se não houver credenciais válidas, faça o login do usuário
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Salve as credenciais para uso futuro
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return redirect('/')
