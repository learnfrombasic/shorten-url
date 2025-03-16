from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from app.services.shorten_url_service import shorten_url_service
from app.models.shorten_url import ShortenURL

router = APIRouter()


@router.post(
    path="/api/v1/shorten-data",
    description="""
    URL shortening: This endpoint generates a short URL from a given long URL.
    The client sends a **POST** request with the original URL as input.
    """,
    status_code=status.HTTP_201_CREATED,
    response_model=ShortenURL,
)
async def create_short_url(long_url: str):
    """
    Handles the creation of a shortened URL.
    """
    try:
        resp = await shorten_url_service.create_short_url(long_url=long_url)
        if not resp:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate short URL",
            )
        return resp
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}"
        )


@router.get(
    path="/{short_url}",
    description="""
    URL redirecting: Redirects users to the original long URL when they access a
    shortened link. The client sends a **GET** request with the short URL.
    """,
)
async def redirect_short_url(short_url: str):
    """
    Redirects a short URL to its corresponding long URL.
    """
    try:
        resp = await shorten_url_service.get_long_url(short_url=short_url)
        if not resp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found"
            )

        return RedirectResponse(url=resp.long_url, status_code=status.HTTP_302_FOUND)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}"
        )


@router.get(path="/api/v1/info", description="", status_code=status.HTTP_200_OK)
def healthcheck():
    try:
        resp = shorten_url_service.get_healthcheck()
        return resp
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}"
        )
