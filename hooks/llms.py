"""Write llms.txt (index) and llms-full.txt (all pages) to the site root.

See https://llmstxt.org. Uses a hook to avoid extra build dependencies.
"""

import re
from pathlib import Path

INTRO = """# HOT Docs

> Documentation for the Humanitarian OpenStreetMap Team (HOT) open source
> mapping tools. They chain together into an end-to-end workflow: imagery
> (Drone TM, OpenAerialMap) -> digitisation (Tasking Manager, fAIr) -> field
> data (Field-TM, ChatMap) -> data access and sharing (Export Tool, Raw Data
> API, uMap). Start with the tools summary to choose tools for a project.
"""

TOOL_DOCS = [
    ("Tasking Manager", "https://hotosm.github.io/tasking-manager/"),
    ("Field-TM", "https://docs.field.hotosm.org/"),
    ("Drone TM", "https://docs.drone.hotosm.org/"),
    ("OpenAerialMap", "https://docs.imagery.hotosm.org/"),
    ("fAIr", "https://github.com/hotosm/fAIr/tree/develop/docs"),
    ("ChatMap", "https://github.com/hotosm/chatmap/tree/master/docs"),
    ("Raw Data API", "https://hotosm.github.io/raw-data-api/"),
    ("Export Tool", "https://github.com/hotosm/osm-export-tool"),
    ("Roadmap", "https://roadmap.hotosm.org"),
]

SECTIONS = [
    ("Tools and workflows", ("index.md", "projects/", "guides/")),
    ("Developer guide", ("dev-guide/", "dev-practices.md", "modules/", "become-a-contributor.md")),
]

pages: dict[str, tuple[str, str, str]] = {}


def _summary(markdown: str) -> str:
    for block in re.split(r"\n\s*\n", markdown):
        text = block.strip()
        if text.endswith(":") or text.startswith(":::") or "://" in text[:12]:
            continue
        if text and not text.startswith(("#", "|", "!", "<", "```", "-", "*", ">")):
            text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", " ".join(text.split()))
            return text[:160].rsplit(" ", 1)[0] + "…" if len(text) > 160 else text
    return ""


def _order(item):
    # Start with the tools summary
    return (item[0] != "projects/tools-summary.md", item[0])


def on_page_markdown(markdown, page, config, files):
    url = config["site_url"].rstrip("/") + "/" + page.url
    # Prefer H1 over ambiguous nav labels like "Intro"
    h1 = re.search(r"^#\s+(.+)$", markdown, re.M)
    pages[page.file.src_uri] = (h1.group(1).strip() if h1 else page.title, url, markdown)
    return markdown


def on_post_build(config):
    out = [INTRO]
    for name, prefixes in SECTIONS:
        out.append(f"\n## {name}\n")
        for src, (title, url, md) in sorted(pages.items(), key=_order):
            if src.startswith(prefixes):
                summary = _summary(md)
                out.append(f"- [{title}]({url})" + (f": {summary}" if summary else ""))
    out.append("\n## Tool documentation\n")
    out += [f"- [{name}]({url})" for name, url in TOOL_DOCS]
    out.append("\n## Optional\n")
    out.append(f"- [All pages as one file]({config['site_url'].rstrip('/')}/llms-full.txt)")

    site = Path(config["site_dir"])
    (site / "llms.txt").write_text("\n".join(out) + "\n")
    full = [INTRO] + [
        f"\n---\n\nSource: {url}\n\n{md.strip()}\n"
        for src, (title, url, md) in sorted(pages.items(), key=_order)
        if src.startswith(tuple(p for _, ps in SECTIONS for p in ps))
    ]
    (site / "llms-full.txt").write_text("\n".join(full))
