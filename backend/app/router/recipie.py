from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas import RecipeOut
from app.crud import get_all_recipes, get_recipe_by_id

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("", response_model=List[RecipeOut])
def list_recipes(limit: int = 50, offset: int = 0):
    return get_all_recipes(limit=limit, offset=offset)


@router.get("/{recipe_id}", response_model=RecipeOut)
def read_recipe(recipe_id: int):
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
