# Tixxety API

Tixxety is a robust and scalable ticketing API built with FastAPI, designed to manage events, ticket reservations, and user authentication. It leverages PostgreSQL for data persistence and Docker for containerization, ensuring a consistent development and deployment experience.

## Features

*   **User Authentication**: Secure user registration and login.
*   **Event Management**: Create and view listings.
*   **Ticket Reservation**: Reserve tickets for events, with checks for availability.
*   **Background Tasks**: Automated background job to expire unpaid/unconfirmed tickets using `APScheduler`.
*   **Database**: PostgreSQL for reliable data storage.
*   **Containerization**: Docker and Docker Compose for easy setup and deployment.
*   **API Documentation**: Automatic API documentation (Swagger UI).

## Technologies Used

*   **FastAPI**: Web framework for building APIs.
*   **SQLAlchemy**: Python SQL toolkit and Object-Relational Mapper (ORM).
*   **PostgreSQL**: Powerful, open-source relational database.
*   **Uvicorn**: ASGI server for running FastAPI applications.
*   **APScheduler**: Python library for scheduling tasks.
*   **Docker & Docker Compose**: For containerization and orchestration.
*   **python-dotenv**: For managing environment variables.
*   **Pytest**: For testing the API endpoints.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Docker
*   Docker Compose

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Princeigwe/tixxety-test-api.git
    cd tixxety-test-api
    ```

2.  **Create a `.env` file:**
    Create a file named `.env` in the root directory of the project. This file will hold your environment variables.
    ```
    # .env
    DATABASE_URL=postgresql://user:password@db:5432/tixxety_db
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=tixxety_db
    ```


3.  **Build and run the services:**
    Use Docker Compose to build the images and start all the services (web API, PostgreSQL database, and PGAdmin).
    ```bash
    docker-compose up --build 
    ```
### Accessing the Application

Once the services are up and running:

*   **Tixxety API**: Accessible at `http://localhost:8000`
    *   Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
    *   Alternative documentation (ReDoc): `http://localhost:8000/redoc`

*   **PGAdmin**: Accessible at `http://localhost:8080`
    *   Login with:
        *   Email: `admin@example.com`
        *   Password: `admin`
    *   You will need to add a new server connection in PGAdmin to connect to your database:
        *   **Host name/address**: `db` (this is the service name from `compose.yml`)
        *   **Port**: `5432`
        *   **Maintenance database**: `tixxety_db`
        *   **Username**: `user`
        *   **Password**: `password`

## Running Tests

To run the tests for the API:

1.  Ensure your Docker Compose services are running (`docker-compose up -d`).
2.  Execute `pytest` inside the `web` service container:
    ```bash
    docker-compose exec web pytest
    ```
## Project Structure

The project is organized into modules, each handling a specific domain:

*   `modules/auth`: Handles user authentication and authorization logic.
*   `modules/events`: Manages event creation.
*   `modules/tickets`: Deals with ticket reservation.
*   `database_config.py`: Contains SQLAlchemy engine setup, session management, and base declarative model.
*   `main.py`: The main FastAPI application entry point, responsible for including routers, setting up CORS, and scheduling background tasks.
*   `Dockerfile`: Defines the Docker image for the FastAPI application.
*   `compose.yml`: Orchestrates the multi-container Docker application (API, PostgreSQL, PGAdmin).

## Assumption
One of the tasks brought up was to utilize Celery to mark reserved tickets as expired after 2 minutes if not paid for. I believe the goal of this was to run it  as background task. 

However, I considered Celery to be an overhead, reason being that one would have to spin up a Celery worker and a Redis instance for it. I went ahead with a better option of utilizing the package: [APScheduler](https://pypi.org/project/APScheduler/). 

This spins up a separate thread away from the main thread, and this can also be configured to run tasks at intervals, as you can see in the code below:
```python

from apscheduler.schedulers.background import BackgroundScheduler

# cron job operation to run background task to expire unpaid tickets at 1-minute intervals
scheduler = BackgroundScheduler()
scheduler.add_job(ticket_services.expire_unpaid_tickets, 'interval', minutes=1) 
scheduler.start()
```

## Note
During user authentication, the request body should be of type `form-data` instead of `json`, with the fields `username` and `password` to represent the user's email and password, respectively.


## Contact

*   **Prince Igwenaghga**
    *   LinkedIn: https://linkedin.com/in/prince-igwenagha
