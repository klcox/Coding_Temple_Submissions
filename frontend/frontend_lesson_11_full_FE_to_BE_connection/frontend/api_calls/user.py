from frontend.api_calls.client import api_request


def get_profile(headers: dict):
    """Get the logged-in user's profile."""    
    
    return api_request(
        "GET",
        "/users/me",
        headers=headers        
    )

def update_profile(headers: dict, profile_updates: dict):
    """Update the logged-in user's profile (email and/or passsword)"""

    return api_request(
        "PATCH",
        "/users/me",
        headers=headers,
        json=profile_updates       
    )

def deactivate_account(headers: dict):
    """Deactivate the logged-in user's account."""

    return api_request(
        "DELETE",
        "/users/me",
        headers=headers              
    )