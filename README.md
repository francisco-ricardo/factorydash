TODO:

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


+-------------------+       +-------------------+       +-------------------+
|                   |       |                   |       |                   |
|      Django       |       |      Celery       |       |    PostgreSQL     |
|                   |       |                   |       |                   |
|  - Web Framework  |       |  - Task Queue     |       |  - Database       |
|  - Models         |       |  - Task Scheduler |       |                   |
|  - Views          |       |                   |       |                   |
|  - Management     |       |                   |       |                   |
|    Commands       |       |                   |       |                   |
+---------+---------+       +---------+---------+       +---------+---------+