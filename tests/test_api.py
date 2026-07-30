import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.text == "ok"


@pytest.mark.asyncio
async def test_list_services(client: AsyncClient) -> None:
    response = await client.get("/api/v1/services")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4
    assert data[0]["slug"] == "development"


@pytest.mark.asyncio
async def test_list_team(client: AsyncClient) -> None:
    response = await client.get("/api/v1/team")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5


@pytest.mark.asyncio
async def test_contact_form_submission(client: AsyncClient) -> None:
    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "subject": "Inquiry about solutions",
        "message": "Hello, I would like to learn more about your services.",
    }
    response = await client.post("/api/v1/contact-messages", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane.doe@example.com"


@pytest.mark.asyncio
async def test_contact_form_honeypot(client: AsyncClient) -> None:
    payload = {
        "name": "Spam Bot",
        "email": "bot@spam.com",
        "subject": "Buy cheap stuff",
        "message": "Buy cheap stuff now at http://spam.com",
        "company_website": "http://spam.com",
    }
    response = await client.post("/api/v1/contact-messages", json=payload)
    assert response.status_code == 201
    # Honeypot returns synthetic response without throwing errors
