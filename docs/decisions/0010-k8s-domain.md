# Use [component]-[env].[tool].[cluster-namespace].hotosm.org for kubernetes namespace

## Context and Problem Statement

We need a universally applicable namespace for DNS resolution of kubernetes
resources. Additionally, we should set a standard for all sub-domain naming for
consistency across our tools.

In this specific case, we are deciding on the DNS resolution for the new
OpenAerialMap eoAPI, which will run alongside the old API for a time while we
work on the uploader. So we will need to find a solution for the k8s setup that
will affect all future tools while also accounting for the peculiarities of the
initial setup.

Our tools have:

- [project] which is an internal designator for project tracking
- [tool-name] which may be the same as [project] but can also designate a specific tool within that project. Examples include `tasking-manager`, `openaerialmap`, `fair-predictor`, and `eoapi`
- [env] such as `dev`, `staging`, and `production`

In the Tasking Manager (running on ECS), we have:

- the frontend _tasks.hotosm.org_, _tasks-dev.hotosm.org_
- backend _tasking-manager-production-api.hotosm.org_, _tasking-manager-dev-api.hotosm.org_

On the existing OAM we have:

- splash page _openaerialmap.org_
- frontend _map.openaerialmap.org_
- backend _api.openaerialmap.org_

This decision will only affect the pattern of internal, predictable domains, not
front-facing "vanity" ones that will be in use for production
(eg. _map.openaerialmap.org_)

## Considered Options

We considered the following schemes:

- [env].[tool-name].[cluster-namespace].hotosm.org (using multiple subdomains)
- [tool-name]-[env].[cluster-namespace].hotosm.org
- [env]-[tool-name].[cluster-namespace].hotosm.org

For managing both the existing APIs temporarily, we can try to use an API
gateway that resolved any option above to _api.openaerialmap.org/v2/_, however
this would require migrating the existing old API to k8s as well. More simply,
we could instead deploy the new API with a hotosm.org
domain: _oam-api.hotosm.org_. Moving the service over to the hotosm.org domain
will help unify our tools for our e2e goals. Eventually we could build the new
frontend as _oam.hotosm.org_.

## Decision Outcome

For the kubernetes namespace we will go with the following naming scheme:

> [component]-[env].[tool].[cluster-namespace].hotosm.org

Our cluster namespace will be "k8s-prod" (including the environment), so the OAM eoAPI will
be _backend-prod.eoapi.k8s-prod.hotosm,org_ which will resolve to _oam-api.hotosm.org_.

We have a list of tools already in use as required AWS tags: `oam`,
`tasking-manager`, `fmtm`, `dronetm`, `fair`, `export-tool`, `raw-data-api`. We
also have a list of accepted environment tags: `dev`, `staging`, `production`,
`demo`, and `testing`. Example components could be `api`, `frontend`, `backend`,
`uploader`, `scheduler`, `worker`, `database`, or `storage`.

### Consequences

We will need to keep the old OAM API intact until we get uploader functionality
into the new API. That will remain as _api.openaerialmap.org_.
