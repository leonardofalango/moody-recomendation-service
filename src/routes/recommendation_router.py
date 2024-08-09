from fastapi import APIRouter, Path, Query, Depends
from src.dependencies.model import get_recommendation_model

router = APIRouter()


@router.get("/{user_id}")
async def get_recommendation_params(
    user_id: str = Path(..., description="The ID of the user"),
    n_recommendations: int = Query(default=10, description="Number of recommendations"),
    k_neighboors: int = Query(default=7, description="Number of neighbors to consider"),
    recommendation_model=Depends(get_recommendation_model),
):
    """
    Get recommendations for a user with specified parameters.
    """
    return recommendation_model.recommend(
        user_id=user_id, n_recommendations=n_recommendations, k_neighboors=k_neighboors
    )


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
