# Mission
Your goal is to build a full-stack application that allows users to build visualizations (eg: graphs, tables, charts) through natural language prompts – something that is very doable given advances in AI (e.g.: LLMs!).

 

1)    You are given the following dataset that contains details about the Top 100 SaaS Companies/Startups in 2025.

2)    A user wants to visualize and understand this data through various prompts. Here are some example prompts that the user expects visualizations for:

a.    [Easy – single column operation] Create a pie chart representing industry breakdown

b.    [Medium – multiple column operation] Create a scatter plot of founded year and valuation

c.     [Hard – data manipulation] Create a table to see which investors appear most frequently

d.    [Extreme – data manipulation with reasoning] – Give me the best representation of data if I want to understand the correlation of ARR and Valuation

3)    In the frontend, your application should allow a user to specify a prompt and return an appropriate visualization. The user should also be able to tweak the visualization using prompts (e.g.: “Change the color of the chart to light blue” / “Make the header row of the table bold”), and be able to add more than 1 visualization.

4)    In the backend, your application should properly process the user query and act on the request. Your solution should be generalizable - we will test against other prompts but of a similar nature.
  
# Phase 1 (Complete)
- Convert this scaffolding into a Top 100 SaaS Companies/Startups 2025 explorer app
- Use the data set top_100_saas_companies_2025.csv as a guide
- We will only need 1 react app. Keep the dashboard. Remove the admin
- We will not need websockets. Remove from the front and backends
- We will not need users, user tables or user auth. Remove from the front and backends
- Leave the items table for now so that we can reference that as a guid
- Remove any other unnecessary feature that are not in the scope of this project.
- The mission is the entire scope of the project. Don't plan for future enhancements or consider scaling
- Continue to use the overall structure we have laid out including all the tooling

# Phase 2 (Complete)
- Create a single table in sqllite with supporting sqlalchemy classes
- create rest endpoints for the table. we only need read type endpoints
- have the frontend read the the companies endpoint and display all fields/values in a table in place of items
  
# Phase 3 - Natural Language Visualization
- Add a prompt input box at the top of the dashboard that calls backend LLM Service
- Create LLM Service that:
  - Uses Anthropic Claude API (key in .env)
  - Engineers prompts using the companies DB schema to craft SQL queries
  - Determines appropriate visualization type (chart, table, etc.) based on user request
  - Returns structured response with SQL + visualization config
- Build guardrails to protect against:
  - SQL injection and dangerous queries (only SELECT allowed)
  - Invalid SQL syntax
  - Bad return data from LLM
  - Rate limiting and error handling
- Frontend should:
  - Send user prompt to backend LLM service
  - Receive visualization config and data
  - Render appropriate chart/table using Chart.js or similar
  - Handle multiple visualizations on same page
  - Allow iterative refinement of visualizations
- Support visualization types:
  - Pie charts (industry breakdown)
  - Scatter plots (founded year vs valuation)
  - Bar charts (top investors, etc.)
  - Tables (custom data aggregations)
  - Line charts (trends over time)
- Example prompts to handle:
  - "Create a pie chart representing industry breakdown"
  - "Create a scatter plot of founded year and valuation"
  - "Show me which investors appear most frequently"
  - "What's the correlation between ARR and Valuation?"
  

