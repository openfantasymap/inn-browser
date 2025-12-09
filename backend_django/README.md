# Fantasy Inn Tycoon - Django Backend

This is the Django backend for Fantasy Inn Tycoon game, providing:
- Django ORM for database management
- Django Admin interface for game data visualization
- Django REST Framework for API endpoints
- SQLite database (can be upgraded to PostgreSQL)

## Status: 🚧 Work in Progress

This is a migration from FastAPI to Django. The project structure is set up but models and business logic are being migrated.

### Completed:
- ✅ Django project structure
- ✅ Django REST Framework configuration
- ✅ CORS configuration for Angular frontend
- ✅ Basic health check endpoint

### In Progress:
- 🔄 Converting Pydantic models to Django ORM models
- 🔄 Migrating game service logic
- 🔄 Creating DRF serializers
- 🔄 Setting up Django Admin interface

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend_django
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (for Admin Interface)

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver 8000
```

The server will be available at:
- API: `http://localhost:8000/api/`
- Admin Interface: `http://localhost:8000/admin/`
- Health Check: `http://localhost:8000/api/health/`

## Django Admin Features

Once models are migrated, you'll be able to:
- 👀 View all game states and players
- 📊 See guest statistics and drops
- 🏠 Manage rooms and upgrades
- 🍖 View tavern items and recipes
- 🧪 Check ingredient inventory
- ✏️ Edit game data directly
- 🔍 Filter and search game entities

## Migration from FastAPI

The original FastAPI backend is in `/backend` directory. This Django version will:
1. Use Django ORM instead of in-memory dictionaries
2. Persist game state to database
3. Provide admin interface for data management
4. Maintain backward compatibility with frontend API

## Next Steps

1. Create Django models for all game entities
2. Migrate game service business logic
3. Create DRF viewsets and serializers
4. Configure Django Admin for all models
5. Test with Angular frontend
6. Deploy with proper database (PostgreSQL)
