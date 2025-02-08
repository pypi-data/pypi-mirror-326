import typer

from .delooper import delooper


app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})
app.command()(delooper)


if __name__ == "__main__":
    app()