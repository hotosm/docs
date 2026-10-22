"""Read recent hotosm.org news from public HTML (Wagtail, no API)."""

import asyncio
import datetime as dt
import json
import logging
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

import httpx

log = logging.getLogger(__name__)

POST_LINK = re.compile(r'href="\s*(/en/news/[^"/\s]+/)\s*"')
# The line under the title is "Oct. 6, 2026" or "Posted by <a>Name</a> • Oct. 6, 2026"
TITLE = re.compile(r'<h1 class="font-bold text-h2">(.*?)</h1>\s*<p class="mt-2">(.*?)</p>', re.S)
BODY_END = re.compile(r'<h1 class="text-h2 font-bold mb-4">|<footer', re.S)
MONTHS = "jan feb mar apr may jun jul aug sep oct nov dec".split()


def parse_date(text: str) -> dt.date | None:
    # Django's "N j, Y": "Oct. 6, 2026", "July 20, 2026", "Sept. 3, 2025"
    m = re.search(r"([A-Za-z]+)\.?\s+(\d{1,2}),\s*(\d{4})", text)
    if not m or m.group(1)[:3].lower() not in MONTHS:
        return None
    return dt.date(int(m.group(3)), MONTHS.index(m.group(1)[:3].lower()) + 1, int(m.group(2)))


class _Text(HTMLParser):
    """Convert HTML headings, paragraphs and lists to simple Markdown."""

    SKIP = {"script", "style", "svg", "button", "form", "nav"}
    BLOCK = {"p", "div", "li", "h2", "h3", "h4", "h5", "tr", "br", "blockquote"}

    def __init__(self):
        super().__init__()
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n\n")
            if tag in ("h2", "h3", "h4", "h5"):
                self.out.append("#" * int(tag[1]) + " ")
            elif tag == "li":
                self.out.append("- ")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.out.append(re.sub(r"\s+", " ", data))

    def text(self) -> str:
        lines = (line.strip() for line in "".join(self.out).split("\n"))
        return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def html_to_text(html: str) -> str:
    p = _Text()
    p.feed(html)
    return p.text()


def parse_post(html: str) -> tuple[str, dt.date, str] | None:
    m = TITLE.search(html)
    if not m or not (date := parse_date(m.group(2))):
        return None
    end = BODY_END.search(html, m.end())
    body = html_to_text(html[m.end() : end.start() if end else None])
    body = re.sub(r"\n+Share$", "", body)  # share buttons
    return html_to_text(m.group(1)), date, body


async def load_news(client: httpx.AsyncClient, src: dict, cache_dir: Path) -> list[dict]:
    """Posts newer than max_age_days, as {url, title, date, text}.

    Walk the newest-first listing until a page has only older posts.
    Cache by URL so refreshes fetch only the listing and new posts.
    """
    base = src["url"]
    cutoff = dt.date.today() - dt.timedelta(days=int(src.get("max_age_days", 730)))
    cache_file = cache_dir / "hotosm_news.json"
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    sem = asyncio.Semaphore(4)
    skip = re.compile("|".join(src.get("exclude_titles", [])) or "$^", re.I)

    async def get(url: str) -> str:
        async with sem:
            r = await client.get(url)
            r.raise_for_status()
            return r.text

    async def post(url: str) -> dict | None:
        if url not in cache:
            parsed = parse_post(await get(url))
            if not parsed:
                log.warning("Could not parse %s", url)
                return None
            title, date, text = parsed
            cache[url] = {"url": url, "title": title, "date": date.isoformat(), "text": text}
        return cache[url]

    posts: dict[str, dict] = {}
    try:
        for page in range(1, int(src.get("max_pages", 40)) + 1):
            urls = [urljoin(base, p) for p in dict.fromkeys(POST_LINK.findall(await get(f"{base}?page={page}")))]
            got = [p for p in await asyncio.gather(*(post(u) for u in urls)) if p]
            recent = [p for p in got if p["date"] >= cutoff.isoformat()]
            posts.update((p["url"], p) for p in recent if not skip.search(p["title"]))
            if not recent:
                break
    except httpx.HTTPError as e:
        if not cache:
            raise
        log.warning("hotosm.org unavailable (%s), using cache", e)
        posts = {
            u: p for u, p in cache.items()
            if p["date"] >= cutoff.isoformat() and not skip.search(p["title"])
        }

    cache = {u: p for u, p in cache.items() if p["date"] >= cutoff.isoformat()}
    cache_file.write_text(json.dumps(cache))
    return sorted(posts.values(), key=lambda p: p["date"], reverse=True)
