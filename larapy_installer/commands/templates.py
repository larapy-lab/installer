from rich.console import Console
from rich.table import Table

console = Console()


def list_templates():
    """
    List available project templates with descriptions.
    """
    console.print("\n[bold cyan]Available Larapy Templates[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Template", style="cyan", width=15)
    table.add_column("Description", style="white")
    
    templates = [
        ("default", "Full-featured web application with authentication, database, and views"),
        ("api", "RESTful API application optimized for building backend services"),
        ("minimal", "Minimal setup with core features only, perfect for quick prototypes"),
        ("full", "Complete application with all features, admin panel, and frontend tools"),
    ]
    
    for name, description in templates:
        table.add_row(name, description)
    
    console.print(table)
    console.print()
    console.print("[dim]Usage: larapy new my-project --template=api[/dim]\n")
