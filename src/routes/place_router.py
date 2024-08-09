from fastapi import APIRouter, Path, Depends
from src.dependencies.db import get_db_controller
from src.types.basic_types import Place, Interaction

router = APIRouter()


@router.post("/interact/")
async def interact(interaction: Interaction, db_controller=Depends(get_db_controller)):
    """
    Rate a place.
    """
    db_controller.interact(interaction)
    return {"message": "success"}


@router.post("/like/{user_id}/{place_id}")
async def like_place(
    place_id: str = Path(..., description="The ID of the place"),
    user_id: str = Path(..., description="The ID of the user"),
    db_controller=Depends(get_db_controller),
):
    """
    Like a place.
    """
    db_controller.like_place(place_id=place_id)
    like_interaction = Interaction(user_id=user_id, place_id=place_id, interactions=1)
    db_controller.interact(like_interaction)
    return {"message": "success"}


@router.get("/get/all")
def get_all_places(db_controller=Depends(get_db_controller)):
    """
    Get all places.
    """
    return {"data": db_controller.get_all_places()}


@router.post("/create")
async def create_place(place: Place, db_controller=Depends(get_db_controller)):
    """
    Create a new place.
    """
    db_controller.create_place(place)
    return {"message": "success"}


@router.get("/get/{place_id}")
def get_place_by_id(
    place_id=Path(..., description="The ID of the place"),
    db_controller=Depends(get_db_controller),
):
    """
    Get place by ID.
    """
    return {"data": db_controller.get_place_by_id(place_id=place_id)}


@router.patch("/update/{place_id}")
async def update_place(
    place: Place,
    place_id=Path(..., description="The ID of the place"),
    db_controller=Depends(get_db_controller),
):
    """
    Update a place.
    """
    db_controller.update_place(place_id=place_id, place=place)
    return {"message": "success"}


@router.delete("/delete/{place_id}")
async def delete_place(
    place_id=Path(..., description="The ID of the place"),
    db_controller=Depends(get_db_controller),
):
    """
    Delete a place.
    """
    db_controller.delete_place(place_id=place_id)
    return {"message": "success"}
