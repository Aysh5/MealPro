from pydantic import BaseModel
from typing import Optional


class RecipeOut(BaseModel):
    id: int
    title: str
    diet_tags: Optional[str] = None
    prep_minutes: Optional[int] = None
    cook_minutes: Optional[int] = None
    ingredients: Optional[str] = None
    instructions: Optional[str] = None
