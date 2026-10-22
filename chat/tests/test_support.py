from pathlib import Path

import yaml

from app.corpus import clean_markdown
from app.support import GENERAL, parse_contacts, support_line

TOOLS = yaml.safe_load(Path("corpus.yaml").read_text())["tools"]
PAGE = clean_markdown((Path(__file__).parents[2] / "docs/tech-contacts.md").read_text())


def test_parse_contacts():
    c = parse_contacts(PAGE, TOOLS)
    assert c[GENERAL] == "https://app.slack.com/client/T042TUWCB/C042TUWCV"
    assert c["Field-TM"] == "https://app.slack.com/client/T042TUWCB/C04PCBFDEGN"
    assert c["fAIr"] == "https://app.slack.com/client/T042TUWCB/C0542U7DLA0"
    assert c["uMap"] == c[GENERAL]
    assert {"Tasking Manager", "Drone TM", "OpenAerialMap", "ChatMap", "Export Tool"} <= c.keys()


def test_support_line():
    c = parse_contacts(PAGE, TOOLS)
    line = support_line(["Drone TM"], c)
    assert "[Drone TM Slack channel](https://app.slack.com/client/T042TUWCB/C089CAULJFP)" in line
    assert "general" not in line
    # Tools without their own channel fall back to general, once
    assert support_line(["uMap", "QField"], c).count("general channel") == 1
    assert "general channel" in support_line([], c)
    assert "slack.hotosm.org" in support_line(["fAIr"], {})
