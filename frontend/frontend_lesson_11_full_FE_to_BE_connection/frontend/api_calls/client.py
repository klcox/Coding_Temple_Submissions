import requests


API_URL = "http://localhost:8000"


def api_request(method: str, endpoint: str, **kwargs):
    """
    Centralized client for all API requests. 
    
    Returns a dictionary containing either the successful response data or the associated error information.
    """

    try:
        response = requests.request(
            method,
            f"{API_URL}{endpoint}",
            timeout=10,
            **kwargs
        )

        response.raise_for_status()  # If the response status code is 4XX or 5XX (an error), this method raises an HTTPError

        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json()
        }

    except requests.Timeout:
        err_msg = "The request timed out. Please try again."

        return {
            "success": False,
            "status_code": None,
            "error_data": {
                "detail": err_msg
            }               
        }

    except requests.ConnectionError:
        err_msg = "Could not connect to the API. Please try again."
        
        return {
            "success": False,
            "status_code": None,
            "error_data": {
                "detail": err_msg
            } 
        }
        
    except requests.HTTPError as err:  # Includes the possible errors as outlined on the backend
        return {
            "success": False,
            "status_code": err.response.status_code,
            "error_data": err.response.json()
        }   
                   
    except requests.RequestException as err_msg:  # Catches any errors not caught above
        err_msg = f"Error: Request failed. {err_msg}"

        return {
            "success": False,
            "status_code": None,
            "error_data": {
                "detail": err_msg
            }  
        }
