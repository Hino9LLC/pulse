# Companies Database Guide

This is a **companies-only** database platform. All items and audit functionality has been removed.

## Database Schema

Your database contains only:

- **`companies`** - SaaS companies data (100 companies)
- **`alembic_version`** - Migration version tracking

## Quick Rebuild

```bash
python rebuild_database.py
```

This will:
1. ✅ Remove existing database
2. ✅ Clear migration history
3. ✅ Generate fresh companies-only migration
4. ✅ Create clean database
5. ✅ Load 100 companies data

## API Endpoints

Your FastAPI application supports:

- `GET /api/health` - Health check
- `GET /api/companies` - List companies with filters
- `GET /api/companies/{id}` - Get specific company
- `GET /api/visualizations` - Create data visualizations

## Verification

```bash
# Check tables
sqlite3 pulse.db ".tables"

# Check company count  
sqlite3 pulse.db "SELECT COUNT(*) FROM companies;"

# View sample data
sqlite3 pulse.db "SELECT company_name, industry FROM companies LIMIT 5;"
```

## Clean Architecture

- ❌ **Removed**: Items model, routes, services, schemas
- ❌ **Removed**: AuditLog model and functionality  
- ❌ **Removed**: Users and WebSocket schemas
- ✅ **Focused**: Pure companies data platform
