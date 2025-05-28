# Use Slack as our primary team and community chat platform

## Context and Problem Statement

We need a platform for:

- Day-to-day team communication and asynchronous coordination.
- Community engagement and support.
- Integration with project tooling (e.g., CI/CD notifications, GitHub activity).
- Easy onboarding for new collaborators and contributors.

Our ideal platform would also:

- Be accessible to external contributors.
- Support persistent message history.
- Be open and interoperable, with low risk of vendor lock-in.
- Respect user privacy and data sovereignty.

## Considered Options

- Slack
- Zulip
- Mattermost
- Rocket.Chat
- Matrix / Element

## Decision Outcome

Slack was adopted early in our organizational growth, largely because:

- Many existing and incoming collaborators were already on Slack.
- It provided a smooth UX with strong mobile and desktop support.
- NGO discounts made the Pro plan affordable, allowing for full message history and
  integrations.

However, as we scale and become more conscious of long-term sustainability, Slack's
proprietary nature and closed ecosystem present issues.

Migrating to an open platform would align better with our values, but the migration
cost and risk of fracturing our community are currently too high.

In 2025, we will be revisiting the use of Slack and possible open source alternatives
(as Slack changed their subscription model and will be costly to maintain with
many users).

## Consequences

- ✅ Good, because our community is already established on Slack.
- ✅ Good, because integrations (e.g., with GitHub, monitoring tools, deployment
  notifications) are mature and easy to configure.
- ✅ Good UX, especially for newcomers, thanks to wide adoption and familiar UI.
- ❌ Bad, because Slack is a proprietary, closed platform with limited options
  for self-hosting or data ownership.
- ❌ Bad, because the free tier is too limited (e.g., no full message history),
  making us reliant on discounted paid plans.
- ❌ Bad, migration to open alternatives (e.g., Zulip or Matrix) would be technically
  possible but socially risky, as many users may not follow or adapt easily.
- ❌ Bad, limited support for open standards and federation restricts long-term
  resilience.
