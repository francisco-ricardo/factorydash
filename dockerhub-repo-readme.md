# FactoryDash Docker Image

**Real-Time Insights for Smart Manufacturing**

FactoryDash is a Django-based web application that provides real-time monitoring and visualization of machine performance data from the NIST Smart Manufacturing Systems (SMS) Test Bed. This Docker image is designed for easy deployment of the FactoryDash application.

---

## Features

- **Real-Time Data Updates**: Uses Django Channels for WebSocket communication, providing live dashboard updates.
- **Data Visualization**: Responsive Bootstrap table with client-side pagination controls.
- **Asynchronous Task Processing**: Celery handles background tasks like data ingestion and database cleanup.
- **Data Persistence**: PostgreSQL database for reliable storage.
- **Scalable Design**: Asynchronous updates with Django Channels, task scheduling with Celery Beat, and Redis-backed channel layers.
- **Production-Ready**: Includes Whitenoise for static file serving and robust environment variable management.

---

## Tech Stack

- **Backend**: Django 5.1, Django Channels 4.0, Celery 5.3, PostgreSQL.
- **Frontend**: Django Templates, Bootstrap 5.3.
- **Infrastructure**: Redis (channel layer & broker), Daphne (ASGI server).
- **DevOps**: Docker, Whitenoise (static files), Supervisord (process management).

---

## Usage

### Pull the Image

```bash
docker pull franciscoricardodev/factorydash:latest
```

### Run the Container

```bash
docker run -p 8080:8080 --env-file .env.factorydash.dev franciscoricardodev/factorydash:latest
```

> **Note**: Ensure that Redis and PostgreSQL are running locally or provide their configurations in the `.env.factorydash.dev` file.

---

## Environment Variables

The following environment variables should be configured in your `.env.factorydash.dev` file:

- `DJANGO_SETTINGS_MODULE`: Django settings module (e.g., `factorydash.settings`).
- `SECRET_KEY`: A secure key for Django.
- `DATABASE_URL`: PostgreSQL connection string.
- `CELERY_BROKER_URL`: Redis URL for Celery.
- `CELERY_RESULT_BACKEND`: Redis URL for Celery results.
- `ALLOWED_HOSTS`: Allowed hosts for the Django app.
- `LOAD_NIST_DATA_SCHEDULE_SECONDS`: Interval for data ingestion tasks.
- `UPDATE_DASHBOARD_SCHEDULE_SECONDS`: Interval for dashboard updates.
- `DATA_RETENTION_DAYS`: Retention period for old data.

---

## Deployment

This image is designed for production use and can be deployed on platforms like Railway or any Docker-compatible environment. It includes:

- **Process Management**: `supervisord.conf` orchestrates Daphne, Celery worker, and Beat.
- **Static File Serving**: Whitenoise serves compressed static files for optimal performance.

---

## Live Demo

Visit the live deployment of FactoryDash at:  
[https://factorydash-production.up.railway.app/](https://factorydash-production.up.railway.app/)

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on the [GitHub repository](https://github.com/francisco-ricardo/factorydash).

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/francisco-ricardo/factorydash/blob/main/LICENSE) file for details.
