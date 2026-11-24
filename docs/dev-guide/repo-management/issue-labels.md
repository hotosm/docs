# Repo Issue Labels

Each issue should have a label `repo:repo-name`, for easier sorting in Linear
(see [Project Management](../../dev-practices.md#project-management)).

## Labelling New Issues

To add the `repo:repo-name` label automatically for each new issue,
we can create the following Github workflow:

```yaml
# We add a label `repo:repo-name` to each new issue,
# for easier tracking in external systems

name: 🏷️ Issue Label

on:
  issues:
    types:
      - opened

jobs:
  issue-label:
    runs-on: ubuntu-latest
    permissions:
      issues: write

    steps:
      - run: gh issue edit "$NUMBER" --add-label "$LABELS"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GH_REPO: ${{ github.repository }}
          NUMBER: ${{ github.event.issue.number }}
          LABELS: repo:drone-tm
```

## Labelling Existing Issues

To bulk tag existing issues in a repo, use Github CLI:

```bash
docker run --rm -it --entrypoint sh maniator/gh
gh auth login

REPO="hotosm/chatmap"
LABEL="repo:chatmap"

gh label create "${LABEL}" --repo "${REPO}" --color "#ededed"

for issue in $(gh issue list --repo "${REPO}" \
  --state open --limit 1000 --json number --jq '.[].number') \
; do
  gh issue edit $issue --repo "${REPO}" --add-label "${LABEL}"
done
```
