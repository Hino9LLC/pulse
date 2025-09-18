"""LLM service for natural language to SQL and visualization generation"""

import json
import re
from typing import Any

import anthropic
from sqlalchemy import text

from ..database.session import get_async_session
from ..settings import settings


class LLMService:
    """Service for processing natural language queries into SQL and visualizations"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.db_schema = {
            "table_name": "companies",
            "columns": {
                "id": "INTEGER PRIMARY KEY",
                "company_name": "VARCHAR(255) NOT NULL - Name of the company",
                "founded_year": "INTEGER NOT NULL - Year the company was founded",
                "headquarters": "VARCHAR(255) NOT NULL - Company headquarters location",
                "industry": "VARCHAR(255) NOT NULL - Industry sector",
                "total_funding_usd": "BIGINT NOT NULL DEFAULT 0 - Total funding in USD",
                "arr_usd": "BIGINT NOT NULL DEFAULT 0 - Annual Recurring Revenue in USD",
                "valuation_usd": "BIGINT NOT NULL DEFAULT 0 - Company valuation in USD",
                "employee_count": "INTEGER - Number of employees",
                "top_investors": "TEXT NOT NULL - List of top investors",
                "product": "TEXT NOT NULL - Description of product/service",
                "g2_rating": "FLOAT NOT NULL - G2 rating out of 5",
                "created_at": "DATETIME NOT NULL",
                "updated_at": "DATETIME NOT NULL",
            },
        }

    async def process_query(self, user_prompt: str) -> dict[str, Any]:
        """Process natural language query and return visualization config + data"""
        try:
            # Get SQL and visualization config from LLM
            llm_response = await self._get_llm_response(user_prompt)

            # Validate and sanitize SQL
            sql_query = self._sanitize_sql(llm_response.get("sql", ""))

            # Execute SQL and get data
            data = await self._execute_sql(sql_query)

            return {
                "success": True,
                "visualization_type": llm_response.get("visualization_type", "table"),
                "title": llm_response.get("title", "Visualization"),
                "sql": sql_query,
                "data": data,
                "chart_config": llm_response.get("chart_config", {}),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "visualization_type": "error",
                "title": "Error",
                "data": [],
            }

    async def _get_llm_response(self, user_prompt: str) -> dict[str, Any]:
        """Get structured response from LLM"""
        system_prompt = f"""
You are a data visualization expert. Given a user's natural language request, generate:
1. A SQL query for the companies database
2. The appropriate visualization type
3. A title for the visualization
4. Chart configuration if applicable

Database Schema:
Table: {self.db_schema["table_name"]}
Columns: {json.dumps(self.db_schema["columns"], indent=2)}

Rules:
- Only use SELECT statements
- Use proper SQL syntax for SQLite
- Choose appropriate visualization types: pie, bar, scatter, line, table
- For aggregations, use appropriate GROUP BY and aggregation functions
- Return response as valid JSON

Example responses:
{{
  "sql": "SELECT industry, COUNT(*) as count FROM companies GROUP BY industry",
  "visualization_type": "pie",
  "title": "Industry Breakdown",
  "chart_config": {{"x_field": "industry", "y_field": "count"}}
}}

{{
  "sql": "SELECT founded_year, valuation_usd FROM companies WHERE valuation_usd > 0",
  "visualization_type": "scatter",
  "title": "Founded Year vs Valuation",
  "chart_config": {{"x_field": "founded_year", "y_field": "valuation_usd"}}
}}
"""

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        response_text = message.content[0].text

        # Try to extract JSON from response
        try:
            # Look for JSON in the response
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return json.loads(response_text)
        except json.JSONDecodeError as err:
            raise ValueError(f"Invalid JSON response from LLM: {response_text}") from err

    def _sanitize_sql(self, sql: str) -> str:
        """Sanitize SQL query to prevent injection and ensure it's safe"""
        # Remove any dangerous keywords
        dangerous_keywords = [
            "DROP",
            "DELETE",
            "INSERT",
            "UPDATE",
            "ALTER",
            "CREATE",
            "EXEC",
            "EXECUTE",
        ]

        sql_upper = sql.upper()
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                raise ValueError(f"Dangerous SQL keyword '{keyword}' not allowed")

        # Must start with SELECT
        if not sql_upper.strip().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")

        # Basic SQL injection prevention
        if any(char in sql for char in [";", "--", "/*", "*/"]):
            if not (sql.count(";") == 1 and sql.rstrip().endswith(";")):
                raise ValueError("Potentially unsafe SQL detected")

        return sql.strip()

    async def _execute_sql(self, sql: str) -> list[dict[str, Any]]:
        """Execute SQL query and return results"""
        async with get_async_session() as session:
            result = await session.execute(text(sql))
            columns = result.keys()
            rows = result.fetchall()

            return [{col: row[i] for i, col in enumerate(columns)} for row in rows]


# Global service instance
llm_service = LLMService()
