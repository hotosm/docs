import datetime as dt

from app.website import parse_date, parse_post

POST = """<h1 class="font-bold text-h2">Mapping &amp; Floods</h1>
<p class="mt-2"> Posted by <a href="/en/members/x/">A Person</a> • Sept. 3, 2025 </p>
<div class="w-block"><p>Intro text.</p><h2>How</h2><ul><li>One</li></ul>
<svg><text>junk</text></svg><button>Share</button></div>
<h1 class="text-h2 font-bold mb-4"> Related Projects </h1><p>not body</p>"""


def test_parse_date():
    assert parse_date("Oct. 6, 2026") == dt.date(2026, 10, 6)
    assert parse_date("Posted by X • July 20, 2026") == dt.date(2026, 7, 20)
    assert parse_date("no date") is None


def test_parse_post():
    title, date, body = parse_post(POST)
    assert title == "Mapping & Floods"
    assert date == dt.date(2025, 9, 3)
    assert body == "Intro text.\n\n## How\n\n- One"
