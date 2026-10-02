"""Compile content/site.toml and snippets/ into dist/index.html."""

import html
import shutil
from pathlib import Path

from tools.manifest import Entry, Part, Section, Site, load_site
from tools.source import extract

ROOT = Path(__file__).resolve().parent.parent
SNIPPETS = ROOT / "snippets"
MANIFEST = ROOT / "content" / "site.toml"
WEB = ROOT / "web"
DIST = ROOT / "dist"


def fill(template: str, slots: dict[str, str]) -> str:
    """Replace every <!-- slot:name --> marker, failing on any miss."""
    for name, value in slots.items():
        marker = f"<!-- slot:{name} -->"
        if marker not in template:
            raise KeyError(f"template has no slot {name!r}")
        template = template.replace(marker, value)
    if "<!-- slot:" in template:
        raise KeyError("template has an unfilled slot")
    return template


def render_entry(entry: Entry) -> str:
    title = html.escape(entry.title)
    blocks = "\n".join(
        f"<pre><code>{html.escape(extract(SNIPPETS, ref))}</code></pre>"
        for ref in entry.code
    )
    return (
        f'<article class="entry" id="{entry.id}">'
        f"<h4>{title}</h4>{blocks}</article>"
    )


def render_section(section: Section) -> str:
    entries = "\n".join(
        render_entry(entry) for entry in section.entries
    )
    return (
        f'<section id="{section.id}">'
        f"<h3>{html.escape(section.title)}</h3>\n{entries}</section>"
    )


def render_part(part: Part) -> str:
    sections = "\n".join(render_section(s) for s in part.sections)
    return (
        f'<section class="part" id="{part.id}">'
        f"<h2>{html.escape(part.title)}</h2>\n{sections}</section>"
    )


def render_page(site: Site) -> str:
    template = (WEB / "template.html").read_text(encoding="utf-8")
    return fill(
        template,
        {
            "styles": (WEB / "styles.css").read_text(encoding="utf-8"),
            "content": "\n".join(render_part(p) for p in site.parts),
        },
    )


def build(output_dir: Path = DIST) -> Path:
    site = load_site(MANIFEST, SNIPPETS)
    page = render_page(site)
    shutil.rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True)
    index = output_dir / "index.html"
    index.write_text(page, encoding="utf-8")
    return index


if __name__ == "__main__":
    print(f"Built {build().relative_to(ROOT)}")
