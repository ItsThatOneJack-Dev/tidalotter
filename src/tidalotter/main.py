import requests
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, TransferSpeedColumn
from rich.console import Console
import sys
from sys import exit
from typing import Tuple
from urllib.parse import quote
import re
from pathlib import Path

def downloadfile(URL:str, Filename:str, Timeout:Tuple[int,int]|int=10):
    console = Console()
    
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
        expand=False,
        transient=True,
    ) as progress:
        
        connect_task = progress.add_task("[green]  [bold]\\[INFO][/bold] Connecting to server...", total=None)
        
        try:
            response = requests.get(URL, stream=True, timeout=Timeout)
            
            if response.status_code == 404:
                progress.update(connect_task, description="[red][bold] \\[ERROR][/bold] Received HTTP response code 404 (Not Found).")
                console.print("[red][bold] \\[ERROR][/bold] Otter LLC's TIDAL download API returned a 404!")
                console.print("[red]        Here are some common steps to fix this:")
                console.print("[red]          - Be more specific in your query.")
                console.print("[red]          - Include the artist's name in your query.")
                console.print(f"[dim]URL: {URL}")
                return False
            
            if response.status_code != 200:
                progress.update(connect_task, description=f"[red][bold] \\[ERROR][/bold] Received HTTP response code {response.status_code}.")
                console.print(f"[red][bold] \\[ERROR][/bold] Otter LLC's TIDAL download API returned a {response.status_code}!")
                console.print(f"[red]        The API could be down currently, try again later!")
                console.print(f"[green]       URL: {URL}")
                return False
            
            total_size = int(response.headers.get('content-length', 0))
            
            progress.remove_task(connect_task)
            
            if total_size > 0:
                download_task = progress.add_task(
                    f"[green]  [bold]\\[INFO][/bold] Downloading {Path(Filename).name}...", 
                    total=total_size
                )
            else:
                download_task = progress.add_task(
                    f"[green]  [bold]\\[INFO][/bold] Downloading {Path(Filename).name} (unknown size)...", 
                    total=None
                )
                 
            downloaded = 0
            with open(Filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress.update(download_task, advance=len(chunk))
                        else:
                            progress.update(download_task, advance=len(chunk))
            
            progress.update(download_task, description=f"[green]  [bold]\\[INFO][/bold] Downloaded {Path(Filename).name}.")
            console.print(f"[green]  [bold]\\[INFO][/bold] Successfully downloaded: {Path(Filename).name}!")
            console.print(f"[green]         Size: {downloaded:,} bytes.")
            return True
            
        except requests.exceptions.Timeout:
            progress.update(connect_task, description="[red][bold] \\[ERROR][/bold] Connection timeout.")
            console.print("[red][bold] \\[ERROR][/bold] Otter LLC's TIDAL download API did not respond within 10 seconds!")
            console.print("[red]        The API could be down currently, try again later!")
            return False
            
        except requests.exceptions.ConnectionError:
            progress.update(connect_task, description="[red][bold] \\[ERROR][/bold] Connection failed.")
            console.print("[red][bold] \\[ERROR][/bold] Otter LLC's TIDAL download API could not be connected to!")
            console.print("[red]        The API could be down currently, try again later!")
            return False
            
        except requests.exceptions.RequestException as e:
            progress.update(connect_task, description="[red][bold] \\[ERROR][/bold] Request failed.")
            console.print("[red][bold] \\[ERROR][/bold] Otter LLC's TIDAL download API could not be connected to!")
            console.print("[red][bold] \\[ERROR][/bold] The following exception occured, preventing a connection:")
            console.print(f"[red]           '{str(e)}'")
            return False
            
        except Exception as e:
            progress.update(connect_task, description="[red][bold] \\[ERROR][/bold] Unexpected error.")
            console.print("[red][bold] \\[ERROR][/bold] Otter LLC's TIDAL download API could not be connected to!")
            console.print("[red][bold] \\[ERROR][/bold] The following exception occured, preventing a connection:")
            console.print(f"[red]           '{str(e)}'")
            return False

def helppage(console):
    console.print("[bold]TidalOtter")
    console.print("[bold](C) ItsThatOneJack")
    console.print("==================")
    console.print("[bold]Syntax:")
    console.print("    [bold]▪[/bold] tidalotter [query] <location> <flags>")
    console.print("")
    console.print("[bold]Examples:")
    console.print("    [bold]▪[/bold] tidalotter \"Affection Addiction\"")
    console.print("    [bold]▪[/bold] tidalotter \"Affection Addiction\" --lossless")
    console.print("    [bold]▪[/bold] tidalotter \"Affection Addiction\" \"C:\\Users\\Jack\\Downloads\"")
    console.print("")
    console.print("[bold]Flags:")
    console.print("    [bold]▪[/bold] \"-ll\" / \"--lossless\" [bold]—[/bold] Download the audio file at lossless quality.")
    console.print("    [bold]▪[/bold] \"-h\"  / \"--high\"     [bold]—[/bold] Download the audio file at high quality.")
    console.print("    [bold]▪[/bold] \"-l\"  / \"--low\"      [bold]—[/bold] Download the audio file at low quality.")
    console.print("    [bold]▪[/bold] \"-h\"  / \"--help\"     [bold]—[/bold] Show this help page.")
    console.print("")
    console.print("[bold]Notes:")
    console.print("    [bold]▪[/bold] When using [bold]lossless[/bold] quality, the outputted file will be of [bold]FLAC[/bold] filetype.")
    console.print("      This is due to how TIDAL only offers [bold]M4A[/bold] files using AAC, a lossy encoding.")
    console.print("    [bold]▪[/bold] When using [bold]high[/bold] or [bold]low[/bold] quality, the outputted file will be of [bold]M4A[/bold] filetype.")
    console.print("      This is due to how [bold]FLAC[/bold] files are inherently [bold]lossless[/bold], and cannot be made lower quality.")
    console.print("    [bold]▪[/bold] Not choosing a quality will result in [bold]low[/bold] quality being used.")
    console.print("    [bold]▪[/bold] The provided location must be a directory, and the path may not include missing directories.")
    console.print("    [bold]▪[/bold] Providing no arguments will result in this help page being displayed.")
    console.print("    [bold]▪[/bold] Providing no location will result in the file being stored within your current working directory.")

def downloadTrack(query:str, location:str, quality:str, timeout:int=10) -> None:
    """Download a track from TIDAL, as the file `location`, with quality `quality`.

    You are expected to validate your inputs prior to calling this function.

    Arguments:
        query:str - The query string to use to find the track.
        location:str - The filename (or directory) to save the track as.
        quality:str - The quality ("LOSSLESS", "HIGH" or "LOW") to use.
        timeout:int - The maximum number of seconds to wait before timing out and erroring.

    Returns:
        None
    """
    if quality.lower() not in ["LOSSLESS","HIGH","LOW"]:raise ValueError(f"quality must be one of: 'LOSSLESS', 'HIGH', 'LOW'!")
    url = f"https://otter.llc/{quote(query)}?download=1&format={'m4a' if quality in ['LOW','HIGH'] else 'flac'}&quality={quality.upper()}"
    downloadfile(url, location, timeout)

def main():
    console = Console()

    processed_arguments = sys.argv[1:]

    query = ""
    location = ""
    flags = []
    
    if len(processed_arguments) > 0:
        query = processed_arguments[0]
    else:
        if processed_arguments == []:
            helppage(console)
            exit(0)
            
    if len(processed_arguments) > 1:
        if not processed_arguments[1].startswith("-"):
            location = processed_arguments[1]
            if len(processed_arguments) > 2:
                flags = processed_arguments[2:]
        else:
            flags = processed_arguments[1:]
    
    if query == "":
        helppage(console) 
        exit(0)
        
    unrecognised_flags = False
    for flag in flags:
        clean_flag = flag.lstrip("-").lower()
        if clean_flag not in ["ll","lossless","h","high","l","low","help"]:
            console.print(f"[red][bold]\\[ERROR][/bold] '{flag}' is not a recognised flag.")
            unrecognised_flags = True
    if unrecognised_flags:
        exit(1)
        
    if any(flag.lstrip("-").lower() in ["h", "help"] for flag in flags):
        helppage(console)
        exit(0)

    clean_flags = [flag.lstrip("-").lower() for flag in flags]
    
    quality_levels = [
        bool({"l", "low"} & set(clean_flags)),
        bool({"h", "high"} & set(clean_flags)),
        bool({"ll", "lossless"} & set(clean_flags))
    ]

    if sum(quality_levels) > 1:
        console.print("[red][bold] \\[ERROR][/bold] You cannot use multiple quality flags together!")
        exit(1)

    quality = ["LOW","HIGH","LOSSLESS"][next((i for i, x in enumerate(quality_levels) if x), None) or 0]

    if location == "":
        location = re.sub(r'[^A-Za-z0-9\s.+_]', '_', query)+(".m4a" if quality in ["LOW", "HIGH"] else ".flac")
    else:
        path = Path(location)
        if path.exists():
            if path.is_file():
                console.print(f"[red][bold] \\[ERROR][/bold] Location points to a file!")
                exit(1)
            elif path.is_dir():
                location = str(path / (re.sub(r'[^A-Za-z0-9\s.+_]', '_', query)+(".m4a" if quality in ["LOW", "HIGH"] else ".flac")))
        else:
            current = path
            while current != current.parent:
                if current.parent.exists():
                    console.print(f"[red][bold] \\[ERROR][/bold] Non-existent folder in path: '{current}'.")
                    exit(1)
                current = current.parent
            console.print(f"[red][bold] \\[ERROR][/bold] Location includes a non-existent directory!")
            exit(1)

    downloadTrack(query,location,quality,10)

if __name__ == "__main__":
    main()