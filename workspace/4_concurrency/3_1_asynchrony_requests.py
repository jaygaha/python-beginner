# How to connect to an api using Ptyhon requests library
import requests

base_url = "https://pokeapi.co/api/v2"

def get_pokemon(pokemon_name):
    url = f"{base_url}/pokemon/{pokemon_name}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failed to fetch data: {response.status_code}")


pokemon_name = "pikachu"
# pokemon_name = "tyranitar"
pokemon_info = get_pokemon(pokemon_name)

if pokemon_info:
    print(f"Pokemon name: {pokemon_info['name'].capitalize()}") # Pokemon name: Pikachu
    print(f"Pokemon id: {pokemon_info['id']}")
    print(f"Pokemon height: {pokemon_info['height']}") # Pokemon height: 4
    print(f"Pokemon weight: {pokemon_info['weight']}") # Pokemon height: 4
    print(f"Pokemon abilities: {pokemon_info['abilities']}")# Pokemon abilities: [{'ability': {'name': 'static', 'url': 'https://pokeapi.co/api/v2/ability/9/'}, 'is_hidden': False, 'slot': 1}, {'ability': {'name': 'lightning-rod', 'url': 'https://pokeapi.co/api/v2/ability/31/'}, 'is_hidden': True, 'slot': 3}]
