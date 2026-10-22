from app.corpus import Doc, chunk_doc, clean_markdown, make_doc, page_url, path_matches, path_weight


def test_globs():
    assert path_matches("docs/a/b.md", ["docs/**/*.md"], [])
    assert path_matches("docs/b.md", ["docs/**/*.md"], [])
    assert not path_matches("docs/decisions/x.md", ["docs/**/*.md"], ["**/decisions/**"])
    assert not path_matches("_posts/en/0500-01-02-tm2-admin_en.md", ["_posts/en/*.md"], ["**/*-tm2-*"])


def test_urls():
    mk = {"mode": "mkdocs", "base": "https://docs.hotosm.org/", "strip": "docs/"}
    assert page_url(mk, "r", "main", "docs/projects/tools-summary.md", {}) == "https://docs.hotosm.org/projects/tools-summary/"
    assert page_url(mk, "r", "main", "docs/index.md", {}) == "https://docs.hotosm.org/"
    sl = {"mode": "starlight", "base": "https://x.org/e2e/", "strip": "src/content/docs/"}
    assert page_url(sl, "r", "main", "src/content/docs/1-imagery/A-Drone.mdx", {}) == "https://x.org/e2e/1-imagery/a-drone/"
    jk = {"mode": "jekyll", "base": "https://learnosm.org"}
    assert page_url(jk, "r", "gh", "p.md", {"permalink": "/en/x/"}) == "https://learnosm.org/en/x/"
    qf = {"mode": "mkdocs", "base": "https://docs.qfield.org/", "strip": "documentation/"}
    assert page_url(qf, "r", "m", "documentation/how-to/gnss.en.md", {}) == "https://docs.qfield.org/how-to/gnss/"
    assert page_url(qf, "r", "m", "documentation/get-started/index.en.md", {}) == "https://docs.qfield.org/get-started/"
    assert page_url({"paths": {"en/x.md": "https://x.org/en/"}}, "r", "m", "en/x.md", {}) == "https://x.org/en/"
    assert page_url({}, "hotosm/chatmap", "master", "docs/a.md", {}) == "https://github.com/hotosm/chatmap/blob/master/docs/a.md"


def test_clean_markdown():
    text = "See [the docs](http://x) ![logo](a.png) <b>bold</b>\n```mermaid\ngraph\n```\n<!-- hi -->"
    assert clean_markdown(text) == "See the docs logo bold"


def test_make_doc_uses_front_matter():
    src = {"name": "LearnOSM", "repo": "hotosm/learnosm", "ref": "gh-pages", "url": {"mode": "jekyll", "base": "https://learnosm.org"}}
    raw = "---\ntitle: Remote editing\npermalink: /en/coordination/remote/\n---\n" + "Some useful text. " * 10
    doc = make_doc(src, "_posts/en/x.md", raw)
    assert doc.title == "Remote editing" and doc.url == "https://learnosm.org/en/coordination/remote/"


def test_chunking_splits_by_heading_and_keeps_anchor():
    body = "# Title\n\nintro " * 1 + "\n\n## Install\n\n" + ("Install step. " * 40) + "\n\n## Usage\n\n" + ("Usage step. " * 40)
    doc = Doc(source="S", path="p.md", url="https://d.org/p/", title="Title", text=body, weight=1.0, anchors=True)
    chunks = chunk_doc(doc)
    assert [c.heading for c in chunks] == ["Install", "Usage"]
    assert chunks[0].url == "https://d.org/p/#install"
    assert chunks[1].text.startswith("Title > Usage")


def test_clean_rst():
    from app.corpus import clean_rst

    raw = (
        "..\n  AUTO-GENERATED\n\n.. _feature-quality:\n\nfeature-quality\n```````````````\n\n"
        "Set ``high`` quality, see :ref:`flags <flags>` and `docs <https://x.org>`_.\n\n"
        "Run this::\n\n    odm --fast\n"
    )
    out = clean_rst(raw).strip()
    assert out.startswith("# feature-quality")
    assert "Set `high` quality, see flags and docs." in out
    assert "Run this:\n" in out and "AUTO-GENERATED" not in out and ".." not in out


def test_roadmap_docs():
    import json

    from app.corpus import roadmap_docs

    raw = json.dumps({
        "generatedAt": "2026-10-20T10:00:00Z",
        "items": [{"title": "ChatMap: bot", "status": "Planned", "group": "Roadmap item",
                   "summary": "A bot.", "owner": "Someone", "targetDate": "2027-03-31T00:00:00Z",
                   "issues": [
                       {"title": "Survey flow", "state": {"name": "Backlog", "type": "backlog"},
                        "assignee": {"name": "Someone"}},
                       {"title": "Old idea", "state": {"name": "Canceled", "type": "canceled"}},
                   ]}],
    })
    docs = roadmap_docs({"name": "Roadmap", "url": {"base": "https://roadmap.hotosm.org"}}, raw)
    assert [d.title for d in docs] == ["Roadmap: ChatMap: bot", "HOT tools roadmap overview"]
    assert "Status: Planned" in docs[0].text and "Target: 2027-03" in docs[0].text
    assert "Someone" not in docs[0].text  # owners and assignees aren't indexed
    assert "- Survey flow (Backlog)" in docs[0].text and "Old idea" not in docs[0].text
    assert not docs[0].anchors


def test_path_weight():
    src = {"weight": 1.2, "path_weights": {"docs/dev-guide/**": 0.5}}
    assert path_weight(src, "docs/dev-guide/testing.md") == 0.5
    assert path_weight(src, "docs/projects/tools-summary.md") == 1.2
