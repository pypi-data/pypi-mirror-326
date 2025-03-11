# main.py
import os
import re
from pathlib import Path
from typing import Optional

import httpx
import typer
from dotenv import load_dotenv
from rich.console import Console

# Load environment variables from .env file (if it exists)
load_dotenv()

# Initialize Rich consoles for output formatting
console = Console()
error_console = Console(stderr=True)

app = typer.Typer()

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
    api_key = os.getenv("JINA_API_KEY")
    if not api_key:
        error_console.print("[bold red]Error:[/] JINA_API_KEY is not set in the environment or .env file.")
        raise typer.Exit(code=1)

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
