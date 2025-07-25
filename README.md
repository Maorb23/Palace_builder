# PalaceBuilder

A Django web application for task management, palace visualization, and AI-powered palace generation.

## Overview

**PalaceBuilder** is a modern Django project that allows users to manage tasks, visualize progress as a palace, and generate palace images using AI (OpenAI GPT-4 and DALL-E 3). The project is modular, extensible, and ready for deployment.

## Features
- Task management with dashboard and user preferences
- Palace generation and visualization
- AI integration for task analysis and image generation
- User authentication and session management
- Responsive UI with Django templates and static assets

## Project Structure

```
.
├── manage.py
├── palace_builder/           # Django project settings and root config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/
│   ├── tasks/                # Task management app
│   └── palaces/              # Palace generation app
├── services/                 # AI integration (OpenAI GPT-4, DALL-E 3)
├── templates/                # HTML templates
├── static/                   # Static files (JS, CSS, images)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

See `project_structure.md` and `modules_schema.md` for detailed module descriptions.

## Setup

### Prerequisites
- Python 3.9+
- [Django 4.2](https://www.djangoproject.com/)
- [OpenAI API key](https://platform.openai.com/)
- (Optional) PostgreSQL for production

### Installation
1. Clone the repo:
   ```sh
   git clone <your-repo-url>
   cd palace
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venvp
   source venvp/bin/activate  # or venvp\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up your environment variables (see `.env.example` if provided).
5. Add your OpenAI API key to `OpenAI_key.txt` (or set as env var).

### Database Migration
Run the following commands to set up the database:
```sh
python manage.py migrate
```

### Create Superuser (for admin access)
```sh
python manage.py createsuperuser
```

### Running the Development Server
```sh
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage
- Log in or register for an account.
- Create and manage tasks via the dashboard.
- Visualize your progress as a palace.
- Use AI features for palace and task generation (requires OpenAI API key).

## manage.py
- `manage.py` is the entry point for all Django administrative tasks:
  - `runserver`: Start the development server
  - `migrate`: Apply database migrations
  - `createsuperuser`: Create an admin user
  - `shell`: Open a Django shell
  - and more (see `python manage.py help`)

## Contributing
Pull requests and issues are welcome! To contribute:
1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Open a pull request

## License
MIT License

## Acknowledgements
- [Django](https://www.djangoproject.com/)
- [OpenAI](https://openai.com/)
- [Pillow](https://python-pillow.org/)
- [Celery](https://docs.celeryq.dev/)
- [Gunicorn](https://gunicorn.org/)
- [Whitenoise](http://whitenoise.evans.io/en/stable/)

---

For more, see the code and issues in this repository. 