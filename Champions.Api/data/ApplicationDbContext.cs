using Champions.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace Champions.Api.Data;
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
    {
    }

    public DbSet<Pokemon> Pokemon { get; set; }
    public DbSet<Move> Moves { get; set; }
    public DbSet<Item> Items { get; set; }
    public DbSet<Ability> Abilities { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
    }
}

