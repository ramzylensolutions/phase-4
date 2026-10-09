import os
from urllib.parse import urlparse
_url = urlparse(os.environ["TEST_DATABASE_URL"])
os.environ["DB_USER"] = _url.username
os.environ["DB_PASSWROD"] = _url.password      # spelled like the field in envretrive.py
os.environ["DB_HOST"] = _url.hostname
os.environ["DB_PORT"] = str(_url.port)
os.environ["DB_NAME"] = _url.path.lstrip("/")
os.environ["TOKEN_KEY"] = "240987"
import pytest_asyncio
import pytest
import asyncpg
from migration_apply import MIGRATION,apply_migration
from httpx import ASGITransport
from app.main import app
from app.dependencies.getapool import get_a_pool
from app.envretrive import settings
import httpx



@pytest_asyncio.fixture(scope="session")
async def pool():
    url = os.environ["TEST_DATABASE_URL"]
    assert url.endswith("_test"),"running on a non test database"
    pool = await asyncpg.create_pool(url)
    await pool.execute("""drop schema public cascade; create schema public;""")
    await apply_migration(pool)
    yield pool
    await pool.close()
@pytest_asyncio.fixture(autouse=True)
async def reset(pool):
 await pool.execute("truncate deals, companies restart identity cascade")
 for name in ("0002_insert_sample_companies.sql","0004_insert_sample_deals.sql"):
    await pool.execute((MIGRATION/name).read_text(encoding="utf-8"))

@pytest_asyncio.fixture
async def client(pool):
    async def override_pool():
      async with pool.acquire() as connection:
         yield connection
    app.dependency_overrides[get_a_pool] = override_pool
    async with httpx.AsyncClient(
      transport=ASGITransport(app=app),
      base_url="http://test",
    ) as c:
       yield c
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers():
    # the same header your verify_token expects
    return {"Authorization": f"Bearer {settings.token_key}"}