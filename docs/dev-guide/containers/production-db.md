# Production Databases

- Production databases are best managed via Kubernetes.
- Generally the install and management of databases is maintained by a
  Kubernetes 'Controller'.
- The controller simply manages the lifecycle of the database cluster,
  allowing for replication, load balancing etc.
- There are a few options (in order of preference, 2024):
  - CloudNativePG
  - CrunchyPG
  - Zalando
  - Percona, Stolon, KubeDB, etc

## CloudNativePG

This guide assumes you have a functioning Kubernetes cluster, plus
available command line tools `kubectl` and `helm`.

CloudNativePG makes four types of resources available:

- Cluster - a replicated database cluster.
- Pooler - load balancing on top of a cluster (pg_bouncer).
- Backup - on demand db backup.
- ScheduledBackup - regular scheduled db backup.

These resources can be used in any namespace of the cluster, so a database
could be deployed in a namespace alongside a tool.

### Operator Install

Via Helm:

```bash
helm upgrade --install cnpg \
    --namespace cnpg-system \
    --create-namespace \
    cnpg/cloudnative-pg
```

### Install Kubectl Plugin

- To simplify management of databases, it's best to install the cnpg plugin.
- Details on their
  [documentation site](https://cloudnative-pg.io/documentation/1.20/kubectl-plugin)
- This allows us to easily do maintenance tasks such as backup, re-scale
  replicas, delete specific replicas, upgrade the db image, etc.

### Create a PostGIS Database

- Now we have the operator installed, this allows us to create databases
  in Kubernetes using `apiVersion: postgresql.cnpg.io/v1` and `kind: Cluster`.
- If we deploy a spec with this properties, a database will automatically
  be deployed and managed by CloudNativePG.
- There are many configuration options available under the `spec` key.

Example:

```bash
cat <<EOF | kubectl apply --filename=-
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: fmtm-db
spec:
  instances: 3
  imageName: ghcr.io/cloudnative-pg/postgis:16
  bootstrap:
    initdb:
      database: fmtm
      postInitTemplateSQL:
        - CREATE EXTENSION postgis;
        - CREATE EXTENSION postgis_topology;
        - CREATE EXTENSION fuzzystrmatch;
        - CREATE EXTENSION postgis_tiger_geocoder;
  storage:
    size: 1Gi
  backup:
    barmanObjectStore:
      destinationPath: "s3://fmtm-db-backups/"
      endpointURL: "https://s3.fmtm.hotosm.org"
      s3Credentials:
        accessKeyId:
          name: fmtm-s3-creds
          key: ACCESS_KEY_ID
        secretAccessKey:
          name: fmtm-s3-creds
          key: ACCESS_SECRET_KEY
    retentionPolicy: "90d"
EOF
```

<!-- markdownlint-disable -->
<details>
  <summary>Fish shell equivalent</summary>
<!-- markdownlint-enable -->
```bash
kubectl apply --filename (echo '
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: fmtm-db
spec:
  instances: 3
  imageName: ghcr.io/cloudnative-pg/postgis:16
  bootstrap:
    initdb:
      database: fmtm
      postInitTemplateSQL:
        - CREATE EXTENSION postgis;
        - CREATE EXTENSION postgis_topology;
        - CREATE EXTENSION fuzzystrmatch;
        - CREATE EXTENSION postgis_tiger_geocoder;
  storage:
    size: 1Gi
  backup:
    barmanObjectStore:
      destinationPath: "s3://fmtm-db-backups/"
      endpointURL: "https://s3.fmtm.hotosm.org"
      s3Credentials:
        accessKeyId:
          name: fmtm-s3-creds
          key: ACCESS_KEY_ID
        secretAccessKey:
          name: fmtm-s3-creds
          key: ACCESS_SECRET_KEY
    retentionPolicy: "90d"
' | psub)
```
<!-- markdownlint-disable -->
</details>
<!-- markdownlint-enable -->

Notes:

- This will use the latest PostGIS version.
  - For Postgres 16 this is PostGIS 3.4.
- For testing, the `backup` section can be removed.
- Full API reference for options (v1.21) on the
  [docs site](https://cloudnative-pg.io/documentation/1.21/cloudnative-pg.v1/)

Alternatively, generate the spec using the `cnpg` plugin:

```bash
kubectl cnpg install generate \
  -n fmtm \
  --replicas 3
```

> To delete the cluster, simply run the same command but use
> `kubectl delete` instead of `kubectl apply`.

### Get the DB Credentials

- By default the database is created in the controller namespace `cnpg-system`.
- A `postgres` password and user `password` are generated as secrets.
- To retrieve them:

```bash
kubectl get secret fmtm-db-app -o jsonpath='{.data.password}' | base64 -d

kubectl get secret fmtm-db-app -o jsonpath='{.data.pgpass}' | base64 -d
```

> In production the `superuserSecret` and `initdb.secret` spec values can be
> set to use a secret from a centralised secret manager.

### Connection Pooling

- `pg_bouncer` can be placed in front with a config such as:

```bash
cat <<EOF | kubectl apply --filename=-
apiVersion: postgresql.cnpg.io/v1
kind: Pooler
metadata:
  name: fmtm-pooler-rw
spec:
  cluster:
    name: fmtm-db
  instances: 3
  type: rw
  pgbouncer:
    poolMode: session
    parameters:
      max_client_conn: "1000"
      default_pool_size: "10"
EOF
```

<!-- markdownlint-disable -->
<details>
  <summary>Fish shell equivalent</summary>
<!-- markdownlint-enable -->
```bash
kubectl apply --filename (echo '
apiVersion: postgresql.cnpg.io/v1
kind: Pooler
metadata:
  name: fmtm-pooler-rw
spec:
  cluster:
    name: fmtm-db
  instances: 3
  type: rw
  pgbouncer:
    poolMode: session
    parameters:
      max_client_conn: "1000"
      default_pool_size: "10"
' | psub)
```
<!-- markdownlint-disable -->
</details>
<!-- markdownlint-enable -->

### Scheduled Backups

To run a daily scheduled backup to S3:

```bash
cat <<EOF | kubectl apply --filename=-
apiVersion: postgresql.cnpg.io/v1
kind: ScheduledBackup
metadata:
  name: fmtm-backup
spec:
  schedule: "0 0 0 * * *"
  backupOwnerReference: self
  cluster:
    name: fmtm-db
  target: prefer-standby
  method: barmanObjectStore
EOF
```

<!-- markdownlint-disable -->
<details>
  <summary>Fish shell equivalent</summary>
<!-- markdownlint-enable -->
```bash
kubectl apply --filename (echo '
apiVersion: postgresql.cnpg.io/v1
kind: ScheduledBackup
metadata:
  name: fmtm-backup
spec:
  schedule: "0 0 0 * * *"
  backupOwnerReference: self
  cluster:
    name: fmtm-db
  target: prefer-standby
  method: barmanObjectStore
' | psub)
```
<!-- markdownlint-disable -->
</details>
<!-- markdownlint-enable -->

#### Restoring The Backup

A new cluster can be deployed, using a backup source:

```bash
cat <<EOF | kubectl apply --filename=-
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: fmtm-db
spec:
  instances: 3
  storage:
    size: 1Gi
  bootstrap:
    recovery:
      source: clusterBackup
  externalClusters:
    - name: clusterBackup
      barmanObjectStore:
        destinationPath: "s3://fmtm-db-backups/"
        endpointURL: "https://s3.fmtm.hotosm.org"
        s3Credentials:
          accessKeyId:
            name: fmtm-s3-creds
            key: ACCESS_KEY_ID
          secretAccessKey:
            name: fmtm-s3-creds
            key: ACCESS_SECRET_KEY
EOF
```

<!-- markdownlint-disable -->
<details>
  <summary>Fish shell equivalent</summary>
<!-- markdownlint-enable -->
```bash
kubectl apply --filename (echo '
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: fmtm-db
spec:
  instances: 3
  storage:
    size: 1Gi
  bootstrap:
    recovery:
      source: clusterBackup
  externalClusters:
    - name: clusterBackup
      barmanObjectStore:
        destinationPath: "s3://fmtm-db-backups/"
        endpointURL: "https://s3.fmtm.hotosm.org"
        s3Credentials:
          accessKeyId:
            name: fmtm-s3-creds
            key: ACCESS_KEY_ID
          secretAccessKey:
            name: fmtm-s3-creds
            key: ACCESS_SECRET_KEY
' | psub)
```
<!-- markdownlint-disable -->
</details>
<!-- markdownlint-enable -->

### Accessing / Exposing The DB

- Note that exposing the database via a URL is typically not recommended
  and is generally not required.
- To connect to the database from an application **deployed in the same cluster**
  we can use the service URL:
  `<service-name>.<namespace>.svc.cluster.local:<service-port>`
- Instead, if external access is in fact required, we can use an Nginx Ingress.
- Documentation for this is available in
  [CloudNativePG docs](https://cloudnative-pg.io/documentation/1.21/expose_pg_services)
