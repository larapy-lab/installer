import typer
from rich.console import Console
from typing import Optional
from larapy_installer.commands.new import create_new_project
from larapy_installer.commands.templates import list_templates
from larapy_installer.commands.versions import list_versions
from larapy_installer import __version__

app = typer.Typer(
    name="larapy",
    help="Larapy Framework Installer - Create new Larapy projects with ease",
    add_completion=False,
)

console = Console()


@app.command()
def new(
    name: str = typer.Argument(..., help="Project name"),
    template: str = typer.Option("default", "--template", "-t", help="Project template (default, api, minimal, full)"),
    python: str = typer.Option("3.11", "--python", "-p", help="Python version to use"),
    database: str = typer.Option("sqlite", "--database", "-d", help="Database type (sqlite, postgresql, mysql)"),
    git: bool = typer.Option(False, "--git", "-g", help="Initialize git repository"),
    force: bool = typer.Option(False, "--force", "-f", help="Force overwrite existing directory"),
):
    """
    Create a new Larapy project
    
    Examples:
    
        larapy new my-project
        
        larapy new my-api --template=api
        
        larapy new my-app --template=full --git
    """
    create_new_project(name, template, python, database, git, force)


@app.command()
def templates():
    """
    List available project templates
    """
    list_templates()


@app.command()
def versions():
    """
    List available Larapy framework versions
    """
    list_versions()


@app.command()
def version():
    """
    Show installer version
    """
    console.print(f"Larapy Installer v{__version__}")


def main():
    app()


if __name__ == "__main__":
    main()
