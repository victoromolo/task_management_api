# Task Management API

This project is a Task Management API built with Django and Django REST Framework. It includes task management features and user authentication functionality.

## Setup

1. Clone the repository
2. Create a virtual environment and activate it
3. Install the required packages:
   ```
   pip install django djangorestframework django-filter
   ```
4. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Start the development server:
   ```
   python manage.py runserver
   ```

## User Model

The project uses a custom user model (`CustomUser`) that extends Django's `AbstractUser`. It includes the following fields:

- Username
- Email (unique)
- Password

Additional fields can be added to the `CustomUser` model in `accounts/models.py` as needed.

## API Endpoints

### User Authentication
- User Registration: POST `/api/accounts/register/`
- User Login: POST `/api/accounts/login/`
- User Logout: POST `/api/accounts/logout/`

### Task Model
The Task model includes the following fields:

- title: CharField
- description: TextField
- due_date: DateField
- priority_level: CharField (choices: LOW, MEDIUM, HIGH)
- status: CharField (choices: PENDING, COMPLETED)
- user: ForeignKey to User model
- created_at: DateTimeField
- updated_at: DateTimeField
- completed_at: DateTimeField (null=True, blank=True)

### Task Management
- List/Create Tasks: GET/POST `/api/tasks/`
- Retrieve/Update/Delete Task: GET/PUT/DELETE `/api/tasks/<task_id>/`
- Mark Task as Complete: POST /api/tasks/<task_id>/complete/
- Mark Task as Incomplete: POST /api/tasks/<task_id>/incomplete/
- Retrieve Task History: GET /api/tasks/<task_id>/history/

### Task Completion Features

- Tasks can be marked as complete or incomplete using the respective endpoints.
- When a task is marked as complete, the completed_at timestamp is set.
- Completed tasks cannot be edited unless they are first marked as incomplete.

### Task History Features

- Task completion and reopening actions are tracked in the TaskHistory model.
- Users can retrieve a list of all their completed tasks.
- Users can view the history of actions performed on a specific task.
- The task history includes the action performed (COMPLETED or REOPENED) and the timestamp of the action.

#### Filtering and Sorting
- Filter tasks: GET `/api/tasks/?status=PENDING&priority_level=HIGH`
- Sort tasks: GET `/api/tasks/?ordering=-due_date`

## Authentication

The API uses Token Authentication. Include the token in the Authorization header for protected endpoints:

```
Authorization: Token <your-token-here>
```

## Task Endpoints

### Create a Task
**URL**: `/api/tasks/`  
**Method**: `POST`  
**Authentication**: Required  
**Request Body**:  
```json
{
    "title": "Task title",
    "description": "Task description",
    "due_date": "YYYY-MM-DD",
    "priority_level": "High",
    "status": "Pending"
}

Static Files
Static files (CSS and JavaScript) are stored in the static/ directory. I have added:

- static/css/styles.css: Contains all the CSS styles for the project.
- static/js/scripts.js: Contains JavaScript functionality for the project.

Forms
We've created custom forms for user authentication and task management:
Accounts App Forms (accounts/forms.py):

CustomUserCreationForm: Extends Django's UserCreationForm for user registration.
LoginForm: Custom form for user login.

Tasks App Forms (tasks/forms.py):

TaskForm: ModelForm for creating and updating tasks.
TaskFilterForm: Form for filtering and sorting tasks.

Templates
Templates are stored in the templates/ directory. i have created:

- base.html: The base template that other templates extend.
- home.html: The homepage template.
Account-related templates in templates/accounts/:

- login.html
- register.html
- profile.html


Task-related templates in templates/tasks/:

- task_list.html
- task_detail.html
- task_form.html



Templates use Django's template language for dynamic content and extend the base.html template for consistent layout.
