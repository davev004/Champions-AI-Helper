import requests
import json
import re

def fetch_legal_items():
    # The 'moveset' folder contains the item breakdowns per Pokémon
    stats_url = "https://www.smogon.com/stats/2026-06/moveset/gen9championsvgc2026regmb-1500.txt"
    print(f"Fetching item usage data from {stats_url}...")
    
    response = requests.get(stats_url)
    if response.status_code != 200:
        print("Failed to reach Showdown stats server. Check the URL.")
        return
        
    lines = response.text.split('\n')
    unique_items = set()
    
    print("Parsing ASCII tables for unique items...")
    
    # 1. Parse the text file to find the "Items" blocks
    in_items_section = False
    for line in lines:
        if "| Items" in line:
            in_items_section = True
            continue
        # End of an item block is marked by the table border
        if in_items_section and "+--" in line:
            in_items_section = False
            continue
            
        if in_items_section:
            # Lines look like: "| Leftovers                                25.0% |"
            parts = line.split('|')
            if len(parts) > 1:
                raw_item = parts[1].strip()
                # Use Regex to strip out the percentage and trailing spaces
                item_name = re.sub(r'\s+\d+\.\d+%', '', raw_item).strip()
                
                # Filter out empty or non-item data
                if item_name and item_name not in ["Other", "Nothing"]:
                    # Format to match PokéAPI's URL expectations
                    api_name = item_name.lower().replace(' ', '-').replace("'", "")
                    unique_items.add(api_name)
                    
    print(f"Found {len(unique_items)} unique competitive items. Hydrating from PokéAPI...")
    
    items_data = []
    manual_intervention_required = []
    base_url = "https://pokeapi.co/api/v2/item/"
    
    # 2. Fetch data from PokéAPI
    for item_name in unique_items:
        res = requests.get(base_url + item_name)
        if res.status_code != 200:
            print(f"  -> Failed to find '{item_name}'. Flagging for manual JSON.")
            manual_intervention_required.append(item_name)
            continue
            
        data = res.json()
        
        try:
            # PokéAPI stores item descriptions in two different places; try effects first, then flavor text
            description = "No description available."
            for entry in data.get("effect_entries", []):
                if entry["language"]["name"] == "en":
                    description = entry["short_effect"].replace('\n', ' ').replace('\f', ' ')
                    break
                    
            if description == "No description available.":
                for entry in data.get("flavor_text_entries", []):
                    if entry["language"]["name"] == "en":
                        description = entry["text"].replace('\n', ' ').replace('\f', ' ')
                        break

            # 3. Determine if the item is consumable (Focus Sash, Berries, etc.)
            is_consumable = any(attr["name"] == "consumable" for attr in data.get("attributes", []))
            
            # 4. Map directly to your C# Item.cs model
            item_model = {
                "Name": data["name"].title().replace('-', ' '),
                "EffectDescription": description,
                "IsConsumable": is_consumable,
                "IsLegalInCurrentFormat": True
            }
            items_data.append(item_model)
            
        except (KeyError, IndexError) as e:
            print(f"  -> Data broken for '{item_name}'. Flagging for manual JSON.")
            manual_intervention_required.append(item_name)
            
    # Export successful data
    with open('champions_items.json', 'w') as outfile:
        json.dump(items_data, outfile, indent=4)
        
    print("\n--- ITEM SCRAPE COMPLETE ---")
    print(f"Successfully exported {len(items_data)} items to champions_items.json!")
    
    if manual_intervention_required:
        print(f"\nThe following {len(manual_intervention_required)} items require manual entry:")
        for missing in manual_intervention_required:
            print(f"- {missing}")

fetch_legal_items()