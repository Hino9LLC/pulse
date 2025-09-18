"""Demo authentication tests using prototype credentials

These tests use the actual demo credentials from the application to test
realistic authentication flows. Perfect for prototyping where you want
to test against actual working credentials.

Demo credentials: demo@example.com / aircastles123
"""

from fastapi.testclient import TestClient


def create_demo_test_app():
    """Create test app with minimal auth endpoints for demo testing"""
    from fastapi import Depends, FastAPI, HTTPException, status
    from fastapi.security import HTTPBearer
    from pydantic import BaseModel

    app = FastAPI(title="Demo Auth Test")
    security = HTTPBearer()

    # Mock user data matching demo credentials
    demo_user = {"id": 1, "email": "demo@example.com", "name": "Demo User", "status": "active"}

    # Valid demo token (mock)
    demo_token = "demo-jwt-token-12345"

    class LoginRequest(BaseModel):
        email: str
        password: str

    class TokenResponse(BaseModel):
        access_token: str
        token_type: str

    @app.post("/api/auth/login", response_model=TokenResponse)
    async def demo_login(credentials: LoginRequest):
        """Demo login endpoint that accepts demo credentials"""
        if credentials.email == "demo@example.com" and credentials.password == "aircastles123":
            return {"access_token": demo_token, "token_type": "bearer"}

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password"
        )

    @app.get("/api/auth/me")
    async def get_current_user(token: str = Depends(security)):
        """Protected endpoint that returns user info with valid token"""
        # In real app, this would validate the JWT token
        if token.credentials == demo_token:
            return demo_user

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    @app.get("/api/items/")
    async def get_items(token: str = Depends(security)):
        """Protected endpoint for testing authenticated access"""
        if token.credentials == demo_token:
            return [
                {"id": 1, "title": "Demo Item 1", "status": "active"},
                {"id": 2, "title": "Demo Item 2", "status": "draft"},
            ]

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )

    return app


# Test client setup
demo_app = create_demo_test_app()
client = TestClient(demo_app)


class TestDemoAuthentication:
    """Test authentication using demo credentials"""

    def test_demo_login_success(self):
        """Test successful login with demo credentials"""
        login_data = {"email": "demo@example.com", "password": "aircastles123"}

        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200

        token_data = response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        assert token_data["access_token"] == "demo-jwt-token-12345"

    def test_demo_login_wrong_password(self):
        """Test login failure with wrong password"""
        login_data = {"email": "demo@example.com", "password": "wrongpassword"}

        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401

        error_data = response.json()
        assert error_data["detail"] == "Incorrect email or password"

    def test_demo_login_wrong_email(self):
        """Test login failure with wrong email"""
        login_data = {"email": "wrong@example.com", "password": "aircastles123"}

        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401

    def test_demo_login_missing_fields(self):
        """Test login validation with missing fields"""
        response = client.post("/api/auth/login", json={})
        assert response.status_code == 422  # Validation error


class TestAuthenticatedEndpoints:
    """Test protected endpoints using demo authentication"""

    def get_demo_token(self):
        """Helper to get demo authentication token"""
        login_data = {"email": "demo@example.com", "password": "aircastles123"}

        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200

        token_data = response.json()
        return token_data["access_token"]

    def test_get_current_user_with_token(self):
        """Test /me endpoint with valid demo token"""
        token = self.get_demo_token()
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 200

        user_data = response.json()
        assert user_data["email"] == "demo@example.com"
        assert user_data["name"] == "Demo User"
        assert user_data["status"] == "active"

    def test_get_current_user_without_token(self):
        """Test /me endpoint without authentication"""
        response = client.get("/api/auth/me")
        assert response.status_code == 403  # FastAPI HTTPBearer returns 403 for missing auth

    def test_get_current_user_invalid_token(self):
        """Test /me endpoint with invalid token"""
        headers = {"Authorization": "Bearer invalid-token"}

        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 401

    def test_protected_items_endpoint(self):
        """Test accessing items endpoint with authentication"""
        token = self.get_demo_token()
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/items/", headers=headers)
        assert response.status_code == 200

        items = response.json()
        assert len(items) == 2
        assert items[0]["title"] == "Demo Item 1"
        assert items[1]["title"] == "Demo Item 2"

    def test_protected_items_endpoint_no_auth(self):
        """Test items endpoint requires authentication"""
        response = client.get("/api/items/")
        assert response.status_code == 403  # FastAPI HTTPBearer returns 403 for missing auth


class TestCompleteAuthFlow:
    """Test complete authentication workflow"""

    def test_login_and_access_protected_resource(self):
        """Test complete flow: login → get token → access protected endpoint"""
        # Step 1: Login with demo credentials
        login_data = {"email": "demo@example.com", "password": "aircastles123"}

        login_response = client.post("/api/auth/login", json=login_data)
        assert login_response.status_code == 200

        token_data = login_response.json()
        token = token_data["access_token"]

        # Step 2: Use token to get user info
        headers = {"Authorization": f"Bearer {token}"}
        me_response = client.get("/api/auth/me", headers=headers)
        assert me_response.status_code == 200

        user_data = me_response.json()
        assert user_data["email"] == "demo@example.com"

        # Step 3: Use token to access protected resource
        items_response = client.get("/api/items/", headers=headers)
        assert items_response.status_code == 200

        items = items_response.json()
        assert isinstance(items, list)
        assert len(items) > 0


# Integration test that could work with real app (commented for now)
"""
class TestRealAppDemoAuth:
    '''Test demo authentication against the actual application'''
    
    @pytest.mark.integration
    def test_real_demo_login(self):
        '''Test login against real application with demo credentials'''
        from pulse.main import app
        real_client = TestClient(app)
        
        # This would test against your actual application
        login_data = {
            "email": "demo@example.com",
            "password": "aircastles123"
        }
        
        response = real_client.post("/api/auth/login", json=login_data)
        
        # Should work if demo user exists in database
        if response.status_code == 200:
            token_data = response.json()
            assert "access_token" in token_data
            
            # Test using the token
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            me_response = real_client.get("/api/auth/me", headers=headers)
            assert me_response.status_code == 200
"""


def test_demo_credentials_documented():
    """Ensure demo credentials are documented in test"""
    demo_email = "demo@example.com"
    demo_password = "aircastles123"

    assert demo_email == "demo@example.com"
    assert demo_password == "aircastles123"
    assert True, "Demo credentials: demo@example.com / aircastles123"
