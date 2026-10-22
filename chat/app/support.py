"""Per-tool support channels, parsed from docs/tech-contacts.md.

The page stays the single source of truth; this only reads its table.
"""

import re

from .index import find_tools

CONTACTS_PATH = "docs/tech-contacts.md"
CONTACTS_URL = "https://docs.hotosm.org/tech-contacts/"
GENERAL = "General"

REF_DEF = re.compile(r"^\[(\w+)\]:\s*(\S+)", re.M)
REF_USE = re.compile(r"\[([^\]]+)\]\[(\w+)\]")
SLACK_CHANNEL = re.compile(r"slack://channel\?team=(\w+)&id=(\w+)")


def web_url(url: str) -> str:
    """slack:// deep links only work with the app installed; use the web client."""
    if m := SLACK_CHANNEL.match(url):
        return f"https://app.slack.com/client/{m.group(1)}/{m.group(2)}"
    return url


def parse_contacts(text: str, tool_aliases: dict) -> dict[str, str]:
    """{tool name: Slack channel URL}, plus GENERAL."""
    refs = {k: web_url(v) for k, v in REF_DEF.findall(text)}
    out: dict[str, dict] = {}
    # First link to "general" in the intro, before the table
    for label, ref in REF_USE.findall(text.split("|", 1)[0]):
        if "general" in label.lower() and ref in refs:
            out[GENERAL] = refs[ref]
            break
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or set(cells[0]) <= set("-: "):
            continue
        names = find_tools(cells[0], tool_aliases)
        links = REF_USE.findall(cells[1])
        if not names or not links or links[0][1] not in refs:
            continue
        out[names[0]] = refs[links[0][1]]
    return out


def support_line(tools: list[str], contacts: dict[str, str]) -> str:
    """Markdown pointing to each tool's Slack channel, or the general one."""
    links, general = [], False
    for t in tools:
        url = contacts.get(t)
        if url and url != contacts.get(GENERAL):
            links.append(f"[{t} Slack channel]({url})")
        else:
            general = True
    if (general or not links) and GENERAL in contacts:
        links.append(f"[HOT Slack general channel]({contacts[GENERAL]})")
    if not links:
        links.append("[HOT Slack](https://slack.hotosm.org)")
    return (
        f"For more help, ask in the {' or '.join(links)}, or contact the tool's "
        f"focal point listed on [Tech Contacts]({CONTACTS_URL})."
    )
