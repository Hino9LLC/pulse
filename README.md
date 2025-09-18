# SaaS Companies Explorer

Create charts and visualizations from natural language prompts using AI. Ask questions like *"Create a pie chart of industry breakdown"* or *"Show correlation between ARR and valuation"* and get instant visualizations.

Built with FastAPI + React + Claude AI, featuring the complete Top 100 SaaS Companies 2025 dataset.

## 🚀 Quick Start (3 steps)

### 1. **Prerequisites**
- **Python 3.11+** and **Node.js 18+**
- **Anthropic API Key** - Get yours at [console.anthropic.com](https://console.anthropic.com) (Claude powers the AI visualizations)

### 2. **Setup**
```bash
git clone <this-repo>
cd pulse
make setup                    # Auto-installs dependencies + creates .env
```

### 3. **Add your API key**
Edit the `.env` file and add your Anthropic API key:
```bash
ANTHROPIC_API_KEY=your_key_here
```

### 4. **Start the app**
```bash
make dev                     # Starts both frontend + backend
```

**🎉 You're ready!** Visit:
- **App**: http://localhost:3200 
- **API docs**: http://localhost:8200/docs

## ✨ Try These Examples

Once running, try these natural language prompts:

- *"Create a pie chart representing industry breakdown"*
- *"Create a scatter plot of founded year and valuation"* 
- *"Show me which investors appear most frequently"*
- *"What's the correlation between ARR and Valuation?"*
- *"Make it light blue"* (modifies the last chart)

## 🎯 What's Included

**Core Features:**
- ✅ **AI-Powered Visualizations**: Natural language to charts/graphs via Claude API
- ✅ **Top 100 SaaS Dataset**: Complete 2025 company data (funding, ARR, valuations, etc.)
- ✅ **Multiple Chart Types**: Pie, bar, scatter, line charts + data tables
- ✅ **Interactive Modifications**: "Make it blue", "Change to bar chart", etc.
- ✅ **Multi-Visualization Dashboard**: Display multiple charts simultaneously

**Technical Stack:**
- ✅ **FastAPI Backend** with async SQLite database
- ✅ **React + TypeScript Frontend** with Ant Design
- ✅ **Modern Python Tooling**: uv, Ruff, Black, MyPy
- ✅ **One-Command Setup**: `make setup` installs everything
- ✅ **Hot Reloading**: Instant feedback during development

**No Docker, no PostgreSQL setup, no complex configuration.**

## 🛠️ Development Commands

```bash
# Main commands
make setup              # One-time setup (installs everything)
make dev               # Start both frontend + backend
make help              # Show all available commands

# Individual services  
make dev-api           # Backend only (port 8200)
make dev-dashboard     # Frontend only (port 3200)

# Code quality
make test              # Run all tests
make lint              # Check code style
make format            # Auto-format code
```

## 🗄️ Dataset

**Top 100 SaaS Companies 2025** with 110+ data points:
- **Company Info**: Name, industry, headquarters, founded year
- **Financials**: Total funding, ARR, valuation, employee count  
- **Investors**: Top investors and funding sources
- **Products**: Main products and G2 ratings

*Data automatically loaded during setup from included CSV file.*

## 🔧 Adding Dependencies

```bash
# Add Python packages
uv add package-name              # Runtime dependency
uv add --dev package-name       # Development dependency
uv sync                         # Install new deps (after git pull)

# Add frontend packages
cd apps/dashboard && npm install package-name
```

## 🚀 Architecture Highlights

**Backend (FastAPI):**
- Async SQLAlchemy with SQLite (production-ready patterns)
- Claude AI integration with SQL injection protection
- Structured logging and error handling
- Auto-generated API documentation

**Frontend (React + TypeScript):**
- Ant Design components for professional UI
- Chart.js for all visualization types  
- Smart prompt detection (new chart vs. modification)
- Responsive design for mobile/desktop

**Security Features:**
- Multi-layer SQL injection prevention
- LLM output validation and sanitization
- CORS configuration for local development

---

*Built with ❤️ for rapid AI application development*