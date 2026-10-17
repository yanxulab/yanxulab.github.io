"""Give each rendered page the stylesheet matching its build, bypassing stale CSS."""

import hashlib
import os
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site")
STYLE_LINK = re.compile(
    r"(?P<before>\bhref=[\"'])(?P<directory>(?:\.{1,2}/)*)"
    r"styles(?:\.[0-9a-f]{12})?\.css(?P<after>[\"'])"
)


def main():
    stylesheet = (OUTPUT / "styles.css").read_bytes()
    digest = hashlib.sha256(stylesheet).hexdigest()[:12]
    versioned = f"styles.{digest}.css"
    (OUTPUT / versioned).write_bytes(stylesheet)
    pages = 0
    for page in OUTPUT.rglob("*.html"):
        original = page.read_text(encoding="utf-8")
        updated, count = STYLE_LINK.subn(
            lambda match: (
                f"{match['before']}{match['directory']}{versioned}{match['after']}"
            ),
            original,
        )
        if count:
            pages += 1
            if updated != original:
                page.write_text(updated, encoding="utf-8")
    print(f"Stylesheet versioned: {versioned} ({pages} pages).")


if __name__ == "__main__":
    main()
