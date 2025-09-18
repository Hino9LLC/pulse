#!/usr/bin/env python3
"""
Script to rebuild the database from scratch using Alembic migrations
"""

import asyncio
import subprocess
import sys
from pathlib import Path


# Add the parent directory to Python path so we can import from src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.pulse.database.session import close_database


def run_alembic_command(command: list[str]) -> bool:
    """Run an Alembic command and return success status"""
    try:
        print(f"🔧 Running: {' '.join(command)}")
        result = subprocess.run(
            command, cwd=project_root, capture_output=True, text=True, check=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {' '.join(command)}")
        print(f"Error: {e.stderr}")
        return False


async def rebuild_database():
    """Rebuild the database from scratch"""
    print("🗑️  Rebuilding database from scratch...")

    # Remove existing database file if it exists
    db_file = project_root / "pulse.db"
    if db_file.exists():
        print(f"🗑️  Removing existing database: {db_file}")
        db_file.unlink()

    # Run Alembic upgrade to create fresh database
    if not run_alembic_command(["alembic", "upgrade", "head"]):
        return False

    print("✅ Database rebuilt successfully!")
    return True


async def load_sample_data():
    """Load sample data after rebuilding"""
    from scripts.load_companies_data import load_companies_data

    print("📊 Loading sample companies data...")
    return await load_companies_data()


async def main():
    """Main function to rebuild database and optionally load data"""
    try:
        # Rebuild database
        if not await rebuild_database():
            print("💥 Database rebuild failed!")
            return False

        # Ask user if they want to load sample data
        load_data = input("📊 Load sample companies data? (y/N): ").strip().lower()
        if load_data in ["y", "yes"]:
            if await load_sample_data():
                print("🎉 Database rebuild and data loading completed!")
            else:
                print("⚠️  Database rebuilt but data loading failed")
                return False
        else:
            print("✅ Database rebuilt successfully (no data loaded)")

        return True

    except Exception as e:
        print(f"💥 Error during database rebuild: {e}")
        return False
    finally:
        await close_database()


if __name__ == "__main__":
    print("🚀 Starting database rebuild...")
    success = asyncio.run(main())

    if not success:
        sys.exit(1)
