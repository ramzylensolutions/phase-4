import asyncio
import asyncpg
from pathlib import Path
import os
MIGRATION = Path(__file__).parent/"migrations"
async def apply_migration(pool):
    async with pool.acquire() as conn:
        await conn.execute(
            """create table if not exists schema
            (version text not null,
            created_at timestamptz not null default current_timestamp)"""
        )
        rows = await conn.fetch("""select version from schema""")
        done = {r["version"] for r in rows}
        for file in sorted(MIGRATION.glob("*.sql")):
            if file.name in done:
                continue
            async with conn.transaction():
                await conn.execute(file.read_text(encoding="utf-8"))
                await conn.execute("""insert into schema(version)values($1)""",file.name)
async def main():
    pool = await asyncpg.create_pool(os.environ["TEST_DATABASE_URL"])
    await apply_migration(pool)
    await pool.close()
if __name__=="__main__":
    asyncio.run(main())
