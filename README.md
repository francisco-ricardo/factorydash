# DESCRIPTION
Real-time insights for Smart Manufacturing


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



NIST_API_URL = "https://smstestbed.nist.gov/vds/current"


docker build -t factorydash:latest -f .devcontainer/Dockerfile .

