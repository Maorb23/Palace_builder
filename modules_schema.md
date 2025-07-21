# PalaceBuilder Modules Schema

## 1. palace_builder (Project Root)
- **settings.py**: Django settings, installed apps, middleware, database config
- **urls.py**: Root URL routing
- **asgi.py/wsgi.py**: ASGI/WSGI entry points

## 2. apps.tasks
- **models.py**: Defines `Task`, `DailySession`, and (optionally) `UserPreferences`
- **views.py**: Task CRUD, dashboard, task completion logic
- **urls.py**: URL patterns for task-related endpoints
- **admin.py**: Admin registration for models

## 3. apps.palaces
- **views.py**: Palace generation, palace progress, image composition
- **admin.py**: Admin registration for palace-related models (if any)

## 4. services
- **openai_service.py**: Functions for GPT-4 task analysis (e.g., `analyze_task`)
- **palace_generator.py**: Functions for DALL-E 3 image generation (e.g., `generate_layer`)

## 5. templates
- **base.html**: Main layout, includes navigation, static assets
- **tasks/dashboard.html**: Task list, input form, palace preview, progress bar

## 6. static
- **js/palace_builder.js**: Frontend interactivity (task actions, palace animations)

## 7. requirements.txt
- Python dependencies for the project

## 8. README.md
- Project documentation, setup instructions 