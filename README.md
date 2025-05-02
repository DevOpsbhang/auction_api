# Auction API

A RESTful API for managing auctions built with Django, PostgreSQL, and JWT authentication.

## Features

- User Authentication with JWT
- Auction Management (CRUD operations)
- Bidding System
- Admin Interface
- API Documentation (Swagger)
- Monitoring (Prometheus + Grafana)
- PostgreSQL Database
- Docker Support
- CI/CD with GitHub Actions

## Tech Stack

- Python 3.10
- Django 4.2.7
- Django REST Framework
- PostgreSQL 13
- Docker & Docker Compose
- JWT Authentication
- Swagger/OpenAPI
- Prometheus & Grafana

## Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Docker and Docker Compose (optional)

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd auction-api
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

### Docker Setup

1. Build and start services:
```bash
docker-compose up --build
```

2. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

3. Create superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

## API Endpoints

### Authentication
- POST /api/auth/register/ - Register new user
- POST /api/auth/login/ - Login and get tokens
- POST /api/auth/token/refresh/ - Refresh JWT token

### Auctions
- GET /api/auctions/ - List all auctions
- POST /api/auctions/create/ - Create new auction
- GET /api/auctions/{id}/ - Get auction details
- PUT /api/auctions/{id}/ - Update auction
- DELETE /api/auctions/{id}/ - Delete auction
- POST /api/auctions/{id}/bids/ - Place bid

## Testing

Run all tests:
```bash
# Using Django test runner
python manage.py test auctions && python manage.py test authentication

# Using pytest with coverage
pytest --cov=.
```

## Monitoring

Access monitoring dashboards:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## CI/CD Pipeline

The GitHub Actions pipeline:
1. Runs tests on every push/PR
2. Builds Docker image
3. Runs on PostgreSQL database
4. Executes all test suites

## Development Guidelines

1. Create feature branch from main
2. Write tests for new features
3. Ensure all tests pass
4. Create pull request
5. Wait for CI checks to pass

## Environment Variables

Key environment variables (see .env.example):
- DB_NAME: PostgreSQL database name
- DB_USER: Database username
- DB_PASSWORD: Database password
- DB_HOST: Database host
- DB_PORT: Database port
- DJANGO_SECRET_KEY: Django secret key
- DEBUG: Debug mode (1/0)

## License

MIT License - see LICENSE file for details
