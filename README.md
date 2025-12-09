# Django Dockerized Application

A basic Django application containerized with Docker.

## Project Structure
```
anjuman/
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── .dockerignore          # Files to exclude from Docker build
├── manage.py              # Django management script
├── db.sqlite3             # SQLite database
├── myproject/             # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── myapp/                 # Django application
    ├── views.py
    ├── urls.py
    └── ...
```

## Prerequisites
- Docker Desktop installed and running
- Python 3.11 (for local development)

## Running with Docker

### Option 1: Using Docker directly

**Build the image:**
```bash
docker build -t django-app .
```

**Run the container:**
```bash
docker run -d -p 8000:8000 --name django-container django-app
```

**Stop the container:**
```bash
docker stop django-container
```

**Remove the container:**
```bash
docker rm django-container
```

### Option 2: Using Docker Compose

**Start the application:**
```bash
docker-compose up
```

**Start in detached mode:**
```bash
docker-compose up -d
```

**Stop the application:**
```bash
docker-compose down
```

**Rebuild and restart:**
```bash
docker-compose up --build
```

## Accessing the Application

Once the container is running, access the application at:
- **Home page:** http://localhost:8000/
- **Admin interface:** http://localhost:8000/admin/

## Docker Commands Reference

**View running containers:**
```bash
docker ps
```

**View all containers (including stopped):**
```bash
docker ps -a
```

**View container logs:**
```bash
docker logs django-container
```

**Access container shell:**
```bash
docker exec -it django-container sh
```

**Remove all stopped containers:**
```bash
docker container prune
```

## Local Development (without Docker)

**Install dependencies:**
```bash
python3 -m pip install -r requirements.txt
```

**Run migrations:**
```bash
python3 manage.py migrate
```

**Start development server:**
```bash
python3 manage.py runserver
```

## Environment Configuration

The application is configured for development with:
- `DEBUG = True`
- `ALLOWED_HOSTS = ['*']`

**⚠️ Warning:** Change these settings before deploying to production!

## Next Steps

1. **Create a superuser for admin access:**
   ```bash
   docker exec -it django-container python manage.py createsuperuser
   ```

2. **Add more views and templates**
3. **Configure a production-ready database (PostgreSQL, MySQL)**
4. **Add static files handling**
5. **Implement proper production settings**

## Troubleshooting

**Port already in use:**
```bash
# Stop any processes using port 8000
docker stop $(docker ps -q --filter "expose=8000")
```

**Container won't start:**
```bash
# Check logs for errors
docker logs django-container
```

**Rebuild image after code changes:**
```bash
docker-compose down
docker-compose up --build
```
