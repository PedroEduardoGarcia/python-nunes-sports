import httpx, pytest
from httpx import Response

@pytest.mark.asyncio
async def test_post_message() -> None:
    async with httpx.AsyncClient(base_url="http://localhost:3000") as client:
        response: Response = await client.post(
            "/api/test",
            json={"username": "JohnDoe"}
        )
    # Assert that the response status code is 200 OK
    assert response.status_code == 200
    # Assert that the response JSON matches the expected output
    assert response.json() == {"message": "Hello from the POST endpoint! You sent: JohnDoe"}
