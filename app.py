import requests
import random
from flask import Flask, jsonify, request
from services.auth_service import verify_token

app = Flask(__name__)

# Base URL for PokeAPI
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"

# Helper function to fetch data from PokeAPI
def fetch_from_pokeapi(endpoint):
    response = requests.get(f"{POKEAPI_BASE_URL}{endpoint}")
    if response.status_code == 200:
        return response.json()
    return None

# Helper function to verify group-based access
def verify_group_permission(required_group):
    user_info = verify_token()
    if isinstance(user_info, tuple):  # Invalid or missing token
        return user_info

    # Extract groups from JWT token
    user_groups = user_info.get("groups", [])
    if required_group not in user_groups:
        return jsonify({"error": "Forbidden: You don't have access to this resource"}), 403
    return user_info

# 1. Get the type(s) of a Pokémon by its name
@app.route("/pokemon/type/<name>", methods=["GET"])
def get_pokemon_type(name):
    user_info = verify_group_permission("Pokemon_type_view")
    if isinstance(user_info, tuple):
        return user_info

    data = fetch_from_pokeapi(f"pokemon/{name.lower()}")
    if not data:
        return jsonify({"error": f"Pokémon '{name}' not found!"}), 404

    types = [t["type"]["name"] for t in data["types"]]
    return jsonify({
        "pokemon": name,
        "types": types,
        "user": user_info["preferred_username"]
    })

# 2. Get a random Pokémon of a specific type
@app.route("/pokemon/random/<pokemon_type>", methods=["GET"])
def get_random_pokemon_by_type(pokemon_type):
    user_info = verify_group_permission("Pokemon_random_view")
    if isinstance(user_info, tuple):
        return user_info

    data = fetch_from_pokeapi(f"type/{pokemon_type.lower()}")
    if not data:
        return jsonify({"error": f"Type '{pokemon_type}' not found!"}), 404

    pokemon = random.choice(data["pokemon"])["pokemon"]["name"]
    return jsonify({
        "random_pokemon": pokemon,
        "type": pokemon_type,
        "user": user_info["preferred_username"]
    })

# 3. Get the Pokémon with the longest name of a specific type
@app.route("/pokemon/longest-name/<pokemon_type>", methods=["GET"])
def get_longest_name_pokemon(pokemon_type):
    user_info = verify_group_permission("Pokemon_advance_view")
    if isinstance(user_info, tuple):
        return user_info

    data = fetch_from_pokeapi(f"type/{pokemon_type.lower()}")
    if not data:
        return jsonify({"error": f"Type '{pokemon_type}' not found!"}), 404

    longest_pokemon = max(
        data["pokemon"], key=lambda p: len(p["pokemon"]["name"])
    )["pokemon"]["name"]

    return jsonify({
        "longest_name_pokemon": longest_pokemon,
        "type": pokemon_type,
        "user": user_info["preferred_username"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
