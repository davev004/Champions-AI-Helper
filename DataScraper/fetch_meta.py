import requests
import json
def translate_to_pokeapi_name(showdown_name):
    # Standardize spaces and casing
    name = showdown_name.lower().strip().replace(' ', '-')
    
    # Strip basic punctuation quirks
    name = name.replace("'", "").replace(".", "")
    
    # 1. Handle Gendered Specifics cleanly without erasing them
    if name == "meowstic-f": return "meowstic-female"
    if name == "meowstic-m": return "meowstic-male"
    if name == "basculegion-f": return "basculegion-female"
    if name == "indeedee-f": return "indeedee-female"
    if name == "oinkologne-f": return "oinkologne-female"
    if name == "meowstic-m-mega": return "meowstic-male-mega"
    if name == "meowstic-f-mega": return "meowstic-male-mega" #both megas are same
    
    # If it's just the base name for gendered species, default to the default API endpoint
    if name == "meowstic": return "meowstic-male" 
    if name == "basculegion": return "basculegion-male"
    if name == "pyroar": return "pyroar-male"
    if name == "indeedee": return "indeedee-male"
    if name == "oinkologne": return "oinkologne-male"

    # 2. Handle Lycanroc & Other Multi-Form Species (Preserving roles!)
    if name == "lycanroc-dusk": return "lycanroc-dusk"
    if name == "lycanroc-midnight": return "lycanroc-midnight"
    if name == "lycanroc": return "lycanroc-midday" # Base Lycanroc in PokéAPI is Midday
    if name == "gourgeist": return "gourgeist-average" # Base Gourgeist in PokéAPI is Average
    
    if name == "aegislash": return "aegislash-shield"
    if name == "mimikyu": return "mimikyu-disguised"
    if name == "palafin": return "palafin-zero"
    if name == "maushold": return "maushold-family-of-four"
    if name == "morpeko": return "morpeko-full-belly"
    
    # 3. Handle Paldean Tauros Breeds
    if name == "tauros-paldea-combat": return "tauros-paldea-combat-breed"
    if name == "tauros-paldea-blaze": return "tauros-paldea-blaze-breed"
    if name == "tauros-paldea-aqua": return "tauros-paldea-aqua-breed"
    
    return name

def fetch_showdown_roster(stats_url):
    print(f"Fetching Regulation M-B stats from {stats_url}...")
    response = requests.get(stats_url)
    
    if response.status_code != 200:
        print("Failed to reach Showdown stats server. Check the URL.")
        return []

    lines = response.text.split('\n')
    roster = []

    for line in lines:
        # Showdown stat lines look like this:
        # | 1    | Garchomp           | 45.123% |
        # We only want lines with data, not the table headers or borders
        if '|' in line and 'Pokemon' not in line:
            columns = [col.strip() for col in line.split('|')]
            
            # The Pokemon name is always in the 3rd column (index 2)
            if len(columns) > 2:
                # Format to match PokéAPI's URL structure
                raw_name = columns[2].strip()
                pokemon_name = translate_to_pokeapi_name(raw_name)
                
                # Filter out the empty spacing and table borders
                if pokemon_name and not pokemon_name.startswith('---'):
                    roster.append(pokemon_name)

    return roster

# Grab the baseline 1500 ELO stats for the current Champions Regulation M-B format
url = "https://www.smogon.com/stats/2026-06/gen9championsvgc2026regmb-1500.txt"
legal_pokemon = fetch_showdown_roster(url)

print(f"Successfully parsed {len(legal_pokemon)} legal Pokémon!")



def fetch_pokemon_champions_data(pokemon_list):
    scraped_data = []
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    
    # Keep track of ones that fail so we can manually add them later
    manual_intervention_required = []

    for name in pokemon_list:
        print(f"Fetching data for {name}...")
        response = requests.get(base_url + name)
        
        if response.status_code != 200:
            print(f"  -> Failed to find {name} (404). Flagging for manual JSON.")
            manual_intervention_required.append(name)
            continue
            
        data = response.json()
        
        try:
            # Format the data to exactly match our C# Pokemon.cs model
            pokemon_model = {
                "Name": data["name"].capitalize(),
                "PrimaryType": data["types"][0]["type"]["name"].capitalize(),
                "SecondaryType": data["types"][1]["type"]["name"].capitalize() if len(data["types"]) > 1 else None,
                "Hp": data["stats"][0]["base_stat"],
                "Attack": data["stats"][1]["base_stat"],
                "Defense": data["stats"][2]["base_stat"],
                "SpecialAttack": data["stats"][3]["base_stat"],
                "SpecialDefense": data["stats"][4]["base_stat"],
                "Speed": data["stats"][5]["base_stat"],
                "LegalAbilities": [ability["ability"]["name"].capitalize() for ability in data["abilities"]]
            }
            scraped_data.append(pokemon_model)
            
        except (KeyError, IndexError) as e:
            # This catches missing 'types', missing 'stats', etc.
            print(f"  -> Data structure broken for {name} (Missing: {e}). Flagging for manual JSON.")
            manual_intervention_required.append(name)
            continue

    # Export the successful ones to JSON
    with open('champions_seed_data.json', 'w') as outfile:
        json.dump(scraped_data, outfile, indent=4)
        
    print("\n--- SCRAPE COMPLETE ---")
    print(f"Successfully exported {len(scraped_data)} Pokémon to champions_seed_data.json!")
    
    if manual_intervention_required:
        print(f"\nThe following {len(manual_intervention_required)} Pokémon require manual entry:")
        for missing in manual_intervention_required:
            print(f"- {missing}")

# Let's start with a small meta sample
top_meta_pokemon = ["garchomp", "pelipper", "incineroar", "flutter-mane"]
fetch_pokemon_champions_data(legal_pokemon)