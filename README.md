# Project Management API

A Django REST API for managing projects, team members, and comments with role-based access control.

## Features

- User Authentication with Token Auth
- Project Management (CRUD operations)
- Role-based Access Control (Owner, Editor, Reader)
- Project Member Management
- Comment System with permissions

## API Endpoints

### Projects

- `GET /api/projects/` - List all accessible projects
- `POST /api/projects/` - Create a new project
- `GET /api/projects/{id}/` - Retrieve a project
- `PUT /api/projects/{id}/` - Update a project
- `DELETE /api/projects/{id}/` - Delete a project

### Project Members

- `GET /api/project-members/` - List project members
- `POST /api/project-members/` - Add member to project
- `PUT /api/project-members/{id}/` - Update member role
- `DELETE /api/project-members/{id}/` - Remove member

### Comments

- `GET /api/comments/?project_id={id}` - List project comments
- `POST /api/comments/` - Create a comment
- `PUT /api/comments/{id}/` - Update a comment
- `DELETE /api/comments/{id}/` - Delete a comment

## Role-Based Permissions

### Project Owner
- Create and delete projects
- Add/remove project members
- Assign roles to members
- Full access to comments

### Editor
- View project details
- Create and edit own comments
- Cannot modify project settings or members

### Reader
- View project details
- View comments
- Cannot modify anything

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project-management-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Testing

Run the test suite with:
```bash
python manage.py test
```


## API Collection

Import the API collection file in Postman:
`api_collection.json`

The collection includes all endpoints:
- Authentication endpoints
- Project management
- Member management
- Comment system
