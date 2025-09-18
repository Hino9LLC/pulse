#!/usr/bin/env python3
"""
Database Rebuild Script for Pulse Companies Platform

This script completely rebuilds the companies-only database from scratch:
1. Removes existing database file
2. Clears migration history
3. Generates fresh migration from models
4. Applies migration to create database
5. Loads companies data

Usage:
    python rebuild_database.py [--keep-migrations]

Options:
    --keep-migrations    Keep existing migration files instead of generating new ones
"""

import argparse
import logging
import shutil
import subprocess
import sys
from pathlib import Path


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return whether it succeeded."""
    logger.info(f"Running: {description}")
    logger.debug(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            logger.debug(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to {description.lower()}")
        logger.error(f"Error: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error(f"Command not found: {cmd[0]}")
        logger.error("Make sure all required tools are installed and in PATH")
        return False


def remove_database_file():
    """Remove the existing database file."""
    db_file = Path("pulse.db")
    if db_file.exists():
        logger.info("Removing existing database file...")
        db_file.unlink()
        logger.info("Database file removed")
    else:
        logger.info("No existing database file found")


def clear_migrations():
    """Clear all migration files."""
    versions_dir = Path("alembic/versions")
    if versions_dir.exists():
        logger.info("Clearing migration history...")
        for file in versions_dir.glob("*.py"):
            if file.name != "__init__.py":
                file.unlink()
                logger.debug(f"Removed {file.name}")

        # Also clear __pycache__
        pycache_dir = versions_dir / "__pycache__"
        if pycache_dir.exists():
            shutil.rmtree(pycache_dir)
            logger.debug("Cleared migration __pycache__")

        logger.info("Migration history cleared")
    else:
        logger.warning("Migration versions directory not found")


def generate_migration():
    """Generate a fresh migration from current models."""
    return run_command(
        ["uv", "run", "alembic", "revision", "--autogenerate", "-m", "companies_only_schema"],
        "Generating fresh migration from models",
    )


def apply_migrations():
    """Apply migrations to create the database."""
    return run_command(
        ["uv", "run", "alembic", "upgrade", "head"], "Applying migrations to create database"
    )


def load_companies_data():
    """Load companies data from CSV."""
    data_script = Path("load_companies_data.py")
    if data_script.exists():
        return run_command(["uv", "run", "python", str(data_script)], "Loading companies data")
    else:
        logger.warning("Companies data script not found - skipping data load")
        return True


def main():
    """Main rebuild process."""
    parser = argparse.ArgumentParser(description="Rebuild Pulse companies database from scratch")
    parser.add_argument(
        "--keep-migrations",
        action="store_true",
        help="Keep existing migration files instead of generating new ones",
    )
    args = parser.parse_args()

    logger.info("=== Starting Companies Database Rebuild ===")

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        logger.error("Not in project root directory. Please run from the pulse project root.")
        return 1

    # Step 1: Remove database file
    remove_database_file()

    # Step 2: Clear migrations (unless keeping them)
    if not args.keep_migrations:
        clear_migrations()

    # Step 3: Generate migration (unless keeping existing ones)
    if not args.keep_migrations:
        if not generate_migration():
            logger.error("Failed to generate migration - aborting")
            return 1

    # Step 4: Apply migrations
    if not apply_migrations():
        logger.error("Failed to apply migrations - aborting")
        return 1

    # Step 5: Load companies data
    if not load_companies_data():
        logger.error("Failed to load companies data - continuing anyway")

    logger.info("=== Companies Database Rebuild Complete ===")
    logger.info("Your companies database has been successfully rebuilt!")

    # Show final status
    db_file = Path("pulse.db")
    if db_file.exists():
        size_mb = db_file.stat().st_size / (1024 * 1024)
        logger.info(f"Database file size: {size_mb:.2f} MB")

    return 0


if __name__ == "__main__":
    sys.exit(main())
