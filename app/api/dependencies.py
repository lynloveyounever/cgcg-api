from app.services.deadline_service import DeadlineService

def get_deadline_service() -> DeadlineService:
    """
    Dependency function that returns an instance of DeadlineService.
    """
    return DeadlineService()