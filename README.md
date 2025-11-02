# Larapy Installer

CLI tool for creating new Larapy framework projects.

## Installation

```bash
pip install larapy-installer
```

## Usage

### Create New Project

```bash
larapy new my-project
```

### Use Specific Template

```bash
larapy new my-api --template=api
larapy new my-app --template=full
larapy new prototype --template=minimal
```

### With Options

```bash
larapy new my-project --git --force
larapy new my-api --template=api --database=postgresql
```

### List Available Templates

```bash
larapy templates
```

### List Framework Versions

```bash
larapy versions
```

### Show Installer Version

```bash
larapy version
```

## Available Templates

- **default**: Full-featured web application with authentication, database, and views
- **api**: RESTful API application optimized for building backend services
- **minimal**: Minimal setup with core features only, perfect for quick prototypes
- **full**: Complete application with all features, admin panel, and frontend tools

## Command Options

### `larapy new <name>`

Create a new Larapy project.

Options:
- `--template, -t`: Template to use (default: default)
- `--python, -p`: Python version (default: 3.11)
- `--database, -d`: Database type (default: sqlite)
- `--git, -g`: Initialize git repository
- `--force, -f`: Force overwrite existing directory

## Development

```bash
git clone https://github.com/larapy-lab/installer
cd installer
pip install -e ".[dev]"
```

## Testing

```bash
pytest tests/
```

## License

MIT License. See [LICENSE](LICENSE) for details.
