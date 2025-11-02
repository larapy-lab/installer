import re
from rich.console import Console

console = Console()


def validate_project_name(name: str):
    """
    Validate project name follows Python package naming conventions.
    """
    if not re.match(r'^[a-z][a-z0-9_-]*$', name):
        console.print("[red]Error:[/red] Invalid project name")
        console.print("Project name must:")
        console.print("  - Start with a lowercase letter")
        console.print("  - Contain only lowercase letters, numbers, hyphens, and underscores")
        console.print("\nValid examples: my-project, blog_app, api2")
        raise SystemExit(1)
    
    if name in ['test', 'tests', 'lib', 'src', 'bin']:
        console.print(f"[red]Error:[/red] '{name}' is a reserved name")
        raise SystemExit(1)
