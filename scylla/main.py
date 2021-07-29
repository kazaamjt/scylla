import asyncio
import time
from pathlib import Path
from typing import List

import click

from .downloader import GraphicDownloader

async def run(urls: List[str], output_dir: Path, max_concurrent: int) -> None:
	start = time.time()
	print(f"Downloading {len(urls)} files:")
	downloader = GraphicDownloader(urls, Path(output_dir), max_concurrent)
	await downloader.start()
	
	end = time.time()
	print()
	print("Finished downloading with ")
	print("Downloading all files took:", int(end - start), "seconds")
	if downloader.errors:
		print("errors:")
		for error in downloader.errors:
			print(f"\t{error.name}:", str(error.error))

@click.command()
@click.option("-f", "--file", prompt="File with urls", help="Path to a file containing urls.")
@click.option("-o", "--output-dir", prompt="Output dir path", help="Directory to store the retrieved files.")
@click.option(
	"-s", "--max-concurrent", default=5,
	help="Maximum number of simultanious files to download. "
	"Setting this to 0 will make scylla try to download all the files at once."
)
def main(
	file: str,
	output_dir: str,
	max_concurrent: int,
) -> None:
	file_path = Path(file)
	if not file_path.exists():
		print(f"No such file: {file}")

	with open(file_path, "r") as f:
		urls = f.read().splitlines()

	asyncio.run(run(urls, Path(output_dir), max_concurrent))


if __name__ == "__main__":
	main()
