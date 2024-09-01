from django.shortcuts import redirect
from rest_framework import viewsets
from googleapiclient.discovery import build
from .models import Task
from .serializers import TaskSerializer
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle


SCOPES = ['https://www.googleapis.com/auth/calendar']

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()  # Certifique-se de que o queryset esteja presente
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        
        # Filtrar por ID
        task_id = self.request.query_params.get('id')
        if task_id:
            queryset = queryset.filter(id=task_id)
        
        # Filtrar por período de datas
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        
        # Filtrar por título (texto composto e palavras parciais)
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        
        return queryset

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

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        
        # Armazena o eventId no banco de dados para futuras atualizações
        task.google_event_id = created_event['id']
        task.save()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        task = self.get_object()
        
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                
        service = build('calendar', 'v3', credentials=creds)

        # Atualizar o evento no Google Calendar usando o eventId armazenado
        if task.google_event_id:
            event = service.events().get(calendarId='primary', eventId=task.google_event_id).execute()

            event['summary'] = task.title
            event['description'] = task.description
            event['start'] = {'dateTime': f'{task.date}T{task.time}', 'timeZone': 'America/Sao_Paulo'}
            event['end'] = {'dateTime': f'{task.date}T{task.time}', 'timeZone': 'America/Sao_Paulo'}

            updated_event = service.events().update(calendarId='primary', eventId=task.google_event_id, body=event).execute()

        return response


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
