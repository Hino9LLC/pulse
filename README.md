# SaaS Companies Explorer

A natural language visualization application built on FastAPI + React, showcasing the Top 100 SaaS Companies 2025 dataset. Users will be able to create charts and visualizations through conversational prompts.

## Quick Start

1. **Clone and setup**:
   ```bash
   git clone <this-repo>
   cd pulse
   make setup
   ```

2. **Start development**:
   ```bash
   make dev
   ```

3. **Access the applications**:
   - FastAPI backend: http://localhost:8200
   - SaaS Companies Explorer: http://localhost:3200
   - API docs: http://localhost:8200/docs

## What's Included

### Current Features (Phase 1 & 2 Complete)
- ✅ **SaaS Companies Dataset**: Complete Top 100 SaaS Companies 2025 data
- ✅ **REST API**: Read-only endpoints for companies data (`/api/companies/`)
- ✅ **Modern Dashboard**: Professional table view with all company metrics
- ✅ **Statistics Overview**: Total companies, unique industries, average ratings
- ✅ **Responsive Design**: Works on desktop and mobile with Ant Design
- ✅ **Fast Backend**: Async FastAPI with SQLite database
- ✅ **Type Safety**: Full TypeScript frontend with proper type definitions

### Planned Features (Next Phase)
- 🔄 **Natural Language Queries**: "Create a pie chart of industry breakdown"
- 🔄 **Dynamic Visualizations**: Charts, graphs, tables generated from prompts
- 🔄 **Interactive Modifications**: "Change color to blue", "Make header bold"
- 🔄 **Multi-visualization Support**: Multiple charts on one dashboard
- 🔄 **Smart Data Analysis**: AI-powered insights and correlation detection

### Developer Experience
- ✅ One-command setup with grandmother-friendly Makefile
- ✅ Ultra-fast dependency management with **uv** (Rust-based)
- ✅ Modern code quality: **Ruff** (linting) + **Black** (formatting) + **MyPy** (types)
- ✅ Comprehensive testing setup with **pytest**
- ✅ Hot reloading for both backend and frontend
- ✅ VS Code/Cursor workspace settings for team consistency

## Requirements

- **Python 3.11+** (for FastAPI backend)
- **Node.js 18+** (for React apps)
- **uv** (auto-installed by Makefile)

That's it! No Docker, no PostgreSQL server, no complex setup.

## Port Strategy

Pulse uses carefully chosen ports to avoid conflicts with common development tools:
- **Backend: 8200** (avoids the very common 8000-8080 range)
- **Frontend: 3200** (avoids the crowded 3000-3010 range)

This 32xx/82xx pattern is memorable and leaves room for additional services.

## Architecture

Built on the foundation of the Pulse scaffolding, optimized for data visualization:

- **SaaS Companies Data Model** with comprehensive company metrics
- **Service layer pattern** for clean business logic separation
- **Read-only REST APIs** optimized for data consumption
- **Structured logging** for debugging and monitoring
- **SQLite database** with 100 pre-loaded companies
- **Modern React frontend** with responsive table design

## Use Cases

Perfect for:
- 📊 **Data Visualization Experimentation** with natural language interfaces
- 🤖 **AI-powered Analytics** prototyping and development
- 📈 **Business Intelligence** dashboard creation
- 🔬 **Learning** modern LLM integration patterns
- 🏗️ **Building** conversational data analysis tools

## Commands

```bash
# Setup
make setup              # Install everything and create .env
make help              # Show all available commands

# Development
make dev               # Start all services
make dev-api           # Start only FastAPI backend
make dev-dashboard     # Start only React dashboard

# Database
make db-migrate        # Run migrations
make db-reset          # Reset database (destructive)

# Code Quality
make test              # Run Python tests
make lint              # Check code style (Ruff + Black + MyPy)
make format            # Format code (Black + Ruff auto-fix)
make clean             # Clean build artifacts
```

## Code Quality Tools

Pulse uses modern, fast Python tooling:

- **🦀 Ruff**: Lightning-fast linting and import sorting (replaces flake8 + isort)
- **⚫ Black**: Uncompromising code formatting
- **🔍 MyPy**: Static type checking for better code quality
- **🧪 Pytest**: Modern testing framework with async support

All tools are pre-configured and run automatically on save in VS Code/Cursor.

### Adding Dependencies

```bash
# Add a new Python package
uv add package-name

# Add a dev dependency  
uv add --dev package-name

# After pulling changes with new dependencies
uv sync
```

## Dataset

The application includes the complete **Top 100 SaaS Companies 2025** dataset with:

- **Company Details**: Name, founding year, headquarters, industry
- **Financial Metrics**: Total funding, ARR, valuation, employee count
- **Investment Info**: Top investors and funding sources
- **Product Info**: Main products and G2 ratings
- **110+ Data Points** across diverse SaaS verticals

Data is automatically loaded during setup and served through REST APIs.

## Production Deployment

While designed for experimentation, Pulse includes production-ready patterns:

- Async SQLAlchemy with proper session management
- JWT authentication with secure practices
- Structured logging for monitoring
- Database migration system
- CORS and security middleware
- Health check endpoints

For production, consider:
- Migrating from SQLite to PostgreSQL
- Adding Redis for caching/sessions
- Setting up proper secret management
- Configuring reverse proxy (nginx)
- Adding monitoring and alerting

## Next Steps

The foundation is complete! Ready to implement natural language visualization features:

1. **LLM Integration**: Add OpenAI/Claude API for query understanding
2. **Chart Generation**: Implement Chart.js/D3.js for dynamic visualizations
3. **Query Parser**: Build system to convert natural language to data operations
4. **Interactive UI**: Add prompt input and visualization display areas

---

Built on the Pulse scaffolding with ❤️ for rapid AI application development.