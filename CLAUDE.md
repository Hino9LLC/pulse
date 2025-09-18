# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Setup & Development
```bash
make help              # Show all available commands
make setup             # Complete setup: install deps, create .env, setup React apps
make dev               # Start all services (FastAPI + React dashboard + admin)
make dev-api           # Start only FastAPI backend (http://localhost:8200)
make dev-dashboard     # Start only React dashboard (http://localhost:3200)
make dev-admin         # Start only React admin (http://localhost:3201)
```

### Database Operations
```bash
make db-migrate        # Run database migrations
make db-reset          # Reset database (DESTRUCTIVE)
```

### Code Quality & Testing
```bash
make test              # Run Python tests
make lint              # Check code style (Python + TypeScript)
make format            # Format code (Python + TypeScript)
make clean             # Clean up build artifacts and caches
```

## Architecture Overview

**SaaS Companies Explorer** is a natural language visualization platform built on the Pulse scaffolding. It showcases the Top 100 SaaS Companies 2025 dataset and enables users to create interactive charts and visualizations through conversational AI prompts using Anthropic Claude.

### Core Database Schema (3 tables)
Located in `src/pulse/database/models.py`:
- **`companies`** - SaaS companies data (name, industry, funding, valuation, etc.)
- **`items`** - Generic content/data model (kept for reference)
- **`audit_logs`** - Simple audit trail for actions

### Application Structure
```
src/pulse/
├── main.py                 # FastAPI app with lifespan management
├── settings.py             # Pydantic settings with PULSE_ prefix + Anthropic API key
├── logging.py              # Structured logging with structlog
├── database/               # SQLAlchemy async models + session management
├── routes/                 # API endpoints (health, companies, visualizations)
├── services/               # Business logic layer (companies, LLM service)
│   ├── companies.py        # Company data operations
│   └── llm.py              # Natural language to SQL + visualization generation
├── schemas/                # Pydantic request/response models
└── middleware/             # Request ID and timing middleware
```

### React Application
```
apps/
└── dashboard/              # SaaS Companies Explorer dashboard (port 3200)
    ├── src/components/
    │   ├── PromptInput.tsx         # Natural language prompt interface
    │   ├── VisualizationChart.tsx  # Chart.js visualization renderer
    │   └── ThemeSwitcher.tsx       # Theme toggle component
    └── src/utils/
        └── api.ts                  # API client with visualization endpoints
```

### Key Architectural Patterns

**Service Layer Pattern**: Business logic separated into dedicated services (`companies.py`, `llm.py`) for clean separation of concerns.

**AI-Powered Query Generation**: LLM service using Anthropic Claude to convert natural language prompts into SQL queries and visualization configurations.

**SQL Injection Prevention**: Comprehensive guardrails with keyword filtering, query validation, and parameterized execution.

**SaaS Companies Data Model**: Specialized database schema optimized for company metrics, funding data, and business intelligence.

**SQLite with Data Pre-loading**: Uses SQLite with 100 pre-loaded SaaS companies from the 2025 dataset.

**Multi-Modal Visualization**: Support for pie charts, bar charts, scatter plots, line charts, and data tables using Chart.js.

**Natural Language Interface**: Conversational prompt system with example queries and real-time visualization generation.

**Modern React Dashboard**: Professional table display with statistics cards, responsive design, and interactive visualizations.

**Structured Logging**: Request tracing with IDs, timing middleware, and JSON logging for production readiness.

### API Design
- **REST**: `/api/health`, `/api/companies/*`, `/api/visualizations/*`
- **Natural Language**: POST `/api/visualizations/generate` - Convert prompts to interactive visualizations
- **Style Modification**: POST `/api/visualizations/modify` - Modify existing visualizations with natural language
- **Data Access**: GET `/api/companies/` - Paginated company data with filtering
- **No Authentication**: Simplified for demonstration and rapid experimentation
- **Pagination**: Standard `skip`/`limit` parameters for data endpoints
- **CORS Enabled**: Frontend-backend communication on localhost ports

## Tech Stack
- **Backend**: FastAPI (Python 3.11+) with async/await throughout
- **AI/LLM**: Anthropic Claude 3.5 Sonnet for natural language processing
- **Database**: SQLite with aiosqlite driver (designed for PostgreSQL migration)
- **Package Management**: uv (modern Python package manager)
- **Testing**: pytest-asyncio with async test patterns
- **Frontend**: React 19 + TypeScript with Ant Design components
- **Visualizations**: Chart.js + react-chartjs-2 for interactive charts
- **Styling**: Tailwind CSS + Ant Design for professional UI
- **Logging**: structlog for structured JSON logging

## Development Context

This scaffolding represents **modern AI-powered data visualization** built with Python/React patterns optimized for rapid experimentation. The system prioritizes:

1. **Minimal Dependencies**: Python 3.11+, Node.js 18+, uv auto-installed
2. **One-Command Setup**: `make setup && make dev` gets everything running
3. **AI Integration**: Natural language to visualization pipeline using Anthropic Claude
4. **Production Patterns**: Proper async, SQL injection prevention, structured logging, database design
5. **Interactive Visualizations**: Real-time chart generation from conversational prompts

**Configuration**: Uses pydantic-settings with `PULSE_` prefix, `.env` file with Anthropic API key for local development.

**Database Migration Path**: SQLite for development simplicity, but all models and queries designed to work with PostgreSQL with minimal changes.

**React Integration**: Modern dashboard showcasing natural language interface with Chart.js visualizations. Ant Design + Tailwind CSS provides professional styling.

**AI-Powered Flow**: User prompt → LLM processing → SQL generation → Data visualization → Interactive chart rendering.

**Security**: Comprehensive SQL injection prevention with query validation, keyword filtering, and SELECT-only restrictions.

## Visualization Features

### Multiple Visualizations Dashboard
Users can create multiple visualizations to build comprehensive dashboards:
- **Additive Creation**: Each new prompt adds another visualization to the dashboard
- **Dashboard Management**: Clear all visualizations or remove individual charts
- **Persistent State**: Visualizations remain available throughout the session

### Natural Language Style Modification
Modify existing visualizations using conversational prompts:
- **Color Changes**: "Make it blue", "Change the color to light blue", "Use pastel colors"
- **Chart Styling**: "Make the title bold", "Use vibrant colors", "Apply corporate theme"
- **Smart Detection**: System automatically detects modification vs. new chart requests
- **Chart Replacement**: Style modifications replace the most recent chart (no duplication)

### Default Styling Behavior
- **Multi-Colored Default**: Charts use varied colors automatically for visual appeal
- **Specific Override**: Single colors only applied when explicitly requested
- **Color Themes**: Support for pastel, vibrant, and corporate color schemes
- **Professional Styling**: Chart.js integration with Ant Design components

### Supported Visualization Types
- **Pie Charts**: Industry breakdowns, market share analysis
- **Bar Charts**: Top performers, frequency analysis, comparisons
- **Scatter Plots**: Correlation analysis, trend identification
- **Line Charts**: Time series, progression tracking
- **Data Tables**: Detailed data exploration (fallback option)

### Example Prompts
**Creation**: "Show me industry breakdown", "Plot ARR vs valuation", "Which investors appear most frequently?"

**Modification**: "Make the pie chart blue", "Use bold title", "Apply pastel theme", "Change legend position"