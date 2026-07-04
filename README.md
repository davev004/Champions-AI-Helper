# Champions-AI-Helper README
## 1. Project Overview

This project is a C#/.NET 6 ASP.NET Core Web API with a Blazor frontend, designed to generate factual, non-hallucinatory team recommendations for the Pokémon Champions (Regulation M-B) meta using a Retrieval-Augmented Generation (RAG) pipeline.
## 2. Prerequisites & Installations

To successfully replicate this environment, ensure the following tools are installed on your system:
### Core Environment

    * VS Code: The recommended IDE for this workflow.

    * .NET 6 SDK: Required for the backend and frontend frameworks.

    * Git: Required for repository version control.

### Command-Line Tools

    * Entity Framework Core CLI: Used for database migrations and schema management. Install globally using:
    ```Bash
        dotnet tool install --global dotnet-ef --version "6.0.*"
    ```
    * SQLite CLI: Used to inspect the database directly from the terminal. Install via winget:
    ```Bash
        winget install --id SQLite.SQLite --exact
    ```
    (Note: Restart your terminal or VS Code after installation to refresh the PATH.)

## 3. Data Pipeline Setup (Python)

The project utilizes Python scripts to scrape legal Pokémon roster data from Smogon usage statistics and enrich it with data from PokéAPI.

    * Python 3.x: Ensure Python is installed to run the scripts located in the /DataScraper folder.

    * Requests Library: Required for API calls and file downloads. Install via:

    ```Bash
        pip install requests
    ```
## 4. Database Configuration

This project uses SQLite for lightweight, local relational storage.

### Dependencies

Ensure the following NuGet packages are installed in your `Champions.Api` project:

    *`Microsoft.EntityFrameworkCore`

    *`Microsoft.EntityFrameworkCore.Design`

    *`Microsoft.EntityFrameworkCore.Sqlite`

### Configuration

In `Champions.Api/Program.cs`, ensure your database context is registered to use SQLite:
```C#
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlite("Data Source=champions.db"));
```
##5. Development Workflow

To initialize the project and seed the database, follow these steps in the terminal:

    1. Generate Developer Certificate: Enables secure HTTPS development.
    ```Bash
        dotnet dev-certs https --trust
    ```
    2. Generate Migration: Creates the initial SQL blueprint from your C# models.
    ```Bash
        dotnet ef migrations add InitialCreate --project .\Champions.Api\
    ```
    3. Run Application: Triggers the `DatabaseSeeder`, which reads your generated JSON files (Pokémon, Moves, Abilities, Items, and Custom Items) and injects them into `champions.db`.
    ```Bash
        dotnet run --project .\Champions.Api\
    ```
## 6. Project Structure

    * `/Champions.Core`: Contains C# Models (`Pokemon.cs`, `Move.cs`, `Item.cs`, `Ability.cs`).

    * `/Champions.Api`: Contains the ASP.NET Core backend and `ApplicationDbContext.cs`.

    * `/Champions.Web`: Contains the Blazor frontend.

    * `/DataScraper`: Contains Python scripts (`fetch_meta.py`, `fetch_abilities.py`, etc.) and JSON data files.