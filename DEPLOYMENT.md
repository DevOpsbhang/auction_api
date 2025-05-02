# Auction API Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- Python 3.10+
- PostgreSQL (for local development)

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/your-repo/auction-api.git
cd auction-api
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Start the services:
```bash
docker-compose up -d
```

4. Apply migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. Create superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

6. Access services:
- API: http://localhost:8000
- Admin: http://localhost:8000/admin
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Production Deployment

1. Set production environment variables:
```bash
export DJANGO_SECRET_KEY=your-secret-key
export DEBUG=0
export DATABASE_URL=postgresql://user:password@db-host:5432/db-name
```

2. Build and run:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

3. Monitor services:
```bash
docker-compose logs -f
```

## CI/CD Pipeline
The GitHub Actions workflow will:
- Run tests on push/PR
- Build Docker image on main branch
- (Optional) Deploy to production

### GitHub Actions Workflow Enhancements
The CI/CD pipeline now includes:
- Running Django tests on push to main branch
- Building the Docker image for the Django app
- (Optional) You can extend the workflow to push the Docker image to a container registry like Docker Hub or GitHub Container Registry

### Deployment Instructions
1. Build and run the Docker containers locally:
```bash
docker-compose up -d --build
```
2. Apply database migrations:
```bash
docker-compose exec web python manage.py migrate
```
3. Create a Django superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```
4. Access the application at http://localhost:8000

### Rolling Updates with Docker Swarm
To perform rolling updates using Docker Swarm:
1. Initialize Docker Swarm (if not already):
```bash
docker swarm init
```
2. Deploy the stack:
```bash
docker stack deploy -c docker-compose.yml auction_stack
```
3. Update the service with a new image:
```bash
docker service update --image auction_app:latest auction_stack_web
```
4. Monitor the update status:
```bash
docker service ps auction_stack_web
```

## Monitoring Setup
1. Access Grafana at http://localhost:3000
2. Login with admin/admin
3. Add Prometheus datasource (http://prometheus:9090)
4. Import Django monitoring dashboard
