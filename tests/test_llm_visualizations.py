"""Tests for LLM-powered visualization endpoints with JSON fields"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from pulse.main import app


class TestLLMVisualizationEndpoints:
    """Test suite for LLM visualization functionality with JSON fields"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)

    @pytest.fixture
    async def async_client(self):
        """Create async test client"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client

    def test_health_endpoint(self, client):
        """Test health endpoint is working"""
        response = client.get("/api/health")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_industry_pie_chart(self, async_client):
        """Test industry breakdown pie chart generation"""
        response = await async_client.post(
            "/api/visualizations/generate",
            json={"prompt": "Create a pie chart representing industry breakdown"},
        )

        assert response.status_code == 200
        data = response.json()

        # Verify successful response
        assert data["success"] is True
        assert data["visualization_type"] == "pie"
        assert "industry" in data["title"].lower()

        # Verify data structure
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

        # Verify data contains expected fields
        first_item = data["data"][0]
        assert "industry" in first_item
        assert "count" in first_item or "companies" in first_item

    @pytest.mark.asyncio
    async def test_investor_frequency_analysis(self, async_client):
        """Test investor frequency analysis with JSON fields"""
        response = await async_client.post(
            "/api/visualizations/generate",
            json={"prompt": "Which investors appear most frequently?"},
        )

        assert response.status_code == 200
        data = response.json()

        # Verify successful response
        assert data["success"] is True
        assert data["visualization_type"] == "bar"
        assert "investor" in data["title"].lower()

        # Verify SQL uses JSON functions
        sql = data["sql"].lower()
        assert "json_each" in sql
        assert "top_investors" in sql

        # Verify data structure
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

        # Verify investor data format
        first_investor = data["data"][0]
        assert "investor" in first_investor
        assert "frequency" in first_investor or "count" in first_investor
        assert isinstance(
            (
                first_investor["frequency"]
                if "frequency" in first_investor
                else first_investor["count"]
            ),
            int,
        )

    @pytest.mark.asyncio
    async def test_product_analysis(self, async_client):
        """Test product analysis with JSON arrays"""
        response = await async_client.post(
            "/api/visualizations/generate",
            json={"prompt": "Show me the most common products or services"},
        )

        assert response.status_code == 200
        data = response.json()

        # Verify successful response
        assert data["success"] is True
        assert data["visualization_type"] in ["bar", "pie"]

        # Verify SQL uses JSON functions for products
        sql = data["sql"].lower()
        assert "json_each" in sql
        assert "product" in sql

        # Verify data structure
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

    @pytest.mark.asyncio
    async def test_founded_year_valuation_scatter(self, async_client):
        """Test scatter plot for founded year vs valuation"""
        response = await async_client.post(
            "/api/visualizations/generate",
            json={"prompt": "Create a scatter plot of founded year and valuation"},
        )

        assert response.status_code == 200
        data = response.json()

        # Verify successful response
        assert data["success"] is True
        assert data["visualization_type"] == "scatter"
        assert "founded" in data["title"].lower() and "valuation" in data["title"].lower()

        # Verify data structure
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

        # Verify scatter plot data
        first_item = data["data"][0]
        assert "founded_year" in first_item
        assert "valuation_usd" in first_item

    @pytest.mark.asyncio
    async def test_arr_valuation_correlation(self, async_client):
        """Test ARR vs Valuation correlation analysis"""
        response = await async_client.post(
            "/api/visualizations/generate",
            json={
                "prompt": (
                    "Give me the best representation of data to understand "
                    "correlation of ARR and Valuation"
                )
            },
        )

        assert response.status_code == 200
        data = response.json()

        # Verify successful response
        assert data["success"] is True
        assert data["visualization_type"] == "scatter"

        # Verify data contains both ARR and valuation
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

        first_item = data["data"][0]
        assert "arr_usd" in first_item
        assert "valuation_usd" in first_item

    @pytest.mark.asyncio
    async def test_specific_investor_filter(self, async_client):
        """Test filtering by specific investor using JSON functions"""
        response = await async_client.post(
            "/api/visualizations/generate",
            json={"prompt": "Show me all companies that have Sequoia as an investor"},
        )

        assert response.status_code == 200
        data = response.json()

        # Verify successful response
        assert data["success"] is True

        # Verify SQL uses JSON functions for filtering
        sql = data["sql"].lower()
        assert ("json_extract" in sql or "json_each" in sql) and "sequoia" in sql

        # Verify data structure
        assert isinstance(data["data"], list)

    @pytest.mark.asyncio
    async def test_invalid_prompt_handling(self, async_client):
        """Test handling of invalid or dangerous prompts"""
        response = await async_client.post(
            "/api/visualizations/generate",
            json={"prompt": "DROP TABLE companies; SELECT * FROM users;"},
        )

        assert response.status_code == 200
        data = response.json()

        # Should either succeed with safe query or fail gracefully
        if not data["success"]:
            assert "error" in data
            assert data["visualization_type"] == "error"
        else:
            # If it succeeds, SQL should be sanitized to SELECT only
            assert data["sql"].upper().strip().startswith("SELECT")
            assert "DROP" not in data["sql"].upper()

    @pytest.mark.asyncio
    async def test_empty_prompt_handling(self, async_client):
        """Test handling of empty prompts"""
        response = await async_client.post("/api/visualizations/generate", json={"prompt": ""})

        assert response.status_code == 400  # Should return bad request for empty prompt

    @pytest.mark.asyncio
    async def test_json_field_data_integrity(self, async_client):
        """Test that JSON field data maintains proper structure"""
        # Get company data to verify JSON structure
        response = await async_client.get("/api/companies?limit=5")

        if response.status_code == 200:
            data = response.json()

            # Verify companies have proper JSON array structure
            for company in data.get("companies", []):
                # top_investors should be an array of strings
                assert isinstance(company["top_investors"], list)
                assert all(isinstance(investor, str) for investor in company["top_investors"])

                # product should be an array of strings
                assert isinstance(company["product"], list)
                assert all(isinstance(product, str) for product in company["product"])

    @pytest.mark.asyncio
    async def test_chart_config_structure(self, async_client):
        """Test that chart configurations are properly structured"""
        response = await async_client.post(
            "/api/visualizations/generate",
            json={"prompt": "Which investors appear most frequently?"},
        )

        assert response.status_code == 200
        data = response.json()

        if data["success"]:
            # Verify chart_config exists and has proper structure
            assert "chart_config" in data
            chart_config = data["chart_config"]

            # For bar charts, should have x_field and y_field
            if data["visualization_type"] == "bar":
                assert "x_field" in chart_config
                assert "y_field" in chart_config

    @pytest.mark.asyncio
    async def test_sql_injection_prevention(self, async_client):
        """Test SQL injection prevention"""
        malicious_prompts = [
            "Show companies; DROP TABLE companies; --",
            "'; DELETE FROM companies; SELECT '1",
            "UNION SELECT * FROM sqlite_master",
        ]

        for prompt in malicious_prompts:
            response = await async_client.post(
                "/api/visualizations/generate", json={"prompt": prompt}
            )

            assert response.status_code == 200
            data = response.json()

            # Should either fail gracefully or sanitize to safe SELECT
            if data["success"]:
                sql = data["sql"].upper()
                assert sql.strip().startswith("SELECT")
                assert "DROP" not in sql
                assert "DELETE" not in sql
                assert "INSERT" not in sql
                assert "UPDATE" not in sql


class TestLLMServiceDirectly:
    """Direct tests for LLM service functionality"""

    @pytest.mark.asyncio
    async def test_llm_service_json_queries(self):
        """Test LLM service generates correct JSON queries"""
        from pulse.database.session import init_database
        from pulse.services.llm import llm_service

        await init_database()

        # Test investor frequency query
        result = await llm_service.process_query("Which investors appear most frequently?")

        assert result["success"] is True
        assert "json_each" in result["sql"].lower()
        assert "top_investors" in result["sql"].lower()
        assert len(result["data"]) > 0

        # Verify data structure
        first_item = result["data"][0]
        assert "investor" in first_item
        assert isinstance(first_item["investor"], str)
        assert "frequency" in first_item or "count" in first_item

    @pytest.mark.asyncio
    async def test_llm_service_product_queries(self):
        """Test LLM service handles product JSON queries"""
        from pulse.database.session import init_database
        from pulse.services.llm import llm_service

        await init_database()

        # Test product analysis query
        result = await llm_service.process_query("What are the most common products?")

        assert result["success"] is True
        sql_lower = result["sql"].lower()
        assert "json_each" in sql_lower
        assert "product" in sql_lower
