from rich import print
import typer
from typing import Annotated

from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens
import secrets

app = typer.Typer(
    name="token",
    help="Tokens management.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(help="The token to check"),
    ],
):
    """
    Check if the passed token is valid - exists or not.
    """
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[bold green]exist[/bold green]."
            if redis_tokens.token_exist(token)
            else "[bold red]doesn't exist[/bold red]"
        ),
    )


@app.command(name="list")
def list_tokens():
    """
    Get all tokens
    """
    print(Markdown("# Available API Tokens"))
    print(Markdown("\n- ".join([""] + redis_tokens.get_tokens())))
    print()


@app.command(name="create")
def create_token():
    """
    Create token
    """
    print(secrets.token_urlsafe(16))


@app.command(name="add")
def add_token(
    token: Annotated[
        str,
        typer.Argument(help="Token to add"),
    ],
):
    """
    Add token
    """
    redis_tokens.add_token(token)
    print(f"Token [bold]{token}[/bold] [bold green]added[/bold green].")


@app.command(name="delete")
def delete_token(
    token: Annotated[
        str,
        typer.Argument(help="Token to delete"),
    ],
):
    """
    Delete token
    """
    redis_tokens.delete_token(token)
    print(f"Token [bold]{token}[/bold] [bold green]deleted[/bold green].")
