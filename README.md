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

