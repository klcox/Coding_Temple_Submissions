from frontend.api_calls.client import api_request


# ==============
# AUTH ENDPOINTS
# ==============


def register_user(username: str, email: str, password: str):
    """Register a new user."""

    user_data = {
        "username": username,
        "email": email,
        "password": password
    }
    
    return api_request(
        "POST",
        "/auth/register",
        json=user_data
    )   
               

def login(username: str, password: str):
    """
    Login for an existing user. 
    
    OAuth2PasswordRequestForm expects form data instead of JSON.
    """

    form_data = {
        "username": username,                
        "password": password
    }
        
    return api_request(
        "POST",
        "/auth/login",
        data=form_data
    )