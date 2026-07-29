import json
import re
from pathlib import Path

VIDEO_EXTENSIONS = {".mkv", ".mp4", ".avi"}


def load_names():
    with open("names.json", "r", encoding="utf-8") as f:
        return json.load(f)


def is_video(file: Path):
    return file.suffix.lower() in VIDEO_EXTENSIONS


def has_bad_chars(text):
    bad = ["�", "├", "Â", "Ã"]
    return any(ch in text for ch in bad)


def rename_files(folder: Path):
    names = load_names()

    renamed = 0
    skipped = 0
    bad_files = []
    missing = []

    for file in folder.iterdir():

        if not is_video(file):
            continue

        stem = file.stem

        m = re.match(r"^(\d+)\s*-\s*(.+)$", stem)

        if not m:
            skipped += 1
            continue

        number = m.group(1)
        english = m.group(2)

        if english not in names:
            missing.append(file.name)
            continue

        finnish = names[english]

        new_name = f"{number.zfill(2)} - {finnish}{file.suffix}"

        if has_bad_chars(new_name):
            bad_files.append(new_name)

        target = folder / new_name

        if target.exists():
            continue

        file.rename(target)
        renamed += 1

    report = folder / "rename_report.txt"

    with open(report, "w", encoding="utf-8") as f:

        f.write(f"Nimetty: {renamed}\n")
        f.write(f"Ohitettu: {skipped}\n\n")

        f.write("Puuttuvat nimet:\n")

        for item in missing:
            f.write(item + "\n")

        f.write("\nEpäilyttävät nimet:\n")

        for item in bad_files:
            f.write(item + "\n")

    print()
    print("========================")
    print("Valmis!")
    print("========================")
    print(f"Nimetty: {renamed}")
    print(f"Ohitettu: {skipped}")
    print("Raportti tallennettu:")
    print(report)


if __name__ == "__main__":
    rename_files(Path.cwd())
