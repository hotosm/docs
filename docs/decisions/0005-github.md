# Use Github as both our code repository & CI/CD

## Context and Problem Statement

We need somewhere to

- Store our code to work on it collaboratively.
- Raise issues and manage documentation around the code.
- Track development via roadmaps and task trackers.

We also need a pipeline runner (CI/CD):

- Create build artifacts for deployment.
- Run automated testing.
- Deploy our code into various development environments.

## Considered Options

- Github
- Gitlab
- Codeberg
- Bitbucket

## Decision Outcome

Github was originally chosen as it provided many benefits for free, over the
competition.

Cost and simplicity are key factors for us, being a small NGO that receives
project specific funding.

Since the decision was taken, Github was acquired by Microsoft and has
some practices that we do not agree with (license violations for Copilot,
amongst others).

Reluctantly, we are stuck with Github due to the migration effort that would
be required.

### Consequences

- Good, because free to use, including uncapped CI/CD usage as an NGO.
- Good, has the most visibility and reach of all other platforms.
- Bad, because as an organization it undertakes many practices we do not agree with.
- Bad, the more we use Github workflows (propriatary), the further we are
  vendor-locked.
- Bad, because it would be difficult to migrate all of the accumulated issues,
  milestones, project boards, subissues, etc.
