# Scripts Directory

This directory contains database management and utility scripts for the Pulse project.

## Available Scripts

### `load_companies_data.py`
Loads SaaS companies data from the CSV file into the database.

**Usage:**
```bash
# From project root
python scripts/load_companies_data.py

# Or using uv
uv run python scripts/load_companies_data.py

# Or using Make
make db-load-data
```

**What it does:**
- Reads data from `top_100_saas_companies_2025.csv`
- Parses and normalizes financial data (funding, ARR, valuation)
- Creates Company records in the database
- Handles data validation and error reporting

### `rebuild_database.py`
Completely rebuilds the database from scratch using Alembic migrations.

**Usage:**
```bash
# Interactive rebuild with data loading option
python scripts/rebuild_database.py

# Or using Make
make db-rebuild
```

**What it does:**
- Removes existing database file
- Runs Alembic migrations to create fresh schema
- Optionally loads sample companies data
- Provides interactive prompts for user choices

## Development Workflow

### First-time Setup
```bash
make setup
make db-rebuild  # Creates database and loads data
```

### Regular Development
```bash
make db-migrate  # Apply new migrations
make db-load-data  # Reload data if needed
```

### Clean Rebuild
```bash
make db-rebuild  # Full interactive rebuild
```

## Dependencies

These scripts require:
- Python packages from `pyproject.toml`
- Access to the main `src/pulse` modules
- CSV data file in project root
- Alembic configuration

## Notes

- Scripts automatically adjust Python path to import from `src/pulse`
- All scripts include proper error handling and logging
- Database operations are transactional and can be safely retried

