from fastapi import APIRouter, Depends, Path
from src.types.basic_types import User
from src.dependencies.db import get_db_controller

router = APIRouter()


@router.get("/get_page/{pagination}")
async def get_all_users(pagination: int = 0, db_controller=Depends(get_db_controller)):
    """
    Get all users. Pagination is set to 30 and offset is set to 0 by default.
    """
    return {"data": db_controller.get_page(quantity=30, off_set=pagination)}


@router.post("/create")
async def create_user(user: User, db_controller=Depends(get_db_controller)):
    """
    Create a new user.
    """
    db_controller.create_user(user)


@router.get("/get/{user_id}")
async def get_by_id(
    user_id: str = Path(..., description="The ID of the user"),
    db_controller=Depends(get_db_controller),
):
    """
    Get user data by ID.
    """
    return {"data": db_controller.get_user_by_id(user_id=user_id)}


@router.patch("update/{user_id}")
async def update_user(
    user: User,
    user_id: str = Path(..., description="The ID of the user"),
    db_controller=Depends(get_db_controller),
):
    """
    Update a user.
    """
    db_controller.update(user_id=user_id, data=user)


@router.delete("delete/{user_id}")
async def delete_user(
    user_id: str = Path(..., description="The ID of the user"),
    db_controller=Depends(get_db_controller),
):
    """
    Delete a user.
    """
    db_controller.delete(user_id=user_id)
