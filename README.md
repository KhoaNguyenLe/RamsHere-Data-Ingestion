# RamsHereBackend

RamsHereBackend is the decoupling of the backend architecture for the RamsHere application. It is a newly initialized Django project configured to serve as a RESTful API. The backend operates independently from the React frontend, allowing for modular development and deployment.

## Project Motivation
The purpose of this repository is to decouple the monolithic application structure by separating the Django backend from the React frontend. This allows both the frontend and backend to scale independently, organize code more effectively, and improve the development workflow.

## Current State & Structure
The project is set up with **Django** and **Django REST Framework (DRF)**.

``` text
RamsHereBackend/
├── api/                   # The primary Django application for all API endpoints
│   ├── migrations/        # Database migrations for the api app
│   ├── admin.py           # Django admin configuration
│   ├── apps.py            # Application configuration
│   ├── models.py          # Database models (Currently empty, ready for defining tables)
│   ├── tests.py           # Unit tests
│   └── views.py           # API views and viewsets
├── core/                  # The root Django project configuration directory
│   ├── asgi.py            # ASGI config for async web servers
│   ├── settings.py        # Central configuration (contains DRF and CORS setups)
│   ├── urls.py            # Global URL routing
│   └── wsgi.py            # WSGI config for sync web servers
├── venv/                  # Python virtual environment containing all dependencies
├── manage.py              # Django's command-line utility for administrative tasks
└── README.md              # Project documentation
```

### Key Configurations
- **Django REST Framework (DRF)** is installed and added to `INSTALLED_APPS` to facilitate the creation of web APIs.
- **django-cors-headers** is installed, added to `INSTALLED_APPS` and `MIDDLEWARE`, and configured with `CORS_ALLOW_ALL_ORIGINS = True` (for development) so that the separate React frontend can seamlessly communicate with the backend.
- **SQLite3** is used as the default development database (`db.sqlite3`).

## Prerequisites
- Python 3.8+ 

## Setup and Installation

### 1. Activate the Virtual Environment
Before running the project or installing any updates, activate the pre-configured virtual environment:

**On Windows:**
```powershell
.\venv\Scripts\Activate.ps1
# or if using Command Prompt:
.\venv\Scripts\activate.bat
```

**On macOS / Linux:**
```bash
source venv/bin/activate
```

### 2. Apply Database Migrations
Although no custom models have been written yet, Django needs to create its internal tables (like tracking users and admin sessions).

```bash
python manage.py migrate
```

### 3. Review / Install Dependencies
If you need to ensure all dependencies are fresh, they were initially installed via:
```bash
pip install django djangorestframework django-cors-headers
```
*(Optionally, generate a requirements file: `pip freeze > requirements.txt`)*

### 4. Create a Superuser (Optional)
To access the Django Admin interface at `/admin/`, you'll need an admin user:
```bash
python manage.py createsuperuser
```

## Running the Server
Start the Django development server:

```bash
python manage.py runserver
```

The backend API will run at `http://localhost:8000/`. You can navigate to `http://localhost:8000/admin/` to view the administrative panel.

## Next Steps for Development
To start adding functionality:
1. **Define Models:** Open `api/models.py` and define your database schemas (e.g., Events, Users, etc.).
2. **Setup Serialization:** Create an `api/serializers.py` file to convert your model instances into JSON format (using DRF's `ModelSerializer`).
3. **Create Views:** Open `api/views.py` to create the endpoints that the frontend will query.
4. **Wire up URLs:** Create an `api/urls.py` file mapping your endpoints, and include it in `core/urls.py`.
