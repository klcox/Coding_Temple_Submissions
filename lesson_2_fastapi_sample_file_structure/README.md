# Sample Structured Fast API

This Python project demonstrates the proper file structure for a Fast API program. In addition to placeholder files/folders, it includes the following functional files:

* `app/main.py`
* `app/config.py`
* (2) schemas - `schemas/recipe.py`, `schemas/ingredient.py`
* (2) routers - `routers/recipes.py`, `routers/ingredients.py`
* `requirements.txt`

## Setup & Usage

1. Clone this repo
2. Create a virtual environment (e.g. for Windows/Git Bash: `python -m venv venv`)
3. Activate the virtual environment (e.g. for Windows/Git Bash: `source venv/Scripts/activate`)
4. Install dependencies (e.g. for Windows/Git Bash: `pip install -r requirements.txt`)
5. In the terminal, run `uvicorn app.main:app`
6. In a browser, visit `http://127.0.0.1:8000` to access the root path
7. In the same browser, append the different URIs to the base URL to see the various responses (e.g. `/recipes`, `/recipes/1`)
8. You can also append `/docs` to the base URL in order to view the auto-generated documentation produced by Swagger. Here, you can view and test all pathways and validation.
