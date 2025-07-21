# PalaceBuilder Project Skeleton

This document describes the initial file and directory structure for the PalaceBuilder Django web application.

## Directory Layout

```
palace_builder/
├── manage.py
├── palace_builder/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   └── palaces/
│       ├── __init__.py
│       ├── views.py
│       └── admin.py
├── services/
│   ├── __init__.py
│   ├── openai_service.py
│   └── palace_generator.py
├── templates/
│   ├── base.html
│   └── tasks/
│       └── dashboard.html
├── static/
│   └── js/
│       └── palace_builder.js
├── requirements.txt
└── README.md
```

## Notes
- `apps/tasks/`: Handles task management, dashboard, and user preferences.
- `apps/palaces/`: Handles palace generation and visualization.
- `services/`: Contains AI integration logic (OpenAI GPT-4, DALL-E 3).
- `templates/`: HTML templates for rendering the UI.
- `static/`: Static files (JS, CSS, images).
- `requirements.txt`: Python dependencies.
- `README.md`: Project documentation. 