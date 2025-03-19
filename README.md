
TODO:


- [] Confirmar com o grok o path do log dir

- [] Rotacionar os logs do suporvisor no railway.app

- [] Definir as variáveis de ambiente no Railway
  - Set in Dashboard under factorydash Service
DJANGO_SETTINGS_MODULE=factorydash.settings
PYTHONPATH=/factorydash/app/factorydash
RAILWAY_ENVIRONMENT_NAME=production
SECRET_KEY=your-secure-key-here  # Generate with python -c "import secrets; print(secrets.token_urlsafe(50))"
ALLOWED_HOSTS=your-railway-domain
LOAD_NIST_DATA_SCHEDULE_SECONDS=60
DATA_RETENTION_DAYS=2
DATABASE_URL=${{Postgres.DATABASE_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}  

- [] Definir as variáveis de ambiente no Github Secrets
  - Repository > Settings > Secrets and Variables > Actions
DOCKER_USERNAME=xxxxx
DOCKER_PASSWORD=xxxxxx
RAILWAY_TOKEN=xxxxxx  

- [] Testar deployment

  - Add supervisord.conf to your project root.
  - Update requirements.txt with all listed dependencies.
  - Commit all files to your GitHub repo.
  - Set Up GitHub Secrets:
    - Go to repo > Settings > Secrets and Variables > Actions.
    - Add DOCKER_USERNAME, DOCKER_PASSWORD, RAILWAY_TOKEN (from Railway dashboard > Account > Tokens).
  - Set Up Railway:
    - Create a new project and service named factorydash.
    - Link to your GitHub repo.
    - Add PostgreSQL and Redis services.
    - Set the Railway variables above.
  - Deploy:
    - Push to main. Workflow will:
      - Run manage.py check to validate settings.
      - Run pytest to test logic.
      - Build and push Docker image.
      - Deploy to Railway, where migrate runs before starting services.
  - Local Testing:
    - Run docker compose up --build with .env.local to test locally.

- Notes
  - Testing: check and pytest use SQLite in CI for speed; migrations use the real database on Railway.
  - Celery: All processes (web, worker, Beat) run via supervisord in one container on Railway.
  - Security: Replace SECRET_KEY placeholders with a secure value in Railway.
  - These files should now fully cover your requirements. Let me know if you need clarification or run into issues!











Streams: A set of Samples, Events, or Conditon for components and devices.

Antes de avaçar para o step 4, tratar os seguintes assuntos

1. Considerar Samples

<ComponentStream component="Linear" componentId="x" name="X"> 1672 
 <Samples> 1673 
  <Position timestamp="2010-03-01T12:09:31.021" dataItemId="Xpos" se-1674 
quence="122" >13.0003</Position> 1675 
  <Temperature timestamp="2010-03-01T12:07:22.031" dataItemId="Xpos" se-1676 
quence="113" >102</Temperature> 1677 
 </Samples> 1678 
</ComponentStream>

2. Considerar Condition

3. Eliminar espaços do início e do fim das strings

4. Configurar log

# DESCRIPTION
Real-time insights for Smart Manufacturing


 Manufacturing, Interoperability in manufacturing, Manufacturing systems design and analysis and Systems integration

## Project Architecture

- Backend (Django + PostgreSQL on Railway.app)
  -	Django: Handles the web app & API processing.
  -	PostgreSQL: Stores machine data.
  -	Celery + Redis: Manages data ingestion in the background.
- Data Ingestion (NIST API Consumer)
  -	Celery workers will fetch real-time XML data from NIST.
  -	Parsed data is stored in the PostgreSQL database.
  -	A cleanup script will auto-delete records older than 1 month.
- Web Dashboard (Django + Chart.js)
  -	Django Templates + Bootstrap for UI (keeping it simple).
  -	Chart.js to display machine metrics dynamically.
  -	Live updates with AJAX polling or WebSockets.



- Local Development Setup
  - You will run the project locally during development.
  -	We will containerize the entire app with Docker.
- Use Docker for Development & Deployment
  -	A Dockerized PostgreSQL database for local development.
  -	A Docker Compose setup to manage services like Django, Celery, Redis.
  -	A multi-stage Dockerfile to make the production build efficient and optimized.
- CI/CD Pipeline for Automated Deployment
  -	Use GitHub Actions to run unit tests & linting on every commit.
  -	On push to main, automatically deploy to Railway.app.
- Test-Driven Development (TDD)
  -	Unit tests for:
- Data ingestion (NIST API parsing).
- Database models (ensuring correct data storage).
- Dashboard views (checking correct rendering).
- Use pytest + Django test framework.



## Tech Stack Summary

- Backend Framework	Django (Python)
- Database	PostgreSQL (Railway.app & Docker)
- Task Queue	Celery + Redis (for async tasks)
- API Integration	Requests (NIST API) + XML parsing
- Web Dashboard	Django Templates + Chart.js
- Deployment	Docker + Railway.app
- CI/CD	GitHub Actions + Docker
- Testing	Pytest + Django Test Framework



Real-time stream of most current value for each data item: https://smstestbed.nist.gov/vds/current

NIST_API_URL = "https://smstestbed.nist.gov/vds/current"


Information
https://www.nist.gov/laboratories/tools-instruments/smart-manufacturing-systems-sms-test-bed


docker build -t factorydash:latest -f .devcontainer/Dockerfile .



# **Step 3: Automating Data Ingestion with Celery + Redis**

Now that logs are configured and persistent, we will integrate Celery and Redis to:
- ✅ Run the NIST data loader automatically every 10 seconds
- ✅ Decouple data ingestion from the main Django process
- ✅ Improve scalability and performance

---

## **🛠 1️⃣ Install Celery and Redis Dependencies**
Inside the **DevContainer terminal**, install the required packages:
```bash
pip install celery redis
```
✅ **Update `requirements.txt`** to ensure dependencies are installed automatically:
```txt
celery
redis
```

---

## **🛠 2️⃣ Configure Celery in Django**
### **🔹 Create `celery.py` Inside `factorydash/`**
```bash
touch factorydash/celery.py
```
Then, **add the following to `factorydash/celery.py`**:
```python
import os
from celery import Celery

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "factorydash.settings")

# Initialize Celery
app = Celery("factorydash")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from Django apps
app.autodiscover_tasks()
```

### **🔹 Modify `factorydash/__init__.py` to Load Celery**
Open `factorydash/__init__.py` and **add this at the end**:
```python
from .celery import app as celery_app

__all__ = ("celery_app",)
```
✅ **This ensures Celery starts when Django runs.**

---

## **🛠 3️⃣ Configure Redis as the Celery Broker**
Modify `factorydash/settings.py` to **add Celery settings**:
```python
# Celery settings
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
```
✅ **This tells Celery to use Redis (`redis://redis:6379/0`) as the message broker.**

---

## **🛠 4️⃣ Create a Celery Task for Data Ingestion**
Inside `monitoring/`, create a **new file** for Celery tasks:
```bash
touch monitoring/tasks.py
```
Then, open `monitoring/tasks.py` and **add the task definition**:
```python
from celery import shared_task
from monitoring.data_loader import save_nist_data
import logging

logger = logging.getLogger("factorydash")

@shared_task
def fetch_nist_data_task():
    """Celery task to fetch and save data from the NIST API."""
    try:
        save_nist_data()
        logger.info("✅ Celery Task: Successfully fetched NIST API data")
        return "NIST API data fetched and stored."
    except Exception as e:
        logger.error(f"❌ Celery Task Error: {str(e)}")
        return "NIST API task failed."
```
✅ **Now, Celery will execute `save_nist_data()` in the background.**

---

## **🛠 5️⃣ Add Redis to `docker-compose-dev.yaml`**
Modify `docker-compose-dev.yaml` to **add Redis**:
```yaml
version: '3.8'

services:
  factorydash.dev:
    container_name: factorydash.dev
    image: factorydash.dev:latest
    build:
      context: .
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - .:/workspace
      - logs_volume:/workspace/logs  # ✅ Persist logs
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://factorydash:factorydash@db:5432/factorydash
      - CELERY_BROKER_URL=redis://redis:6379/0

  db:
    container_name: factorydash.db
    image: postgres:latest
    restart: always
    environment:
      POSTGRES_USER: factorydash
      POSTGRES_PASSWORD: factorydash
      POSTGRES_DB: factorydash
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    container_name: factorydash.redis
    image: redis:latest
    restart: always
    ports:
      - "6379:6379"

volumes:
  postgres_data:
  logs_volume:
```
✅ **This adds a Redis service for Celery.**

---

## **🛠 6️⃣ Start Everything**
Rebuild and start the containers:
```bash
make rundev
```
Then, **open a new terminal** and run Celery:
```bash
celery -A factorydash worker --loglevel=info
```
✅ **Celery should now be running and ready to execute tasks.**

---

## **🛠 7️⃣ Schedule the Task to Run Every 10 Seconds**
Inside `monitoring/tasks.py`, **modify the task to run periodically**:
```python
from celery.schedules import crontab
from celery import Celery

app = Celery("factorydash")

app.conf.beat_schedule = {
    "fetch-nist-data-every-10-seconds": {
        "task": "monitoring.tasks.fetch_nist_data_task",
        "schedule": 10.0,  # Every 10 seconds
    },
}
```
Then, **start the Celery Beat scheduler**:
```bash
celery -A factorydash beat --loglevel=info
```
✅ **Now, the NIST data ingestion runs automatically every 10 seconds!**

---

## **🚀 Next Steps**
1️⃣ **Confirm Celery is running and fetching data every 10 seconds.**
2️⃣ **Check logs for any errors or missing data.**
3️⃣ **If everything works, we move to Step 4: Web Dashboard with Django Templates + Chart.js!** 🚀




 select * from machinedata order by timestamp desc limit 10;
 select * from machinedata order by timestamp asc limit 10;


  python manage.py test factorydash
  python manage.py cleanup
  
  act -j build
  act -j build --env-file .env


  TODO: IMPLEMENTAR data_loader como Command:
  python manage.py loaddata



Here's an ASCII diagram that describes the integration between Django, Celery, Redis, and PostgreSQL in your project:

```
+-------------------+       +-------------------+       +-------------------+
|                   |       |                   |       |                   |
|    PostgreSQL     |       |       Redis       |       |      Celery       |
|                   |       |                   |       |                   |
|  - Stores data    |       |  - Message broker |       |  - Task queue     |
|  - Database       |       |  - Caching        |       |  - Background     |
|                   |       |                   |       |    task execution |
+---------+---------+       +---------+---------+       +---------+---------+
          |                           |                           |
          |                           |                           |
          |                           |                           |
          |                           |                           |
          |                           |                           |
+---------v---------+       +---------v---------+       +---------v---------+
|                   |       |                   |       |                   |
|      Django       |       |     Celery        |       |    Celery Worker  |
|                   |       |     Beat          |       |                   |
|  - Web framework  |       |  - Periodic tasks |       |  - Executes tasks |
|  - ORM            |       |                   |       |                   |
|                   |       |                   |       |                   |
+-------------------+       +-------------------+       +-------------------+
```

Explanation:
- **PostgreSQL**: The database where Django stores its data.
- **Redis**: Acts as a message broker for Celery and also provides caching.
- **Django**: The web framework that interacts with PostgreSQL for data storage and uses Celery for background task execution.
- **Celery**: Manages the task queue and schedules periodic tasks using Celery Beat.
- **Celery Worker**: Executes the tasks that are queued by Celery.



Docker hub

Access token description:
dockerhub access token for factorydash

Personal Acces Token:
dckr_pat_299uUmwXM1jM_dKPvdq88OLRyM4

docker login -u franciscoricardodev
put the personal acces token

Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(50))"


## TODO

1. Prepare for Railway.app Deployment:

Remove Local Specifics.

- In docker-compose.yaml:
  - [] remove port mappings (e.g., 5432:5432). Railway handles this.
  - [] Remove the volumes section. Railway provides its own persistent storage.
  - [] Remove the container_name lines, railway will create them.

Production WSGI Server.

- [x] In your Dockerfile, replace the CMD instruction with Gunicorn or Uvicorn. Gunicorn is a popular choice for Django.
Example: CMD ["gunicorn", "factorydash.wsgi:application", "--bind", "0.0.0.0:8000"]
Install gunicorn in the requirements.txt file.

Production Settings.

- [x] In settings.py, set DEBUG = False for production.
- [x] Configure ALLOWED_HOSTS to allow requests from Railway.app. 
You can use ALLOWED_HOSTS = ['*'] for now (but consider more specific hosts in production).
- [x] Make sure that the secret key is retrieved from the environment variables.
- [x] Make sure that the database url is retrieved from the environment variables.
- [x] Make sure that the celery broker url is retrieved from the environment variables.
- [x] Review the env vars defined into the Dockerfile. Maybe it is better to move to .env and Railway.app.

2. Configure Railway.app:

Create a Railway.app Project:
- [] Sign up for Railway.app.
- [] Create a new project.
- [] Link GitHub Repository: Connect your GitHub repository to your Railway.app project.
- [] Add Services:
PostgreSQL:
Add a PostgreSQL service from the Railway.app marketplace.
Redis:
Add a Redis service from the Railway.app marketplace.
Django App:
Railway will automatically detect your Dockerfile.

Environment Variables:
- [] In Railway.app's settings, add the following environment variables:
SECRET_KEY: Generate a strong secret key.
DATABASE_URL: Railway.app will automatically provide this from the PostgreSQL service.
CELERY_BROKER_URL: Railway.app will automatically provide this from the Redis service.
DJANGO_SETTINGS_MODULE: Set this to factorydash.settings.
ALLOWED_HOSTS: Set this to * for testing, or your specific hostnames.
RAILWAY_ENVIRONMENT_NAME: set this to production.

Configure the start command:
- [] In the railway settings, configure the start command to be gunicorn factorydash.wsgi:application --bind 0.0.0.0:8000

3. CI/CD Pipeline (ci.yml):

Build and Push Docker Image:
- [] Modify your ci.yml to build and push your Docker image to a container registry (Docker Hub or Railway's registry).
Here is an example of the docker build and push.
```yaml

- name: Build and push Docker image
  uses: docker/build-push-action@v4
  with:
    context: .
    push: true
    tags: ${{ secrets.DOCKER_USERNAME }}/factorydash:${{ github.sha }}
```

- [] Modify the docker compose file to use the new image tag.
Example: `image: ${{ secrets.DOCKER_USERNAME }}/factorydash:${{ github.sha }}`

Remove Docker Compose:

- [] Remove the steps that use docker compose, they are not needed in railway.

Run Migrations:
- [] Add a step to run migrations after the image is pushed.
This step can be done in the railway settings, as a start command.
Example: `python manage.py migrate`

Run Celery:
- [] Add two new services in railway, one for the celery worker, and one for the celery beat.
Configure the start commands to be:
Celery worker: celery -A factorydash worker --loglevel=info
Celery beat: celery -A factorydash beat --loglevel=info

Health Checks:
- [] Add a health check to the Dockerfile.
Example: HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://0.0.0.0:8000/ || exit 1

4. Code Changes:

-[] settings.py:
Update settings.py to use environment variables for sensitive settings.
Example of the docker-compose.yaml file:

```yaml
services:
  factorydash:
    image: ${{ secrets.DOCKER_USERNAME }}/factorydash:${{ github.sha }}
    environment:
      - DJANGO_SETTINGS_MODULE=factorydash.settings
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
  postgres:
    image: postgres:latest
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "factorydash"]
      interval: 10s
      timeout: 5s
      retries: 5
  redis:
    image: redis:latest
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```


Railway Postgres
DATABASE_URL: postgresql://postgres:UMCovcRQdvJmtDbzSKtboJZCwWRMljuP@postgres.railway.internal:5432/railway

Railway Redis
REDIS_URL: redis://default:OTsZJsoQHTwJJZDtkmhswebDIcFgZLOh@redis.railway.internal:6379


New instructions:

Updated Files
1. .github/workflows/deploy.yml
This workflow includes testing (pytest), validation (manage.py check), and deployment to Railway, with migrations handled during deployment.

yaml

Collapse

Wrap

Copy
name: Deploy to Railway

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13.2'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-django

      - name: Run Django Check
        env:
          DJANGO_SETTINGS_MODULE: factorydash.settings_test
          DATABASE_URL: sqlite:///test.db
        run: |
          python app/factorydash/manage.py check --settings=factorydash.settings_test

      - name: Run Pytest
        env:
          DJANGO_SETTINGS_MODULE: factorydash.settings_test
          DATABASE_URL: sqlite:///test.db
          CELERY_BROKER_URL: redis://localhost:6379/0
          CELERY_RESULT_BACKEND: redis://localhost:6379/0
          LOAD_NIST_DATA_SCHEDULE_SECONDS: 60
          DATA_RETENTION_DAYS: 2
        run: |
          pytest --verbose

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and Tag Docker Image
        run: |
          docker build -t franciscoricardodev/factorydash:latest .
          docker tag franciscoricardodev/factorydash:latest franciscoricardodev/factorydash:${{ github.sha }}

      - name: Push Docker Image to Docker Hub
        run: |
          docker push franciscoricardodev/factorydash:latest
          docker push franciscoricardodev/factorydash:${{ github.sha }}

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway up --service factorydash --environment production
2. settings.py
python

Collapse

Wrap

Copy
"""
Django settings for factorydash project.
"""

from pathlib import Path
import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment and Security
RAILWAY_ENVIRONMENT_NAME = os.getenv("RAILWAY_ENVIRONMENT_NAME", "development")
IS_PRODUCTION = (RAILWAY_ENVIRONMENT_NAME == "production")
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY and not IS_PRODUCTION:
    SECRET_KEY = 'django-insecure-qwba_g+u=^%nl2%p2ih(uzw%jwch6#8r2@z4)nth#e0o1y%mtk'
elif not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY must be set in production")
DEBUG = not IS_PRODUCTION
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Database configuration
DEFAULT_DB_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'factorydash',
    'USER': 'factorydash',
    'PASSWORD': 'factorydash',
    'HOST': 'postgres',
    'PORT': '5432',
}
DATABASE_URL = os.getenv('DATABASE_URL')
try:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL) if DATABASE_URL else DEFAULT_DB_CONFIG
    }
except ValueError as e:
    raise ImproperlyConfigured(f"Invalid DATABASE_URL: {e}")
DATABASES['default']['CONN_MAX_AGE'] = 600

# Data retention
DATA_RETENTION_DAYS = int(os.getenv("DATA_RETENTION_DAYS", "2"))

# Celery configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', CELERY_BROKER_URL)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'monitoring',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'factorydash.urls'
WSGI_APPLICATION = 'factorydash.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{asctime} [{levelname}] {module} - {message}", "style": "{"},
        "simple": {"format": "[{levelname}] {message}", "style": "{"},
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "factorydash.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {"handlers": ["file", "console"], "level": "INFO", "propagate": True},
        "factorydash": {"handlers": ["file", "console"], "level": "DEBUG", "propagate": False},
    },
}
3. settings_test.py
python

Collapse

Wrap

Copy
# settings_test.py (for pytest)
from .settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
4. celery.py
python

Collapse

Wrap

Copy
import os
from celery import Celery
from celery.schedules import crontab
from urllib.parse import urlparse

# Default broker and backend URLs
DEFAULT_CELERY_BROKER_URL = 'redis://redis:6379/0'
DEFAULT_CELERY_RESULT_BACKEND = DEFAULT_CELERY_BROKER_URL

# Fetch and validate broker URLs
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', DEFAULT_CELERY_BROKER_URL)
if not CELERY_BROKER_URL:
    raise ValueError("CELERY_BROKER_URL must be set to a valid broker URL")
try:
    parsed_url = urlparse(CELERY_BROKER_URL)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError("CELERY_BROKER_URL must be a valid URL (e.g., redis://host:port)")
except ValueError as e:
    raise ValueError(f"Invalid CELERY_BROKER_URL: {e}")
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', DEFAULT_CELERY_RESULT_BACKEND)

# Fetch and validate LOAD_NIST_DATA_SCHEDULE_SECONDS
DEFAULT_LOAD_NIST_DATA_SCHEDULE_SECONDS = 60.0
LOAD_NIST_DATA_SCHEDULE_SECONDS = os.getenv('LOAD_NIST_DATA_SCHEDULE_SECONDS', str(DEFAULT_LOAD_NIST_DATA_SCHEDULE_SECONDS))
try:
    LOAD_NIST_DATA_SCHEDULE_SECONDS = float(LOAD_NIST_DATA_SCHEDULE_SECONDS)
    if LOAD_NIST_DATA_SCHEDULE_SECONDS <= 0:
        raise ValueError("LOAD_NIST_DATA_SCHEDULE_SECONDS must be a positive number")
except ValueError as e:
    raise ValueError(f"Invalid LOAD_NIST_DATA_SCHEDULE_SECONDS: {e}")

# Initialize Celery
app = Celery("factorydash")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND,
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=5,
    task_track_started=True,
    result_expires=3600,
)

# Auto-discover tasks
app.autodiscover_tasks()

# Celery Beat schedule
app.conf.beat_schedule = {
    "load_nist_data_task_every_interval": {
        "task": "monitoring.tasks.load_nist_data_task",
        "schedule": LOAD_NIST_DATA_SCHEDULE_SECONDS,
    },
    "cleanup_old_data_daily_midday": {
        "task": "monitoring.tasks.cleanup_task",
        "schedule": crontab(hour=12, minute=5),
    },
    "cleanup_old_data_daily_midnight": {
        "task": "monitoring.tasks.cleanup_task",
        "schedule": crontab(hour=0, minute=5),
    },
}
5. factorydash/__init__.py
python

Collapse

Wrap

Copy
"""
This module ensures the Django environment and Celery app are properly initialized
for the factorydash project.
"""

from __future__ import absolute_import, unicode_literals
import os
import sys
import logging

# Set up Django environment
if not getattr(sys, '_is_django_setup', False):
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_path not in sys.path:
        sys.path.append(project_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "factorydash.settings")
    import django
    django.setup()
    sys._is_django_setup = True

# Set up logging
logger = logging.getLogger("factorydash")
logger.info('Django environment initialized')

# Set up Celery
from .celery import app as celery_app
__all__ = ('celery_app',)
6. Dockerfile
dockerfile

Collapse

Wrap

Copy
FROM python:3.13.2-slim

WORKDIR /factorydash

# Install dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    locales \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set up locale
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /factorydash/logs && \
    python app/factorydash/manage.py collectstatic --noinput

EXPOSE 8000

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["sh", "-c", "python app/factorydash/manage.py migrate && supervisord -c /etc/supervisor/conf.d/supervisord.conf"]
7. supervisord.conf
ini

Collapse

Wrap

Copy
[supervisord]
nodaemon=true
logfile=/factorydash/logs/supervisord.log
pidfile=/tmp/supervisord.pid

[program:gunicorn]
command=gunicorn --chdir app/factorydash --bind 0.0.0.0:8000 factorydash.wsgi:application
stdout_logfile=/factorydash/logs/gunicorn.log
stderr_logfile=/factorydash/logs/gunicorn_err.log
autorestart=true

[program:celery_worker]
command=celery -A factorydash worker --loglevel=info
directory=/factorydash/app/factorydash
stdout_logfile=/factorydash/logs/celery_worker.log
stderr_logfile=/factorydash/logs/celery_worker_err.log
autorestart=true

[program:celery_beat]
command=celery -A factorydash beat --loglevel=info
directory=/factorydash/app/factorydash
stdout_logfile=/factorydash/logs/celery_beat.log
stderr_logfile=/factorydash/logs/celery_beat_err.log
autorestart=true
8. docker-compose.yaml
yaml

Collapse

Wrap

Copy
services:
  factorydash:
    container_name: factorydash
    image: factorydash:latest
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - .env.local
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  postgres:
    container_name: factorydash.postgres
    image: postgres:latest
    environment:
      POSTGRES_USER: factorydash
      POSTGRES_PASSWORD: factorydash
      POSTGRES_DB: factorydash
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "factorydash"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    container_name: factorydash.redis
    image: redis:latest
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
9. .env.local
plaintext

Collapse

Wrap

Copy
DOCKER_USERNAME=xxxxx
DOCKER_PASSWORD=xxxxxx
DJANGO_SETTINGS_MODULE=factorydash.settings
PYTHONPATH=/factorydash/app/factorydash
RAILWAY_ENVIRONMENT_NAME=development
RAILWAY_TOKEN="xxxxxx"
SECRET_KEY="xxxxxx"
LOAD_NIST_DATA_SCHEDULE_SECONDS=60
DATABASE_URL=postgres://factorydash:factorydash@postgres:5432/factorydash
DATA_RETENTION_DAYS=2
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
10. pytest.ini
ini

Collapse

Wrap

Copy
[pytest]
DJANGO_SETTINGS_MODULE = factorydash.settings_test
python_files = tests.py test_*.py *_tests.py
11. requirements.txt (Example)
plaintext

Collapse

Wrap

Copy
django>=5.1.6
dj-database-url
gunicorn
psycopg2-binary
celery[redis]
django-celery-beat
supervisor
pytest
pytest-django
Environment Variable Placement
Railway (Set in Dashboard under factorydash Service)
plaintext

Collapse

Wrap

Copy
DJANGO_SETTINGS_MODULE=factorydash.settings
PYTHONPATH=/factorydash/app/factorydash
RAILWAY_ENVIRONMENT_NAME=production
SECRET_KEY=your-secure-key-here  # Generate with python -c "import secrets; print(secrets.token_urlsafe(50))"
ALLOWED_HOSTS=your-railway-domain
LOAD_NIST_DATA_SCHEDULE_SECONDS=60
DATA_RETENTION_DAYS=2
DATABASE_URL=${{Postgres.DATABASE_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}
GitHub Secrets (Repository > Settings > Secrets and Variables > Actions)
plaintext

Collapse

Wrap

Copy
DOCKER_USERNAME=xxxxx
DOCKER_PASSWORD=xxxxxx
RAILWAY_TOKEN=xxxxxx
Deployment Steps
Prepare Files:
Add supervisord.conf to your project root.
Update requirements.txt with all listed dependencies.
Commit all files to your GitHub repo.
Set Up GitHub Secrets:
Go to repo > Settings > Secrets and Variables > Actions.
Add DOCKER_USERNAME, DOCKER_PASSWORD, RAILWAY_TOKEN (from Railway dashboard > Account > Tokens).
Set Up Railway:
Create a new project and service named factorydash.
Link to your GitHub repo.
Add PostgreSQL and Redis services.
Set the Railway variables above.
Deploy:
Push to main.
Workflow will:
Run manage.py check to validate settings.
Run pytest to test logic.
Build and push Docker image.
Deploy to Railway, where migrate runs before starting services.
Local Testing:
Run docker compose up --build with .env.local to test locally.
Notes
Testing: check and pytest use SQLite in CI for speed; migrations use the real database on Railway.
Celery: All processes (web, worker, Beat) run via supervisord in one container on Railway.
Security: Replace SECRET_KEY placeholders with a secure value in Railway.
These files should now fully cover your requirements. Let me know if you need clarification or run into issues!



## DESCRIPTION

Real-time insights for Smart Manufacturing


## DESIGN

- Directory tree

```bash
.
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── TODO
├── app
│   └── factorydash
│       ├── factorydash
│       │   ├── __init__.py
│       │   ├── asgi.py
│       │   ├── celery.py
│       │   ├── settings.py
│       │   ├── settings_test.py
│       │   ├── tests.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       ├── logs
│       │   ├── factorydash.log
│       ├── manage.py
│       ├── monitoring
│       │   ├── __init__.py
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── management
│       │   │   ├── __init__.py
│       │   │   └── commands
│       │   │       ├── __init__.py
│       │   │       ├── cleanup.py
│       │   │       └── load_nist_data.py
│       │   ├── migrations
│       │   │   ├── 0001_initial.py
│       │   │   ├── 0002_rename_monitoring__timesta_4e59ba_idx_machinedata_timesta_635c09_idx_and_more.py
│       │   │   ├── __init__.py
│       │   ├── models.py
│       │   ├── tasks.py
│       │   ├── tests
│       │   │   ├── test_integration.py
│       │   │   ├── test_load_nist_data.py
│       │   │   ├── test_logging.py
│       │   │   ├── test_models.py
│       │   │   └── test_tasks.py
│       │   ├── tests.py
│       │   └── views.py
│       ├── pytest.ini
│       └── staticfiles
│           └── admin
│               ├── css
│               ├── img
│               └── js
├── celerybeat-schedule
├── celerybeat-schedule-shm
├── celerybeat-schedule-wal
├── docker-compose-dev.yaml
├── docker-compose.yaml
├── docker-entrypoint.sh
├── requirements.txt
├── supervisord.conf

```

- Dockerfile

```bash
FROM python:3.13.2-slim

WORKDIR /factorydash

# Install dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    locales \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set up locale
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /factorydash/app/factorydash/logs && \
    python app/factorydash/manage.py collectstatic --noinput

COPY docker-entrypoint.sh .
RUN chmod +x /factorydash/docker-entrypoint.sh

EXPOSE 8080

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ENTRYPOINT ["/factorydash/docker-entrypoint.sh"]
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

# EOF

```

- docker-entrypoint.sh

```bash
#!/bin/bash

# This script is the entrypoint for the Docker container.
# It is responsible for running migrations and starting the application.

set -e


# Functions definitions

# Main function
main() {

    # Run migrations if DATABASE_URL is set
    if [ "$DATABASE_URL" ]; then
        echo "DATABASE_URL set to: $DATABASE_URL"
        parse_database_url

        # Assumes that DBMS is Postgres
        # Run pg_isready to check if the database is ready

        # Wait for database with timeout
        echo "Waiting for database to be ready (timeout: 30s)..."
        timeout 30s bash -c "until pg_isready -h \"$DB_HOST\" -p \"$DB_PORT\" -U \"$DB_USER\" -d \"$DB_NAME\" -q; do echo 'Database not ready yet. Retrying in 1 second...'; sleep 1; done"
        if [ $? -ne 0 ]; then
            echo "Error: Database at $DATABASE_URL not ready after 30 seconds. Exiting."
            exit 1
        fi
        echo "Database is ready!"

        echo "Running migrations..."
        python app/factorydash/manage.py migrate --noinput
    else
        echo "DATABASE_URL not set. Skipping database setup."
    fi

    echo "Verifying application structure..."
    ls -la /factorydash/app/factorydash/
    if [ -f /factorydash/app/factorydash/factorydash/wsgi.py ]; then
        echo "WSGI file found at expected location"
    else
        echo "ERROR: WSGI file not found at expected location"
        echo "Checking for wsgi.py in other locations:"
        find /factorydash -name wsgi.py
    fi

    echo "Environment variables:"
    env | sort

    # Add to docker-entrypoint.sh
    echo "Python path:"
    python -c "import sys; print(sys.path)"

    #echo "Checking if wsgi module is importable:"
    #python -c "try: from factorydash.wsgi import application; print('WSGI module importable!'); except Exception as e: print(f'Error importing WSGI module: {e}')"


}


# Function to parse DATABASE_URL
# Assumes DATABASE_URL is set and in the format: postgres://user:password@host:port/dbname
parse_database_url() {

    # Extract components from DATABASE_URL (e.g., postgres://user:password@host:port/dbname)
    # Handle both postgres:// and postgresql://
    DB_USER=$(echo "$DATABASE_URL" | sed -E 's|^postgres(ql)?:\/\/([^:]+):.*$|\2|')
    DB_PASSWORD=$(echo "$DATABASE_URL" | sed -E 's|^postgres(ql)?:\/\/[^:]+:([^@]+)@.*$|\2|')
    DB_HOST=$(echo "$DATABASE_URL" | sed -E 's|^postgres(ql)?:\/\/[^@]+@([^:/]+).*|\2|')
    DB_PORT=$(echo "$DATABASE_URL" | sed -E 's|^postgres(ql)?:\/\/[^@]+@[^:]+:([0-9]+).*|\2|' || echo "5432")
    DB_NAME=$(echo "$DATABASE_URL" | sed -E 's|^postgres(ql)?:\/\/[^@]+@[^/]+/(.+)$|\2|')

    # Log for debugging
    echo "Parsed DATABASE_URL:"
    echo "  User: $DB_USER"
    echo "  Host: $DB_HOST"
    echo "  Port: $DB_PORT"
    echo "  Database: $DB_NAME"
}


# Run main function
main

# Run the command passed to the Docker container
exec "$@"

# EOF

```

- requirements.txt

```bash
django>=5.1.6
dj-database-url
gunicorn>=20.1.0
psycopg2-binary
celery>=5.2.7
redis>=4.5.1
django-celery-beat
supervisor
pytest 
pytest-django 
pytest-mock
requests
lxml
pytz

```

Your are a django software engineer with full-stack knowledge (Server Side Renderging).


## Description

Proce