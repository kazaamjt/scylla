from pathlib import Path

import click
import colorama

from . import out

@click.command()
@click.option("-f", "--file", prompt="File with uri's", help="Path to a file containing urls.")
@click.option("-s", "--max-simultanious", default=5, help="Maximum number of simultanious files to download.")
@click.option("-v", "--verbose", count=True)
def main(file: str, max: int, verbose: int) -> None:
	colorama.init()
	out.set_level(verbose)

	file_path = Path(file)
	if not file_path.exists():
		out.error(f"No such file: {file}")

	with open(file_path, "r") as f:
		urls = f.read().splitlines()


if __name__ == "__main__":
	main()
