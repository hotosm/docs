from app.config import APP_DIR
from app.recommend import Planner

planner = Planner(APP_DIR / "rules.yaml")


def tool_ids(plan):
    return {t["id"] for s in plan["stages"] for t in s["tools"]}


def test_waste_points_small_team_goes_straight_to_field():
    plan = planner.recommend(
        {
            "goal": "waste collection points in my city",
            "existing": "none",
            "visible": "no",
            "area": "large",
            "team": "small",
            "detail": "simple",
            "experience": "none",
            "openness": "open",
        }
    )
    assert "chatmap" in tool_ids(plan)
    assert not tool_ids(plan) & {"tm", "fair", "dronetm", "export"}
    assert plan["scope"] == "Field collection only"


def test_buildings_poor_imagery_with_drone_is_full_e2e():
    plan = planner.recommend(
        {
            "existing": "partial",
            "visible": "yes",
            "area": "town",
            "imagery": "poor",
            "drone": "yes",
            "team": "small",
            "remote": "yes",
            "detail": "structured",
            "experience": "some",
            "openness": "open",
        }
    )
    assert {"dronetm", "oam", "tm", "fair", "fieldtm", "export"} <= tool_ids(plan)
    assert plan["scope"] == "Full end-to-end workflow"


def test_private_data_drops_osm_tools():
    plan = planner.recommend(
        {"visible": "yes", "area": "town", "imagery": "good", "remote": "yes",
         "team": "none", "experience": "expert", "openness": "private"}
    )
    assert not tool_ids(plan) & {"tm", "fair"}
    assert any("private" in n for n in plan["notes"])


def test_conditional_questions_and_invalid_answers():
    ids = [q["id"] for q in planner.visible_questions({"visible": "no", "team": "none"})]
    assert "imagery" not in ids and "detail" not in ids
    assert planner.validate({"visible": "bogus", "area": "town"}) == {"area": "town"}


def test_describe_mentions_tools():
    plan = planner.recommend({"visible": "no", "team": "few", "detail": "simple"})
    assert "ChatMap" in planner.describe(plan)
