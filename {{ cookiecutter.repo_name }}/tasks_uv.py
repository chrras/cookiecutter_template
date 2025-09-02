import os

from invoke import Context, task

WINDOWS = os.name == "nt"
PROJECT_NAME = "{{ cookiecutter.project_name }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"

# Setup commands
@task
def create_venv(ctx: Context) -> None:
    """Create a uv environment with the given project name and Python version.

    Usage:
        invoke create_venv
        invoke create_venv --python=3.12.
    """
    ctx.run(f"uv venv --python {PYTHON_VERSION} .venv", echo=True, pty=not WINDOWS)

@task
def dependencies(ctx: Context) -> None:
    """Install project dependencies and activate the virtual environment."""
    ctx.run("uv sync", echo=True, pty=not WINDOWS)
    ctx.run("source .venv/bin/activate", echo=True, pty=not WINDOWS)

# Project commands
@task
def preprocess_data(ctx: Context) -> None:
    """Preprocess data."""
    ctx.run(f"uv run src/{PROJECT_NAME}/data.py data/raw data/processed", echo=True, pty=not WINDOWS)

@task
def train(ctx: Context) -> None:
    """Train model."""
    ctx.run(f"uv run src/{PROJECT_NAME}/train.py", echo=True, pty=not WINDOWS)

@task
def test(ctx: Context) -> None:
    """Run tests."""
    ctx.run("uv run coverage run -m pytest tests/", echo=True, pty=not WINDOWS)
    ctx.run("uv run coverage report -m -i", echo=True, pty=not WINDOWS)

@task
def docker_build(ctx: Context, progress: str = "plain") -> None:
    """Build docker images."""
    ctx.run(
        f"docker build -t train:latest . -f dockerfiles/train.dockerfile --progress={progress}",
        echo=True,
        pty=not WINDOWS
    )
    ctx.run(
        f"docker build -t api:latest . -f dockerfiles/api.dockerfile --progress={progress}",
        echo=True,
        pty=not WINDOWS
    )

# Documentation commands
@task
def build_docs(ctx: Context) -> None:
    """Build documentation."""
    ctx.run("uv run mkdocs build --config-file docs/mkdocs.yaml --site-dir build", echo=True, pty=not WINDOWS)

@task
def serve_docs(ctx: Context) -> None:
    """Serve documentation."""
    ctx.run("uv run mkdocs serve --config-file docs/mkdocs.yaml", echo=True, pty=not WINDOWS)
