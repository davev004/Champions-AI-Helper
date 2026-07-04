using Champions.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace Champions.Api.Data;
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
    {
    }

public DbSet<Pokemon> Pokemon { get; set; } = null!;
public DbSet<Move> Moves { get; set; } = null!;
public DbSet<Item> Items { get; set; } = null!;
public DbSet<Ability> Abilities { get; set; } = null!;

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
    }
}

