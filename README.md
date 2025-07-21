# PalaceBuilder

PalaceBuilder is a Django web application that transforms daily task completion into the construction of a beautiful AI-generated palace. Each completed task adds a new architectural layer, motivating productivity through visual rewards.

## Features
- Add, view, and complete daily tasks
- AI-powered task analysis and categorization (GPT-4)
- AI-generated palace layers (DALL-E 3)
- Progressive palace building with visual feedback
- Real-time updates and completion celebrations

## Tech Stack
- Django 4.2, Django REST Framework
- OpenAI GPT-4, DALL-E 3
- SQLite (dev) / PostgreSQL (prod)
- Django Channels (real-time)

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
3. **Run migrations**
   ```
   python manage.py migrate
   ```
4. **Create a superuser**
   ```
   python manage.py createsuperuser
   ```
5. **Start the development server**
   ```
   python manage.py runserver
   ```
6. **Access the app**
   - Visit `http://localhost:8000/`

## Directory Structure
See `project_structure.md` for details.

## License
MIT 