import asyncio
import os
from pathlib import Path
import shutil
from argparse import ArgumentParser

async def copy_file(file_path, output_folder):
    try:
        file_extension = file_path.suffix.lstrip('.')
        if file_extension == '':
            file_extension = 'Void extention'
        destination_folder = output_folder / file_extension
        destination_folder.mkdir(parents=True, exist_ok=True)
        destination_path = destination_folder / file_path.name
        
        await asyncio.to_thread(shutil.copy2, file_path, destination_path)
        #print (f"Скопійовано файл {file_path} до {destination_path}")
    except Exception as e:
        print(f"Помилка {e} : {file_path} ")

async def read_folder(source_folder, output_folder):
    tasks = []
    try:
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = Path(root) / file
                #print (f"Прочитано {file_path}")
                tasks.append(copy_file(file_path, output_folder))
        
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Помилка {e} : {source_folder}")

async def main():
    parser = ArgumentParser()
    parser.add_argument("source", type=str)
    parser.add_argument("destination", type=str)

    args = parser.parse_args()
    source_folder = Path(args.source).resolve()
    output_folder = Path(args.destination).resolve()

    if not source_folder.exists():
        print(f"Папка {source_folder} не існує.")
        return

    if not output_folder.exists():
        output_folder.mkdir(parents=True, exist_ok=True)

    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    asyncio.run(main())
