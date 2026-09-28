# Module 4 Project — Part 1: API Documentation

**Your Name: Kelly Cox**



\---



1. ### JSONPlaceholder API



#### Base URL



https://jsonplaceholder.typicode.com





#### Authentication Method



None





#### Tested Endpoints



1. ###### GET /users (Get all users)



Sample Response (200, OK):



\[

&#x20; {

&#x20;   "id": 1,

&#x20;   "name": "Leanne Graham",

&#x20;   "username": "Bret",

&#x20;   "email": "Sincere@april.biz",

&#x20;   "address": {

&#x20;     "street": "Kulas Light",

&#x20;     "suite": "Apt. 556",

&#x20;     "city": "Gwenborough",

&#x20;     "zipcode": "92998-3874",

&#x20;     "geo": {

&#x20;       "lat": "-37.3159",

&#x20;       "lng": "81.1496"

&#x20;     }

&#x20;   },

&#x20;   "phone": "1-770-736-8031 x56442",

&#x20;   "website": "hildegard.org",

&#x20;   "company": {

&#x20;     "name": "Romaguera-Crona",

&#x20;     "catchPhrase": "Multi-layered client-server neural-net",

&#x20;     "bs": "harness real-time e-markets"

&#x20;   }

&#x20; },

&#x09;...additional users

]

###### 

###### 2\. GET /posts?userId=2 (Query Parameter - Get all posts by a specific user)



Sample Response (200, OK):



\[

&#x20; {

&#x20;   "userId": 2,

&#x20;   "id": 11,

&#x20;   "title": "et ea vero quia laudantium autem",

&#x20;   "body": "delectus reiciendis molestiae occaecati non minima eveniet qui voluptatibus\\naccusamus in eum beatae sit\\nvel qui neque voluptates ut commodi qui incidunt\\nut animi commodi"

&#x20; },

&#x09;...additional posts

]



###### 3\. POST /posts (POST \[create] a new post)



*\*\*Note: the created post does not persist on the server.*



Sample Response (201, Created):



{

&#x20; "title": "Test Title",

&#x20; "body": "Test Body",

&#x20; "userId": 1,

&#x20; "id": 101

}



###### 4\. GET /users/1/todos (Nested Resource - Get all todos for a specific user)



Sample Response (200, OK):



\[

&#x20; {

&#x20;   "userId": 1,

&#x20;   "id": 1,

&#x20;   "title": "delectus aut autem",

&#x20;   "completed": false

&#x20; },

&#x09;...additional todos

]



###### 5\. GET /users/posts (Testing Error Handling - Nonexistent Resource)



Sample Response (404, Not Found):



{}





#### Rate Limits



All endpoints returned rate limit headers and values similar to the following:



Header                | Value

\-------------------------------------------------------

X-Ratelimit-Limit     | 1000

X-Ratelimit-Remaining | 999

X-Ratelimit-Reset     | 1780057932





#### One Thing That Surprised Me or Which Did Not Work as Expected



I was most surprised by the rate limits as I noticed several things:



* It appears that the reset date/time is in the past.
* Even after running my script multiple times, the Remaining and Limit amounts remained the same at 999 and 1000, respectively, with each run.
* Upon researching the API documentation (including the associated GitHub), there is little to no discussion of rate limits.



In this sense, it appears that this API does not actively enforce rate limits. I can understand this design decision in that the API is free to use, does not require authorization, and is relatively simple to use (primarily for testing and learning purposes). Nevertheless, I was surprised to learn this, and I found it interesting that rate limits were not discussed more clearly in the API documentation as such contradicts the principles of good design we learned in this module.



\---





### 2\. PokeAPI



#### Base URL



https://pokeapi.co/api/v2





#### Authentication Method



None





#### Tested Endpoints



1. ###### GET /pokemon/25 (Get a specific pokemon)



Sample Response (200, OK):



*\*\*Note: Using here the response for a different pokemon (Clefairy, #35) as the actual response for Pikachu (#25) was extremely long. The response below was taken from the API documentation.*



{

&#x20; "id": 35,

&#x20; "name": "clefairy",

&#x20; "base\_experience": 113,

&#x20; "height": 6,

&#x20; "is\_default": true,

&#x20; "order": 56,

&#x20; "weight": 75,

&#x20; "abilities": \[

&#x20;   {

&#x20;     "is\_hidden": true,

&#x20;     "slot": 3,

&#x20;     "ability": {

&#x20;       "name": "friend-guard",

&#x20;       "url": "https://pokeapi.co/api/v2/ability/132/"

&#x20;     }

&#x20;   }

&#x20; ],

&#x20; "forms": \[

&#x20;   {

&#x20;     "name": "clefairy",

&#x20;     "url": "https://pokeapi.co/api/v2/pokemon-form/35/"

&#x20;   }

&#x20; ],

&#x20; "game\_indices": \[

&#x20;   {

&#x20;     "game\_index": 35,

&#x20;     "version": {

&#x20;       "name": "white-2",

&#x20;       "url": "https://pokeapi.co/api/v2/version/22/"

&#x20;     }

&#x20;   }

&#x20; ],

&#x20; "held\_items": \[

&#x20;   {

&#x20;     "item": {

&#x20;       "name": "moon-stone",

&#x20;       "url": "https://pokeapi.co/api/v2/item/81/"

&#x20;     },

&#x20;     "version\_details": \[

&#x20;       {

&#x20;         "rarity": 5,

&#x20;         "version": {

&#x20;           "name": "ruby",

&#x20;           "url": "https://pokeapi.co/api/v2/version/7/"

&#x20;         }

&#x20;       }

&#x20;     ]

&#x20;   }

&#x20; ],

&#x20; "location\_area\_encounters": "/api/v2/pokemon/35/encounters",

&#x20; "moves": \[

&#x20;   {

&#x20;     "move": {

&#x20;       "name": "pound",

&#x20;       "url": "https://pokeapi.co/api/v2/move/1/"

&#x20;     },

&#x20;     "version\_group\_details": \[

&#x20;       {

&#x20;         "level\_learned\_at": 1,

&#x20;         "version\_group": {

&#x20;           "name": "red-blue",

&#x20;           "url": "https://pokeapi.co/api/v2/version-group/1/"

&#x20;         },

&#x20;         "move\_learn\_method": {

&#x20;           "name": "level-up",

&#x20;           "url": "https://pokeapi.co/api/v2/move-learn-method/1/"

&#x20;         },

&#x20;         "order": 1

&#x20;       }

&#x20;     ]

&#x20;   }

&#x20; ],

&#x20; "species": {

&#x20;   "name": "clefairy",

&#x20;   "url": "https://pokeapi.co/api/v2/pokemon-species/35/"

&#x20; },

&#x20; "sprites": {

&#x20;   "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/35.png",

&#x20;   "back\_female": null,

&#x20;   "back\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/35.png",

&#x20;   "back\_shiny\_female": null,

&#x20;   "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/35.png",

&#x20;   "front\_female": null,

&#x20;   "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/35.png",

&#x20;   "front\_shiny\_female": null,

&#x20;   "other": {

&#x20;     "dream\_world": {

&#x20;       "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/35.svg",

&#x20;       "front\_female": null

&#x20;     },

&#x20;     "home": {

&#x20;       "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/35.png",

&#x20;       "front\_female": null,

&#x20;       "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/shiny/35.png",

&#x20;       "front\_shiny\_female": null

&#x20;     },

&#x20;     "official-artwork": {

&#x20;       "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/35.png",

&#x20;       "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/35.png"

&#x20;     },

&#x20;     "showdown": {

&#x20;       "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/back/35.gif",

&#x20;       "back\_female": null,

&#x20;       "back\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/back/shiny/35.gif",

&#x20;       "back\_shiny\_female": null,

&#x20;       "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/35.gif",

&#x20;       "front\_female": null,

&#x20;       "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/35.gif",

&#x20;       "front\_shiny\_female": null

&#x20;     }

&#x20;   },

&#x20;   "versions": {

&#x20;     "generation-i": {

&#x20;       "red-blue": {

&#x20;         "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/red-blue/back/35.png",

&#x20;         "back\_gray": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/red-blue/back/gray/35.png",

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/red-blue/35.png",

&#x20;         "front\_gray": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/red-blue/gray/35.png"

&#x20;       },

&#x20;       "yellow": {

&#x20;         "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/yellow/back/35.png",

&#x20;         "back\_gray": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/yellow/back/gray/35.png",

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/yellow/35.png",

&#x20;         "front\_gray": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-i/yellow/gray/35.png"

&#x20;       }

&#x20;     },

&#x20;     "generation-ii": {

&#x20;       "crystal": {

&#x20;         "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/crystal/back/35.png",

&#x20;         "back\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/crystal/back/shiny/35.png",

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/crystal/35.png",

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/crystal/shiny/35.png"

&#x20;       },

&#x20;       "gold": {

&#x20;         "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/gold/back/35.png",

&#x20;         "back\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/gold/back/shiny/35.png",

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/gold/35.png",

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/gold/shiny/35.png"

&#x20;       },

&#x20;       "silver": {

&#x20;         "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/silver/back/35.png",

&#x20;         "back\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/silver/back/shiny/35.png",

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/silver/35.png",

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-ii/silver/shiny/35.png"

&#x20;       }

&#x20;     },

&#x20;     "generation-iii": {

&#x20;       "emerald": {

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/emerald/35.png",

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/emerald/shiny/35.png"

&#x20;       },

&#x20;       "firered-leafgreen": {

&#x20;         "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/firered-leafgreen/back/35.png",

&#x20;         "back\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/firered-leafgreen/back/shiny/35.png",

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/firered-leafgreen/35.png",

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/firered-leafgreen/shiny/35.png"

&#x20;       },

&#x20;       "ruby-sapphire": {

&#x20;         "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/ruby-sapphire/back/35.png",

&#x20;         "back\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/ruby-sapphire/back/shiny/35.png",

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/ruby-sapphire/35.png",

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/ruby-sapphire/shiny/35.png"

&#x20;       }

&#x20;     },

&#x20;     "generation-iv": {

&#x20;       "diamond-pearl": {

&#x20;         "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/diamond-pearl/back/35.png",

&#x20;         "back\_female": null,

&#x20;         "back\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/diamond-pearl/back/shiny/35.png",

&#x20;         "back\_shiny\_female": null,

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/diamond-pearl/35.png",

&#x20;         "front\_female": null,

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/diamond-pearl/shiny/35.png",

&#x20;         "front\_shiny\_female": null

&#x20;       },

&#x20;       "heartgold-soulsilver": {

&#x20;         "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/heartgold-soulsilver/back/35.png",

&#x20;         "back\_female": null,

&#x20;         "back\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/heartgold-soulsilver/back/shiny/35.png",

&#x20;         "back\_shiny\_female": null,

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/heartgold-soulsilver/35.png",

&#x20;         "front\_female": null,

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/heartgold-soulsilver/shiny/35.png",

&#x20;         "front\_shiny\_female": null

&#x20;       },

&#x20;       "platinum": {

&#x20;         "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/platinum/back/35.png",

&#x20;         "back\_female": null,

&#x20;         "back\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/platinum/back/shiny/35.png",

&#x20;         "back\_shiny\_female": null,

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/platinum/35.png",

&#x20;         "front\_female": null,

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iv/platinum/shiny/35.png",

&#x20;         "front\_shiny\_female": null

&#x20;       }

&#x20;     },

&#x20;     "generation-v": {

&#x20;       "black-white": {

&#x20;         "animated": {

&#x20;           "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/35.gif",

&#x20;           "back\_female": null,

&#x20;           "back\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/shiny/35.gif",

&#x20;           "back\_shiny\_female": null,

&#x20;           "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/35.gif",

&#x20;           "front\_female": null,

&#x20;           "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/shiny/35.gif",

&#x20;           "front\_shiny\_female": null

&#x20;         },

&#x20;         "back\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/back/35.png",

&#x20;         "back\_female": null,

&#x20;         "back\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/back/shiny/35.png",

&#x20;         "back\_shiny\_female": null,

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/35.png",

&#x20;         "front\_female": null,

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/shiny/35.png",

&#x20;         "front\_shiny\_female": null

&#x20;       }

&#x20;     },

&#x20;     "generation-vi": {

&#x20;       "omegaruby-alphasapphire": {

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vi/omegaruby-alphasapphire/35.png",

&#x20;         "front\_female": null,

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vi/omegaruby-alphasapphire/shiny/35.png",

&#x20;         "front\_shiny\_female": null

&#x20;       },

&#x20;       "x-y": {

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vi/x-y/35.png",

&#x20;         "front\_female": null,

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vi/x-y/shiny/35.png",

&#x20;         "front\_shiny\_female": null

&#x20;       }

&#x20;     },

&#x20;     "generation-vii": {

&#x20;       "icons": {

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vii/icons/35.png",

&#x20;         "front\_female": null

&#x20;       },

&#x20;       "ultra-sun-ultra-moon": {

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vii/ultra-sun-ultra-moon/35.png",

&#x20;         "front\_female": null,

&#x20;         "front\_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vii/ultra-sun-ultra-moon/shiny/35.png",

&#x20;         "front\_shiny\_female": null

&#x20;       }

&#x20;     },

&#x20;     "generation-viii": {

&#x20;       "icons": {

&#x20;         "front\_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-viii/icons/35.png",

&#x20;         "front\_female": null

&#x20;       }

&#x20;     }

&#x20;   }

&#x20; },

&#x20; "cries": {

&#x20;   "latest": "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/35.ogg",

&#x20;   "legacy": "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/legacy/35.ogg"

&#x20; },

&#x20; "stats": \[

&#x20;   {

&#x20;     "base\_stat": 35,

&#x20;     "effort": 0,

&#x20;     "stat": {

&#x20;       "name": "speed",

&#x20;       "url": "https://pokeapi.co/api/v2/stat/6/"

&#x20;     }

&#x20;   }

&#x20; ],

&#x20; "types": \[

&#x20;   {

&#x20;     "slot": 1,

&#x20;     "type": {

&#x20;       "name": "fairy",

&#x20;       "url": "https://pokeapi.co/api/v2/type/18/"

&#x20;     }

&#x20;   }

&#x20; ],

&#x20; "past\_types": \[

&#x20;   {

&#x20;     "generation": {

&#x20;       "name": "generation-v",

&#x20;       "url": "https://pokeapi.co/api/v2/generation/5/"

&#x20;     },

&#x20;     "types": \[

&#x20;       {

&#x20;         "slot": 1,

&#x20;         "type": {

&#x20;           "name": "normal",

&#x20;           "url": "https://pokeapi.co/api/v2/type/1/"

&#x20;         }

&#x20;       }

&#x20;     ]

&#x20;   }

&#x20; ],

&#x20; "past\_abilities": \[

&#x20;   {

&#x20;     "generation": {

&#x20;       "name": "generation-iv",

&#x20;       "url": "https://pokeapi.co/api/v2/generation/4/"

&#x20;     },

&#x20;     "abilities": \[

&#x20;       {

&#x20;         "ability": null,

&#x20;         "is\_hidden": true,

&#x20;         "slot": 3

&#x20;       }

&#x20;     ]

&#x20;   }

&#x20; ]

}



###### 2\. GET /type/13 (Get information/all pokemon pertaining to a specific type)



Sample Response (200, OK):



*\*\*Note: Using here the response for a different pokemon type (ground, ID 5) as the actual response for electric-type pokemon (ID 13) was extremely long. The response below was taken from the API documentation.*



{

&#x20; "id": 5,

&#x20; "name": "ground",

&#x20; "damage\_relations": {

&#x20;   "no\_damage\_to": \[

&#x20;     {

&#x20;       "name": "flying",

&#x20;       "url": "https://pokeapi.co/api/v2/type/3/"

&#x20;     }

&#x20;   ],

&#x20;   "half\_damage\_to": \[

&#x20;     {

&#x20;       "name": "bug",

&#x20;       "url": "https://pokeapi.co/api/v2/type/7/"

&#x20;     }

&#x20;   ],

&#x20;   "double\_damage\_to": \[

&#x20;     {

&#x20;       "name": "poison",

&#x20;       "url": "https://pokeapi.co/api/v2/type/4/"

&#x20;     }

&#x20;   ],

&#x20;   "no\_damage\_from": \[

&#x20;     {

&#x20;       "name": "electric",

&#x20;       "url": "https://pokeapi.co/api/v2/type/13/"

&#x20;     }

&#x20;   ],

&#x20;   "half\_damage\_from": \[

&#x20;     {

&#x20;       "name": "poison",

&#x20;       "url": "https://pokeapi.co/api/v2/type/4/"

&#x20;     }

&#x20;   ],

&#x20;   "double\_damage\_from": \[

&#x20;     {

&#x20;       "name": "water",

&#x20;       "url": "https://pokeapi.co/api/v2/type/11/"

&#x20;     }

&#x20;   ]

&#x20; },

&#x20; "past\_damage\_relations": \[

&#x20;   {

&#x20;     "generation": {

&#x20;       "name": "generation-v",

&#x20;       "url": "https://pokeapi.co/api/v2/generation/5/"

&#x20;     },

&#x20;     "damage\_relations": {

&#x20;       "no\_damage\_to": \[

&#x20;         {

&#x20;           "name": "normal",

&#x20;           "url": "https://pokeapi.co/api/v2/type/1/"

&#x20;         }

&#x20;       ],

&#x20;       "half\_damage\_to": \[

&#x20;         {

&#x20;           "name": "steel",

&#x20;           "url": "https://pokeapi.co/api/v2/type/9/"

&#x20;         }

&#x20;       ],

&#x20;       "double\_damage\_to": \[

&#x20;         {

&#x20;           "name": "ghost",

&#x20;           "url": "https://pokeapi.co/api/v2/type/8/"

&#x20;         }

&#x20;       ],

&#x20;       "no\_damage\_from": \[

&#x20;         {

&#x20;           "name": "normal",

&#x20;           "url": "https://pokeapi.co/api/v2/type/1/"

&#x20;         }

&#x20;       ],

&#x20;       "half\_damage\_from": \[

&#x20;         {

&#x20;           "name": "poison",

&#x20;           "url": "https://pokeapi.co/api/v2/type/4/"

&#x20;         }

&#x20;       ],

&#x20;       "double\_damage\_from": \[

&#x20;         {

&#x20;           "name": "ghost",

&#x20;           "url": "https://pokeapi.co/api/v2/type/8/"

&#x20;         }

&#x20;       ]

&#x20;     }

&#x20;   }

&#x20; ],

&#x20; "game\_indices": \[

&#x20;   {

&#x20;     "game\_index": 4,

&#x20;     "generation": {

&#x20;       "name": "generation-i",

&#x20;       "url": "https://pokeapi.co/api/v2/generation/1/"

&#x20;     }

&#x20;   }

&#x20; ],

&#x20; "generation": {

&#x20;   "name": "generation-i",

&#x20;   "url": "https://pokeapi.co/api/v2/generation/1/"

&#x20; },

&#x20; "move\_damage\_class": {

&#x20;   "name": "physical",

&#x20;   "url": "https://pokeapi.co/api/v2/move-damage-class/2/"

&#x20; },

&#x20; "names": \[

&#x20;   {

&#x20;     "name": "ã˜ã‚ã‚“",

&#x20;     "language": {

&#x20;       "name": "ja",

&#x20;       "url": "https://pokeapi.co/api/v2/language/1/"

&#x20;     }

&#x20;   }

&#x20; ],

&#x20; "pokemon": \[

&#x20;   {

&#x20;     "slot": 1,

&#x20;     "pokemon": {

&#x20;       "name": "sandshrew",

&#x20;       "url": "https://pokeapi.co/api/v2/pokemon/27/"

&#x20;     }

&#x20;   }

&#x20; ],

&#x20; "moves": \[

&#x20;   {

&#x20;     "name": "sand-attack",

&#x20;     "url": "https://pokeapi.co/api/v2/move/28/"

&#x20;   }

&#x20; ]

}





#### Rate Limits



None (The associated headers/values, e.g. X-Ratelimit-Limit, did not even appear in the response.)





#### One Thing That Surprised Me or Which Did Not Work as Expected



I was surprised at the lack of rate limits as well as the lack of use of filler headers for rate limits such as those used in JSONPlaceholder API. I was also surprised at the depth and breadth of information utilized across the API and in the responses. This made the documentation rather overwhelming, and this made it very tedious and somewhat complicated when accessing various elements of the response in that the data is so deeply nested. For example: pokemon\_by\_type\['damage\_relations']\['no\_damage\_to']\[0]\['name'].



\---





### 3\. DummyJSON API



#### Base URL



https://dummyjson.com





#### Authentication Method



None.



However, the developer does provide the option to use sample users, sample tokens, and authentication headers in order to test accessing the API as a logged-in user:



headers: {

&#x20;   "Authorization": "Bearer YOUR\_ACCESS\_TOKEN\_HERE",

&#x20;   "Content-Type": "application/json"

&#x20; }





#### Tested Endpoints



1. ###### GET /products/1 (Get a specific product)



Sample Response (200, OK):



{

&#x20; "id": 1,

&#x20; "title": "Essence Mascara Lash Princess",

&#x20; "description": "The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.",

&#x20; "category": "beauty",

&#x20; "price": 9.99,

&#x20; "discountPercentage": 7.17,

&#x20; "rating": 4.94,

&#x20; "stock": 5,

&#x20; "tags": \[

&#x20;   "beauty",

&#x20;   "mascara"

&#x20; ],

&#x20; "brand": "Essence",

&#x20; "sku": "RCH45Q1A",

&#x20; "weight": 2,

&#x20; "dimensions": {

&#x20;   "width": 23.17,

&#x20;   "height": 14.43,

&#x20;   "depth": 28.01

&#x20; },

&#x20; "warrantyInformation": "1 month warranty",

&#x20; "shippingInformation": "Ships in 1 month",

&#x20; "availabilityStatus": "Low Stock",

&#x20; "reviews": \[

&#x20;   {

&#x20;     "rating": 2,

&#x20;     "comment": "Very unhappy with my purchase!",

&#x20;     "date": "2024-05-23T08:56:21.618Z",

&#x20;     "reviewerName": "John Doe",

&#x20;     "reviewerEmail": "john.doe@x.dummyjson.com"

&#x20;   },

&#x20;   {

&#x20;     "rating": 2,

&#x20;     "comment": "Not as described!",

&#x20;     "date": "2024-05-23T08:56:21.618Z",

&#x20;     "reviewerName": "Nolan Gonzalez",

&#x20;     "reviewerEmail": "nolan.gonzalez@x.dummyjson.com"

&#x20;   },

&#x20;   {

&#x20;     "rating": 5,

&#x20;     "comment": "Very satisfied!",

&#x20;     "date": "2024-05-23T08:56:21.618Z",

&#x20;     "reviewerName": "Scarlett Wright",

&#x20;     "reviewerEmail": "scarlett.wright@x.dummyjson.com"

&#x20;   }

&#x20; ],

&#x20; "returnPolicy": "30 days return policy",

&#x20; "minimumOrderQuantity": 24,

&#x20; "meta": {

&#x20;   "createdAt": "2024-05-23T08:56:21.618Z",

&#x20;   "updatedAt": "2024-05-23T08:56:21.618Z",

&#x20;   "barcode": "9164035109868",

&#x20;   "qrCode": "..."

&#x20; },

&#x20; "thumbnail": "...",

&#x20; "images": \["...", "...", "..."]

}



###### 2\. PATCH /products/1 (Update a specific product)



*\*\*Note: the update does not persist on the server.*



Sample Response (200, OK):



{

&#x20; "id": 1,

&#x20; "title": "Essence Mascara Lash Princess",

&#x20; "price": 12.99,

&#x20; "discountPercentage": 10.48,

&#x20; "stock": 99,

&#x20; "rating": 2.56,

&#x20; "images": \["https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/1.webp"],

&#x20; "thumbnail": "https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/thumbnail.webp",

&#x20; "description": "The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.",

&#x20; "brand": "Essence",

&#x20; "category": "beauty"

}



###### 3\. DELETE /products/1 (Delete a specific product)



*\*\*Note: the deletion does not persist on the server.*



Sample Response (200, OK):



{

&#x20; "id": 1,

&#x20; "title": "Essence Mascara Lash Princess",

&#x20; "description": "The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.",

&#x20; "category": "beauty",

&#x20; "price": 9.99,

&#x20; "discountPercentage": 7.17,

&#x20; "rating": 4.94,

&#x20; "stock": 5,

&#x20; "tags": \[

&#x20;   "beauty",

&#x20;   "mascara"

&#x20; ],

&#x20; "brand": "Essence",

&#x20; "sku": "RCH45Q1A",

&#x20; "weight": 2,

&#x20; "dimensions": {

&#x20;   "width": 23.17,

&#x20;   "height": 14.43,

&#x20;   "depth": 28.01

&#x20; },

&#x20; "warrantyInformation": "1 month warranty",

&#x20; "shippingInformation": "Ships in 1 month",

&#x20; "availabilityStatus": "Low Stock",

&#x20; "reviews": \[

&#x20;   {

&#x20;     "rating": 2,

&#x20;     "comment": "Very unhappy with my purchase!",

&#x20;     "date": "2024-05-23T08:56:21.618Z",

&#x20;     "reviewerName": "John Doe",

&#x20;     "reviewerEmail": "john.doe@x.dummyjson.com"

&#x20;   },

&#x20;   {

&#x20;     "rating": 2,

&#x20;     "comment": "Not as described!",

&#x20;     "date": "2024-05-23T08:56:21.618Z",

&#x20;     "reviewerName": "Nolan Gonzalez",

&#x20;     "reviewerEmail": "nolan.gonzalez@x.dummyjson.com"

&#x20;   },

&#x20;   {

&#x20;     "rating": 5,

&#x20;     "comment": "Very satisfied!",

&#x20;     "date": "2024-05-23T08:56:21.618Z",

&#x20;     "reviewerName": "Scarlett Wright",

&#x20;     "reviewerEmail": "scarlett.wright@x.dummyjson.com"

&#x20;   }

&#x20; ],

&#x20; "returnPolicy": "30 days return policy",

&#x20; "minimumOrderQuantity": 24,

&#x20; "meta": {

&#x20;   "createdAt": "2024-05-23T08:56:21.618Z",

&#x20;   "updatedAt": "2024-05-23T08:56:21.618Z",

&#x20;   "barcode": "9164035109868",

&#x20;   "qrCode": "..."

&#x20; },

&#x20; "thumbnail": "...",

&#x20; "images": \["...", "...", "..."],

&#x20; "isDeleted": true,

&#x20; "deletedOn": "2024-05-24T08:56:21.618Z"

}





#### Rate Limits



All endpoints returned rate limit headers and values such as the following:



Header                | Value

\-------------------------------------------------------

X-Ratelimit-Limit     | 100

X-Ratelimit-Remaining | 99

X-Ratelimit-Reset     | 1790105612



However, similar to JSONPlaceholder API, it appears DummyJSON API does not actively enforce rate limits as these values (e.g. 99 and 100) remained the same regardless of the number of calls.



#### One Thing That Surprised Me or Which Did Not Work as Expected



Once again, I was surprised at the lack of true rate limits. I was also surprised at the variety of resources available. I can see how this would be very valuable for testing, and I certainly will be bookmarking this API for testing regarding future projects.



\---



### 4\. One Thing That Surprised Me Overall



I was very surprised that the documentation for each API above provided rather detailed information regarding the resources available and sample responses yet lacked other topics of significant consideration for users of the API, such as sections outlining (or outlining more explicitly) authentication, rate limits, status codes, and error formats. As a comparative example, the documentation for GitHub Rest API utilized in an earlier assignment, while overwhelming, was extremely thorough in these respects. As a user, I found the latter documentation much more helpful than that of the APIs tested above, and, as a result, I will aim to implement similar documentation structures for users of any APIs I develop in the future.



\---

