import pytest
import uuid
BAD_HEADERS =[pytest.param({},id="No Token"),
              pytest.param({"Authorization":"Bearer 244444"}),
              pytest.param({"Authorization":"240987"}),]
@pytest.mark.parametrize("domain , expected",[
    ("zylensolutions.com", "Zylen Solutions"),
    ("google.com", "Google"),
    ("zoho.com", "Zoho"),
    ("amazon.com", "Amazon"),
    ("tesla.com", "Tesla"),
]
) 
async def test_get_companyname(client,pool,auth_headers,domain,expected):
    c_id = await pool.fetchval("""select id from companies where domain = $1""",domain)
    response = await client.get(f"/company/{c_id}",headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == expected

@pytest.mark.parametrize("headers",BAD_HEADERS)
async def test_tokenkey_verify(client,pool,headers):
    c_id = await pool.fetchval("""select id from companies limit 1""")
    response = await client.get(f"/company/{c_id}",headers=headers)
    assert response.status_code == 404    

async def test_unknown_company_returns_404(client, auth_headers):
    response = await client.get(f"/company/{uuid.uuid4()}", headers=auth_headers)
    assert response.status_code == 404


async def test_invalid_id_returns_422(client, auth_headers):
    response = await client.get("/company/not-a-uuid", headers=auth_headers)
    assert response.status_code == 422

import pytest

BASE = {
    "name": "Acme Corporation",
    "domain": "acme.com",
    "industry": "Manufacturing",
    "employees": 250,
    "active": True,
    "metadata": {"region": "APAC", "tier": "gold"},
}
async def test_create_company_201(client, auth_headers):
    r = await client.post("/companies_post", json=BASE, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert "id" in data
    assert "created_at" in data