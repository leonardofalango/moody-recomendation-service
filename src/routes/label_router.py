from fastapi import APIRouter, Path, Depends
from src.dependencies.db import get_db_controller
from src.types.basic_types import Label


router = APIRouter()


@router.get("/get/all")
async def get_all_labels(db_controller=Depends(get_db_controller)):
    """
    Get all labels.
    """
    return {"data": db_controller.get_all_labels()}


@router.post("/create")
async def create_label(label: Label, db_controller=Depends(get_db_controller)):
    """
    Create a new label.
    """
    db_controller.create_label(label=label)
    return {"message": "success"}


@router.get("/get/{label_id}")
async def get_label_by_id(
    label_id=Path(..., description="The ID of the label"),
    db_controller=Depends(get_db_controller),
):
    """
    Get label by ID.
    """
    return {"data": db_controller.get_label_by_id(label_id=label_id)}


@router.patch("/update/{label_id}")
async def update_label(
    label: Label,
    label_id=Path(..., description="The ID of the label"),
    db_controller=Depends(get_db_controller),
):
    """
    Update a label.
    """
    db_controller.update_label(label_id=label_id, label=label)
    return {"message": "success"}


@router.delete("/delete/{label_id}")
async def delete_label(
    label_id=Path(..., description="The ID of the label"),
    db_controller=Depends(get_db_controller),
):
    """
    Delete a label.
    """
    db_controller.delete_label(label_id=label_id)
    return {"message": "success"}
