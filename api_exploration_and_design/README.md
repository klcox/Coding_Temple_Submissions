# API Exploration and Design

## Part 1 - Exploration

Contents:
*`api_explorer.py`
*`api_documentation.md`
*`requirements.txt`

This portion of the project utilizes Python and REST API principles to explore 3 public APIS:

*JSONPlaceholder
*PokeAPI
*DummyJSON

In `api_explorer.py`, numerous requests are made across the APIs to demonstrate response status codes and headers, server responses for GET, POST, PATCH, and DELETE requests, as well as extraction of data from the responses.

### Setup & Usage

1. Clone this repo
2. Create a virtual environment (e.g. for Windows/Git Bash: `python -m venv venv`)
3. Activate the virtual environment (e.g. for Windows/Git Bash: `source venv/Scripts/activate`)
4. Install dependencies (e.g. for Windows/Git Bash: `pip install -r requirements.txt`)
5. In the terminal, run `python api_explorer.py`

Then, `api_documentation.md` describes the exploration in greater detail, including the following for each API:

*Base URL
*Authentication method (if any)
*Endpoints tested (HTTP method, URI, description, and example response shape)
*Rate limit observations
*One thing that surprised me or did not work as expected

## Part 2 - Design

For this portion of the project, `api_design.md ` presents a suggested design for a Study Tracker app. The design includes:

*Application Description
*Resources
*Relationships
*Endpoints
*Sample Request/Response Schemas
*Authentication Information
*Error Responses
*Notes for Future Consideration