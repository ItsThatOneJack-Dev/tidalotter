# TidalOtter

TidalOtter, the easy TIDAL download client!

TidalOtter is a CLI (Command Line Interface) for Otter LLC (oterin)'s TIDAL download API.
It provides an easy way to download music as either FLAC files, or M4A files!

## Usage

### Syntax

`tidalotter [query] <location> <flags>`

### Examples

- `tidalotter`
- `tidalotter "Affection Addiction"`
- `tidalotter "Affection Addiction" --lossless`
- `tidalotter "Affection Addiction" "C:\Users\Jack\Downloads"`
- `tidalotter "Affection Addiction" "C:\Users\Jack\Downloads" --lossless`

### Flags

- `-ll`/`--lossless` — Download the audio file at lossless quality.
- `-h`/`--high` — Download the audio file at high quality.
- `-l`/`--low` — Download the audio file at low quality.
- `-h`/`--help` — Show this help page.

### Notes

- When using `lossless` quality, the outputted file will be of `FLAC` filetype.
  This is due to how TIDAL only offers `M4A` files using AAC, a lossy encoding.
- When using `high` or `low` quality, the outputted file will be of `M4A` filetype.
  This is due to how `FLAC` files are inherently `lossless`, and cannot be made lower quality.
- Not choosing a quality will result in `low` quality being used.
- The provided location must be a directory, and the path may not include missing directories.
- Providing no arguments will result in this help page being displayed.
- Providing no location will result in the file being stored within your current working directory.
