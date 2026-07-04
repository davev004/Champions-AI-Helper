using System.Runtime.CompilerServices;

namespace Champions.Core.Models;

public class Pokemon
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string PrimaryType { get; set; }
    public string? SecondaryType { get; set; }

    //Base Stats

    public int HP { get; set; }
    public int Attack { get; set; }
    public int Defense { get; set; }
    public int SpecialAttack { get; set; }
    public int SpecialDefense { get; set; }
    public int Speed { get; set; }

    //Useful
    public List<Move> LegalMoves { get; set; } = new List<Move>();
    public List<Ability> LegalAbilities { get; set; } = new List<Ability>();
}