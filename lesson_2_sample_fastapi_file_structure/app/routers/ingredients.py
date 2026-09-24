from fastapi import APIRouter, HTTPException
from app.schemas.ingredient import IngredientCreate, IngredientResponse

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

ingredients_list = [
    {
        "id": 1,
        "name": "Green Onion",
        "category": "vegetable"        
    },
    {
        "id": 2,
        "name": "Lettuce",
        "category": "vegetable"        
    },
    {
        "id": 3,
        "name": "Tortellini",
        "category": "pasta"        
    }
]

next_id: int = 4  # Initializing variable to 4 based on the list above


@router.get("/", response_model=list[IngredientResponse])
def list_ingredients():
    """GET all ingredients. Returns the ingredients as a list of dictionaries."""

    return ingredients_list

@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(ingredient_id: int):
    """GET a specific ingredient by ID. Returns the ingredient as a JSON object."""

    for ingredient in ingredients_list:
        if ingredient["id"] == ingredient_id:
            return ingredient

    raise HTTPException(status_code=404, detail="Ingredient not found.")

@router.post("/", response_model=IngredientResponse, status_code=201)
def create_ingredient(ingredient: IngredientCreate):
    """POST a new ingredient. Returns the created ingredient as a JSON object."""

    global next_id  # Refers to the variable established above
    new_ingredient = {"id": next_id, **ingredient.model_dump()}
    ingredients_list.append(new_ingredient)
    next_id += 1  # Increments the global variable for later use

    return new_ingredient