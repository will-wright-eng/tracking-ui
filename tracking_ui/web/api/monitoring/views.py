from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check() -> bool:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """
    return True
