from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress
from db.connection import connect_db
from db.schema import create_tables
from db.operations import insert_country, insert_province, insert_city, get_countries, get_provinces
from data.geo_data import GEO_DATA
import time

console = Console()

def display_menu():
    console.print("\n[bold cyan]Geo Database Management Tool[/bold cyan]")
    console.print("1. Insert Single Country")
    console.print("2. Insert Continent Data")
    console.print("3. Insert Province")
    console.print("4. Insert City")
    console.print("5. Exit")
    return Prompt.ask("Select an option", choices=['1', '2', '3', '4', '5'])

def display_countries(cursor):
    countries = get_countries(cursor)
    if not countries:
        console.print("[yellow]No countries available.[/yellow]")
        return []
    table = Table(title="Available Countries")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Continent", style="green")
    for country in countries:
        table.add_row(country[0], country[1], country[2])
    console.print(table)
    return countries

def display_provinces(cursor, country_id):
    provinces = get_provinces(cursor, country_id)
    if not provinces:
        console.print("[yellow]No provinces available for this country.[/yellow]")
        return []
    table = Table(title="Available Provinces")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    for province in provinces:
        table.add_row(province[0], province[1])
    console.print(table)
    return provinces

def insert_continent_data(cursor, db_type, continent):
    if continent not in GEO_DATA:
        console.print(f"[red]Continent '{continent}' not found.[/red]")
        return
    data = GEO_DATA[continent]
    total_tasks = sum(len(provinces) * (len(cities) + 1) + 1 for provinces in data.values() for cities in provinces.values())
    
    with Progress() as progress:
        task = progress.add_task(f"[green]Inserting {continent} data...", total=total_tasks)
        
        for country, provinces in data.items():
            country_id = insert_country(cursor, db_type, country, continent)
            if country_id:
                progress.update(task, advance=1)
                for province, cities in provinces.items():
                    province_id = insert_province(cursor, db_type, province, country_id)
                    if province_id:
                        progress.update(task, advance=1)
                        for city in cities:
                            insert_city(cursor, db_type, city, province_id)
                            progress.update(task, advance=1)
                            time.sleep(0.1)  # Simulate processing time
    console.print(f"[green]Successfully inserted data for {continent}[/green]")

def run_cli(args):
    if args.db_type == 'sqlite':
        conn = connect_db(args.db_type, None, None, None, args.database, None)
    else:
        conn = connect_db(args.db_type, args.host, args.user, args.password, args.database, args.port)
    
    cursor = conn.cursor()
    
    if create_tables(cursor, args.db_type):
        console.print("[green]Database tables created successfully[/green]")
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            name = Prompt.ask("Enter country name")
            continent = Prompt.ask("Enter continent")
            country_id = insert_country(cursor, args.db_type, name, continent)
            if country_id:
                console.print(f"[green]Country '{name}' inserted successfully[/green]")
        
        elif choice == '2':
            console.print("\nAvailable continents: " + ", ".join(GEO_DATA.keys()))
            continent = Prompt.ask("Enter continent name")
            insert_continent_data(cursor, args.db_type, continent)
        
        elif choice == '3':
            countries = display_countries(cursor)
            if not countries:
                continue
            country_id = Prompt.ask("Enter country ID")
            if not any(country[0] == country_id for country in countries):
                console.print("[red]Invalid country ID[/red]")
                continue
            name = Prompt.ask("Enter province name")
            province_id = insert_province(cursor, args.db_type, name, country_id)
            if province_id:
                console.print(f"[green]Province '{name}' inserted successfully[/green]")
        
        elif choice == '4':
            countries = display_countries(cursor)
            if not countries:
                continue
            country_id = Prompt.ask("Enter country ID")
            if not any(country[0] == country_id for country in countries):
                console.print("[red]Invalid country ID[/red]")
                continue
            provinces = display_provinces(cursor, country_id)
            if not provinces:
                continue
            province_id = Prompt.ask("Enter province ID")
            if not any(province[0] == province_id for province in provinces):
                console.print("[red]Invalid province ID[/red]")
                continue
            name = Prompt.ask("Enter city name")
            city_id = insert_city(cursor, args.db_type, name, province_id)
            if city_id:
                console.print(f"[green]City '{name}' inserted successfully[/green]")
        
        elif choice == '5':
            break
    
    cursor.close()
    conn.close()
    console.print("[cyan]Goodbye![/cyan]")