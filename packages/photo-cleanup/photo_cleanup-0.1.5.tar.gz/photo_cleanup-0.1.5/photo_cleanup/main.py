import typer
from typing import Optional
from typing_extensions import Annotated
from pathlib import Path
from rich.console import Console

app = typer.Typer()

_RAW_EXTENSIONS = ['.ARW','.DNG','.NEF','.RAW']
_IMAGE_EXTENSIONS = ['.JPG', '.JPEG']

stderr = Console(stderr=True)
stdout = Console(stderr=False)

def cleandir(dir: Path, dry_run: bool ):
    for entry in dir.iterdir():
        if entry.is_dir():
            # Skip special directories like #Recycle and #snapshot
            if entry.name[0] != "#":               
                cleandir(entry, dry_run)
        else:
            if entry.suffix in _RAW_EXTENSIONS:
                for ext in _IMAGE_EXTENSIONS:
                    candidate = entry.with_suffix(ext)
                    if candidate.exists():
                        if not dry_run:
                            candidate.unlink()
                        stdout.print(candidate.absolute())

@app.command()
def main(startdir: Annotated[Path, typer.Argument()] = "./", dry_run: Annotated[Optional[bool],typer.Option()] = False ):
    """
    Photo cleanup tool. Recursively deletes unnecessary JPG files in a folder when a matching RAW file with extensions ['.ARW','.DNG','.NEF','.RAW'] exists
    """
    stderr.print(f"Cleaning files recursively from {startdir.absolute()}")
    if dry_run:
        stderr.print("Dry run, no files will be deleted",)
    cleandir(startdir, dry_run)
    
    
if __name__ == "__main__":
    app()
    
    