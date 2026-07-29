import json
import re
from pathlib import Path

VIDEO_EXTENSIONS = {".mkv", ".mp4", ".avi"}


def load_names():
    with open("names.json", "r", encoding="utf-8") as f:
        return json.load(f)


def rename_files():
    folder = Path.cwd()
    names = load_names()

    renamed = 0
    skipped = 0
    report = []

    for file in folder.iterdir():

        if not file.is_file():
            continue

        if file.suffix.lower() not in VIDEO_EXTENSIONS:
            continue

        # Etsii tiedostonimestä ensimmäisen numeron (01, XY001, SM049...)
        match = re.search(r"(\d{2,3})", file.stem)

        if not match:
            skipped += 1
            report.append(f"Ei jaksonumeroa: {file.name}")
            continue

        number = match.group(1)[-2:]  # 001 -> 01

        if number not in names:
            skipped += 1
            report.append(f"Numeroa {number} ei löydy names.json: {file.name}")
            continue

        new_name = f"{number} - {names[number]}{file.suffix}"

        target = folder / new_name

        if target.exists():
            skipped += 1
            report.append(f"On jo olemassa: {new_name}")
            continue

        file.rename(target)
        renamed += 1

    with open("rename_report.txt", "w", encoding="utf-8") as f:
        f.write(f"Nimetty: {renamed}\n")
        f.write(f"Ohitettu: {skipped}\n\n")

        for line in report:
            f.write(line + "\n")

    print("=" * 40)
    print("PokemonRenamer")
    print("=" * 40)
    print(f"Nimetty : {renamed}")
    print(f"Ohitettu: {skipped}")
    print("Raportti: rename_report.txt")


if __name__ == "__main__":
    rename_files()
