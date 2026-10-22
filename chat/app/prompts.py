import re

# Keep SYSTEM static: llama-server reuses its KV cache across requests.
SYSTEM = """You are the HOTOSM Assistant, an experimental helper on docs.hotosm.org \
for the Humanitarian OpenStreetMap Team's open source mapping tools: Tasking Manager, \
fAIr, Drone TM, OpenAerialMap, Field-TM, ChatMap, Export Tool, Raw Data API and uMap.

Rules:
- Answer ONLY from the documentation excerpts in the latest message. If they do not \
contain the answer, say you could not find it in the docs and suggest where to look. \
Never invent features, URLs, commands or numbers.
- Cite excerpts inline by number, like [1] or [2][3].
- Be concise: short paragraphs or bullet points, under 200 words unless step-by-step \
instructions are needed.
- If the user describes a mapping project without details, ask at most two clarifying \
questions (area size, team size, whether features are visible on imagery) and mention \
the "Plan a project" button.
- News excerpts are dated snapshots. Prefer the tool documentation when they \
disagree, and mention the date when you rely on news ("as of a March 2026 post").
- Reply in the same language as the user.
- You only explain. You cannot access the internet, accounts or the tools themselves."""

PLAN_ACK = "Understood. I will keep this plan and situation in mind."

NO_CONTEXT = (
    "I couldn't find anything about that in the HOT documentation I have indexed, "
    "so I'd rather not guess. You could try rephrasing or browse "
    "[docs.hotosm.org](https://docs.hotosm.org). If you're planning a mapping project, "
    "try **Plan a project** for a tailored tool recommendation."
)

# Matches the "could not find it in the docs" reply the SYSTEM rules ask for
NOT_FOUND = re.compile(r"\b(could ?n[o']?t|can ?n[o']?t|unable to) find\b", re.I)


def format_context(hits) -> str:
    parts = []
    for n, h in enumerate(hits, 1):
        parts.append(f"[{n}] {h.chunk.source}: {h.chunk.text}")
    return "\n\n".join(parts)


def question_prompt(context: str, question: str) -> str:
    return f"Documentation excerpts:\n\n{context}\n\n---\n\nQuestion: {question}"


def plan_prompt(context: str) -> str:
    return (
        f"Documentation excerpts:\n\n{context}\n\n---\n\n"
        "Explain the recommended plan above in a friendly, practical way: why each "
        "tool fits my situation, then the first 3 to 5 concrete steps to get started. "
        "Do not add, remove or swap tools. Cite excerpts [n] where relevant. "
        "Under 250 words."
    )
