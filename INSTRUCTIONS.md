# Mission
Your goal is to build a full-stack application that allows users to build visualizations (eg: graphs, tables, charts) through natural language prompts – something that is very doable given advances in AI (e.g.: LLMs!).

 

1)    You are given the following dataset that contains details about the Top 100 SaaS Companies/Startups in 2025.

2)    A user wants to visualize and understand this data through various prompts. Here are some example prompts that the user expects visualizations for:

a. ✅   [Easy – single column operation] Create a pie chart representing industry breakdown → **Multi-colored pie chart with industry distribution**

b. ✅   [Medium – multiple column operation] Create a scatter plot of founded year and valuation → **Interactive scatter plot with correlation analysis**

c. ✅    [Hard – data manipulation] Create a table to see which investors appear most frequently → **Bar chart with JSON field parsing and frequency analysis**

d. ✅   [Extreme – data manipulation with reasoning] – Give me the best representation of data if I want to understand the correlation of ARR and Valuation → **Scatter plot with optimized scaling and correlation insights**

3) ✅   In the frontend, your application should allow a user to specify a prompt and return an appropriate visualization. The user should also be able to tweak the visualization using prompts (e.g.: "Change the color of the chart to light blue" / "Make the header row of the table bold"), and be able to add more than 1 visualization. **FULLY IMPLEMENTED** with smart modification detection, chart replacement logic, and dashboard management.

4) ✅   In the backend, your application should properly process the user query and act on the request. Your solution should be generalizable - we will test against other prompts but of a similar nature. **FULLY IMPLEMENTED** with comprehensive LLM service, SQL injection protection, and robust query generation.
  
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
  
# Phase 3 - Natural Language Visualization (Complete)
- ✅ Add a prompt input box at the top of the dashboard that calls backend LLM Service
- ✅ Create LLM Service that:
  - Uses Anthropic Claude 3.5 Sonnet API (key in .env)
  - Engineers prompts using the companies DB schema to craft SQL queries
  - Determines appropriate visualization type (chart, table, etc.) based on user request
  - Returns structured response with SQL + visualization config + styling
- ✅ Build comprehensive guardrails to protect against:
  - SQL injection and dangerous queries (only SELECT allowed)
  - Invalid SQL syntax and prohibited SQL operations
  - Bad return data from LLM with JSON validation
  - Rate limiting and comprehensive error handling
- ✅ Frontend implementation:
  - Send user prompt to backend LLM service
  - Receive visualization config and data
  - Render charts using Chart.js with react-chartjs-2
  - Handle multiple visualizations on same page with dashboard management
  - Support iterative refinement and style modifications of visualizations
- ✅ Support all visualization types:
  - Pie charts (industry breakdown) with custom colors and styling
  - Scatter plots (founded year vs valuation, ARR vs valuation)
  - Bar charts (top investors, product frequency, etc.)
  - Line charts (trends over time)
  - Data tables (fallback for complex aggregations)
- ✅ Successfully handles all example prompts:
  - "Create a pie chart representing industry breakdown" → Multi-colored pie chart
  - "Create a scatter plot of founded year and valuation" → Interactive scatter plot
  - "Show me which investors appear most frequently" → Bar chart with JSON field parsing
  - "What's the correlation between ARR and Valuation?" → Scatter plot analysis

# Phase 3.5 - Enhanced Visualization Features (Complete)
## Multiple Visualizations Dashboard
- ✅ **Dashboard Interface**: Users can create and manage multiple visualizations simultaneously
- ✅ **Additive Creation**: Each new prompt adds another visualization to the dashboard
- ✅ **Individual Management**: Remove specific visualizations or clear entire dashboard
- ✅ **Session Persistence**: Visualizations remain active throughout user session

## Natural Language Style Modification System
- ✅ **Smart Detection**: Automatic differentiation between new chart requests vs style modifications
- ✅ **Style Keywords**: Comprehensive vocabulary for detecting modification requests:
  - Color changes: "make it blue", "change color to light blue", "use pastel colors"
  - Styling: "make title bold", "use vibrant theme", "apply corporate colors"
  - Layout: "change legend position", "make it larger", "use italic text"
- ✅ **Chart Replacement Logic**: Style modifications replace the most recent visualization (no duplication)
- ✅ **Context-Aware Processing**: Modification requests include existing visualization context

## Advanced Styling & Color Management
- ✅ **Multi-Color Defaults**: Charts automatically use varied colors for visual appeal
- ✅ **Specific Color Override**: Single colors applied only when explicitly requested
- ✅ **Color Themes**: Support for pastel, vibrant, and corporate color schemes
- ✅ **Color Vocabulary**: Comprehensive mapping of color names to hex values
- ✅ **Chart.js Integration**: Professional styling with Ant Design components

## JSON Field Processing
- ✅ **SQLite JSON Functions**: Proper handling of JSON arrays (investors, products)
- ✅ **Complex Queries**: Support for json_each() operations for frequency analysis
- ✅ **Data Normalization**: Clean parsing of comma-separated and JSON data formats

## Backend API Enhancement
- ✅ **Dual Endpoints**:
  - `/api/visualizations/generate` - Create new visualizations
  - `/api/visualizations/modify` - Modify existing visualizations with context
- ✅ **Enhanced Schemas**: Extended chart configuration with styling properties
- ✅ **Context Processing**: LLM receives existing visualization data for informed modifications

## Example Interactions Implemented
**Creation Flow**:
1. "Show me industry breakdown" → Creates colorful pie chart
2. "Plot ARR vs valuation" → Creates scatter plot
3. "Which investors appear most frequently?" → Creates bar chart

**Modification Flow**:
1. "Make it blue" → Applies single blue color to most recent chart
2. "Use bold title" → Updates title styling
3. "Apply pastel theme" → Changes entire color scheme

# Phase 4 - Final Cleanup & Polish
- Remove all items endpoints, frontend logic, database schema, fastapi models and schemas
- Remove unused authentication/user related code and middleware
- Clean up unused imports and dependencies related to removed features
- Fix the "Per Page" feature in the react table
- Move G2 rating column after founded date
- Add proper error handling and logging for LLM service requests
- Add request validation and basic rate limiting for visualization endpoint
- Update API documentation to reflect only active endpoints
- Clean up unused utility functions and middleware
- Remove audit logs table and related code (not needed for this scope)
- Add loading states and better error messages in frontend
- Optimize database queries and add proper indexing
- Add basic usage analytics for generated visualizations
- Ensure all visualization types render properly with edge cases
- Add export functionality for generated visualizations (optional enhancement)
  

