"""Version the stylesheet and interaction scripts to avoid stale cached layouts."""

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
SCRIPT_LINK = re.compile(
    r"(?P<before>\bsrc=[\"'])(?P<directory>(?:\.{1,2}/)*|/)"
    r"assets/(?P<name>site|figure-viewer)(?:\.[0-9a-f]{12})?\.js(?P<after>[\"'])"
)


def main():
    stylesheet = (OUTPUT / "styles.css").read_bytes()
    digest = hashlib.sha256(stylesheet).hexdigest()[:12]
    versioned = f"styles.{digest}.css"
    (OUTPUT / versioned).write_bytes(stylesheet)
    script_versions = {}
    for name in ("site", "figure-viewer"):
        script = (OUTPUT / "assets" / f"{name}.js").read_bytes()
        script_digest = hashlib.sha256(script).hexdigest()[:12]
        versioned_script = f"{name}.{script_digest}.js"
        (OUTPUT / "assets" / versioned_script).write_bytes(script)
        script_versions[name] = versioned_script
    pages = 0
    for page in OUTPUT.rglob("*.html"):
        original = page.read_text(encoding="utf-8")
        updated, count = STYLE_LINK.subn(
            lambda match: (
                f"{match['before']}{match['directory']}{versioned}{match['after']}"
            ),
            original,
        )
        updated, script_count = SCRIPT_LINK.subn(
            lambda match: (
                f"{match['before']}{match['directory']}assets/{script_versions[match['name']]}{match['after']}"
            ),
            updated,
        )
        if count:
            pages += 1
        if (count or script_count) and updated != original:
            page.write_text(updated, encoding="utf-8")
    print(f"Stylesheet versioned: {versioned} ({pages} pages).")
    print(f"Interactions versioned: {', '.join(script_versions.values())}.")


if __name__ == "__main__":
    main()
