import asyncpg
import pytest
from migration_apply import apply_migration

async def test_all_files_migrated(pool):
    rows = await pool.fetch("""select version from schema order by version""")
    assert [r["version"] for r in rows] == ["0001_create_companies.sql","0002_insert_sample_companies.sql","0003_create_deals.sql","0004_insert_sample_deals.sql"]


async def test_column_names(pool):
    async def columns(table):
        rows = await pool.fetch("select column_name from information_schema.columns where table_name = $1",table)
        return {r["column_name"] for r in rows}
    assert await columns("companies") == {
        "id", "name", "domain", "industry", "employees",
        "active", "metadata", "created_at",
    }
    assert await columns("deals") =={
        "id", "company_id", "title", "amount", "status",
        "expected_close", "metadata", "created_at",
    }


async def test_sample_data(pool):
    assert await pool.fetchval("select count(*) from companies") == 5
    assert await pool.fetchval("select count(*) from deals") == 5

async def test_duplicate_domain_rejected(pool):
    with pytest.raises(asyncpg.UniqueViolationError):
        await pool.execute(
            """insert into companies(name,domain,industry,employees,metadata)
               values ('Fake','google.com','Tech',1,'{}')"""
        )
async def test_deal_needs_existing_company(pool):
    with pytest.raises(asyncpg.ForeignKeyViolationError):
        await pool.execute(
            """insert into deals(company_id,title,amount,status)
               values (gen_random_uuid(),'Orphan',10,'won')"""
        )
async def test_running_twice_conflict(pool):
    await apply_migration(pool)
    assert await pool.fetchval("select count(*) from schema") == 4
    assert await pool.fetchval("select count(*) from companies") == 5