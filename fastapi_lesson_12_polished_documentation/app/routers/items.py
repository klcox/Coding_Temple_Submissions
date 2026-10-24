from fastapi import APIRouter, HTTPException, Query
from app.schemas.item import ItemCreate, ItemResponse
from typing import Optional


router = APIRouter()


items: list[dict] = [  # Using an in-memory list to simulate a database
    {
        "id": 1,
        "name": "Charging Cable",
        "description": "For Android phones, supports USB and USB-C",
        "price": 12.99,
        "category": "accessories"     
    },
    {
        "id": 2,  # Description is absent as it is an optional field
        "name": "Lenovo Laptop",        
        "price": 320.99,
        "category": "electronics"     
    }
]

next_id = 3
 

@router.get(
    "/", 
    response_model = list[ItemResponse], 
    responses = {  
        200: {"description": "OK - List returned successfully"},      
        400: {"description": "Bad Request - Query parameter error (min_price cannot be greater than max_price)"},
        422: {"description": "Validation Error - Invalid query parameter"}
    },
    summary = "Gets a list of all items"
)
def list_items(
    min_price: float = Query(default=1.00, gt=0, description="Filter by price, min_price must be greater than 0"),
    max_price: float = Query(default=99999.99, gt=0, description="Filter by price, max_price must be greater than 0"),
    category: Optional[str] = Query(default=None, min_length=1, max_length=50, description="Filter by category, must be between 1 and 50 characters")
):
    """
    Gets a list of all items in the database.        

    Includes options for filtering:
    - Filter by item price: min_price only, max_price only, or both (values must be greater than zero) (e.g. '?min_price=100')
    - Filter by item category (must be between 1 and 50 characters) (e.g. '?category=electronics)   
   
    Defaults:
    - min_price defaults to $1
    - max_price defaults to $99999.99
    - category defaults to None   
    
    Returns: 
    A list of item objects, ordered by ID. (Future features will include sorting and pagination.)

    Standard Response: 
    200 - OK (successfully located and returned the list)

    Possible Errors:
    - 400 - Bad Request (min_price cannot be greater than max_price)
    - 422 - Validation Error (one or more of the validation requirements has been violated)
    """

    results = items.copy()

    if min_price > max_price:  # Ensure min_price is not greater than max_price
        raise HTTPException(status_code=400, detail="min_price cannot be greater than max_price")

    results = [item for item in results if min_price <= item["price"] <= max_price]  # Select only the items that fall between the min_ and max_price (either defaults or user-supplied query parameters)

    if category:  # If the user supplied the category as a query parameter, select only the items that match this category       
        results = [item for item in results if item["category"] == category]
    
    return results


@router.post(
    "/",
    response_model = ItemResponse,
    status_code = 201,
    responses = {
        201: {"description": "Created - Item created successfully"},
        409: {"description": "Conflict - An item with this name already exists"},
        422: {"description": "Validation Error - Check request body"}
    },
    summary = "Create a new item"    
)
def create_item(item: ItemCreate):
    """
    Creates a new item and adds it to the database.

    The request body should contain:
    - **name**: (Required) The item name (string, must be unique, must be between 1-100 characters)
    - **description**: (Optional) A description of the item (string, max length of 500 characters)
    - **price**: (Required) The price of the item in USD (float, must be greater than 0)
    - **category**: (Required) The item category (string, must be between 1-50 characters)    

    Returns:
    The newly-created item object, now inclusive of the server-generated ID.

    Standard Response: 
    201 - Created (successfully created the item)

    Possible Errors:
    - 409 - Conflict (the item 'name' is not unique)
    - 422 - Validation Error (one or more of the validation requirements has been violated)
    """

    global next_id

    for existing_item in items:
        if existing_item["name"].lower() == item.name.lower():
            raise HTTPException(status_code=409, detail=f"An item with the name '{item.name}' already exists.")
    
    new_item = {"id": next_id, **item.model_dump()}
    items.append(new_item)

    next_id += 1

    return new_item


@router.get(
    "/{item_id}",
    response_model = ItemResponse,
    responses = {
        200: {"description": "OK - Item located successfully"},        
        404: {"description": "Not Found"},
        422: {"description": "Validation Error - The item_id provided is not an integer"}     
    },
    summary = "Get a specific item by ID"   
)
def get_item(item_id: int):
    """
    Get a specific item by ID.

    Locates the item in the database using the item_id provided or raises a 404 error if the item is not found.        

    Returns:
    The requested item object.

    Standard Response: 
    200 - OK (successfully located and returned the item)

    Possible Errors:
    - 404 - Not Found (the item with the provided item_id was not found)
    - 422 - Validation Error (the item_id provided is not an integer)
    """

    for item in items:
        if item["id"] == item_id:
            return item
    
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    

@router.delete(
    "/{item_id}",    
    responses = {
        200: {"description": "OK - Item deleted successfully"},       
        404: {"description": "Not Found"},
        422: {"description": "Validation Error - The item_id provided is not an integer"}     
    },
    summary = "Delete a specific item by ID"   
)
def delete_item(item_id: int):
    """
    Delete a specific item by ID.

    Locates the item in the database using the item_id provided.
    
    If the item is found: the item is deleted from the database.
    
    If the item is not found: raises a 404 error.    

    Returns:
    A message indicating the item was successfully deleted.

    Standard Response: 
    200 - OK (successfully located and deleted the item)   

    Possible Errors:
    - 404 - Not Found (the item with the provided item_id was not found)
    - 422 - Validation Error (the item_id provided is not an integer) 
    """

    for item in items:
        if item["id"] == item_id:
            items.remove(item)

            return {"message": f"Item {item_id} deleted successfully."}       
    
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")    