from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from src.services.shorten_url_service import shorten_url_serivce

router = APIRouter()


@router.post(
    path="/data/shorten",
    description="""
URL shortening. To create a new short URL, a client sends a POST request, which contains
one parameter: the original long URL
""",
    status_code=201,
)
async def create_short_url(req: object):
    resp = shorten_url_serivce.create_short_url(req=req)
    if not resp:
        raise HTTPException(...)
    return resp


@router.get(
    path="/shortUrl/{id}",
    description="""
URL redirecting. To redirect a short URL to the corresponding long URL, a client sends a
GET request.
""",
    status_code=301,
)
async def redirect_short_url(id: str):
    resp = shorten_url_serivce.redirect_short_url(id=id)
    if not resp:
        raise HTTPException(...)
    return RedirectResponse(url=resp.get("long_url"))
