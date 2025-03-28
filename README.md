
# FactoryDash

**Real-Time Insights for Smart Manufacturing.**

FactoryDash is a Django-based web application providing real-time 
monitoring and visualization of machine performance data from the 
NIST Smart Manufacturing Systems (SMS) Test Bed. The SMS Test Bed 
combines Computer-Aided Technologies (CAx) tools, a Manufacturing 
Lab with CNC and inspection equipment, and MTConnect-standardized 
data services to advance smart manufacturing research across the 
product lifecycle. FactoryDash harnesses this data for actionable 
insights via a server-side rendered (SSR) dashboard, powered by 
Django Channels for live updates and Celery for data processing. 
Developed for my professional portfolio, this project showcases 
mastery of Django’s ecosystem, real-time web technologies, 
CI/CD pipelines, and scalable architecture, deployed on Railway 
with a Docker image available at 
`docker pull franciscoricardodev/factorydash:latest`.

## Features

- Real-Time Dashboard: Displays live machine metrics 
(e.g., timestamp, machine ID, parameter, value) with 
WebSocket updates every 10 seconds.

- Paginated Data Delivery: WebSocket consumer implements 
pagination (20 entries/page) using Django’s Window functions 
for efficient metric retrieval.

- Data Visualization: Responsive Bootstrap table with client-side 
pagination controls.

- NIST SMS Integration: Fetches MTConnect data from the SMS Test 
Bed via Celery tasks, stored in PostgreSQL.

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

- Live URL: `https://factorydash-production.up.railway.app/`

## Project Structure





## EOF

# factorydash: Real-time Smart Manufacturing Insights

**A Django-based application providing real-time monitoring and 
analysis of manufacturing data.**

This project addresses the need for efficient and insightful monitoring of 
smart manufacturing processes. It leverages data from the NIST Smart 
Manufacturing Systems Test Bed (SMS Test Bed), providing a real-time 
dashboard for visualizing key performance indicators (KPIs) and operational 
status. The SMS Test Bed uses the MTConnect standard for data collection and 
offers various data dissemination channels: a volatile data stream via 
MTConnect agents, a queryable data repository 
(NIST Material Data Curation System - MDCS), and pre-compiled data packages. 
`factorydash` primarily utilizes the real-time, volatile data stream for 
up-to-the-second insights.  The SMS Test Bed aims to advance smart manufacturing 
research and development across the product lifecycle, highlighting challenges 
and requirements for cyber-physical infrastructure while providing a valuable 
data source for researchers.

## Table of Contents

- Project Title and Overview
- Installation Instructions
- Running the Application
- Configuration
- Features
- Testing
- Deployment
- Contributing
- License
- References
- Contact


## Installation Instructions

1. **Clone the repository:**
```bash
git clone <repository_url>
cd factorydash
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. Set up the database: (PostgreSQL is recommended; SQLite is used for testing)
- Create a PostgreSQL database and user. 
Update factorydash/factorydash/settings.py with your database credentials.
- Run database migrations:
```bash
python manage.py migrate
```
- Collect static files:
```bash
python manage.py collectstatic
```

4. Running the Application
This project uses Docker Compose for development and deployment.

- Start the development environment:
```bash 
docker-compose -f docker-compose-dev.yaml up -d
```

This starts PostgreSQL, Redis, Celery Beat, Celery Worker, and Daphne (the ASGI server).

- Access the dashboard: Once the containers are running, open your web browser and navigate to http://localhost:8000/.

- Makefile Targets (if applicable): The Makefile (if provided) offers convenient targets for managing the development environment (e.g., make up, make down, make test).

5. Configuration

- Database: Configure database settings in factorydash/factorydash/settings.py. For production, use a robust database like PostgreSQL.
- Environment Variables: The application uses environment variables extensively (database credentials, API keys, Celery settings). Use a .env file:
```bash
DATABASE_URL=postgres://user:password@host:port/database
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
LOAD_NIST_DATA_SCHEDULE_SECONDS=10  # Adjust data update frequency
DATA_RETENTION_DAYS=2              # Adjust data retention period
```
- .env file loading: Ensure your deployment process loads environment variables from a .env file.

6. Features
- Real-time Data Updates: Uses Django Channels for WebSocket communication, providing live dashboard updates.
- Data Ingestion: Consumes data from the NIST API, parsing XML responses efficiently.
- Asynchronous Task Processing: Uses Celery for background tasks (data ingestion, database cleanup).
- Data Persistence: Stores data in a PostgreSQL database (SQLite for development/testing).
- Responsive UI: Uses Bootstrap for a clean and responsive user interface.
- Data Pagination: Efficiently handles large datasets by paginating the displayed data.

7. Testing
The project uses `pytest` for testing. Run tests with:

```bash 
pytest
```
(or a Makefile target if one is defined)

8. Deployment
This application is designed for deployment using Docker and Docker Compose. Instructions for specific platforms (e.g., Railway.app) should be provided in separate documentation or within the deployment scripts. Ensure proper configuration of environment variables for production.

9. Contributing
Contributions are welcome! Please open an issue or submit a pull request. Follow standard contribution guidelines (e.g., forking, branching, testing).

10. License
This project is licensed under the MIT License - see the LICENSE file for details.

11. References
Helu M, Hedberg Jr T (2020) Connecting, Deploying, and Using the Smart Manufacturing Systems Test Bed. National Institute of Standards and Technology. doi: 10.6028/NIST.AMS.200-2
Helu M, Hedberg Jr T (2020) Recommendations for collecting, curating, and re-using manufacturing data. National Institute of Standards and Technology, Report NIST AMS300-11. doi: 10.6028/NIST.AMS.300-11
Hedberg Jr T, Helu M, Newrock M (2017) Software requirements specification to distribute manufacturing data. National Institute of Standards and Technology, Report NIST AMS300-2. doi: 10.6028/NIST.AMS.300-2
Helu M, Hedberg Jr T, Barnard Feeney A (2017) Reference architecture to integrate heterogeneous manufacturing systems for the digital thread. CIRP Journal of Manufacturing Science and Technology doi: 10.1016/j.cirpj.2017.04.002

12. Contact
Email: franciscoricardo.dev@gmail.com
LinkedIn: Francisco Aguiar
GitHub: francisco-ricardo
   
