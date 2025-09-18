# Testing Strategy for Pulse

This directory contains tests organized for rapid prototyping with incremental complexity.

## Test Organization

### `test_basic.py`
- **Purpose**: Smoke tests to ensure Python environment works
- **Scope**: Basic imports and environment validation
- **When to use**: Always - these should always pass

### `test_endpoints.py` 
- **Purpose**: Basic endpoint testing with minimal dependencies
- **Scope**: Simple FastAPI endpoints without database/auth complexity
- **Pattern**: Isolated test app with mock endpoints
- **When to use**: Early prototyping, ensuring basic API structure works

### `test_demo_auth.py`
- **Purpose**: Authentication testing using demo credentials
- **Scope**: Login flow, protected endpoints, token validation
- **Pattern**: Mock authentication with realistic demo user (demo@example.com / aircastles123)
- **When to use**: Testing auth flows during prototyping

### `test_advanced_endpoints.py`
- **Purpose**: Advanced testing patterns (commented examples)
- **Scope**: Database mocking, authentication, full integration tests
- **Pattern**: Comprehensive mocking with pytest fixtures
- **When to use**: When features stabilize and you need robust testing

## Running Tests

```bash
# Run all tests
make test

# Run only Python tests  
make test-python

# Run only React tests
make test-react

# Run with coverage
PYTHONPATH=src uv run pytest --cov=pulse
```

## Testing Philosophy for Prototyping

### ✅ **Start Simple**
- Begin with basic smoke tests (`test_basic.py`)
- Add simple endpoint tests (`test_endpoints.py`)
- Test authentication with demo credentials (`test_demo_auth.py`)
- Gradually increase complexity as features stabilize

### ✅ **Avoid Over-Testing Early**
- Don't write comprehensive tests for rapidly changing features
- Focus on core functionality and API contracts
- Test the "happy path" first

### ✅ **Use Examples as Templates**
- `test_advanced_endpoints.py` provides patterns for later
- Copy and adapt patterns when you need more sophisticated testing
- Uncomment examples when features are stable

## Key Patterns

### Basic Endpoint Testing
```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
```

### Demo Authentication Testing
```python
def test_demo_login():
    """Test with actual prototype credentials"""
    login_data = {
        "email": "demo@example.com",
        "password": "aircastles123"
    }
    
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test protected endpoint
    protected_response = client.get("/api/items/", headers=headers)
    assert protected_response.status_code == 200
```

### Mocking for Complex Dependencies
```python
# See test_advanced_endpoints.py for examples of:
# - Database mocking
# - Authentication mocking  
# - Service layer mocking
# - WebSocket testing patterns
```

## When to Expand Testing

1. **API contracts stabilize** → Add comprehensive endpoint tests
2. **Business logic complexity grows** → Add unit tests for services  
3. **Multiple user workflows** → Add integration tests
4. **Pre-production** → Add load/performance tests

## Coverage Goals

- **Prototyping Phase**: 20-40% coverage, focus on critical paths
- **Feature Development**: 60-80% coverage, comprehensive endpoint testing
- **Production Ready**: 80%+ coverage, full integration testing

Remember: **Good enough tests that run are better than perfect tests that don't exist yet.**
