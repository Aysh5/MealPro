import json
from pathlib import Path

from app.db import init_db, get_connection

JSON_PATH = Path(__file__).resolve().parent / "raw" / "recipes.json"


def parse_minutes(value):
    """
    Convert strings like '10 mins', '1 hr', 'No Time' into an integer minutes or None.
    """
    if not value:
        return None
    s = str(value).lower().strip()
    if "no time" in s:
        return None

    total = 0
    # handles "X hr" and "Y min"
    parts = s.replace("hours", "hr").replace("hour", "hr").replace("mins", "min").split()
    for i, token in enumerate(parts):
        if token.isdigit() and i + 1 < len(parts):
            unit = parts[i + 1]
            n = int(token)
            if unit.startswith("hr"):
                total += n * 60
            elif unit.startswith("min"):
                total += n
    return total if total > 0 else None


def main():
    if not JSON_PATH.exists():
        raise FileNotFoundError(f"JSON not found at: {JSON_PATH}")

    init_db()

    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    
    recipes = data if isinstance(data, list) else data.get("recipes", [])
    if not recipes:
        print(" No recipes found in JSON (unexpected format).")
        return

    inserted = 0

    with get_connection() as conn:
        for r in recipes:
            title = (r.get("name") or "").strip()
            if not title:
                continue

            
            diet_tags = (r.get("diet_tags") or r.get("diet") or "").strip()

            times = r.get("times") or {}
            prep_minutes = parse_minutes(times.get("Preparation"))
            cook_minutes = parse_minutes(times.get("Cooking"))

            # ingredients/steps are lists -> store as JSON strings in SQLite
            ingredients = json.dumps(r.get("ingredients", []), ensure_ascii=False)
            instructions = json.dumps(r.get("steps", []), ensure_ascii=False)

            conn.execute(
                """
                INSERT INTO recipes (title, diet_tags, prep_minutes, cook_minutes, ingredients, instructions)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (title, diet_tags, prep_minutes, cook_minutes, ingredients, instructions),
            )
            inserted += 1

        conn.commit()

    print(f"✅ Imported {inserted} recipes into mealpro.db")


if __name__ == "__main__":
    main()
