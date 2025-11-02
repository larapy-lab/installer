import subprocess
from pathlib import Path


def clone_repository(url: str, destination: str, branch: str = "main"):
    """
    Clone a git repository to the specified destination.
    """
    try:
        subprocess.run(
            ['git', 'clone', '--branch', branch, '--depth', '1', url, destination],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to clone repository: {e.stderr}")


def init_git_repo(path: str):
    """
    Initialize a new git repository and make initial commit.
    """
    try:
        subprocess.run(['git', 'init'], cwd=path, check=True, capture_output=True)
        subprocess.run(['git', 'add', '.'], cwd=path, check=True, capture_output=True)
        subprocess.run(
            ['git', 'commit', '-m', 'Initial commit'],
            cwd=path,
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to initialize git repository: {e.stderr}")
