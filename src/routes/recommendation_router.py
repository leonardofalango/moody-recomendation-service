from fastapi import APIRouter, Path, Query, Depends, HTTPException
from src.dependencies.model import get_recommendation_model

from src.exceptions.httpExceptions import NotFoundException

router = APIRouter()


@router.get("/{user_id}/{page}/")
async def get_recommendation_params(
    user_id: str = Path(..., description="The ID of the user"),
    page: int = Path(..., description="Page number"),
    items_per_page: int = Query(10, description="Number of items per page"),
    k_neighboors: int = Query(default=7, description="Number of neighbors to consider"),
    recommendation_model=Depends(get_recommendation_model),
):
    """
    Get recommendations for a user with specified parameters.
    """

    try:
        recommendation_model.clear_cache(user_id=user_id)

        return recommendation_model.recommend(
            user_id=user_id,
            k_neighboors=k_neighboors,
            page=page,
            items_per_page=items_per_page,
        )

    except NotFoundException as e:
        return HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        return {"message": str(e)}


@router.delete("/clear_cache/")
async def clear_cache(
    user_id: str = Query(default=None, description="User to delete from cache"),
    recommendation_model=Depends(get_recommendation_model),
):
    """
    Clear the cache.
    """
    recommendation_model.clear_cache(user_id=user_id)
    return {"message": "success"}
