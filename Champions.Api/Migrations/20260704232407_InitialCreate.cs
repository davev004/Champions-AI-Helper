using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Champions.Api.Migrations
{
    public partial class InitialCreate : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Abilities",
                columns: table => new
                {
                    Id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Name = table.Column<string>(type: "TEXT", nullable: false),
                    Description = table.Column<string>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Abilities", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Items",
                columns: table => new
                {
                    Id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Name = table.Column<string>(type: "TEXT", nullable: false),
                    EffectDescription = table.Column<string>(type: "TEXT", nullable: false),
                    IsConsumable = table.Column<bool>(type: "INTEGER", nullable: false),
                    IsCurrentlyLegal = table.Column<bool>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Items", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Moves",
                columns: table => new
                {
                    Id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Name = table.Column<string>(type: "TEXT", nullable: false),
                    Type = table.Column<string>(type: "TEXT", nullable: false),
                    Category = table.Column<string>(type: "TEXT", nullable: false),
                    BasePower = table.Column<int>(type: "INTEGER", nullable: true),
                    Accuracy = table.Column<int>(type: "INTEGER", nullable: true),
                    PP = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Moves", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Pokemon",
                columns: table => new
                {
                    Id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Name = table.Column<string>(type: "TEXT", nullable: false),
                    PrimaryType = table.Column<string>(type: "TEXT", nullable: false),
                    SecondaryType = table.Column<string>(type: "TEXT", nullable: true),
                    HP = table.Column<int>(type: "INTEGER", nullable: false),
                    Attack = table.Column<int>(type: "INTEGER", nullable: false),
                    Defense = table.Column<int>(type: "INTEGER", nullable: false),
                    SpecialAttack = table.Column<int>(type: "INTEGER", nullable: false),
                    SpecialDefense = table.Column<int>(type: "INTEGER", nullable: false),
                    Speed = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Pokemon", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "AbilityPokemon",
                columns: table => new
                {
                    LegalAbilitiesId = table.Column<int>(type: "INTEGER", nullable: false),
                    PokemonWithAbilityId = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AbilityPokemon", x => new { x.LegalAbilitiesId, x.PokemonWithAbilityId });
                    table.ForeignKey(
                        name: "FK_AbilityPokemon_Abilities_LegalAbilitiesId",
                        column: x => x.LegalAbilitiesId,
                        principalTable: "Abilities",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_AbilityPokemon_Pokemon_PokemonWithAbilityId",
                        column: x => x.PokemonWithAbilityId,
                        principalTable: "Pokemon",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "MovePokemon",
                columns: table => new
                {
                    CanLearnId = table.Column<int>(type: "INTEGER", nullable: false),
                    LegalMovesId = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_MovePokemon", x => new { x.CanLearnId, x.LegalMovesId });
                    table.ForeignKey(
                        name: "FK_MovePokemon_Moves_LegalMovesId",
                        column: x => x.LegalMovesId,
                        principalTable: "Moves",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_MovePokemon_Pokemon_CanLearnId",
                        column: x => x.CanLearnId,
                        principalTable: "Pokemon",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_AbilityPokemon_PokemonWithAbilityId",
                table: "AbilityPokemon",
                column: "PokemonWithAbilityId");

            migrationBuilder.CreateIndex(
                name: "IX_MovePokemon_LegalMovesId",
                table: "MovePokemon",
                column: "LegalMovesId");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "AbilityPokemon");

            migrationBuilder.DropTable(
                name: "Items");

            migrationBuilder.DropTable(
                name: "MovePokemon");

            migrationBuilder.DropTable(
                name: "Abilities");

            migrationBuilder.DropTable(
                name: "Moves");

            migrationBuilder.DropTable(
                name: "Pokemon");
        }
    }
}
