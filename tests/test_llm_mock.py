"""Tests for LLM service with mocked responses"""

from unittest.mock import AsyncMock, patch

import pytest

from pulse.database.session import init_database
from pulse.services.llm import LLMService


class TestLLMServiceMocked:
    """Test LLM service with mocked Anthropic responses"""

    @pytest.fixture(autouse=True)
    async def setup_database(self):
        """Initialize database for each test"""
        await init_database()

    @pytest.mark.asyncio
    async def test_investor_frequency_with_mock(self):
        """Test investor frequency query with mocked LLM response"""
        # Mock LLM response for investor frequency
        mock_llm_response = {
            "sql": (
                "SELECT json_each.value as investor, COUNT(*) as frequency "
                "FROM companies, json_each(top_investors) GROUP BY investor "
                "HAVING frequency > 1 ORDER BY frequency DESC LIMIT 15"
            ),
            "visualization_type": "bar",
            "title": "Most Frequent Investors",
            "chart_config": {"x_field": "investor", "y_field": "frequency"},
        }

        with patch.object(LLMService, "_get_llm_response", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_llm_response

            llm_service = LLMService()
            result = await llm_service.process_query("Which investors appear most frequently?")

            # Verify the result
            assert result["success"] is True
            assert result["visualization_type"] == "bar"
            assert "investor" in result["title"].lower()

            # Verify SQL contains JSON functions
            sql = result["sql"].lower()
            assert "json_each" in sql
            assert "top_investors" in sql

            # Verify we got real data from database
            assert isinstance(result["data"], list)
            assert len(result["data"]) > 0

            # Check top investor is Sequoia (from our test data)
            first_investor = result["data"][0]
            assert first_investor["investor"] == "Sequoia"
            assert first_investor["frequency"] == 18

    @pytest.mark.asyncio
    async def test_product_analysis_with_mock(self):
        """Test product analysis with mocked LLM response"""
        mock_llm_response = {
            "sql": (
                "SELECT json_each.value as product, COUNT(*) as companies "
                "FROM companies, json_each(product) GROUP BY product "
                "ORDER BY companies DESC LIMIT 10"
            ),
            "visualization_type": "bar",
            "title": "Most Common Products",
            "chart_config": {"x_field": "product", "y_field": "companies"},
        }

        with patch.object(LLMService, "_get_llm_response", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_llm_response

            llm_service = LLMService()
            result = await llm_service.process_query("Show me the most common products")

            # Verify the result
            assert result["success"] is True
            assert result["visualization_type"] == "bar"

            # Verify SQL uses JSON functions
            sql = result["sql"].lower()
            assert "json_each" in sql
            assert "product" in sql

            # Verify we got real data
            assert isinstance(result["data"], list)
            assert len(result["data"]) > 0

    @pytest.mark.asyncio
    async def test_industry_breakdown_with_mock(self):
        """Test industry breakdown pie chart"""
        mock_llm_response = {
            "sql": (
                "SELECT industry, COUNT(*) as count FROM companies "
                "GROUP BY industry ORDER BY count DESC"
            ),
            "visualization_type": "pie",
            "title": "Industry Breakdown",
            "chart_config": {"x_field": "industry", "y_field": "count"},
        }

        with patch.object(LLMService, "_get_llm_response", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_llm_response

            llm_service = LLMService()
            result = await llm_service.process_query(
                "Create a pie chart representing industry breakdown"
            )

            # Verify the result
            assert result["success"] is True
            assert result["visualization_type"] == "pie"
            assert "industry" in result["title"].lower()

            # Verify we got industry data
            assert isinstance(result["data"], list)
            assert len(result["data"]) > 0

            # Check data structure
            first_item = result["data"][0]
            assert "industry" in first_item
            assert "count" in first_item

    @pytest.mark.asyncio
    async def test_sql_sanitization_works(self):
        """Test that SQL sanitization prevents dangerous queries"""
        # Mock a response that tries to be dangerous
        mock_llm_response = {
            "sql": "DROP TABLE companies; SELECT * FROM companies",
            "visualization_type": "table",
            "title": "Dangerous Query",
            "chart_config": {},
        }

        with patch.object(LLMService, "_get_llm_response", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_llm_response

            llm_service = LLMService()
            result = await llm_service.process_query("Some dangerous prompt")

            # Should fail due to SQL sanitization
            assert result["success"] is False
            assert result["visualization_type"] == "error"

    @pytest.mark.asyncio
    async def test_json_query_execution(self):
        """Test that JSON queries execute correctly against real database"""
        # Test investor frequency query directly
        from sqlalchemy import text

        from pulse.database.session import get_async_session

        sql = (
            "SELECT json_each.value as investor, COUNT(*) as frequency "
            "FROM companies, json_each(top_investors) GROUP BY investor "
            "HAVING frequency > 1 ORDER BY frequency DESC LIMIT 5"
        )

        async with get_async_session() as session:
            result = await session.execute(text(sql))
            rows = result.fetchall()
            columns = result.keys()

            # Convert to list of dicts
            data = [{col: row[i] for i, col in enumerate(columns)} for row in rows]

            # Verify we got results
            assert len(data) > 0

            # Verify structure
            first_item = data[0]
            assert "investor" in first_item
            assert "frequency" in first_item

            # Top investor should be Sequoia
            assert first_item["investor"] == "Sequoia"
            assert first_item["frequency"] > 1

    @pytest.mark.asyncio
    async def test_product_json_query_execution(self):
        """Test product JSON query execution"""
        from sqlalchemy import text

        from pulse.database.session import get_async_session

        sql = (
            "SELECT json_each.value as product, COUNT(*) as companies "
            "FROM companies, json_each(product) GROUP BY product "
            "ORDER BY companies DESC LIMIT 5"
        )

        async with get_async_session() as session:
            result = await session.execute(text(sql))
            rows = result.fetchall()
            columns = result.keys()

            # Convert to list of dicts
            data = [{col: row[i] for i, col in enumerate(columns)} for row in rows]

            # Verify we got results
            assert len(data) > 0

            # Verify structure
            first_item = data[0]
            assert "product" in first_item
            assert "companies" in first_item
            assert isinstance(first_item["product"], str)
            assert isinstance(first_item["companies"], int)

    def test_database_json_structure(self):
        """Test that our database actually contains JSON arrays"""
        import sqlite3

        conn = sqlite3.connect("pulse.db")
        cursor = conn.cursor()

        # Check that we have JSON arrays in the database
        cursor.execute("SELECT top_investors, product FROM companies LIMIT 3")
        rows = cursor.fetchall()

        assert len(rows) > 0

        for top_investors, product in rows:
            # Should be JSON strings that start with [
            assert top_investors.startswith("[") and top_investors.endswith("]")
            assert product.startswith("[") and product.endswith("]")

            # Should be valid JSON
            import json

            investors = json.loads(top_investors)
            products = json.loads(product)

            assert isinstance(investors, list)
            assert isinstance(products, list)
            assert all(isinstance(inv, str) for inv in investors)
            assert all(isinstance(prod, str) for prod in products)

        conn.close()
