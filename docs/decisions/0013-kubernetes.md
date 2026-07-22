# Using Kubernetes to deploy our tools

## Context and Problem Statement

HOT maintains a growing set of tools (Tasking Manager, OpenAerialMap, fAIr,
FieldTM, DroneTM, Export Tool / Raw Data API, ChatMap, and more), with a small
core tech team plus community contributors. For a team our size, how we deploy
these tools matters a lot.

A few things pushed us to rethink our approach:

- We rely almost entirely on donated cloud credits (today, AWS), with few
  guarantees. We want to have flexibility to move providers, or self-host, without
  rewriting all of our deployment logic.
- Our setup had sprawled. Around 2023 we had settled on Terraform managing AWS
  ECS, plus a lot of hand-managed EC2 instances and other AWS services. Each
  tool was an isolated island.
- Resources were used poorly. With tens of tools, we ran many servers
  (EC2 instances) that sat idle most of the time, but still struggled under load
  spikes. That is both wasteful and fragile.
- Some tools are genuinely hard to run on a single VM. fAIr needs GPU nodes,
  cold-start ML inference, pipeline orchestration and autoscaling. DroneTM
  needs to spread OpenDroneMap processing across many workers.

The obvious counter-argument is that we are a small NGO and Kubernetes is complex.
Most of our developers specialise in backend or frontend work, so asking them to
also learn a distributed computing platform is tricky.
This record explains why we decided it was worth it, and where we decided on
practical compromises.

## Considered Options

- Keep the status quo: per-tool EC2 + SSH and/or Docker Compose, with
  Terraform + Elastic Container Service (ECS) for a few services.
- Lean further into a vendor's managed platform via Terraform: more ECS, or
  the equivalent on another cloud (Cloud Run, Azure Container Apps).
- Use a lighter orchestrator: Nomad or Docker Swarm.
- Use Kubernetes, with a managed control plane (EKS) and the option to
  self-host later (e.g. Talos).

The tipping point came in 2025. DevelopmentSeed's rebuild of the OpenAerialMap
backend gave us the choice of Kubernetes or Docker Compose. We had been
thinking about Kubernetes for a while, the Senior Tech Lead had used it before,
and DevSeed could help, so we took the plunge.

## Decision Outcome

We chose Kubernetes as the standard way to deploy our tools, running on AWS EKS
as the control plane. We are moving tools onto it slowly, not all at once.

The migration is gradual and limited on purpose. OpenAerialMap moved first
(Sep '25). Shared Login, ChatMap, and others are in progress. Importantly,
Tasking Manager and Raw Data API are not currently planned for migration: where
the effort is not worth the benefit, tools stay where they are. Kubernetes is
the default, but not a hard requirement.

The cluster runs a set of well-known open-source tools:

- Karpenter for node autoscaling (separate CPU, GPU and fAIr-inference pools).
- ArgoCD for GitOps. The cluster state lives in this repo.
- CloudNativePG for managed Postgres, cert-manager and external-dns for TLS and
  DNS, sealed-secrets for secrets, Velero for backups, and Knative for
  cold-start / serverless inference.
- OpenTofu (Terraform) provisions the underlying infrastructure, and Helm
  packages the apps.

### Why we chose this route

- Cloud-agnostic. Kubernetes works across all the major cloud providers and
  self-hosting options. If our funding is cut or we need to move, we can shift
  our infrastructure without rewriting a load of vendor-specific logic. We
  picked EKS for the control plane, but that choice can be undone.
- Consolidation. One system for DevOps to manage, instead of many separate EC2
  instances and AWS services.
- Load spreading and autoscaling. A shared cluster gives us a big buffer across
  all our tools. Idle capacity gets reused, and spikes are handled by
  autoscaling instead of over-sized standalone VMs.
- Lower cost, hopefully. Fewer, better-used VMs should mean a smaller bill.
  This is what we expect, but it still needs to be proven.
- Skills that transfer. The team learns general container and distributed
  computing concepts, rather than ECS-only tooling. Kubernetes is a useful
  skill to have, and not tied to one vendor.
- fAIr genuinely needs it. GPU nodes, cold-start inference, ZenML/MLflow
  pipelines, autoscaling and lots of connected services are all easy in
  Kubernetes and awkward elsewhere. DroneTM benefits too, with ScaleODM
  spreading ODM jobs across the cluster.
- Simple deployment of sophisticated tools: once the cluster is up and running,
  we can grab any open-source helm chart and run tools in a production
  environment within minutes (e.g. all our supporting tools, e.g. ODK Central).
- Our collaborators use it. DevSeed, HeiGIT and NAXA all run Kubernetes, which
  makes sharing knowledge and working together easier.

### Consequences

The good:

- One consistent, documented, GitOps-managed way to deploy and watch our tools.
- A single flexible pool of compute for very different workloads (web APIs, GPU
  inference, batch imagery processing).
- We are far less tied to any one cloud provider.
- GitOps means that once code is released in the repo, it can
  be released into a staging environment or production pretty quickly.

The costs we accept:

- Complexity and a learning curve. Kubernetes brings distributed computing
  ideas that many specialised devs are not that interested in. EC2 + SSH is
  simpler to reason about, and some of the team understandably prefer it.
- Bus factor. Deep Kubernetes knowledge currently sits with one person, which
  is a single point of failure. We are working on this with skillshare
  sessions, tutorials and the docs in this repo, to spread the knowledge.
- Harder to self-host. Running our tools outside HOT infrastructure is more
  involved on Kubernetes. We will provide good options for this, but it
  is slightly more involved fro devs and contributors.
- No way to avoid using containers.

### Guardrails

To keep the complexity in check and right-sized for a team like ours:

- Migrate slowly, and only where the benefit is clear. Leave tools on other
  infrastructure when it makes sense (e.g. Tasking Manager, Raw Data API).
- Prefer well-known, well-documented open-source (CNCF) components over
  custom tooling or vendor-locked approaches.
- Treat knowledge sharing as part of the work, not an afterthought.
- Keep the EKS choice loosely coupled, so self-hosting or another provider is
  still realistic.
- Do not optimise for DevOps best practices, but instead for ease of use.
  Security matters, but our threat model is not that of a large corporate, and
  we value understanding over sophistication.
