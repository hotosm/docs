# Use [tier]-[dashed-name].[cluster-namespace].hotosm.org for kubernetes namespace

## Context and Problem Statement

We need a universally applicable namespace for DNS resolution of kubernetes resources. Additionally, we should set a standard for all sub-domain naming for consistency across our tools. 

In this specific case, we are deciding on the DNS resolution for the new OpenAerialMap eoAPI, which will run alongside the old API for a time while we work on the uploader. So we will need to find a solution for the k8s setup that will affect all future tools while also accounting for the peculiarities of the initial setup. 

Our tools have:
- [project-name] such as `tasking-manager` and `openaerialmap`
- [env] such as `dev`, `staging`, and `production`

In the Tasking Manager (running on ECS), we have:
- the frontend tasks.hotosm.org, tasks-dev.hotosm.org
- backend tasking-manager-production-api.hotosm.org, tasking-manager-dev-api.hotosm.org

On the existing OAM we have:
- splash page openaerialmap.org
- frontend map.openaerialmap.org
- **backend api.openaerialmap.org**

## Considered Options

We considered the following schemes:

- [env].[project-name].[cluster-namespace].hotosm.org (using multiple subdomains)
- [project-name]-[env].[cluster-namespace].hotosm.org
- [env]-[project-name].[cluster-namespace].hotosm.org

For managing both the existing APIs temporarily, we can try to use an API gateway that resolved any option above to _api.openaerialmap.org/v2/_, however this would require migrating the existing old API to k8s as well. More simply, we could instead deploy the new API with a hotosm.org domain: _oam-api.hotosm.org_. Moving the service over to the hotosm.org domain will help unify our tools for our e2e goals. Eventually we could build the new frontend as _oam.hotosm.org_.

## Decision Outcome

For the kubernetes namespace we will go with the following naming scheme: 

> [project-name]-[env].[cluster-namespace].hotosm.org

Our cluster namespace will be "k8s", so the OAM eoAPI will be _oam-api-dev.k8s.hotosm.org_ which will resolve to _oam-api.hotosm.org_. 

### Consequences

We will need to keep the old OAM API intact until we get uploader functionality into the new API. That will remain as _api.openaerialmap.org_.


