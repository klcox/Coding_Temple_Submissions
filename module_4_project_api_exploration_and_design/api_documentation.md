# Module 4 Project — Part 1: API Documentation



---



## 1. JSONPlaceholder API



### Base URL



https://jsonplaceholder.typicode.com





### Authentication Method



None





### Tested Endpoints



#### 1. GET /users (Get all users)



Sample Response (200, OK):

```json

[

 {

   "id": 1,

   "name": "Leanne Graham",

   "username": "Bret",

   "email": "Sincere@april.biz",

   "address": {

     "street": "Kulas Light",

     "suite": "Apt. 556",

     "city": "Gwenborough",

     "zipcode": "92998-3874",

     "geo": {

       "lat": "-37.3159",

       "lng": "81.1496"

     }

   },

   "phone": "1-770-736-8031 x56442",

   "website": "hildegard.org",

   "company": {

     "name": "Romaguera-Crona",

     "catchPhrase": "Multi-layered client-server neural-net",

     "bs": "harness real-time e-markets"

   }

 },

	...additional users

]

```

#### 2. GET /posts?userId=2 (Query Parameter - Get all posts by a specific user)



Sample Response (200, OK):
```json

[

 {

   "userId": 2,

   "id": 11,

   "title": "et ea vero quia laudantium autem",

   "body": "delectus reiciendis molestiae occaecati non minima eveniet qui voluptatibusnaccusamus in eum beatae sitnvel qui neque voluptates ut commodi qui inciduntnut animi commodi"

 },

	...additional posts

]
```


#### 3. POST /posts (POST [create] a new post)



***Note: the created post does not persist on the server.*



Sample Response (201, Created):
```json


{

 "title": "Test Title",

 "body": "Test Body",

 "userId": 1,

 "id": 101

}
```


#### 4. GET /users/1/todos (Nested Resource - Get all todos for a specific user)



Sample Response (200, OK):
```json


[

 {

   "userId": 1,

   "id": 1,

   "title": "delectus aut autem",

   "completed": false

 },

	...additional todos

]
```


#### 5. GET /users/posts (Testing Error Handling - Nonexistent Resource)



Sample Response (404, Not Found):
```json


{}

```



### Rate Limits



All endpoints returned rate limit headers and values similar to the following:



| Header | Value |
|---|---|
| X-Ratelimit-Limit | 1000 |
| X-Ratelimit-Remaining | 999 |
| X-Ratelimit-Reset | 1780057932 |





### One Thing That Surprised Me or Which Did Not Work as Expected



I was most surprised by the rate limits as I noticed several things:



- It appears that the reset date/time is in the past.
- Even after running my script multiple times, the Remaining and Limit amounts remained the same at 999 and 1000, respectively, with each run.
- Upon researching the API documentation (including the associated GitHub), there is little to no discussion of rate limits.



In this sense, it appears that this API does not actively enforce rate limits. I can understand this design decision in that the API is free to use, does not require authorization, and is relatively simple to use (primarily for testing and learning purposes). Nevertheless, I was surprised to learn this, and I found it interesting that rate limits were not discussed more clearly in the API documentation as such contradicts the principles of good design we learned in this module.









## 2. PokeAPI



### Base URL



https://pokeapi.co/docs/v2





### Authentication Method



None





### Tested Endpoints



#### 1. GET /pokemon/25 (Get a specific pokemon)



Sample Response (200, OK):



***Note: Using here the response for a different pokemon (Clefairy, #35) as the actual response for Pikachu (#25) was extremely long. The response below was taken from the API documentation.*

```json

{

 "id": 35,

 "name": "clefairy",

 "base_experience": 113,

 "height": 6,

 "is_default": true,

 "order": 56,

 "weight": 75,

 "abilities": [

   {

     "is_hidden": true,

     "slot": 3,

     "ability": {

       "name": "friend-guard",

       "url": "https://pokeapi.co/api/v2/ability/132/"

     }

   }

 ],

 "forms": [

   {

     "name": "clefairy",

     "url": "https://pokeapi.co/api/v2/pokemon-form/35/"

   }

 ],

 "game_indices": [

   {

     "game_index": 35,

     "version": {

       "name": "white-2",

       "url": "https://pokeapi.co/api/v2/version/22/"

     }

   }

 ],

 "held_items": [

   {

     "item": {

       "name": "moon-stone",

       "url": "https://pokeapi.co/api/v2/item/81/"

     },

     "version_details": [

       {

         "rarity": 5,

         "version": {

           "name": "ruby",

           "url": "https://pokeapi.co/api/v2/version/7/"

         }

       }

     ]

   }

 ],

 "location_area_encounters": "/api/v2/pokemon/35/encounters",

 "moves": [

   {

     "move": {

       "name": "pound",

       "url": "https://pokeapi.co/api/v2/move/1/"

     },

     "version_group_details": [

       {

         "level_learned_at": 1,

         "version_group": {

           "name": "red-blue",

           "url": "https://pokeapi.co/api/v2/version-group/1/"

         },

         "move_learn_method": {

           "name": "level-up",

           "url": "https://pokeapi.co/api/v2/move-learn-method/1/"

         },

         "order": 1

       }

     ]

   }

 ],

 "species": {

   "name": "clefairy",

   "url": "https://pokeapi.co/api/v2/pokemon-species/35/"

 },

 "sprites": {

   "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/35.png",

   "back_female": null,

   "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/35.png",

   "back_shiny_female": null,

   "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/35.png",

   "front_female": null,

   "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/35.png",

   "front_shiny_female": null,

   "other": {

     "dream_world": {

       "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/35.svg",

       "front_female": null

     },

     "home": {

       "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/35.png",

       "front_female": null,

       "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/shiny/35.png",

       "front_shiny_female": null

     },

     "official-artwork": {

       "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/35.png",

       "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/35.png"

     },

     "showdown": {

       "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/back/35.gif",

       "back_female": null,

       "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/back/shiny/35.gif",

       "back_shiny_female": null,

       "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/35.gif",

       "front_female": null,

       "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/35.gif",

       "front_shiny_female": null

     }

   },

   "versions": {

     "generation-i": {

       "red-blue": {

         "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/red-blue/back/35.png",

         "back_gray": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/red-blue/back/gray/35.png",

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/red-blue/35.png",

         "front_gray": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/red-blue/gray/35.png"

       },

       "yellow": {

         "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/yellow/back/35.png",

         "back_gray": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/yellow/back/gray/35.png",

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/yellow/35.png",

         "front_gray": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/yellow/gray/35.png"

       }

     },

     "generation-ii": {

       "crystal": {

         "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/crystal/back/35.png",

         "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/crystal/back/shiny/35.png",

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/crystal/35.png",

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/crystal/shiny/35.png"

       },

       "gold": {

         "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/gold/back/35.png",

         "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/gold/back/shiny/35.png",

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/gold/35.png",

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/gold/shiny/35.png"

       },

       "silver": {

         "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/silver/back/35.png",

         "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/silver/back/shiny/35.png",

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/silver/35.png",

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/silver/shiny/35.png"

       }

     },

     "generation-iii": {

       "emerald": {

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/emerald/35.png",

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/emerald/shiny/35.png"

       },

       "firered-leafgreen": {

         "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/firered-leafgreen/back/35.png",

         "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/firered-leafgreen/back/shiny/35.png",

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/firered-leafgreen/35.png",

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/firered-leafgreen/shiny/35.png"

       },

       "ruby-sapphire": {

         "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/ruby-sapphire/back/35.png",

         "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/ruby-sapphire/back/shiny/35.png",

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/ruby-sapphire/35.png",

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/ruby-sapphire/shiny/35.png"

       }

     },

     "generation-iv": {

       "diamond-pearl": {

         "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/diamond-pearl/back/35.png",

         "back_female": null,

         "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/diamond-pearl/back/shiny/35.png",

         "back_shiny_female": null,

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/diamond-pearl/35.png",

         "front_female": null,

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/diamond-pearl/shiny/35.png",

         "front_shiny_female": null

       },

       "heartgold-soulsilver": {

         "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/heartgold-soulsilver/back/35.png",

         "back_female": null,

         "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/heartgold-soulsilver/back/shiny/35.png",

         "back_shiny_female": null,

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/heartgold-soulsilver/35.png",

         "front_female": null,

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/heartgold-soulsilver/shiny/35.png",

         "front_shiny_female": null

       },

       "platinum": {

         "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/platinum/back/35.png",

         "back_female": null,

         "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/platinum/back/shiny/35.png",

         "back_shiny_female": null,

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/platinum/35.png",

         "front_female": null,

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/platinum/shiny/35.png",

         "front_shiny_female": null

       }

     },

     "generation-v": {

       "black-white": {

         "animated": {

           "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/35.gif",

           "back_female": null,

           "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/shiny/35.gif",

           "back_shiny_female": null,

           "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/35.gif",

           "front_female": null,

           "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/shiny/35.gif",

           "front_shiny_female": null

         },

         "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/back/35.png",

         "back_female": null,

         "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/back/shiny/35.png",

         "back_shiny_female": null,

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/35.png",

         "front_female": null,

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/shiny/35.png",

         "front_shiny_female": null

       }

     },

     "generation-vi": {

       "omegaruby-alphasapphire": {

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vi/omegaruby-alphasapphire/35.png",

         "front_female": null,

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vi/omegaruby-alphasapphire/shiny/35.png",

         "front_shiny_female": null

       },

       "x-y": {

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vi/x-y/35.png",

         "front_female": null,

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vi/x-y/shiny/35.png",

         "front_shiny_female": null

       }

     },

     "generation-vii": {

       "icons": {

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vii/icons/35.png",

         "front_female": null

       },

       "ultra-sun-ultra-moon": {

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vii/ultra-sun-ultra-moon/35.png",

         "front_female": null,

         "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vii/ultra-sun-ultra-moon/shiny/35.png",

         "front_shiny_female": null

       }

     },

     "generation-viii": {

       "icons": {

         "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-viii/icons/35.png",

         "front_female": null

       }

     }

   }

 },

 "cries": {

   "latest": "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/35.ogg",

   "legacy": "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/legacy/35.ogg"

 },

 "stats": [

   {

     "base_stat": 35,

     "effort": 0,

     "stat": {

       "name": "speed",

       "url": "https://pokeapi.co/api/v2/stat/6/"

     }

   }

 ],

 "types": [

   {

     "slot": 1,

     "type": {

       "name": "fairy",

       "url": "https://pokeapi.co/api/v2/type/18/"

     }

   }

 ],

 "past_types": [

   {

     "generation": {

       "name": "generation-v",

       "url": "https://pokeapi.co/api/v2/generation/5/"

     },

     "types": [

       {

         "slot": 1,

         "type": {

           "name": "normal",

           "url": "https://pokeapi.co/api/v2/type/1/"

         }

       }

     ]

   }

 ],

 "past_abilities": [

   {

     "generation": {

       "name": "generation-iv",

       "url": "https://pokeapi.co/api/v2/generation/4/"

     },

     "abilities": [

       {

         "ability": null,

         "is_hidden": true,

         "slot": 3

       }

     ]

   }

 ]

}

```

#### 2. GET /type/13 (Get information/all pokemon pertaining to a specific type)



Sample Response (200, OK):


***Note: Using here the response for a different pokemon type (ground, ID 5) as the actual response for electric-type pokemon (ID 13) was extremely long. The response below was taken from the API documentation.*

```json


{

 "id": 5,

 "name": "ground",

 "damage_relations": {

   "no_damage_to": [

     {

       "name": "flying",

       "url": "https://pokeapi.co/api/v2/type/3/"

     }

   ],

   "half_damage_to": [

     {

       "name": "bug",

       "url": "https://pokeapi.co/api/v2/type/7/"

     }

   ],

   "double_damage_to": [

     {

       "name": "poison",

       "url": "https://pokeapi.co/api/v2/type/4/"

     }

   ],

   "no_damage_from": [

     {

       "name": "electric",

       "url": "https://pokeapi.co/api/v2/type/13/"

     }

   ],

   "half_damage_from": [

     {

       "name": "poison",

       "url": "https://pokeapi.co/api/v2/type/4/"

     }

   ],

   "double_damage_from": [

     {

       "name": "water",

       "url": "https://pokeapi.co/api/v2/type/11/"

     }

   ]

 },

 "past_damage_relations": [

   {

     "generation": {

       "name": "generation-v",

       "url": "https://pokeapi.co/api/v2/generation/5/"

     },

     "damage_relations": {

       "no_damage_to": [

         {

           "name": "normal",

           "url": "https://pokeapi.co/api/v2/type/1/"

         }

       ],

       "half_damage_to": [

         {

           "name": "steel",

           "url": "https://pokeapi.co/api/v2/type/9/"

         }

       ],

       "double_damage_to": [

         {

           "name": "ghost",

           "url": "https://pokeapi.co/api/v2/type/8/"

         }

       ],

       "no_damage_from": [

         {

           "name": "normal",

           "url": "https://pokeapi.co/api/v2/type/1/"

         }

       ],

       "half_damage_from": [

         {

           "name": "poison",

           "url": "https://pokeapi.co/api/v2/type/4/"

         }

       ],

       "double_damage_from": [

         {

           "name": "ghost",

           "url": "https://pokeapi.co/api/v2/type/8/"

         }

       ]

     }

   }

 ],

 "game_indices": [

   {

     "game_index": 4,

     "generation": {

       "name": "generation-i",

       "url": "https://pokeapi.co/api/v2/generation/1/"

     }

   }

 ],

 "generation": {

   "name": "generation-i",

   "url": "https://pokeapi.co/api/v2/generation/1/"

 },

 "move_damage_class": {

   "name": "physical",

   "url": "https://pokeapi.co/api/v2/move-damage-class/2/"

 },

 "names": [

   {

     "name": "ã˜ã‚ã‚“",

     "language": {

       "name": "ja",

       "url": "https://pokeapi.co/api/v2/language/1/"

     }

   }

 ],

 "pokemon": [

   {

     "slot": 1,

     "pokemon": {

       "name": "sandshrew",

       "url": "https://pokeapi.co/api/v2/pokemon/27/"

     }

   }

 ],

 "moves": [

   {

     "name": "sand-attack",

     "url": "https://pokeapi.co/api/v2/move/28/"

   }

 ]

}

```



### Rate Limits



None (The associated headers/values, e.g. X-Ratelimit-Limit, did not even appear in the response.)





### One Thing That Surprised Me or Which Did Not Work as Expected



I was surprised at the lack of rate limits as well as the lack of use of filler headers for rate limits such as those used in JSONPlaceholder API. I was also surprised at the depth and breadth of information utilized across the API and in the responses. This made the documentation rather overwhelming, and this made it very tedious and somewhat complicated when accessing various elements of the response in that the data is so deeply nested. For example: `pokemon_by_type['damage_relations']['no_damage_to'][0]['name']`.









## 3. DummyJSON API



### Base URL



https://dummyjson.com





### Authentication Method



None.



However, the developer does provide the option to use sample users, sample tokens, and authentication headers in order to test accessing the API as a logged-in user:


```json
headers: {

   "Authorization": "Bearer YOUR_ACCESS_TOKEN_HERE",

   "Content-Type": "application/json"

 }
```




### Tested Endpoints



#### 1. GET /products/1 (Get a specific product)



Sample Response (200, OK):
```json


{

 "id": 1,

 "title": "Essence Mascara Lash Princess",

 "description": "The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.",

 "category": "beauty",

 "price": 9.99,

 "discountPercentage": 7.17,

 "rating": 4.94,

 "stock": 5,

 "tags": [

   "beauty",

   "mascara"

 ],

 "brand": "Essence",

 "sku": "RCH45Q1A",

 "weight": 2,

 "dimensions": {

   "width": 23.17,

   "height": 14.43,

   "depth": 28.01

 },

 "warrantyInformation": "1 month warranty",

 "shippingInformation": "Ships in 1 month",

 "availabilityStatus": "Low Stock",

 "reviews": [

   {

     "rating": 2,

     "comment": "Very unhappy with my purchase!",

     "date": "2024-05-23T08:56:21.618Z",

     "reviewerName": "John Doe",

     "reviewerEmail": "john.doe@x.dummyjson.com"

   },

   {

     "rating": 2,

     "comment": "Not as described!",

     "date": "2024-05-23T08:56:21.618Z",

     "reviewerName": "Nolan Gonzalez",

     "reviewerEmail": "nolan.gonzalez@x.dummyjson.com"

   },

   {

     "rating": 5,

     "comment": "Very satisfied!",

     "date": "2024-05-23T08:56:21.618Z",

     "reviewerName": "Scarlett Wright",

     "reviewerEmail": "scarlett.wright@x.dummyjson.com"

   }

 ],

 "returnPolicy": "30 days return policy",

 "minimumOrderQuantity": 24,

 "meta": {

   "createdAt": "2024-05-23T08:56:21.618Z",

   "updatedAt": "2024-05-23T08:56:21.618Z",

   "barcode": "9164035109868",

   "qrCode": "..."

 },

 "thumbnail": "...",

 "images": ["...", "...", "..."]

}
```


#### 2. PATCH /products/1 (Update a specific product)



***Note: the update does not persist on the server.*



Sample Response (200, OK):

```json

{

 "id": 1,

 "title": "Essence Mascara Lash Princess",

 "price": 12.99,

 "discountPercentage": 10.48,

 "stock": 99,

 "rating": 2.56,

 "images": ["https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/1.webp"],

 "thumbnail": "https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/thumbnail.webp",

 "description": "The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.",

 "brand": "Essence",

 "category": "beauty"

}

```

#### 3. DELETE /products/1 (Delete a specific product)



***Note: the deletion does not persist on the server.*



Sample Response (200, OK):
```json


{

 "id": 1,

 "title": "Essence Mascara Lash Princess",

 "description": "The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.",

 "category": "beauty",

 "price": 9.99,

 "discountPercentage": 7.17,

 "rating": 4.94,

 "stock": 5,

 "tags": [

   "beauty",

   "mascara"

 ],

 "brand": "Essence",

 "sku": "RCH45Q1A",

 "weight": 2,

 "dimensions": {

   "width": 23.17,

   "height": 14.43,

   "depth": 28.01

 },

 "warrantyInformation": "1 month warranty",

 "shippingInformation": "Ships in 1 month",

 "availabilityStatus": "Low Stock",

 "reviews": [

   {

     "rating": 2,

     "comment": "Very unhappy with my purchase!",

     "date": "2024-05-23T08:56:21.618Z",

     "reviewerName": "John Doe",

     "reviewerEmail": "john.doe@x.dummyjson.com"

   },

   {

     "rating": 2,

     "comment": "Not as described!",

     "date": "2024-05-23T08:56:21.618Z",

     "reviewerName": "Nolan Gonzalez",

     "reviewerEmail": "nolan.gonzalez@x.dummyjson.com"

   },

   {

     "rating": 5,

     "comment": "Very satisfied!",

     "date": "2024-05-23T08:56:21.618Z",

     "reviewerName": "Scarlett Wright",

     "reviewerEmail": "scarlett.wright@x.dummyjson.com"

   }

 ],

 "returnPolicy": "30 days return policy",

 "minimumOrderQuantity": 24,

 "meta": {

   "createdAt": "2024-05-23T08:56:21.618Z",

   "updatedAt": "2024-05-23T08:56:21.618Z",

   "barcode": "9164035109868",

   "qrCode": "..."

 },

 "thumbnail": "...",

 "images": ["...", "...", "..."],

 "isDeleted": true,

 "deletedOn": "2024-05-24T08:56:21.618Z"

}
```




### Rate Limits



All endpoints returned rate limit headers and values such as the following:



| Header | Value |
|---|---|
| X-Ratelimit-Limit | 100 |
| X-Ratelimit-Remaining | 99 |
| X-Ratelimit-Reset | 1790105612 |



However, similar to JSONPlaceholder API, it appears DummyJSON API does not actively enforce rate limits as these values (e.g. 99 and 100) remained the same regardless of the number of calls.



### One Thing That Surprised Me or Which Did Not Work as Expected



Once again, I was surprised at the lack of true rate limits. I was also surprised at the variety of resources available. I can see how this would be very valuable for testing, and I certainly will be bookmarking this API for testing regarding future projects.







## 4. One Thing That Surprised Me Overall



I was very surprised that the documentation for each API above provided rather detailed information regarding the resources available and sample responses yet lacked other topics of significant consideration for users of the API, such as sections outlining (or outlining more explicitly) authentication, rate limits, status codes, and error formats. As a comparative example, the documentation for GitHub Rest API utilized in an earlier assignment, while overwhelming, was extremely thorough in these respects. As a user, I found the latter documentation much more helpful than that of the APIs tested above, and, as a result, I will aim to implement similar documentation structures for users of any APIs I develop in the future.





