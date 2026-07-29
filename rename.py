import json
import re
from pathlib import Path

VIDEO_EXTENSIONS = {".mkv", ".mp4", ".avi"}
BAD_CHARS = {"�", "├", "Â", "Ã"}


def load_names():
    with open("names.json", "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_title(title: str) -> str:
    """Poistaa välimerkit ja ylimääräiset välilyönnit vertailua varten."""
    title = re.sub(r"[!?.,:;\"']", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.strip().lower()


def is_video(file: Path) -> bool:
    return file.suffix.lower() in VIDEO_EXTENSIONS


def has_bad_chars(text: str) -> bool:
    return any(ch in text for ch in BAD_CHARS)


def build_lookup(names):
    lookup = {}
    for eng, fin in names.items():
        lookup[normalize_title(eng)] = fin
    return lookup


def rename_files(folder: Path):
    names = load_names()
    lookup = build_lookup(names)

    renamed = 0
    skipped = 0
    missing = []
    bad = []

    for file in folder.iterdir():

        if not file.is_file():
            continue

        if not is_video(file):
            continue

        match = re.match(r"^(\d+)\s*-\s*(.+)$", file.stem)

        if not match:
            skipped += 1
            continue

        episode = match.group(1).zfill(2)
        english = normalize_title(match.group(2))

        if english not in lookup:
            missing.append(file.name)
            continue

        finnish = lookup[english]

        if has_bad_chars(finnish):
            bad.append(finnish)

        new_file = folder / f"{episode} - {finnish}{file.suffix}"

        if new_file.exists():
            skipped += 1
            continue

        file.rename(new_file)
        renamed += 1

    report = folder / "rename_report.txt"

    with open(report, "w", encoding="utf-8") as f:
        f.write("PokemonRenamer raportti\n")
        f.write("=" * 40 + "\n\n")

        f.write(f"Nimetty: {renamed}\n")
        f.write(f"Ohitettu: {skipped}\n\n")

        f.write("Ei löytynyt nimikartasta:\n")
        if missing:
            for item in missing:
                f.write(f" - {item}\n")
        else:
            f.write(" Ei yhtään\n")

        f.write("\nMahdollinen merkistövirhe:\n")
        if bad:
            for item in bad:
                f.write(f" - {item}\n")
        else:
            f.write(" Ei yhtään\n")

    print("=" * 40)
    print("PokemonRenamer")
    print("=" * 40)
    print(f"Nimetty : {renamed}")
    print(f"Ohitettu: {skipped}")
    print(f"Raportti: {report}")


if __name__ == "__main__":
    rename_files(Path.cwd())
