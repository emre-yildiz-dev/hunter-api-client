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
from hunter_client import create_client

client = create_client(api_key="your_api_key")

with client:
    # Search a domain
    emails = client.domain_search(domain="example.com", limit=10)
    
    # Find someone's email
    email = client.email_finder(
        domain="example.com",
        first_name="John",
        last_name="Doe"
    )
    
    # Verify an email
    result = client.email_verifier("john.doe@example.com")
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

## Future Developments

### Authentication
Adding OAuth2 and API key management to secure endpoints and manage user access.

### Tests
Expanding test coverage with more edge cases, performance tests, and end-to-end testing scenarios.

### Rate Limiting
Implementing intelligent rate limiting to handle Hunter.io's API limits gracefully and provide better user feedback.

## Tech Stack

- Python 3.11+
- FastAPI - Web framework
- Pydantic - Data validation
- httpx - HTTP client
- pytest - Testing
- Docker - Containerization

## License

MIT