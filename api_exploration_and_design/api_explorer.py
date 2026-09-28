"""
Module 4 Project — Part 1: API Exploration
Explore 3 public APIs and document what you find.
"""

import requests


BASE_URLS = {
    "jsonplaceholder": "https://jsonplaceholder.typicode.com",
    "pokeapi": "https://pokeapi.co/api/v2",
    "dummyjson": "https://dummyjson.com"
}


def print_response_overview(uri, response):
    """Helper function for the exploration functions below. Takes a URI and request response; prints the HTTP method, URI, status code and reason, as well as key response headers."""

    print(f"\n{'-' * 19} New Request, Response Information: {'-' * 19}")
    print(f"{'HTTP Method':<15} | {'URI':<15} | {'Status Code':<15} | {'Status Reason':<20.20}")  # Status Reason utilizes a greater width to account for the varying widths of different status reasons
    print(f"{'-' * 74}")
    print(f"{response.request.method:<15} | {uri:<15} | {response.status_code:<15} | {response.reason:<20.20}")
    print(f"{'-' * 74}")

    print(f"\n{'Header':<21} | {'Value':<32.32}")
    print(f"{'-' * 55}")

    headers = [         
        "Content-Type",
        "Content-Length",
        "X-Ratelimit-Limit",
        "X-Ratelimit-Remaining",
        "X-Ratelimit-Reset"
    ]

    if response.headers:
        for header in headers:
            if header in response.headers:
                print(f"{header:<21} | {response.headers.get(header):<32.32}")
    else:
        print("Headers could not be retrieved.")    
    

# ============================================================
# API 1: JSONPlaceholder
# Documentation: https://jsonplaceholder.typicode.com/guide/
# ============================================================


def explore_jsonplaceholder():
    """Explores JSONPlaceholder API utilizing various requests."""

    print("\n=== API 1: JSONPlaceholder ===")

    # Request 1 - GET all users

    uri_1 = "/users"
    
    try:
        response_1 = requests.get(BASE_URLS["jsonplaceholder"] + uri_1, timeout=10)  # Timeout quits the request within the time limit (here, 10 seconds) if the server does not respond to the request; prevents the request attempt from running indefinitely        

        print_response_overview(uri_1, response_1)

        response_1.raise_for_status()  # If the response status code is 4XX or 5XX (an error), this method raises an HTTPError

    except requests.RequestException as err_msg:
        print(f"\nRequest failed: {err_msg}")     
       
    else:  # The else block only runs if no exception occurred
        users = response_1.json()  # .json() converts the response JSON to a Python object

        print(f"\n{'-' * 13} GET All Users, Results: {'-' * 14}")
        print(f"{'Name':<24} | {'Email Address':<25.25}")
        print(f"{'-' * 52}")
        for user in users:
            print(f"{user['name']:<24} | {user['email']:<25.25}")
        print(f"{'-' * 52}")
        

    # Request 2 - GET posts by a specific user (User 2)
    
    uri_2 = "/posts?userId=2"  # Query parameter ?userId=2 is used to filter the posts collection resource - User 2's posts

    try:
        response_2 = requests.get(BASE_URLS["jsonplaceholder"] + uri_2, timeout=10)

        print_response_overview(uri_2, response_2)

        response_2.raise_for_status()

    except requests.RequestException as err_msg:
        print(f"\nRequest failed: {err_msg}")
        
    else:   
        posts = response_2.json()

        print(f"\n{'-' * 10} GET Posts by a Specific User, Results: {'-' * 9}")
        print(f"User 2 has {len(posts)} posts. Find a sample below:\n")
        print(f"{'Post ID':<7} | {'Post Title':<23.23} | {'Post Body':<23.23}")
        print(f"{'-' * 59}")
        for post in posts[:3]:  # Showing only the first 3 posts for readability
            print(f"{post['id']:<7} | {post['title'][:20]}... | {post['body'][:20]}...")
        print(f"{'-' * 59}")


    # Request 3 - POST a new post
    
    uri_3 = "/posts"

    post_data = {
        "title": "Test Title",
        "body": "Test Body",
        "userId": 1
    }

    try:
        response_3 = requests.post(BASE_URLS["jsonplaceholder"] + uri_3, json=post_data, timeout=10)  # json=post_data converts the Python dictionary to JSON for interpretation by the server

        print_response_overview(uri_3, response_3)

        response_3.raise_for_status()

    except requests.RequestException as err_msg:
        print(f"\nRequest failed: {err_msg}")
        
    else:   
        created_post = response_3.json()

        print(f"\n{'-' * 4} POST a new post, Results: {'-' * 3}")
        print(f"New post confirmed:\n")  # If otherwise unsuccessful, the except block above would catch any errors and prevent these print statements from running        
        print(f"{'Post ID':<7} | {'Post Title':<12.12} | {'Post Body':<12.12}")
        print(f"{'-' * 34}")
        print(f"{created_post['id']:<7} | {created_post['title']:<12.12} | {created_post['body']:<12.12}")
        print(f"{'-' * 34}")
        print("**Note: This creation will not persist on the server! It is for demo only.") 
        print(f"{'-' * 74}")


    # Request 4 - GET to-dos for a specific user (User 1)
      
    uri_4 = "/users/1/todos"  # This URI refers to a nested resource - User 1's to-dos

    try:
        response_4 = requests.get(BASE_URLS["jsonplaceholder"] + uri_4, timeout=10)

        print_response_overview(uri_4, response_4)

        response_4.raise_for_status()

    except requests.RequestException as err_msg:
        print(f"\nRequest failed: {err_msg}")
        
    else:   
        to_dos = response_4.json()

        print(f"\n{'-' * 2} GET To-Dos for a Specific User, Results: {'-' * 2}")
        print(f"User 1 has {len(to_dos)} to-dos. Find a sample below:\n")
        print(f"{'To-Do ID':<8} | {'Title':<23.23} | {'Completed':<10}")
        print(f"{'-' * 46}")
        for to_do in to_dos[:4]:  # Showing only the first 4 to-dos for readability
            to_do_title = to_do['title'] if len(to_do['title']) < 20 else to_do['title'][:20] + "..."

            status = "Yes" if to_do["completed"] else "No"
            print(f"{to_do['id']:<8} | {to_do_title:<23} | {status:<10}")
        print(f"{'-' * 46}")


    # Request 5 - Test error handling by utilizing a nonexistent URI    
                          
    uri_5 = "/users/posts"
    
    try:
        response_5 = requests.get(BASE_URLS["jsonplaceholder"] + uri_5, timeout=10)          

        print_response_overview(uri_5, response_5)

        response_5.raise_for_status()  

    except requests.RequestException as err_msg:
        print(f"\nRequest failed: {err_msg}")     
        
    else:  
        print("The request was successful.")
    

# ============================================================
# API 2: PokeAPI
# Documentation: https://pokeapi.co/docs/v2
# ============================================================

def explore_pokeapi():
    """Explores PokeAPI utilizing various requests."""

    print("\n=== API 2: PokeAPI ===")

    # Request 1 - GET a specific pokemon (Pikachu)
        
    uri_1 = "/pokemon/25"  # 25 refers to the ID for Pikachu
   
    try:
        response_1 = requests.get(BASE_URLS["pokeapi"] + uri_1, timeout=10)

        print_response_overview(uri_1, response_1)

        response_1.raise_for_status()

    except requests.RequestException as err_msg:
        print(f"\nRequest failed: {err_msg}")
        
    else:        
        selected_pokemon = response_1.json()

        print(f"\n{'-' * 7} GET a Specific Pokemon, Results: {'-' * 7}")   
        print(f"{'Name':<12.12} | {'Height':<6} | {'Weight':<6} | {'Current Ability':<15.15}")
        print(f"{'-' * 48}")  # Dashes/spacing are extended to maintain formatting so as to keep together the table data and the table header/title

        for ability in selected_pokemon["abilities"]:
            if not ability["is_hidden"]:
                current_ability = ability  # Per the API documentation, pokemon have multiple possible abilities but can have only one active, non-hidden ability at a time.

        print(f"{selected_pokemon['name']:<12.12} | {selected_pokemon['height']:<6} | {selected_pokemon['weight']:<6} | {current_ability['ability']['name']:<15.15}")        
        print(f"{'-' * 48}")

        print(f"\n{selected_pokemon['name']} also has the following hidden abilities: ")
        for ability in selected_pokemon["abilities"]:
            if ability["is_hidden"]:
                print(ability["ability"]["name"])


        # Request 2 - GET pokemon of a specific type (Using the first 'type' URL from the above pokemon response - Electric Pokemon)
        ## Request 2 is included in the else block as it is dependent on Request 1 being successful

        type_url = selected_pokemon["types"][0]["type"]["url"]  # Should be https://pokeapi.co/api/v2/type/13/; this API includes a trailing slash in the URL
        uri_2 = type_url.removeprefix(BASE_URLS["pokeapi"])  # Removes the characters before /type/# for use in the helper function

        try:
            response_2 = requests.get(type_url, timeout=10)  # type_url already includes the BASE_URL from above

            print_response_overview(uri_2, response_2)

            response_2.raise_for_status()

        except requests.RequestException as err_msg:
            print(f"\nRequest failed: {err_msg}")
            
        else:    
            pokemon_by_type = response_2.json()

            print(f"\n{'-' * 16} GET Pokemon of a Specific Type, Results: {'-' * 17}") 
            print(f"How {pokemon_by_type['name']}-type pokemon relate to other pokemon types in battle:\n")
            print(f"{'Ineffective Against':<20} | {'Not Very Effective Against':<26} | {'Super Effective Against':<22}")
            print(f"{'-' * 75}")
            print(f"{pokemon_by_type['damage_relations']['no_damage_to'][0]['name']:<20} | {pokemon_by_type['damage_relations']['half_damage_to'][0]['name']:<26} | {pokemon_by_type['damage_relations']['double_damage_to'][0]['name']:22}")

            print(f"\nSample pokemon of the {pokemon_by_type['name']} type:\n")
            print(f"{'Pokemon Name':<12.12} | {'Pokemon URI':<13.13}")
            print(f"{'-' * 28}")
            for pokemon in pokemon_by_type["pokemon"][:5]:  # Showing only the first 5 pokemon for readability
                pokemon_uri = pokemon["pokemon"]["url"].removeprefix(BASE_URLS["pokeapi"])  
                print(f"{pokemon['pokemon']['name']:<12.12} | {pokemon_uri:<13.13}")
            print(f"{'-' * 28}")

 
    # Document the response structure in a comment below - Top-level keys in the /pokemon response:

    # Top-level keys for /pokemon include:
        ## "count" - the number of pokemon
        ## "next" - the URL for the next page of pokemon
        ## "results" - a list of dictionaries containing pokemon from the current page, ordered by pokemon ID number 

    # Top-level keys for /pokemon/{id} include:
        ## "id" - the pokemon's ID
        ## "name" - the pokemon's name
        ## "base_experience" - the base experience gained for defeating this pokemon
        ## "height" - the pokemon's height in decimeters
        ## "is_default" - boolean value; set to "true" for only one pokemon per species
        ## "order" - the order number, used for sorting
        ## "weight" - the pokemon's weight in hectograms
        ## "abilities" - a list of potential abilities for this pokemon
        ## "forms" - a list of forms this pokemon can take
        ## "game_indices" - a list of game indices pertinent to this pokemon by generation
        ## "held_items" - a list of items this pokemon may be holding when encountered
        ## "location_area_encounters" - the URL for a list of location areas and encounter details
        ## "moves" - a list of moves along with learn methods and level details
        ## "past_types" - a list of details showing types this pokemon had in previous generations
        ## "past_abilities" - a list of details showing abilities this pokemon had in previous generations 
        ## "past_stats" - a list of details showing stats this pokemon had in previous generations 
        ## "sprites" - a set of sprites used to depict this pokemon in the game
        ## "cries" - a set of cries associated with this pokemon
        ## "species" - the pokemon's species
        ## "stats" - a list of base stat values for this pokemon
        ## "types" - a list of details showing the types this pokemon has
      

# ============================================================
# API 3: DummyJSON
# Documentation: https://dummyjson.com/docs 
# ============================================================

def explore_dummyjson():
    """Explores DummyJSON API utilizing various requests."""

    print("\n=== API 3: DummyJSON ===")

    # Request 1 - GET a specific product (Product 1)
    
    uri_1 = "/products/1"
    
    try:
        response_1 = requests.get(BASE_URLS["dummyjson"] + uri_1, timeout=10)          

        print_response_overview(uri_1, response_1)

        response_1.raise_for_status()  

    except requests.RequestException as err_msg:
        print(f"\nRequest failed: {err_msg}")     
        
    else:  
        product = response_1.json() 
        
        print(f"\n{'-' * 20} GET a Specific Product, Results: {'-' * 20}")
        print(f"{'ID':<5} | {'Name':<35.35} | {'Category':<15.15} | {'Price':<10}")
        print(f"{'-' * 74}")        
        print(f"{product['id']:<5} | {product['title']:<35.35} | {product['category']:<15.15} | ${product['price']:<10}")
        print(f"{'-' * 74}")
    

        # Request 2 - Update (PATCH) a specific product (Product 1)    
        ## Request 2 is included in the else block as it is dependent on Request 1 being successful   

        new_product_data = {
            "price": 12.99
        }           
        
        try:
            response_2 = requests.patch(BASE_URLS["dummyjson"] + uri_1, json=new_product_data, timeout=10)          

            print_response_overview(uri_1, response_2)

            response_2.raise_for_status()  

        except requests.RequestException as err_msg:
            print(f"\nRequest failed: {err_msg}")     
            
        else:  
            updated_product = response_2.json() 
            
            print(f"\n{'-' * 15} Update (PATCH) a Specific Product, Results: {'-' * 14}")            
            print(f"{'ID':<5} | {'Name':<35.35} | {'Category':<15.15} | {'Price':<10}")
            print(f"{'-' * 74}")        
            print(f"{updated_product['id']:<5} | {updated_product['title']:<35.35} | {updated_product['category']:<15.15} | ${updated_product['price']:<10}")
            print(f"{'-' * 74}")

            print(f"The product price has been updated from ${product['price']} to ${updated_product['price']}.")
            print("**Note: This update will not persist on the server! It is for demo only.")
            print(f"{'-' * 74}")


    # Request 3 - DELETE a specific product (Product 1)     
                  
    try:
        response_3 = requests.delete(BASE_URLS["dummyjson"] + uri_1, timeout=10)          

        print_response_overview(uri_1, response_3)

        response_3.raise_for_status()  

    except requests.RequestException as err_msg:
        print(f"\nRequest failed: {err_msg}")     
        
    else:  
        deleted_product = response_3.json() 
        
        print(f"\n{'-' * 19} DELETE a Specific Product, Results: {'-' * 18}")

        if deleted_product['isDeleted']:
            print(f"The product has been deleted.")
            print("**Note: This deletion will not persist on the server! It is for demo only.")      

        print(f"{'-' * 74}")              
           
  
# ============================================================
# Run all explorations
# ============================================================

if __name__ == "__main__":
    explore_jsonplaceholder()
    explore_pokeapi()
    explore_dummyjson()
    print("\n=== Exploration complete! ===")