# Run with: uvicorn app.main:app --reload
# Docs at:  http://127.0.0.1:8000/docs

from fastapi import FastAPI
from textwrap import dedent
from app.routers import items


openapi_tags = [
    {
        "name": "Items", 
        "description": "Create, search for, and delete inventory items"
    }
]


app = FastAPI(
    title = "Sample Inventory API",
    description = dedent(""" 
        A sample inventory application utilizing FastAPI. 

        ## Features
        - Review existing items, with optional filtering by price and/or category
        - Search for a specific item by ID
        - Create a new item
        - Delete a specific item by ID
    """),
    version = "1.0.0",
    openapi_tags = openapi_tags,
    contact = {
        "name": "Example Name", 
        "email": "example_email@test.com"
    },
    license_info = {
        "name": "MIT License",
        "url": "https://opensource.org/license/mit/"
    }
)


app.include_router(
    items.router,
    prefix = "/items",
    tags = ["Items"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)