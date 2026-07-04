namespace Champions.Core.Models;

public class Item
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string EffectDescription { get; set; }
    public bool IsConsumable { get; set; }
    public bool IsCurrentlyLegal { get; set; } = true;

}