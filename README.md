
**Task Manager API**
====================

**Descrição**
-------------

Esta é uma API Restful desenvolvida em Django com Django Rest Framework para gerenciar tarefas. A API está integrada ao Google Calendar, permitindo que eventos sejam criados e excluídos automaticamente no Google Calendar ao criar ou excluir uma tarefa.

**Requisitos**
--------------

*   **Python 3.12**
*   **Django 5.1**
*   **Django Rest Framework**
*   **Google Calendar API**

**Instalação**
--------------

1.  **Clone o repositório:**
    
        git clone https://github.com/joaosmendess/task-manager-api.git
        cd task-manager-api
        
    
2.  **Crie um ambiente virtual e ative-o:**
    
        python -m venv venv
        source venv/bin/activate  # No Windows use: venv\Scripts\activate
        
    
3.  **Instale as dependências do projeto:**
    
        pip install -r requirements.txt
    
4.  **Configure as credenciais do Google Calendar:**
    *   Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/).
    *   Ative a Google Calendar API.
    *   Crie as credenciais OAuth 2.0 e baixe o arquivo `credentials.json`.
    *   Coloque o arquivo `credentials.json` na raiz do seu projeto.
5.  **Configure as variáveis de ambiente (opcional):**
    *   Certifique-se de configurar as variáveis de ambiente necessárias, como `SECRET_KEY`, `DEBUG`, etc.
6.  **Execute as migrações do banco de dados:**
    
        python manage.py migrate
    
7.  **Inicie o servidor de desenvolvimento:**
    
        python manage.py runserver
    

**Como Usar**
-------------

### **Endpoints**

*   **Criar uma nova tarefa:**
    *   **POST /api/tasks/**
    *   **Exemplo de payload:**
        
            {
                "title": "Reunião com o cliente",
                "description": "Discussão sobre o novo projeto",
                "date": "2024-09-01",
                "time": "10:00:00"
            }
            
        
*   **Buscar tarefas:**
    *   **GET /api/tasks/**
    *   **Parâmetros de busca:**
    
    *   `id`: Busca uma tarefa específica por ID.
    *   `start_date` e `end_date`: Busca tarefas dentro de um intervalo de datas.
    *   `title`: Busca tarefas pelo título, suportando busca parcial.
    
*   **Atualizar uma tarefa:**
    *   **PUT /api/tasks/{id}/**
    *   **Exemplo de payload:**
        
            {
                "title": "Reunião com o cliente - Atualizada",
                "description": "Discussão sobre o novo projeto - Atualizada",
                "date": "2024-09-01",
                "time": "11:00:00"
            }
            
        
*   **Excluir uma tarefa:**
    *   **DELETE /api/tasks/{id}/**

**Integração com Google Calendar**
----------------------------------

*   Ao criar ou excluir uma tarefa, um evento correspondente será criado ou excluído automaticamente no Google Calendar.
*   Para realizar a autenticação com a Google Calendar API, acesse o endpoint `/api/auth/` e siga as instruções para autenticação.

**Teste da API**
----------------

Você pode testar a API usando ferramentas como Insomnia ou Postman. Todos os endpoints devem estar acessíveis via `http://127.0.0.1:8000/api/`.

**Contribuindo**
----------------

Sinta-se à vontade para enviar pull requests. Para grandes mudanças, por favor, abra uma issue primeiro para discutir o que você gostaria de mudar.

**Licença**
-----------

Este projeto está licenciado sob a [MIT License](LICENSE).
