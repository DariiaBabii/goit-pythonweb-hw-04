import argparse
import asyncio
from pathlib import Path
import logging
from aiofiles.os import makedirs, rename

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("errors.log"), logging.StreamHandler()]
)

async def read_folder(source: Path, destination: Path):
    try:
        for item in source.iterdir():
            if item.is_dir():
                await read_folder(item, destination)
            elif item.is_file():
                await sort_file(item, destination)
    except Exception as e:
        logging.error(f"An error occurred while reading the folder {source}: {e}")

async def sort_file(file_path: Path, destination: Path):
    try:
        ext = file_path.suffix.lstrip('.').lower() or "others"
        dest_folder = destination / ext

        await makedirs(dest_folder, exist_ok=True)

        dest_file = dest_folder / file_path.name
        await rename(file_path, dest_file)
        logging.info(f"File {file_path} copied to {dest_file}")
    except Exception as e:
        logging.error(f"An error occurred while copying the file {file_path}: {e}")


async def main():
    parser = argparse.ArgumentParser(description="Copy or process files from source to destination.")
    
    parser.add_argument(
        '-s', '--source', 
        required=True, 
        type=str, 
        help="Path to the source folder"
    )
    parser.add_argument(
        '-d', '--destination', 
        required=True, 
        type=str, 
        help="Path to the output folder")
    args = parser.parse_args()

    source = Path(args.source)
    destination = Path(args.destination)

    if not source.exists() or not source.is_dir():
        logging.error("The specified output folder does not exist or is not a folder.")
        return
    
    await makedirs(destination, exist_ok=True)
    await read_folder(source, destination)

if __name__ == "__main__":
    asyncio.run(main())