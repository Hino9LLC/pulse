#!/usr/bin/env python3
"""
Script to load SaaS companies data from CSV into the database
"""

import asyncio
import csv
import sys
from pathlib import Path


# Add src to path to import pulse modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pulse.database.models import Company
from pulse.database.session import close_database, get_async_session, init_database
from pulse.utils.data_normalization import parse_currency_to_float, parse_employee_count


async def load_companies_data():
    """Load companies data from CSV file into database"""

    csv_file = Path("top_100_saas_companies_2025.csv")
    if not csv_file.exists():
        print(f"❌ CSV file not found: {csv_file}")
        return False

    # Initialize database
    await init_database()

    companies_loaded = 0

    async with get_async_session() as session:
        try:
            # Read CSV data
            with open(csv_file, encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Create company instance with normalized values
                    company = Company(
                        company_name=row["Company Name"],
                        founded_year=int(row["Founded Year"]),
                        headquarters=row["HQ"],
                        industry=row["Industry"],
                        total_funding_usd=parse_currency_to_float(row["Total Funding"]),
                        arr_usd=parse_currency_to_float(row["ARR"]),
                        valuation_usd=parse_currency_to_float(row["Valuation"]),
                        employee_count=parse_employee_count(row["Employees"]),
                        top_investors=row["Top Investors"],
                        product=row["Product"],
                        g2_rating=float(row["G2 Rating"]),
                    )

                    session.add(company)
                    companies_loaded += 1

                # Commit all companies
                await session.commit()
                print(f"✅ Successfully loaded {companies_loaded} companies into database")

        except Exception as e:
            await session.rollback()
            print(f"❌ Error loading companies data: {e}")
            return False

        finally:
            await close_database()

    return True


if __name__ == "__main__":
    print("📊 Loading SaaS companies data into database...")
    success = asyncio.run(load_companies_data())

    if success:
        print("🎉 Data loading complete!")
    else:
        print("💥 Data loading failed!")
        sys.exit(1)
