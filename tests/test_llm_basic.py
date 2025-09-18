"""Basic tests for LLM service functionality"""

import asyncio

import pytest

from pulse.database.session import init_database
from pulse.services.llm import llm_service


class TestLLMBasicFunctionality:
    """Test basic LLM service functionality"""

    @pytest.fixture(autouse=True)
    async def setup_database(self):
        """Initialize database for each test"""
        await init_database()

    @pytest.mark.asyncio
    async def test_investor_frequency_query(self):
        """Test that LLM generates correct investor frequency queries"""
        result = await llm_service.process_query("Which investors appear most frequently?")

        assert result["success"] is True
        assert result["visualization_type"] == "bar"
        assert "investor" in result["title"].lower()

        # Verify SQL uses JSON functions
        sql = result["sql"].lower()
        assert "json_each" in sql
        assert "top_investors" in sql
        assert "group by" in sql

        # Verify data structure
        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0

        # Check first result
        first_investor = result["data"][0]
        assert "investor" in first_investor
        assert "frequency" in first_investor or "count" in first_investor

        # Should be Sequoia as most frequent
        assert first_investor["investor"] == "Sequoia"

    @pytest.mark.asyncio
    async def test_industry_breakdown_query(self):
        """Test industry breakdown pie chart"""
        result = await llm_service.process_query(
            "Create a pie chart representing industry breakdown"
        )

        assert result["success"] is True
        assert result["visualization_type"] == "pie"
        assert "industry" in result["title"].lower()

        # Verify SQL structure
        sql = result["sql"].lower()
        assert "select" in sql
        assert "industry" in sql
        assert "count" in sql or "group by" in sql

        # Verify data
        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0

    @pytest.mark.asyncio
    async def test_product_analysis_query(self):
        """Test product analysis with JSON arrays"""
        result = await llm_service.process_query("Show me the most common products")

        assert result["success"] is True

        # Verify SQL uses JSON functions for products
        sql = result["sql"].lower()
        assert "json_each" in sql
        assert "product" in sql

        # Verify data structure
        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0

    @pytest.mark.asyncio
    async def test_scatter_plot_query(self):
        """Test scatter plot generation"""
        result = await llm_service.process_query(
            "Create a scatter plot of founded year and valuation"
        )

        assert result["success"] is True
        assert result["visualization_type"] == "scatter"

        # Verify data has required fields
        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0

        first_item = result["data"][0]
        assert "founded_year" in first_item
        assert "valuation_usd" in first_item

    @pytest.mark.asyncio
    async def test_sql_sanitization(self):
        """Test that dangerous SQL is blocked"""
        dangerous_prompts = [
            "DROP TABLE companies",
            "DELETE FROM companies",
            "INSERT INTO companies VALUES",
            "UPDATE companies SET",
        ]

        for prompt in dangerous_prompts:
            result = await llm_service.process_query(prompt)

            # Should either fail or produce safe SELECT query
            if result["success"]:
                sql = result["sql"].upper()
                assert sql.strip().startswith("SELECT")
                assert "DROP" not in sql
                assert "DELETE" not in sql
                assert "INSERT" not in sql
                assert "UPDATE" not in sql
            else:
                assert result["visualization_type"] == "error"

    @pytest.mark.asyncio
    async def test_json_query_examples(self):
        """Test specific JSON query patterns work correctly"""
        # Test filtering by specific investor
        result = await llm_service.process_query("Show companies with Sequoia as investor")

        if result["success"]:
            sql = result["sql"].lower()
            # Should use JSON functions to filter
            assert "json_extract" in sql or "json_each" in sql
            assert "sequoia" in sql.lower()


def test_sync_wrapper():
    """Test wrapper for running async tests synchronously"""

    async def run_basic_test():
        await init_database()
        result = await llm_service.process_query("Which investors appear most frequently?")
        return result["success"] and len(result["data"]) > 0

    success = asyncio.run(run_basic_test())
    assert success
