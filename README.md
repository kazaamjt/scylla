# Scylla

Scyla downloads files in parallel.  
It is aimed at speeding up concurrent downloads, not at being as fast as possible per download.  
There are probably a bunch of tools out there that are faster, as that is not scylas goal.  
The reason scylla exists is because I had to repeatedly download a bunch of files and it took a while with `wget`.  

It can be used from the command line or as importable module.  
From the commandline it is quite easy to use:  

```bash
kazaamjt@workstation:~$ scylla -f url_list -o artifacts/
```

Alternativly you can import the module from in a script.  

## CLI Options

As mentioned, the CLI is quite simple, it does not have many options:  

```bash
kazaamjt@workstation:~$ scylla --help
Usage: scylla [OPTIONS]

Options:
  -f, --file TEXT               Path to a file containing urls.
  -o, --output-dir TEXT         Directory to store the retrieved files.
  -s, --max-concurrent INTEGER  Maximum number of simultanious files to
                                download. Setting this to 0 will make scylla
                                try to download all the files at once.
  --help                        Show this message and exit.
```

## Using as a module

Using as a module is also not very difficult.  
Do note that the module uses `async`, so it does have some gotchas.  
Also note that the module is fully typed, hopefully making its usage easier.  

To use it simply import the module and instantiate the `Downloader` class:  

```Python
import asyncio
from pathlib import Path

import scylla

urls = [
    "https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.10.17.tar.xz",
    "https://example.com/",
]

async def main() -> None:
    downloader = Downloader(urls, Path("."))
    await downloader.start()

if __name__ == "__main__":
    asyncio.run(main())
```

The most important gotcha here is making sure the `downloader` class is instantiated in
the same event-loop as `Downloader.start` is called from.  
We do this here by wrapping them in a single `async` function.  

And that's it really.  

The class has a couple more init parameters that are more for advanced usage:

    - max_concurrent: int = 5  
      Same as the CLI, this changes the maximum number of downloads that run simultaniously.  
    - chunk_report_cb: Optional[ChunkReportCallback] = None  
      The function passed to this parameter will be called everytime a chunk was succesfully downloaded and saved.  
      Usefull for tracking download progress.  
    - report_done_cb: Optional[Callable[[str], None]] = None  
      The function passed to this parameter will be called everytime a download is completed.  
      The parameter being passed back is the name of the file.  



