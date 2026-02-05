from typing import List, Optional
from app.db import get_connection


def get_all_recipes(limit: int = 50, offset: int = 0) -> List[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, title, diet_tags, prep_minutes, cook_minutes, ingredients, instructions
            FROM recipes
            ORDER BY id ASC
            LIMIT ? OFFSET ?;
            """,
            (limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]


def get_recipe_by_id(recipe_id: int) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, title, diet_tags, prep_minutes, cook_minutes, ingredients, instructions
            FROM recipes
            WHERE id = ?;
            """,
            (recipe_id,),
        ).fetchone()

        return dict(row) if row else None
