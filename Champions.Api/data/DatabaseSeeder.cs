using System.Text.Json;
using Champions.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace Champions.Api.Data
{
    public static class DatabaseSeeder
    {
        public static async Task SeedAsync(ApplicationDbContext context)
        {
            // Ensure the database is created and migrations are applied
            await context.Database.MigrateAsync();

            // 1. Seed Abilities
            if (!context.Abilities.Any())
            {
                var abilitiesJson = await File.ReadAllTextAsync("../DataScraper/champions_abilities.json");
                var abilities = JsonSerializer.Deserialize<List<Ability>>(abilitiesJson);
                if (abilities != null)
                {
                    await context.Abilities.AddRangeAsync(abilities);
                    await context.SaveChangesAsync();
                }
            }

            // 2. Seed Items (Scraped + Custom)
            if (!context.Items.Any())
            {
                var allItems = new List<Item>();

                // Load the official items from PokéAPI
                var scrapedItemsJson = await File.ReadAllTextAsync("../DataScraper/champions_items.json");
                var scrapedItems = JsonSerializer.Deserialize<List<Item>>(scrapedItemsJson);
                if (scrapedItems != null)
                {
                    allItems.AddRange(scrapedItems);
                }

                // Load your custom Champions items
                if (File.Exists("../DataScraper/champions_custom_items.json"))
                {
                    var customItemsJson = await File.ReadAllTextAsync("../DataScraper/champions_custom_items.json");
                    var customItems = JsonSerializer.Deserialize<List<Item>>(customItemsJson);
                    if (customItems != null)
                    {
                        allItems.AddRange(customItems);
                    }
                }

                // Save everything to the database at once
                if (allItems.Any())
                {
                    await context.Items.AddRangeAsync(allItems);
                    await context.SaveChangesAsync();
                }
            }

            // 3. Seed Moves
            if (!context.Moves.Any())
            {
                var movesJson = await File.ReadAllTextAsync("../DataScraper/champions_moves_full.json");
                var moves = JsonSerializer.Deserialize<List<Move>>(movesJson);
                if (moves != null)
                {
                    await context.Moves.AddRangeAsync(moves);
                    await context.SaveChangesAsync();
                }
            }

            // 4. Seed Pokémon (Base Stats & Types)
            if (!context.Pokemon.Any())
            {
                var pokemonJson = await File.ReadAllTextAsync("../DataScraper/champions_seed_data.json");
                
                // We use a custom JsonDocument here so we can read the "LegalAbilities" array from JSON
                // and map it to the actual EF Core objects we just seeded above.
                using JsonDocument doc = JsonDocument.Parse(pokemonJson);
                var pokemons = new List<Pokemon>();
                var allAbilities = await context.Abilities.ToListAsync();

                foreach (JsonElement element in doc.RootElement.EnumerateArray())
                {
                    var pokemon = new Pokemon
                    {
                        Name = element.GetProperty("Name").GetString() ?? "",
                        PrimaryType = element.GetProperty("PrimaryType").GetString() ?? "",
                        SecondaryType = element.GetProperty("SecondaryType").ValueKind != JsonValueKind.Null ? element.GetProperty("SecondaryType").GetString() : null,
                        HP = element.GetProperty("Hp").GetInt32(),
                        Attack = element.GetProperty("Attack").GetInt32(),
                        Defense = element.GetProperty("Defense").GetInt32(),
                        SpecialAttack = element.GetProperty("SpecialAttack").GetInt32(),
                        SpecialDefense = element.GetProperty("SpecialDefense").GetInt32(),
                        Speed = element.GetProperty("Speed").GetInt32()
                    };

                    // Map the abilities
                    var abilityNames = element.GetProperty("LegalAbilities").EnumerateArray().Select(a => a.GetString()).ToList();
                    pokemon.LegalAbilities = allAbilities.Where(a => abilityNames.Contains(a.Name)).ToList();

                    pokemons.Add(pokemon);
                }
                
                await context.Pokemon.AddRangeAsync(pokemons);
                await context.SaveChangesAsync();
            }

            // 5. Build the Learnset Bridge (Many-to-Many Magic)
            // We check if the first Pokemon has any moves. If not, we haven't mapped the learnsets yet.
            var firstMon = await context.Pokemon.Include(p => p.LegalMoves).FirstOrDefaultAsync();
            if (firstMon != null && !firstMon.LegalMoves.Any())
            {
                var learnsetJson = await File.ReadAllTextAsync("../DataScraper/champions_learnset_mapping.json");
                var learnsets = JsonSerializer.Deserialize<Dictionary<string, List<string>>>(learnsetJson);
                
                var allMoves = await context.Moves.ToListAsync();
                var allPokemon = await context.Pokemon.ToListAsync();

                if (learnsets != null)
                {
                    foreach (var kvp in learnsets)
                    {
                        var targetPokemon = allPokemon.FirstOrDefault(p => p.Name.ToLower() == kvp.Key.ToLower());
                        if (targetPokemon != null)
                        {
                            // Find the actual Move objects that match the names in the JSON array
                            var validMoves = allMoves.Where(m => kvp.Value.Contains(m.Name.ToLower().Replace(' ', '-'))).ToList();
                            targetPokemon.LegalMoves = validMoves;
                        }
                    }
                    // One final save updates all the bridging tables!
                    await context.SaveChangesAsync();
                }
            }
        }
    }
}