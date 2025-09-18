"""LLM service for natural language to SQL and visualization generation"""

import json
import logging
from typing import Any

import anthropic
from sqlalchemy import text

from ..database.session import get_async_session
from ..settings import settings


logger = logging.getLogger("pulse.llm")


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
            # Log the error with context
            logger.error(
                "LLM query processing failed",
                extra={
                    "user_prompt": user_prompt,
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
            )

            return {
                "success": False,
                "error": str(e),
                "visualization_type": "error",
                "title": "Visualization Error",
                "data": [],
                "sql": "",
            }

    async def _get_llm_response(self, user_prompt: str) -> dict[str, Any]:
        """Get structured response from LLM"""
        system_prompt = f"""
You are a data visualization expert for the Top 100 SaaS Companies/Startups 2025 dataset.
You MUST handle these 4 REQUIRED visualization types:

1. [Easy] Create a pie chart representing industry breakdown
2. [Medium] Create a scatter plot of founded year and valuation
3. [Hard] Create a bar chart to see which investors appear most frequently
4. [Extreme] Give me the best representation of data to understand correlation of ARR and Valuation

CRITICAL REQUIREMENTS:
- ONLY generate SELECT statements - NO INSERT, UPDATE, DELETE, CREATE, DROP, or ANY other SQL commands
- ALL queries MUST start with "SELECT"
- Use basic SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT clauses only

Database Schema - Top 100 SaaS Companies 2025:
Table: {self.db_schema["table_name"]}
Columns: {json.dumps(self.db_schema["columns"], indent=2)}

SPECIAL HANDLING FOR INVESTOR ANALYSIS:
For "which investors appear most frequently", create a bar chart showing investor frequency:
- Extract individual investor names from the top_investors field
- Count how many times each investor appears across companies
- Show only investors that appear multiple times
- Use bar chart visualization to show investor frequency ranking

VISUALIZATION TYPES: pie, bar, scatter, line
IMPORTANT: NO table visualizations allowed - use bar charts instead for tabular data

MANDATORY JSON FORMAT - RETURN ONLY VALID JSON WITH NO ADDITIONAL TEXT:
{{
  "sql": "SELECT ...",
  "visualization_type": "pie|bar|scatter|line",
  "title": "Chart Title",
  "chart_config": {{"x_field": "column1", "y_field": "column2"}}
}}

CRITICAL: Return ONLY the JSON object, no explanatory text before or after!

REQUIRED EXAMPLES - MUST SUPPORT THESE:

1. Industry breakdown (pie):
{{
  "sql": "SELECT industry, COUNT(*) as company_count FROM companies GROUP BY industry ORDER BY company_count DESC",
  "visualization_type": "pie",
  "title": "Industry Breakdown",
  "chart_config": {{"x_field": "industry", "y_field": "company_count"}}
}}

2. Founded year vs valuation (scatter):
{{
  "sql": "SELECT founded_year, valuation_usd FROM companies WHERE valuation_usd > 0 ORDER BY founded_year",
  "visualization_type": "scatter",
  "title": "Founded Year vs Valuation",
  "chart_config": {{"x_field": "founded_year", "y_field": "valuation_usd"}}
}}

3. Most frequent investors (bar) - Show investor frequency as a bar chart:
{{
  "sql": "SELECT TRIM(investor) as investor_name, COUNT(*) as frequency FROM (SELECT TRIM(SUBSTR(top_investors, 1, INSTR(top_investors || ',', ',') - 1)) as investor FROM companies WHERE top_investors != '' AND top_investors NOT LIKE '%N/A%') GROUP BY investor_name HAVING frequency > 1 ORDER BY frequency DESC LIMIT 15",
  "visualization_type": "bar",
  "title": "Most Frequent Investors",
  "chart_config": {{"x_field": "investor_name", "y_field": "frequency"}}
}}

4. ARR vs Valuation correlation (scatter):
{{
  "sql": "SELECT arr_usd, valuation_usd FROM companies WHERE arr_usd > 0 AND valuation_usd > 0 ORDER BY arr_usd",
  "visualization_type": "scatter",
  "title": "ARR vs Valuation Correlation",
  "chart_config": {{"x_field": "arr_usd", "y_field": "valuation_usd"}}
}}

REMEMBER: Must support ALL 4 requirement examples. Only SELECT statements.
        """  # noqa: S608 E501

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        response_text = message.content[0].text

        # Try to extract JSON from response
        try:
            # Look for JSON in the response (find first complete JSON object)
            brace_count = 0
            start_idx = -1
            end_idx = -1

            for i, char in enumerate(response_text):
                if char == "{":
                    if start_idx == -1:
                        start_idx = i
                    brace_count += 1
                elif char == "}":
                    brace_count -= 1
                    if brace_count == 0 and start_idx != -1:
                        end_idx = i
                        break

            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx : end_idx + 1]
                return json.loads(json_str)
            else:
                # Fallback to trying the entire response as JSON
                return json.loads(response_text)
        except json.JSONDecodeError as err:
            raise ValueError(f"Invalid JSON response from LLM: {response_text}") from err

    def _sanitize_sql(self, sql: str) -> str:
        """Sanitize SQL query to prevent injection and ensure it's safe"""
        if not sql or not sql.strip():
            raise ValueError(
                "Empty SQL query received from LLM. Please try rephrasing your request."
            )

        sql_clean = sql.strip()
        sql_upper = sql_clean.upper()

        # Check for dangerous keywords
        dangerous_keywords = [
            "DROP",
            "DELETE",
            "INSERT",
            "UPDATE",
            "ALTER",
            "CREATE",
            "EXEC",
            "EXECUTE",
            "GRANT",
            "REVOKE",
            "TRUNCATE",
        ]

        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                raise ValueError(
                    f"SQL validation failed: '{keyword}' keyword not allowed. "
                    f"Only SELECT queries are permitted. "
                    f"Generated query: {sql_clean[:100]}{'...' if len(sql_clean) > 100 else ''}"
                )

        # Must start with SELECT
        if not sql_upper.startswith("SELECT"):
            raise ValueError(
                f"SQL validation failed: Query must start with 'SELECT'. "
                f"Found: '{sql_clean.split()[0] if sql_clean.split() else 'empty'}'. "
                f"Please try rephrasing your request to focus on data retrieval."
            )

        # Check for prohibited clauses/patterns
        prohibited_patterns = [
            ("WITH ", "CTE/WITH clauses"),
            ("CREATE ", "table creation"),
            ("INTO ", "INSERT INTO or SELECT INTO"),
        ]

        for pattern, description in prohibited_patterns:
            if pattern in sql_upper:
                raise ValueError(
                    f"SQL validation failed: {description} not allowed. "
                    f"Use simple SELECT statements only. "
                    f"Generated query: {sql_clean[:100]}{'...' if len(sql_clean) > 100 else ''}"
                )

        # Basic SQL injection prevention
        dangerous_chars = [";", "--", "/*", "*/"]
        for char in dangerous_chars:
            if char in sql_clean:
                if not (
                    char == ";" and sql_clean.count(";") == 1 and sql_clean.rstrip().endswith(";")
                ):
                    raise ValueError(
                        f"SQL validation failed: Unsafe character sequence '{char}' detected. "
                        f"Please try a simpler query format."
                    )

        return sql_clean

    async def _execute_sql(self, sql: str) -> list[dict[str, Any]]:
        """Execute SQL query and return results"""
        async with get_async_session() as session:
            result = await session.execute(text(sql))
            columns = result.keys()
            rows = result.fetchall()

            return [{col: row[i] for i, col in enumerate(columns)} for row in rows]


# Global service instance
llm_service = LLMService()
