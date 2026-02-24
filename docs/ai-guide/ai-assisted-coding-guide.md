# Practical Guide: Working with AI Tools as a Developer

**Boundaries, workflows, and expectations for a small NGO development team**

---

## The Golden Rule

**You are the author. You are accountable.**

If you used AI to generate code, documentation, or analysis - and it is wrong, insecure, biased, or breaks something - that is on you. Not the tool. You submitted it. You own it.

This is not punitive. It is the same standard we hold for any tool: if you use a calculator and enter the wrong numbers, the mistake is yours.

---

## What AI Is Good For (Appropriate To Use Here)

- **First drafts and boilerplate:** Config files, repetitive scaffolding, test stubs, standard templates.
- **Explaining unfamiliar code:** "What does this function do?" is a great use of AI. Treat it like a patient colleague who may occasionally be confidently wrong.
- **Brainstorming approaches:** "What are three ways I could structure this migration?" - then evaluate each with your own judgement. Note that LLMs are trained to be agreeable an tend to affirm your opinion. Try to phrase questions in an unbiased way, and be wary that the response may not account for all possible options.
- **Creating quick prototypes:** If you need to assess the feasibility of an idea, nothing beats creating a quick prototype to test, before planning the well architected solution. LLMs can generate a throw away test quite quickly.
- **Drafting documentation:** Let AI produce a first pass, then rewrite it in your own words to ensure accuracy.
- **Debugging assistance:** Paste an error message and ask for possible causes. Verify before applying.
- **Refactoring suggestions:** AI can suggest cleaner patterns. Be aware that often LLMs are prone to mission-creep. If you need a small refactor, then be sure to nail down exactly what is needed and set guardrails, else the scope of the refactor may quickly grow.
- **Learning new libraries or languages:** Use AI as a tutor, not a substitute for understanding.

## What AI Is Bad At (Be Cautious Here)

- **Architecture decisions:** AI does not understand your system's history, constraints, or users. It will happily suggest a redesign that ignores your actual context.
- **Security-sensitive code:** AI-generated code frequently has vulnerabilities — missing input validation, insecure defaults, outdated patterns. All security-relevant code must be manually engineered and reviewed.
- **Domain-specific logic:** AI often fails on edge cases unique to your domain. _(Example from geospatial: AI routinely mishandles anti-meridian polygon wrapping because it does not understand spherical geometry unless explicitly guided.)_. It may help to provide domain specific context and add more specific instructions. In some cases, LLMs are just not appropriate tools: using general models to pinpoint specialized knowledge.
- **Choosing dependencies:** LLMs frequently generate custom implementations instead of using well-tested libraries. Always check: does a maintained library already solve this? If yes, use it.
- **Anything involving beneficiary or sensitive data:** Never paste personal data, donor information, or internal strategy into AI tools. Ensure access restrictions are set when sharing your code repository containing secret files such as `.env` files with agents.
  HOT staff can refer to the [internal AI Policy](https://docs.google.com/document/d/13bGovnFVOouF7iRv0CVxSYjP3ky048KQYkrdg4mIcHU) for more details.

## What AI Must Not Be Used For

- **Submitting code you have not read and understood.** If you cannot explain what it does line by line, do not submit it.
- **Generating reports or communications** that go to beneficiaries, donors, or partners without human review. AI can draft; a human must finalise.
- **Replacing your own learning.** If a task is assigned to help you learn a codebase or technology, do the thinking yourself first. Use AI to check your work, not to bypass it.
- **Feeding sensitive or private data into any AI tool.** This includes names, contact details, health data, financial information, and internal strategy documents.

---

## The Workflow: How to Actually Use AI Well

### 1. Think First, Then Prompt

Before asking AI anything, spend enough time forming your own mental model of the problem. What are the constraints? What approaches come to mind? This is the "pre-testing effect" - trying to answer a question yourself, even imperfectly, before consulting AI produces better understanding and retention.

### 2. Decide How You Would Like To Be Assisted

- **Ideas only**: xxx. Most appropriate for xxx
- **Pair programming**: xxx. Most appropriate for xxx
- **Agentic mode**: xxx. Most appropriate for xxx
- **Review only**: xxx. Most appropriate for xxx

### 3. Write a Clear Spec, Not a Vague Request

- **Bad:** "Make this work better."
- **Good:** "Refactor this function to handle null input gracefully. Return an empty list instead of throwing. Keep the existing API signature. Add a unit test for the null case."

The more precise your prompt, the more useful the output.

### 4. Review Everything

- Read every line of generated code.
- Check that it uses existing project libraries and patterns rather than reinventing solutions.
- Run the tests. If there are no tests, write them before accepting the code.
- Ask yourself: "Could I explain this to a colleague?" If not, dig deeper before committing.
- Ask yourself: "Am I overcomplicating this? Could this be achieved with a simpler pattern?" LLMs can have a tendency to apply complex patterns to solve what are often simple problems (particularly if they can be solved with an already well developed and maintained tool / library).
- Where possible, add detailed comments as to **why** a line of code is needed (not explaining _what_ the line of code does, which should be self-explanatory, and is often what LLMs do).

### 5. Keep Changes Small

Do not ask AI to generate an entire feature in one shot. Break work into small, reviewable increments. This mirrors good engineering practice regardless of whether AI is involved.

### 6. Label AI-Assisted Work

When committing code or submitting PRs that include substantial AI-generated content, note it. A simple convention:

```
Assisted-by: [tool name, e.g. Claude, Copilot]
```

This is not about shame. It is about transparency and helping reviewers calibrate their attention. It is also becoming standard practice in major open source projects (LLVM, QGIS, Drupal, Fedora).

### 7. Do Not Iterate Blindly

If AI gives you broken code and you keep pasting the error back in hoping it will fix itself - stop. After two or three failed attempts, step back and debug manually. Blindly looping with an AI wastes time and teaches you nothing.

---

## Contributing to Open Source with AI

If your work involves contributing to upstream open source projects, additional care is required.

### Respect Maintainer Time

Every PR you submit costs someone time to review. Before submitting AI-assisted contributions:

- Read the project's contributing guidelines and AI policy (if one exists).
- Ensure the contribution is high quality, well-tested, and clearly explained.
- Write the PR description yourself - do not let AI generate it.
- Be prepared to answer questions about your code during review.

### Do Not Chase Volume

One excellent, well-tested PR is worth more than ten AI-generated patches that each require maintainer effort to evaluate. Quality over quantity. Always.

### Prefer Existing Libraries

This is critical: LLMs have a strong tendency to generate bespoke implementations rather than using established libraries. Before accepting AI-generated code that solves a common problem, ask:

- Is there an existing library the project already uses for this?
- Is there a community-standard solution?
- Will a maintainer look at this custom code and wonder why the standard library was not used?

If the answer to any of these is yes, use the library. This reduces maintenance burden and aligns with open source norms.

### Do Not Use AI for "Good First Issues"

Several projects (including LLVM) explicitly forbid this. These issues exist as learning opportunities for new contributors. Using AI to solve them defeats the purpose and displaces human growth. This applies even if the project has not formalised the rule.

---

## Security Checklist for AI-Generated Code

Before merging any AI-generated code, verify:

- [ ] Input validation is present and correct
- [ ] No hardcoded secrets, tokens, or credentials
- [ ] Dependencies are pinned and from trusted sources
- [ ] Error handling does not leak sensitive information
- [ ] No unnecessary permissions or access scopes
- [ ] SQL queries are parameterised (no string concatenation)
- [ ] File paths are sanitised against traversal attacks
- [ ] Output encoding is appropriate for the context (HTML, JSON, etc.)

---

## Protecting Your Own Skills

AI can make you faster, but it can also make you dependent if you are not deliberate about learning.

- **Space your learning.** Do not cram an entire AI-assisted session into one marathon. Come back to the same problem area across multiple days.
- **Diversify tasks.** If AI is handling the rote work, use the free time for deeper exploration - reading documentation, understanding architecture, reviewing others' code.
- **Explain what you learned.** After an AI-assisted session, write a short note (even just for yourself) about what you now understand that you did not before.
- **Maintain manual skills.** Regularly write code, debug problems, and read error messages without AI. Like any skill, it atrophies without practice.

---

## Approved Tools and Data Boundaries

| Category                                   | Guidance                                                                                                                                                                                                                                                                          |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Code completion** (e.g. Copilot, Cursor) | Permitted for non-sensitive code. Review all suggestions.                                                                                                                                                                                                                         |
| **Chat-based AI** (e.g. Claude, ChatGPT)   | Permitted for general development questions. Never paste sensitive data.                                                                                                                                                                                                          |
| **AI code review tools**                   | Only if they keep a human in the loop. Fully automated review bots may post comments about code, but cannot change the content without human approval.                                                                                                                            |
| **AI agents** (autonomous)                 | Not permitted to update code directly on shared platforms (e.g. within PRs) without explicit human approval of each action. They may be used on local machines, such as in a developers IDE, as long as workflows are manually approved and the final code is quality controlled. |

In summary, it is essential to **not allow automated commits from AI agents**, but most other usage is permitted.

---

## Policy Review

This guide should be reviewed every three months or whenever a significant change occurs in AI tooling, team composition, or organisational risk posture. AI capabilities are evolving rapidly; our practices must keep pace.
