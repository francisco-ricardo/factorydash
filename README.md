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
   
