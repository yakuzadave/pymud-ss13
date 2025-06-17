import re
from pathlib import Path


def split_sections(raw_path: Path, out_dir: Path) -> None:
    if not raw_path.exists():
        print(f"Raw documentation not found at {raw_path}")
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    text = raw_path.read_text().strip()
    if not text:
        print("Raw documentation file is empty")
        return

    sections = re.split(r"^# ", text, flags=re.MULTILINE)
    for section in sections:
        if not section.strip():
            continue
        title, *body = section.splitlines()
        safe_title = re.sub(r"[^a-zA-Z0-9]+", "_", title.strip()).lower()
        dest = out_dir / f"{safe_title}.md"
        dest.write_text("# " + title + "\n" + "\n".join(body).strip() + "\n")
        print(f"Wrote {dest}")


def main() -> None:
    raw_file = Path('.github/ai-outputs/docs/generated-docs-raw.md')
    dest_dir = Path('docs/generated')
    split_sections(raw_file, dest_dir)


if __name__ == '__main__':
    main()
