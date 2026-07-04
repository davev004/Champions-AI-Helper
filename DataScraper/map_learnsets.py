import requests
import json
import time

def recover_learnset_mappings():
    print("Reading champions_seed_data.json...")
    
    try:
        with open('champions_seed_data.json', 'r') as file:
            pokemon_data = json.load(file)
    except FileNotFoundError:
        print("Error: Could not find champions_seed_data.json. Make sure you are in the right directory.")
        return

    pokemon_learnsets = {}
    base_pokemon_url = "https://pokeapi.co/api/v2/pokemon/"

    print(f"Fetching filtered learnsets for {len(pokemon_data)} Pokémon...")

    for pokemon in pokemon_data:
        # Format the name back to PokéAPI standard (e.g., "Tapu Koko" -> "tapu-koko")
        api_name = pokemon["Name"].lower().replace(' ', '-').replace("'", "")
        
        # Handle specific edge cases if your JSON saved them differently
        if api_name == "meowstic": api_name = "meowstic-male"
        if api_name == "basculegion": api_name = "basculegion-male"
        if api_name == "lycanroc": api_name = "lycanroc-midday"
        
        response = requests.get(base_pokemon_url + api_name)
        if response.status_code != 200:
            print(f"  -> Failed to find {api_name} on PokéAPI. Skipping.")
            continue
            
        data = response.json()
        legal_moves = []
        
        # Extract moves and apply the Gen 9 legality filter
        for move_entry in data.get("moves", []):
            move_name = move_entry["move"]["name"]
            
            is_in_current_gen = False
            for version_detail in move_entry.get("version_group_details", []):
                # Filter out old moves like Pursuit or Return
                if version_detail["version_group"]["name"] == "champions":
                    is_in_current_gen = True
                    break
                    
            if is_in_current_gen:
                legal_moves.append(move_name)
                
        # Save the mapping for this specific Pokémon
        pokemon_learnsets[pokemon["Name"]] = legal_moves
        
        # Small delay to be polite to PokéAPI
        time.sleep(0.1)

    # Export the mapping for Entity Framework Core
    with open('champions_learnset_mapping.json', 'w') as outfile:
        json.dump(pokemon_learnsets, outfile, indent=4)
        
    print("\n--- RECOVERY COMPLETE ---")
    print("Successfully regenerated champions_learnset_mapping.json!")

recover_learnset_mappings()