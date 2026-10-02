"""Compile content/site.toml and snippets/ into dist/index.html."""

import html
import json
import re
import shutil
from pathlib import Path

from tools.highlight import highlight
from tools.manifest import (
    CodeRef,
    Entry,
    Part,
    Section,
    Site,
    Table,
    load_site,
)
from tools.results import asserts_as_results
from tools.source import extract
from tools.tokens import css_variables, load_tokens

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


INLINE_CODE = re.compile(r"`([^`]+)`")


def inline(text: str) -> str:
    """Escape text and turn `backticks` into <code> elements."""
    return INLINE_CODE.sub(r"<code>\1</code>", html.escape(text))


def render_code(ref: CodeRef) -> str:
    source = extract(SNIPPETS, ref)
    if ref.is_demo:
        source = asserts_as_results(source)
    return f"<pre><code>{highlight(source)}</code></pre>"


def render_table(table: Table) -> str:
    header = "".join(
        f"<th>{inline(cell)}</th>" for cell in table.header
    )
    rows = "".join(
        "<tr>"
        + "".join(f"<td>{inline(cell)}</td>" for cell in row)
        + "</tr>"
        for row in table.rows
    )
    return (
        f"<table><thead><tr>{header}</tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )


def render_meta(entry: Entry) -> str:
    if entry.table:
        return ""
    if entry.time:
        text = f"Time {entry.time} · Space {entry.space}"
    elif all(ref.is_class for ref in entry.code):
        text = "Definition"
    else:
        text = "Syntax"
    return f'<p class="meta">{html.escape(text)}</p>'


def render_entry(entry: Entry) -> str:
    parts = [
        f'<article class="entry" id="{entry.id}">',
        f'<h4><a href="#{entry.id}">{inline(entry.title)}</a></h4>',
        render_meta(entry),
    ]
    if entry.use_when:
        parts.append(
            '<p class="use-when"><span class="label">Use when:</span> '
            f"{inline(entry.use_when)}</p>"
        )
    parts.extend(render_code(ref) for ref in entry.code)
    if entry.table:
        parts.append(render_table(entry.table))
    if entry.gotcha:
        parts.append(
            '<p class="gotcha"><span class="label">Gotcha:</span> '
            f"{inline(entry.gotcha)}</p>"
        )
    parts.append("</article>")
    return "".join(parts)


def render_section(section: Section) -> str:
    intro = (
        f'<p class="section-intro">{inline(section.intro)}</p>'
        if section.intro
        else ""
    )
    entries = "\n".join(
        render_entry(entry) for entry in section.entries
    )
    return (
        f'<section class="section" id="{section.id}">'
        f"<h3>{inline(section.title)}</h3>{intro}\n{entries}</section>"
    )


def render_part(part: Part) -> str:
    sections = "\n".join(render_section(s) for s in part.sections)
    return (
        f'<section class="part" id="{part.id}">'
        f"<h2>{html.escape(part.title)}</h2>\n{sections}</section>"
    )


def toc_link(anchor: str, title: str) -> str:
    return f'<a href="#{anchor}">{inline(title)}</a>'


def render_toc(site: Site) -> str:
    parts = "".join(
        f"<li>{toc_link(part.id, part.title)}<ol>"
        + "".join(
            f"<li>{toc_link(section.id, section.title)}</li>"
            for section in part.sections
        )
        + "</ol></li>"
        for part in site.parts
    )
    return (
        '<nav class="toc" aria-label="Contents">'
        f'<p class="toc-title">Contents</p><ol>{parts}</ol></nav>'
    )


def jump_index(site: Site) -> str:
    """Return [id, title, context, keywords, kind] jump-list rows."""
    rows = []
    for part in site.parts:
        rows.append([part.id, part.title, "Part", "", "part"])
        for section in part.sections:
            rows.append(
                [section.id, section.title, part.title, "", "section"]
            )
            rows.extend(
                [
                    entry.id,
                    entry.title,
                    section.title,
                    " ".join(entry.aliases),
                    "entry",
                ]
                for entry in section.entries
            )
    # "</" would end the <script> element early
    return json.dumps(rows, separators=(",", ":")).replace("</", "<\\/")


def render_styles() -> str:
    tokens = load_tokens(WEB / "tokens.toml")
    styles = (WEB / "styles.css").read_text(encoding="utf-8")
    return css_variables(tokens) + styles


def render_page(site: Site) -> str:
    template = (WEB / "template.html").read_text(encoding="utf-8")
    return fill(
        template,
        {
            "styles": render_styles(),
            "toc": render_toc(site),
            "jump-index": jump_index(site),
            "script": (WEB / "app.js").read_text(encoding="utf-8"),
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
