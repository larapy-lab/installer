import httpx
from rich.console import Console
from rich.table import Table

console = Console()


def list_versions():
    """
    List available Larapy framework versions from PyPI.
    """
    console.print("\n[bold cyan]Available Larapy Framework Versions[/bold cyan]\n")
    
    try:
        response = httpx.get("https://pypi.org/pypi/larapy-framework/json", timeout=10.0)
        
        if response.status_code == 200:
            data = response.json()
            versions = sorted(
                data["releases"].keys(),
                key=lambda v: [int(x) for x in v.split('.') if x.isdigit()],
                reverse=True
            )
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Version", style="cyan", width=15)
            table.add_column("Release Date", style="white")
            
            for version in versions[:15]:
                releases = data["releases"][version]
                if releases:
                    upload_time = releases[0].get("upload_time", "Unknown")
                    if upload_time != "Unknown":
                        upload_time = upload_time.split('T')[0]
                    table.add_row(version, upload_time)
            
            console.print(table)
            console.print()
            console.print(f"[dim]Latest version: {versions[0]}[/dim]\n")
        else:
            console.print("[red]Error:[/red] Failed to fetch versions from PyPI")
            console.print("[yellow]Note:[/yellow] larapy-framework package may not be published yet")
            
    except httpx.RequestError as e:
        console.print(f"[red]Error:[/red] Network error: {str(e)}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
