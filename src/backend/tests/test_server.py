import pytest
import httpx

@pytest.mark.asyncio
async def test_post_message():
    async with httpx.AsyncClient(base_url="http://localhost:3000") as client:
        response = await client.post(
            "/api/post",
            json={"username": "JohnDoe"}
        )
    
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from the POST endpoint! You sent: JohnDoe"}
