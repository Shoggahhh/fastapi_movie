from rich import print
import typer
from typing import Annotated

from api.api_v1.auth.services import redis_tokens

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
        typer.Argument(help="The token ti check"),
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
