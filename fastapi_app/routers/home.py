from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(
    tags=['Home']
)


@router.get(path="/")   # TEMP временная заглушка-редирект на доки
async def homepage():
    # return {"url": "http://127.0.0.1:8000/docs"}
    return RedirectResponse("http://127.0.0.1:8000/docs")