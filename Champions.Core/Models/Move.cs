namespace Champions.Core.Models;

public class Move
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Type { get; set; }
    public string Category { get; set; }
    public int? BasePower { get; set; }
    public int? Accuracy { get; set; }
    public int PP { get; set; }

    //Also useful
    public List<Pokemon> CanLearn { get; set; } = new List<Pokemon>();
}