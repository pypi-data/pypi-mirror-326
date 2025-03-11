# main.py
import configparser
import contextlib
import getpass
import os
import re
from pathlib import Path
from typing import Optional

import httpx
import typer
from appdirs import user_config_dir
from dotenv import load_dotenv
from rich.console import Console

# Load environment variables from .env file (if it exists)
load_dotenv()

# Initialize Rich consoles for output formatting
console = Console()
error_console = Console(stderr=True)


def get_config_path() -> Path:
    config_dir = user_config_dir("jinafetch")  # Remove ensure_exists parameter
    config_dir_path = Path(config_dir)
    config_dir_path.mkdir(parents=True, exist_ok=True)  # Manual directory creation
    return config_dir_path / "config.ini"


def ensure_api_key() -> str:
    """Get API key from env or config file, prompt if missing."""
    if api_key := os.getenv("JINA_API_KEY"):
        return api_key

    config_path = get_config_path()
    config = configparser.ConfigParser()

    with contextlib.suppress(Exception):
        config.read(config_path)
        if config.has_option("DEFAULT", "JINA_API_KEY"):
            return config.get("DEFAULT", "JINA_API_KEY")
    error_console.print("\n[bold yellow]First-time setup required![/]")
    error_console.print("1. Get your Jina API key from: [link]https://jina.ai/reader[/]")
    api_key = getpass.getpass("2. Enter your API key (input hidden): ").strip()

    config["DEFAULT"] = {"JINA_API_KEY": api_key}
    with config_path.open("w") as f:
        config.write(f)
    config_path.chmod(0o600)  # Secure file permissions

    error_console.print(f"\n✅ API key saved to [italic]{config_path}[/]")
    return api_key


app = typer.Typer()


@app.command()
def configure():
    """Update the stored JINA_API_KEY"""
    config_path = get_config_path()
    error_console.print("\n[bold yellow]Updating Jina API Key configuration[/]")

    new_key = getpass.getpass("Enter new API key (input hidden): ").strip()

    config = configparser.ConfigParser()
    config["DEFAULT"] = {"JINA_API_KEY": new_key}
    with config_path.open("w") as f:
        config.write(f)
    config_path.chmod(0o600)

    console.print(f"\n✅ [bold green]API key updated in[/] [italic]{config_path}[/]")


@app.command()
def show_config():
    """Display where the API key is stored"""
    config_path = get_config_path()
    console.print(f"\n🔑 Configuration file location: [italic]{config_path}[/]")
    console.print("To update the key: [bold cyan]jinafetch configure[/]")


# Define typer options at module level
_DEFAULT_OUTPUT = typer.Option(None, help="Optional path to save the output Markdown file.")


def sanitize_filename(url: str) -> str:
    """
    Generate a sanitized filename from the URL.
    If no sensible name can be inferred, return a random filename.
    """
    # Extract the last part of the URL after the last '/'
    match = re.search(r"([^/]+)\.?(?:html|htm|php|asp|aspx|jsp)?$", url)
    if match:
        return re.sub(r"[^a-zA-Z0-9_-]", "_", match[1]) + ".md"

    # Fallback to a random filename
    return f"output_{os.urandom(4).hex()}.md"


@app.command()
def fetch(
    url: str,
    output: Optional[Path] = _DEFAULT_OUTPUT,
):
    """
    Fetch content from the Jina Reader API and save it to a Markdown file.
    The API key is loaded from the environment variable JINA_API_KEY.
    """
    api_key = ensure_api_key()

    jina_url = f"https://r.jina.ai/{url}"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = httpx.get(jina_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        content = response.text
    except httpx.HTTPStatusError as e:
        error_console.print(f"[bold red]Error fetching content:[/] {e.response.status_code} - {e.response.text}")
        raise typer.Exit(code=1) from e
    except httpx.RequestError as e:
        error_console.print(f"[bold red]Request failed:[/] {e}")
        raise typer.Exit(code=1) from e

    # Determine the output file path
    if output is None:
        filename = sanitize_filename(url)
        output = Path.cwd() / filename
    else:
        output = output.resolve()

    # Save the content to the output file
    try:
        with output.open("w") as f:
            f.write(content)
        console.print(f"[bold green]Success:[/] Content saved to [italic]{output}[/]")
    except Exception as e:
        error_console.print(f"[bold red]Error saving file:[/] {e}")
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
