import json
import requests

def fetch_abilities():
    print("Reading champions_seed_data.json...")
    
    # 1. Load your existing Pokémon data
    with open('champions_seed_data.json', 'r') as file:
        pokemon_data = json.load(file)

    # 2. Extract a unique set of abilities
    unique_abilities = set()
    for pokemon in pokemon_data:
        for ability in pokemon.get("LegalAbilities", []):
            # Format to match PokéAPI's URL structure
            unique_abilities.add(ability.lower().replace(' ', '-'))

    print(f"Found {len(unique_abilities)} unique abilities. Fetching descriptions...")

    abilities_data = []
    manual_intervention_required = []
    base_url = "https://pokeapi.co/api/v2/ability/"

    # 3. Fetch each ability from PokéAPI
    for ability_name in unique_abilities:
        response = requests.get(base_url + ability_name)
        
        if response.status_code != 200:
            print(f"  -> Failed to find '{ability_name}'. Flagging for manual JSON.")
            manual_intervention_required.append(ability_name)
            continue
            
        data = response.json()
        
        try:
            # Find the first English description
            description = "No description available."
            for entry in data.get("flavor_text_entries", []):
                if entry["language"]["name"] == "en":
                    # Clean up weird newlines returned by PokéAPI
                    description = entry["flavor_text"].replace('\n', ' ').replace('\f', ' ')
                    break

            # Format to match your C# Ability.cs model
            ability_model = {
                "Name": data["name"].capitalize().replace('-', ' '),
                "Description": description
            }
            abilities_data.append(ability_model)
            
        except (KeyError, IndexError) as e:
            print(f"  -> Data broken for '{ability_name}'. Flagging for manual JSON.")
            manual_intervention_required.append(ability_name)
            continue

    # 4. Export to a new JSON file
    with open('champions_abilities.json', 'w') as outfile:
        json.dump(abilities_data, outfile, indent=4)
        
    print(f"\n--- ABILITY SCRAPE COMPLETE ---")
    print(f"Successfully exported {len(abilities_data)} abilities to champions_abilities.json!")
    
    if manual_intervention_required:
        print(f"\nThe following {len(manual_intervention_required)} custom abilities require manual entry:")
        for missing in manual_intervention_required:
            print(f"- {missing}")

# Run the function
fetch_abilities()