# HOT's Development Practices

This was last updated on 08/07/2024 and details our idealised
software development practices.

## Open-Source Model

- All code developed at HOT is open-source.
  - We rely heavily on community feedback to steer our development.
  - Contribution from **anyone** is welcome.
- We follow a git-flow, or fork-and-pr model:
  - Developers should create a fork of the repo they wish to modify.
  - Code is added to a branch inside _the fork_.
  - A pull request (merge request or PR) is made against the development
    branch of the original repository.
- Our code is generally licensed
  [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html)
  unless otherwise specified.

## Repo Management

### Branches

- Generally our repos will have three key branches:
  - **dev**: the ongoing development to which PRs are made.
  - **stage**: optional branch where new features pass quality control
    stages prior to deployment to the main website.
  - **main**: the code that is currently deployed to the main website.

### Issues

#### Issue Labels

- Label issues where appropriate, for example as backend or frontend.
- Priorities can be assigned:.
  - `priority:critical`: blocking current tasks or user workflow.
  - `priority:high`: should be addressed as a priority.
  - `priority:low`: backlog of tasks that will be addressed in time.
- Difficulty can be **estimated** (and may not be accurate):

  - `effort:low`: small task, likely a few hours.
  - `effort:medium`: larger task, may take a day or two.
  - `effort:high`: a broader scope task with unclear timeline.

    > Ideally there should not be many tasks with `effort:high`.
    > If there are, consider breaking them down to smaller tasks.

- The quality control status can be tracked:

  - `qa:ready`: the issue has been fixed and is ready to test.
  - `qa:fail`: the issue was not fixed as intended and requires additional
    work from the developer.
  - The `qa:xx` label can be removed when an issue is closed.

- Issues marked `good first issue` are approachable to newcomers in the repo.
  - Ideally the repo should always have a few low priority `good first issue`
    tags to help foster open source contribution / onboarding.

#### Issue Assignment

- Assign issues to the dev who will work on it.
- Issues can be assigned in advance if the devs is known.
- Devs can self-assign tasks.

### PRs

#### PR Drafts

- Create a draft PR for works in progress.
- Push as early as possible to draft, especially if there is a chance you
  may get sidetracked on other work (so another dev could feasibly pick
  up where you left off).

#### PR Assignment

- Assign yourself if you are working on the issue.
- Assign another dev if you need to pass off the development to them.
- The re-assigned dev can then assign the task back to the original dev for
  validation.

#### PR Review

- Any developer can review a PR, **as long as one dev reviews** prior to
  merge.
- Assign devs for review - frontend can review backend and vice versa.
- Once review is complete and the PR is out of draft state, then any dev can
  merge.

### Milestones

- Encapsulates a set of issues into a logical bigger task, with or without
  an assigned deadline.
- Discussed in team meetings and decided on via priorities.
- Project Owner (PO) decides on priorities, tech lead decides on which tasks
  are required to achieve that goal.
- Milestones are grouped into a release, which has a set deadline.

### Releases

- A release encompasses multiple milestones, plus additional bugfixes
  and minor improvements.
- Releases are tracked on the roadmap and have an _approximate_ deadline.
- Ideally releases should be around once a month at minimum, to regularly
  deliver incremental updates to the user (~agile project management).

### Roadmaps

#### Technical Roadmap

- Higher level roadmap based on releases and milestones.
- Managed on the Git repo hosting service (e.g. Github), linked in the README.
- The roadmap should include:
  - Milestones spanning the work start and end date.
  - Releases labelled over the top, showing the anticipated next release date
    and how it relates to the milestones.

#### User Roadmap

- Most users do not want to delve into Github roadmaps and issues.
- A simpler user-centric roadmap can be written in simple Markdown
  table syntax.
- The key columns / categories in order:
  - In Progress: what is being worked on right now.
  - Next: what will be worked on in upcoming releases.
  - Future: a concept envisioned, but not fully planned out.

### Task Board

- An optional stage to easier visualise developer time.
- Should be as automated as possible:
  - Issues added to a project are added to the backlog.
  - Issues assigned to a dev are moved to 'In Progress'.
  - Issues labelled with `QA Ready` are moved to 'Review'.
  - Issues completed should be moved to 'Complete'.
- Ideally we can keep track of which developer is working on
  what task.
- This becomes especially important when we also have outside collaborators.

### Discussions

- To discuss more general topics in the public, so that anyone can contribute.
- Partly used to document the design decisions we have taken.
- Tag people specially for input, as it makes them more likely to add ideas.
- We can also use these for the staging server tests on each release cycle,
  e.g. <https://github.com/hotosm/fmtm/discussions/1335>

### Release Notes

- No technical details, move those to a dropdown in markdown:

```md
<details>
  <summary>Technical Summary</summary>
    * Add healthcare form category & minor fixes by @spwoodcock in https://github.com/hotosm/fmtm/pull/1555
    * Fix/requested page redirection by @NSUWAL123 in https://github.com/hotosm/fmtm/pull/1559
    * Test coverage for update project route by @azharcodeit in https://github.com/hotosm/fmtm/pull/1557
</details>
```

- Higher level info on bugs fixed, new features added, things improved.
- Add screenshots throughout.
