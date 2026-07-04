import requests
import json
import time

def fetch_full_learnsets_and_moves():
    # 1. Load your existing legal roster
    print("Reading champions_seed_data.json...")
    with open('champions_seed_data.json', 'r') as file:
        pokemon_data = json.load(file)

    pokemon_learnsets = {}
    unique_moves = set()
    base_pokemon_url = "https://pokeapi.co/api/v2/pokemon/"

    print(f"Fetching full learnsets for {len(pokemon_data)} Pokémon...")

    # 2. Extract every move for every Pokémon
    for pokemon in pokemon_data:
        # Note: You would use your translate_to_pokeapi_name helper here if needed
        api_name = pokemon["Name"].lower().replace(' ', '-')
        
        response = requests.get(base_pokemon_url + api_name)
        if response.status_code != 200:
            print(f"  -> Failed to find {api_name} on PokéAPI.")
            continue
            
        data = response.json()
        legal_moves = []
        
        for move_entry in data.get("moves", []):
            move_name = move_entry["move"]["name"]
    
            # Check if the move is legal in the current generation (Gen 9)
            is_in_current_gen = False
            for version_detail in move_entry.get("version_group_details", []):
                if version_detail["version_group"]["name"] == "champions":
                    is_in_current_gen = True
                break
            
    # Only add the move to your database if it survives the filter
            if is_in_current_gen:
                legal_moves.append(move_name)
                unique_moves.add(move_name)
            
        # Save the mapping for this specific Pokémon
        pokemon_learnsets[pokemon["Name"]] = legal_moves

    # Export the mapping (This is what EF Core will use to build the Many-to-Many table)
    with open('champions_learnset_mapping.json', 'w') as outfile:
        json.dump(pokemon_learnsets, outfile, indent=4)
        
    print(f"\nFound {len(unique_moves)} total unique moves across the meta!")
    print("Hydrating move stats from PokéAPI...")

    # 3. Fetch the actual stats for all unique moves
    moves_data = []
    base_move_url = "https://pokeapi.co/api/v2/move/"
    
    for move_name in unique_moves:
        res = requests.get(base_move_url + move_name)
        if res.status_code != 200:
            continue
            
        data = res.json()
        
        try:
            # Map directly to your C# Move.cs model
            move_model = {
                "Name": data["name"].title().replace('-', ' '),
                "Type": data["type"]["name"].capitalize(),
                "Category": data["damage_class"]["name"].capitalize(),
                "BasePower": data.get("power"), 
                "Accuracy": data.get("accuracy") 
            }
            moves_data.append(move_model)
        except Exception as e:
            pass

    # Export the actual move data
    with open('champions_moves_full.json', 'w') as outfile:
        json.dump(moves_data, outfile, indent=4)
        
    print("\n--- FULL LEARNSET SCRAPE COMPLETE ---")

fetch_full_learnsets_and_moves()