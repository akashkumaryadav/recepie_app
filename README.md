[![Deploy to EC2](https://github.com/akashkumaryadav/recepie_app/actions/workflows/deploy.yml/badge.svg)](https://github.com/akashkumaryadav/recepie_app/actions/workflows/deploy.yml)
[![Static Badge](https://img.shields.io/badge/View%20Test%20Coverage-blue?link=https%3A%2F%2Fakashkumaryadav.github.io%2Frecepie_app%2Findex.html)](https://akashkumaryadav.github.io/recepie_app/index.html)



# Recipe App

A Django-based application for managing and sharing recipes. This application allows users to create, view, and manage their favorite recipes, with features such as user authentication, recipe categorization, and more.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Using GitHub Actions](#using-github-actions)
- [License](#license)

## Prerequisites

Before running the application, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.10+](https://www.python.org/downloads/) (for local development)

## Setup Instructions

1. **Clone the Repository**:

   Clone the repository to your local machine using:

   ```bash
   git clone https://github.com/akashkumaryadav/recepie_app
   cd recipe_app
   ```
2. Create a .env File: Create a .env file in the root directory of the project and add the following environment variables:

```text
SECRET_KEY="mytopsecret"

# Database configs
DB_NAME=
DB_USERNAME="postgres"
DB_PASSWORD="postgres"
DB_HOSTNAME=
DB_PORT=

# Email configs
EMAIL_USER = 
EMAIL_PASSWORD = 
```
3. Build the docker image
   ```bash
   docker-compose build
   ```
4. Run Database Migrations: Start the services and run database migrations:
   ```bash
   docker-compose up -d
   docker-compose exec web python manage.py migrate
   ```
5. Create a Superuser:
  ```bash
    docker-compose exec web python manage.py createsuperuser
  ```


6. Run Tests
    To run tests for your application:
   ```bash
      docker-compose exec web python manage.py test
   ```

7. View Logs
    To view the logs of the web service:
    ```bash
      docker-compose logs web
    ```
