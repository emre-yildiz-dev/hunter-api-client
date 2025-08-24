# Hunter.io API Client

A clean Python client for the Hunter.io API. Find emails, verify addresses, and search domains with ease.

## What it does

This client makes it simple to work with Hunter.io's email finding and verification services. Whether you need to find someone's email address, verify if an email exists, or search for all emails associated with a domain, this tool has you covered.

Built with FastAPI for the web interface and uses modern Python practices throughout.

## Quick Start

### 1. Install

```bash
# Set up Python environment
uv venv --python 3.11

# Install dependencies
uv pip install --python .venv/bin/python -e ".[dev]"
```

### 2. Configure

Create a `.env` file and add your Hunter.io API key:

```
HUNTER_API_KEY=your_api_key_here
```

### 3. Run

```bash
.venv/bin/python -m hunter_client.main
```

That's it! The API is now running at `http://127.0.0.1:8000`

## Using the API

### Available Endpoints

- `GET /domain-search` - Find all emails for a domain
- `POST /email-finder` - Find a specific person's email
- `POST /email-verifier` - Check if an email is valid
- `GET /account` - View your account details

Visit `http://127.0.0.1:8000/docs` for interactive documentation.

### Python Example

```python
from hunter_client.client import create_client

client = create_client(api_key="your_api_key")

with client:
    # Search a domain
    emails = client.domain.search(domain="example.com", limit=10)
    
    # Find someone's email
    email = client.email.find(
        domain="example.com",
        first_name="John",
        last_name="Doe"
    )
    
    # Verify an email
    result = client.email.verify("john.doe@example.com")
```

## Development

### Running Tests

```bash
# Run all tests
.venv/bin/pytest

# Unit tests only
.venv/bin/pytest tests/unit

# Integration tests only
.venv/bin/pytest tests/integration
```

### Code Quality

```bash
# Type checking
.venv/bin/mypy src

# Linting
.venv/bin/flake8 src tests

# Format code
.venv/bin/black src tests
.venv/bin/isort src tests
```

### Docker

```bash
docker-compose up  # Run with Docker
```

## TODO: Future Developments

- [ ] **Authentication (SQLite + JWT)** - Implement secure user authentication with JWT tokens and SQLite database for user management. This will enable multi-user support, API key management per user, and role-based access control (RBAC).

- [ ] **Rate Limiting (Redis)** - Add Redis-based rate limiting to protect the API from abuse and manage Hunter.io's API limits effectively. Implement sliding window algorithms with configurable limits per user and endpoint.

- [ ] **Database Layer (PostgreSQL/SQLite)** - Integrate a persistent database layer to store user profiles, API usage history, cached responses, and audit logs. This enables better analytics and user management.

- [ ] **Caching with Redis** - Enhance performance with Redis caching for Hunter.io responses. Implement TTL-based cache invalidation, selective cache bypass, and distributed caching for multi-instance deployments.

- [ ] **Monitoring with ELK Stack** - Set up comprehensive monitoring using Elasticsearch, Logstash, and Kibana (ELK Stack) for real-time system health observation, log aggregation, and performance metrics visualization.

- [ ] **Background Tasks (Celery + Redis)** - Implement asynchronous task processing with Celery and Redis for handling long-running operations like bulk email verification, scheduled domain scans, and report generation.

## Tech Stack

- Python 3.11+
- FastAPI - Web framework
- Pydantic - Data validation
- httpx - HTTP client
- pytest - Testing
- Docker - Containerization

## License

MIT