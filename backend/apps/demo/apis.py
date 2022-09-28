from fastapi import APIRouter

router = APIRouter(prefix="/demo", tags=["Demo"])


@router.get("/hello")
async def hello(name: str = "") -> str:
    return f"hello {name}"
