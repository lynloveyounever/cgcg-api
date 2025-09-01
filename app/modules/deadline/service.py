# Business logic for Deadline interactions
import httpx
from ...core.config import settings
from . import schemas

class DeadlineService:
    async def get_jobs(self) -> list[schemas.DeadlineJob]:
        """Fetches job data from the Deadline web service."""
        # This is a mock implementation. In a real scenario, you would query the actual API.
        # For example: 
        # async with httpx.AsyncClient() as client:
        #     try:
        #         response = await client.get(f"{settings.DEADLINE_WEBSERVICE_URL}/api/jobs")
        #         response.raise_for_status()
        #         # Assuming the API returns a list of jobs in the expected format
        #         return [schemas.DeadlineJob(**job) for job in response.json()]
        #     except httpx.HTTPStatusError as e:
        #         # Handle HTTP errors (e.g., 404, 500)
        #         print(f"HTTP error occurred: {e}")
        #         return []
        #     except Exception as e:
        #         # Handle other errors (e.g., connection error)
        #         print(f"An error occurred: {e}")
        #         return []

        # Returning mock data for demonstration
        return [
            schemas.DeadlineJob(id="job-001", name="Scene_01_Render", status="Completed", user="lynloveyounever"),
            schemas.DeadlineJob(id="job-002", name="Scene_02_Render", status="Rendering", user="lynloveyounever"),
        ]

deadline_service = DeadlineService()
