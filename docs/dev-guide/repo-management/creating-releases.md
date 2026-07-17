# Creating Releases

This is the new process that all apps will eventually follow.
As of 10-06-2026 not currently implement for fAIr, ChatMap,
uMap, Tasking Manager, Export Tool.

## 1. Bumping the version in the code

Most repos track a single version through a few files:

- `package.json` - tracks frontend version.
- `pyproject.toml` & `__version__.py` - track backend (Python version)
- `Chart.yaml` - tracks the helm chart version (for Kubernetes releases)

!!! note

      Ideally all of these versions are in sync.

      Common release processes for bigger teams / products do allow for
      separate versioning of the different components (frontend, backend,
      helm chart, etc).

      Due to small team size and simplicity, we opt to keep the version
      consistent across all components.

## 2. Making the release in Github

1. Update the version throughout the code ([Bumping a Version](./version-control#bumping-a-version)).
   Note that it's possible to update the versions manually, but using the listed
   tools simply helps to keep them properly in sync.
2. Go to the Releases page of your repo
   (<https://github.com/ORG/REPO/releases>).
3. Click `Draft a new release`.
4. Click `Choose a tag`, then input the current version number and press
   enter (this will automatically create a matching tag for your release).
5. Set the `Release title` to v`x.x.x`, replacing with your version number.
6. Add a description if possible, then release.

!!! note

      For Python / NPM packages, this should trigger a publishing workflow,
      making the package available publicly.

      For tools, this will trigger a build pipeline in Github to create
      versioned container images & publish the helm chart for deployment.

## 3. Deploy to Kubernetes

!!! note

      This step might be automated, depending on the outcome of:
      [https://github.com/hotosm/k8s-infra/issues/90](https://github.com/hotosm/k8s-infra/issues/90)

1. Within the [k8s-infra](https://github.com/hotosm/k8s-infra)
   repository, we deploy our tools using a 'pull' approach via
   ArgoCD.
2. Argo will scan the version set for our tools within the k8s-infra repo.
   E.g. https://github.com/hotosm/k8s-infra/blob/8417a4eeb922abfdb4d468dc089dc655845f7f2e/apps/drone-tm.yaml#L12
3. Update this version to match the latest release version & push to `main`.
4. Within ~3 mins, Argo will pull the image and create a new release in the defined
   Kubernetes namespace (also in the file linked above).

## 4. View the deployment in k8s

- Access the cluster via [Tailscale](../../devops/tailscale-cluster-access.md).
- Go to the correct namespace, e.g. `drone`.
- View the pods in the namespace `kubectl get all`.
- You will see a rolling release happening, as the new pods are deployed
  in parallel, tested to be working, then the old pods shut down if
  the deployment was a success.
- This process should at most take about 3-5 mins.

!!! note

      You can also view the progress in the ArgoCD UI.

## 5. Revert a release

Best case:

- You can revert the version number defined in `k8s-infra`,
  and it rolls back the version deployed.

Worst case:

- If things are stuck and you can't revert / it's an emergency:
  then comment out e.g. the `drone-tm.yaml` ArgoCD app manifest in k8s infra,
  then push & sync via Argo. This will totally remove the deployment / app!
  (but keeps the database data, don't worry).
- Once the content of `kubectl get all` is totally removed from the namespace,
  you can then uncomment the `drone-tm.yaml`, sync with Argo and get a new
  deployment made of the exact version.

!!! note

      In theory, the database schema / migrations should not be an issue and
      will hopefully roll back. Especially for e.g. DroneTM, which uses alembic.

      Worst case here is to connect to the database and manually revert the
      schema to be compatible with the rollback release...

      To connect to the db, see
      [production database](../../devops/production-db.md#accessing--exposing-the-db)
