from fastapi import FastAPI
from pydantic import BaseModel

# Establish API
app = FastAPI()


# GET Endpoints

@app.get("/")
def read_root():
    """Root path. Returns a JSON object with a message welcoming the user to the API."""

    return {"message": "Welcome to my first API!"}

@app.get("/about")
def about_me():
    """Returns a JSON object with information about me, the API creator."""

    return {
        "name": "Kelly Cox",
        "current_module": "Module 5 - FAST API",
        "fun_fact": "I like to study foreign languages."
    }

@app.get("/greet/{name}")
def greet_user(name: str):
    """Returns a JSON object with a message customized to the name included in the URI."""

    return {"message": f"Hello, {name}!"}


# POST Endpoints
 
class Message(BaseModel):
    message: str  # Required
    shout: bool = False  # Optional, default value is False
    
@app.post("/echo")
def echo_message(message: Message):
    """Returns a JSON object with the 'message' from the POST request. If 'shout' in the request is True, the 'message' in the JSON object is converted to upper-case."""

    if message.shout:  
        return {"message": message.message.upper()}

    return {"message": message.message}