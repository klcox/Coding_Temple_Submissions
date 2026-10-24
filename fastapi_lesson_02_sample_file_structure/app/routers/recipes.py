from fastapi import APIRouter, HTTPException
from app.schemas.recipe import RecipeCreate, RecipeResponse

router = APIRouter(prefix="/recipes", tags=["Recipes"])  # Prefix prepends "/recipes" to all paths below; tags group paths together for documentation

recipes_list = [
    {
        "id": 1,
        "title": "Thai Turkey Lettuce Wraps",
        "cuisine": "Thai",
        "prep_time_minutes": 15,
        "servings": 6
    },
    {
        "id": 2,
        "title": "Burger Bowls",
        "cuisine": "American",
        "prep_time_minutes": 5,
        "servings": 4
    },
    {
        "id": 3,
        "title": "Tortellini Alfredo",
        "cuisine": "Italian",
        "prep_time_minutes": 5,
        "servings": 6
    }
]

next_id: int = 4  # Initializing variable to 4 based on the list above


@router.get("/", response_model=list[RecipeResponse])
def list_recipes():
    """GET all recipes. Returns the recipes as a list of dictionaries."""

    return recipes_list

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int):
    """GET a specific recipe by ID. Returns the recipe as a JSON object."""
 
    for recipe in recipes_list:
        if recipe["id"] == recipe_id:
            return recipe

    raise HTTPException(status_code=404, detail="Recipe not found.")

@router.post("/", response_model=RecipeResponse, status_code=201)
def create_recipe(recipe: RecipeCreate):
    """POST a new recipe. Returns the created recipe as a JSON object."""

    global next_id  # Refers to the variable established above
    new_recipe = {"id": next_id, **recipe.model_dump()}
    recipes_list.append(new_recipe)
    next_id += 1  # Increments the global variable for later use

    return new_recipe