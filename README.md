
# FactoryDash

**Real-Time Insights for Smart Manufacturing.**

FactoryDash is a Django-based web application providing real-time 
monitoring and visualization of machine performance data from the 
NIST Smart Manufacturing Systems (SMS) Test Bed
(https://www.nist.gov/laboratories/tools-instruments/smart-manufacturing-systems-sms-test-bed). 
The SMS Test Bed uses the MTConnect standard for data collection and 
offers various data dissemination channels: a volatile data stream via 
MTConnect agents, a queryable data repository 
(NIST Material Data Curation System - MDCS), and pre-compiled data packages. 
`factorydash` primarily utilizes the real-time, volatile data stream for 
up-to-the-second insights.  The SMS Test Bed aims to advance smart manufacturing 
research and development across the product lifecycle, highlighting challenges 
and requirements for cyber-physical infrastructure while providing a valuable 
data source for researchers.

FactoryDash harnesses this data for actionable 
insights via a server-side rendered (SSR) dashboard, powered by 
Django Channels for live updates and Celery for data processing. 
Developed for my professional portfolio, this project showcases 
mastery of Django’s ecosystem, real-time web technologies, 
CI/CD pipelines, and scalable architecture, deployed on Railway 
with a Docker image available at 
`docker pull franciscoricardodev/factorydash:latest`.

## Features

- Real-time Data Updates: Uses Django Channels for WebSocket 
communication, providing live dashboard updates.

- Paginated Data Delivery: WebSocket consumer implements 
pagination (20 entries/page) using Django’s Window functions 
for efficient metric retrieval.

- Old Data Removal: Celery task cleanup_task deletes MachineData 
records older than the retention period, configurable via 
DATA_RETENTION_DAYS.

- Data Visualization: Responsive Bootstrap table with client-side 
pagination controls.

- Responsive UI: Uses Bootstrap for a clean and responsive user interface.

- Data Ingestion: Consumes data from the NIST API, parsing XML responses 
efficiently.

- Asynchronous Task Processing: Uses Celery for background tasks 
(data ingestion, database cleanup).

- Data Persistence: Stores data in a PostgreSQL database.

- Scalable Design: Asynchronous updates with Django Channels, task 
scheduling with Celery Beat, and Redis-backed channel layers.

- Production-Ready: Hosted on Railway with Whitenoise for static 
file serving and robust environment variable management.

## Tech Stack

- Backend: Django 5.1, Django Channels 4.0, Celery 5.3, PostgreSQL.

- Frontend: Django Templates, Bootstrap 5.3.

- Infrastructure: Railway (PaaS), Redis (channel layer & broker), 
  Daphne (ASGI server).

- DevOps: GitHub Actions (CI/CD), Docker, Whitenoise (static files), 
  Makefile (local setup).

- Testing: Pytest, Pytest-Django.

- Tools: Python 3.13, Docker, Git, Supervisord (process management).

## Architecture

FactoryDash is designed for modularity, performance, and reliability:

1. Data Ingestion:

- Celery task load_nist_data_task fetches NIST SMS Test Bed data every 
9 seconds (configurable via LOAD_NIST_DATA_SCHEDULE_SECONDS), storing it 
in MachineData.

- PostgreSQL with indexes on timestamp and machine_id ensures query efficiency.

2. Real-Time Updates:

- `update_dashboard` task, scheduled via django-celery-beat, triggers WebSocket 
  broadcasts every 10 seconds (configurable via UPDATE_DASHBOARD_SCHEDULE_SECONDS).

- `DashboardConsumer` delivers paginated (20 entries/page) machine data, 
prioritizing recent unique metrics per machine.

3. Frontend:

- SSR with Django Templates ensures fast initial loads and SEO compatibility.

- WebSocket client updates a Bootstrap table dynamically with pagination controls.

4. Deployment:

- Railway hosts the app with `supervisord.conf` managing Daphne, Celery worker, 
and Beat.

- Whitenoise serves compressed static files, enhancing production performance.

5. CI/CD:

- GitHub Actions automates `pytest` testing, Docker image builds 
(`franciscoricardodev/factorydash`), and Railway deployment on `main` branch changes.

## Installation

### Prerequisites

- Docker (with Docker Compose)

- Git

- Make (for Makefile usage)

### Local Setup

FactoryDash leverages Docker Compose and a `Makefile` for a streamlined local development 
environment, defined in `docker-compose-dev.yaml` and managed via `.devcontainer` scripts 
and configs.

1. Clone the Repository:

```bash

git clone https://github.com/yourusername/factorydash.git
cd factorydash

```

2. Configure Environment:

- Create .env.factorydash.dev and .env.postgres.dev, then customize:

```bash

# .env.factorydash.dev
DJANGO_SETTINGS_MODULE=factorydash.settings
PYTHONPATH=/factorydash/app/factorydash
RAILWAY_ENVIRONMENT_NAME=development
SECRET_KEY="your-secret-key"  # Generate a secure key
ALLOWED_HOSTS="*"
LOAD_NIST_DATA_SCHEDULE_SECONDS=9
UPDATE_DASHBOARD_SCHEDULE_SECONDS=10
CLEANUP_OLD_DATA_SCHEDULE_HOURS=1
DATA_RETENTION_DAYS=2
DATABASE_URL=postgres://factorydash:factorydash@postgres.dev:5432/factorydash
CELERY_BROKER_URL=redis://redis.dev:6379/0
CELERY_RESULT_BACKEND=redis://redis.dev:6379/0
PORT=8080

# .env.postgres.dev
POSTGRES_USER=factorydash
POSTGRES_PASSWORD=factorydash
POSTGRES_DB=factorydash

```

3. Build and Start Services:

- Build and run containers:

```bash
make up
```

- Uses `docker-compose-dev.yaml` to start `factorydash.dev` (app), `postgres.dev`, 
and `redis.dev` with health checks.

- Launch application processes:

```bash
make run
```

- Executes `supervisord` with `.devcontainer/supervisord.dev.conf` to manage Daphne, 
Celery worker, and Beat.

- The entrypoint script (`docker-entrypoint-dev.sh`) runs migrations and sets up 
periodic tasks automatically.

4. Access:

- Dashboard: `http://127.0.0.1:8080/`

- Admin: `http://127.0.0.1:8080/admin/` (create superuser with 
`docker exec -it factorydash.dev python manage.py createsuperuser`)

5. Manage Services:

- Stop application processes: make stop

- Shut down containers: make down

- View commands: make help

6. Docker Hub Alternative:

- Pull and run the pre-built image:

```bash

docker pull franciscoricardodev/factorydash:latest
docker run -p 8080:8080 --env-file .env.factorydash.dev franciscoricardodev/factorydash:latest

```

- Note: Requires local Redis and PostgreSQL unless overridden in .env.factorydash.dev.

## Deployment

Hosted on Railway with CI/CD automation and a public Docker image.

- Docker Image:
  - Pull the latest image: `docker pull franciscoricardodev/factorydash:latest`

- Configuration:

  - `RAILWAY_PUBLIC_DOMAIN`: `factorydash-production.up.railway.app`

  - Env vars (`DATABASE_URL`, `CELERY_BROKER_URL`, `SECRET_KEY`, etc.) managed via 
    Railway dashboard for security and flexibility.

- Process Management:

  - `supervisord.conf` orchestrates Daphne, Celery worker, and Beat.

- CI/CD:

  - GitHub Actions pipeline runs `pytest` tests, builds and pushes Docker images to 
    Docker Hub, and deploys to Railway on `main` branch pushes/PRs.

- Railway Postgres Maintenance:

  - Periodic optimization of the PostgreSQL database on Railway can be done with the 
    following commands:

```bash
railway link
railway connect Postgres
DELETE FROM machinedata WHERE timestamp < NOW() - INTERVAL '2 days'; # Customize as desired
VACUUM;
VACUUM FULL;
ANALYZE machinedata;
REINDEX TABLE machinedata;
```

  - Complements the cleanup_task for efficient storage management.

- Live URL: `https://factorydash-production.up.railway.app/`

## Project Structure

.
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
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
│       ├── manage.py
│       ├── monitoring
│       │   ├── __init__.py
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── consumers.py
│       │   ├── management
│       │   │   ├── __init__.py
│       │   │   └── commands
│       │   │       ├── __init__.py
│       │   │       ├── cleanup.py
│       │   │       ├── load_nist_data.py
│       │   │       └── setup_periodic_tasks.py
│       │   ├── migrations
│       │   │   ├── __init__.py
│       │   ├── models.py
│       │   ├── routing.py
│       │   ├── tasks.py
│       │   ├── templates
│       │   │   └── monitoring
│       │   │       └── dashboard.html
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
├── docker-compose-dev.yaml
├── docker-entrypoint.sh
├── requirements.txt
├── supervisord.conf

## Development Practices

- Type Hints: PEP 484-compliant for maintainability and IDE support.

- Docstrings: PEP 257-compliant documentation across all modules.

- Environment Variables: Comprehensive configuration with validation 
  (e.g., `SECRET_KEY`, `DATABASE_URL`) for security and portability.

- Testing: `pytest` and `pytest-django` ensure reliability, integrated 
  into CI/CD.

- Performance: Pagination in `DashboardConsumer`, database indexing, 
  and Whitenoise compression optimize scalability.

-  DevOps: `Makefile` and Docker Compose streamline local setup; 
  GitHub Actions automates CI/CD.

## Challenges Overcome

- WebSocket Pagination: Leveraged Window and RowNumber in DashboardConsumer 
  for efficient, unique metric delivery.

- Async/Sync Integration: Resolved Channels’ async context with `sync_to_async` 
  for ORM calls.

- CI/CD Setup: Configured GitHub Actions for testing, Docker builds, and Railway 
  deployment with retry logic.

## Future Enhancements

- Expanded Tests: Add WebSocket and edge-case coverage in `pytest`.

- Metric Filters: Enable user-defined queries for SMS Test Bed data.

- Alerts: Integrate real-time notifications for critical events.

- UI Upgrades: Add `Chart.js` for trend visualizations.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request. 
Follow standard contribution guidelines (e.g., forking, branching, testing).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## About

Developed by Francisco Ricardo as a portfolio project to demonstrate proficiency in 
Django’s ecosystem, real-time web applications, and smart manufacturing analytics. 
Using the NIST SMS Test Bed, FactoryDash reflects my ability to deliver 
production-ready solutions with modern DevOps practices-skills.

- Contact: franciscoricardo.dev@gmail.com

- LinkedIn: www.linkedin.com/in/francisco-aguiar-3ab650a0

- GitHub: https://github.com/francisco-ricardo

## References

- Helu M, Hedberg Jr T (2020) Connecting, Deploying, and Using the 
Smart Manufacturing Systems Test Bed. 
National Institute of Standards and Technology. doi: 10.6028/NIST.AMS.200-2

