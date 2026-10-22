from pathlib import Path

import yaml

from app.index import find_tools

TOOLS = yaml.safe_load(Path("corpus.yaml").read_text())["tools"]


def test_find_tools():
    assert set(find_tools("difference between tm and ftm?", TOOLS)) == {"Tasking Manager", "Field-TM"}
    assert find_tools("is it fair to use Drone TM?", TOOLS) == ["Drone TM"]
    assert find_tools("what is fAIr", TOOLS) == ["fAIr"]
    assert find_tools("how do I map buildings?", TOOLS) == []
