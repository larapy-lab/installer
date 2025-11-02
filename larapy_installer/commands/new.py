import os
import subprocess
import shutil
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from larapy_installer.utils.git import clone_repository, init_git_repo
from larapy_installer.utils.validation import validate_project_name

console = Console()


def create_new_project(name: str, template: str, python: str, database: str, git: bool, force: bool):
    """
    Create a new Larapy project by cloning the application template.
    """
    
    project_path = Path.cwd() / name
    
    if project_path.exists() and not force:
        console.print(f"[red]Error:[/red] Directory '{name}' already exists")
        console.print(f"Use --force to overwrite existing directory")
        return
    
    if project_path.exists() and force:
        console.print(f"[yellow]Warning:[/yellow] Removing existing directory '{name}'")
        shutil.rmtree(project_path)
    
    validate_project_name(name)
    
    template_branches = {
        'default': 'main',
        'api': 'api',
        'minimal': 'minimal',
        'full': 'full'
    }
    
    branch = template_branches.get(template, 'main')
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        task = progress.add_task("Creating Larapy project...", total=7)
        
        progress.update(task, description=f"Cloning {template} template...")
        clone_repository(
            url="https://github.com/larapy-lab/larapy",
            destination=str(project_path),
            branch=branch
        )
        progress.advance(task)
        
        progress.update(task, description="Removing .git directory...")
        git_dir = project_path / '.git'
        if git_dir.exists():
            shutil.rmtree(git_dir)
        progress.advance(task)
        
        progress.update(task, description="Configuring environment...")
        setup_environment(project_path, database)
        progress.advance(task)
        
        progress.update(task, description="Installing dependencies...")
        install_dependencies(project_path, python)
        progress.advance(task)
        
        progress.update(task, description="Generating application key...")
        generate_app_key(project_path)
        progress.advance(task)
        
        if git:
            progress.update(task, description="Initializing git repository...")
            init_git_repo(str(project_path))
        progress.advance(task)
        
        progress.update(task, description="Finalizing setup...")
        progress.advance(task)
    
    console.print(f"\n[green]Project '{name}' created successfully![/green]\n")
    console.print("[bold]Next steps:[/bold]")
    console.print(f"  cd {name}")
    console.print(f"  python artisan migrate")
    console.print(f"  python artisan serve")
    console.print(f"\n[dim]Visit: http://localhost:8000[/dim]\n")


def setup_environment(project_path: Path, database: str):
    """
    Copy .env.example to .env and configure database.
    """
    env_example = project_path / '.env.example'
    env_file = project_path / '.env'
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        
        if database != 'sqlite':
            with open(env_file, 'r') as f:
                content = f.read()
            
            content = content.replace('DB_CONNECTION=sqlite', f'DB_CONNECTION={database}')
            
            if database == 'postgresql':
                content = content.replace(
                    'DB_DATABASE=storage/database.sqlite',
                    'DB_DATABASE=larapy\nDB_HOST=localhost\nDB_PORT=5432\nDB_USERNAME=postgres\nDB_PASSWORD='
                )
            elif database == 'mysql':
                content = content.replace(
                    'DB_DATABASE=storage/database.sqlite',
                    'DB_DATABASE=larapy\nDB_HOST=localhost\nDB_PORT=3306\nDB_USERNAME=root\nDB_PASSWORD='
                )
            
            with open(env_file, 'w') as f:
                f.write(content)


def install_dependencies(project_path: Path, python: str):
    """
    Install project dependencies using pip.
    """
    try:
        result = subprocess.run(
            ['pip', 'install', '-e', '.'],
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            console.print(f"[yellow]Warning:[/yellow] Failed to install dependencies")
            console.print(f"[dim]{result.stderr}[/dim]")
    except subprocess.TimeoutExpired:
        console.print(f"[yellow]Warning:[/yellow] Dependency installation timed out")
    except Exception as e:
        console.print(f"[yellow]Warning:[/yellow] {str(e)}")


def generate_app_key(project_path: Path):
    """
    Generate application encryption key.
    """
    env_file = project_path / '.env'
    
    if env_file.exists():
        import secrets
        key = secrets.token_urlsafe(32)
        
        with open(env_file, 'r') as f:
            content = f.read()
        
        if 'APP_KEY=' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('APP_KEY='):
                    lines[i] = f'APP_KEY={key}'
                    break
            content = '\n'.join(lines)
        else:
            content += f'\nAPP_KEY={key}\n'
        
        with open(env_file, 'w') as f:
            f.write(content)
