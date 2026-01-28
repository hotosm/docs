# Testing with Kubernetes Locally

!!! note

    This page was created before we had our
    [k8s-infra](https://github.com/hotosm/k8s-infra) repository.

    It is recommend to follow the guides on the
    [docs page](https://hotosm.github.io/k8s-infra) for that repo,
    including how to set up a local cluster using TalosOS instead.

We will use an official tool Kubernetes-In-Docker (KIND) to run Kubernetes via
Docker locally.

This is useful for testing Kubernetes configuration locally,
and trialing software too.

## Install Tools

### Kubectl

Used to control Kubernetes clusters.

```bash
temp_dir=$(mktemp -d)
cd "${temp_dir}"

[ $(uname -m) = x86_64 ] && curl -Lo ./kubectl \
https://dl.k8s.io/release/\
$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/\
$(uname -s | tr '[:upper:]' '[:lower:]')/amd64/kubectl

chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl

rm -rf "$temp_dir"
```

### KIND

Used to run a Kubernetes cluster locally.

```bash
temp_dir=$(mktemp -d)
cd "${temp_dir}"

[ $(uname -m) = x86_64 ] && curl -Lo ./kind \
https://kind.sigs.k8s.io/dl/v0.22.0/kind-$(uname)-amd64

chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

rm -rf "$temp_dir"
```

<!-- markdownlint-disable -->
<details>
  <summary>Optional Config</summary>
<!-- markdownlint-enable -->

Kubie: used to easily switch Kubernetes context (i.e. multiple clusters).

```bash
temp_dir=$(mktemp -d)
cd "${temp_dir}"

[ $(uname -m) = x86_64 ] && curl -Lo ./kubie \
https://github.com/sbstp/kubie/releases/download/v0.23.0/kubie-\
$(uname -s | tr '[:upper:]' '[:lower:]')-amd64

chmod +x ./kubie
sudo mv ./kubie /usr/local/bin/kubie

rm -rf "$temp_dir"
```

Helm: used to install software into the cluster.

```bash
temp_dir=$(mktemp -d)
cd "${temp_dir}"

[ $(uname -m) = x86_64 ] && curl -Lo ./helm.tar.gz \
https://get.helm.sh/helm-v3.14.3-$(uname -s | tr '[:upper:]' '[:lower:]')-amd64.tar.gz

tar -xvzf helm.tar.gz
sudo mv $(uname -s | tr '[:upper:]' '[:lower:]')-amd64/helm /usr/local/bin/helm

rm -rf "$temp_dir"
```

BASH (bashrc) aliases

```bash
echo alias k='kubectl' >> ~/.bashrc
echo alias kcc='kubie ctx' >> ~/.bashrc
echo alias ns='kubie ns' >> ~/.bashrc
source ~/.bashrc
```

fish aliases

```bash
echo alias k='kubectl' >> ~/.config/fish/config.fish
echo alias kcc='kubie ctx' >> ~/.config/fish/config.fish
echo alias ns='kubie ns' >> ~/.config/fish/config.fish
source ~/.config/fish/config.fish
```

<!-- markdownlint-disable -->
</details>
<!-- markdownlint-enable -->

## Create a Cluster

- Run the following to create a cluster with Ingress ports bound:

```bash
cat <<EOF | kind create cluster --name local --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 7080
    protocol: TCP
  - containerPort: 443
    hostPort: 7433
    protocol: TCP
EOF
```

> The cluster will be named 'kind-local'

<!-- markdownlint-disable -->
<details>
  <summary>Fish shell equivalent</summary>
<!-- markdownlint-enable -->
```bash
kind create cluster --name local --config (echo '
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 7080
    protocol: TCP
  - containerPort: 443
    hostPort: 7433
    protocol: TCP
' | psub)
```
<!-- markdownlint-disable -->
</details>
<!-- markdownlint-enable -->

> Cluster services will be accessible under <http://localhost:7080>
>
> Change the hostPort variable if you wish to use a different port.

## Deploy the Ingress Controller

Contour uses Envoy and may be a good choice in production.

But the simplest and most battle tested in the Nginx ingress.

Deploy with:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Check when it is ready:

```bash
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

### Test the Ingress

Run test service:

```bash
cat <<EOF | kubectl apply --filename=-
kind: Pod
apiVersion: v1
metadata:
  name: foo-app
  labels:
    app: foo
spec:
  containers:
  - command:
    - /agnhost
    - netexec
    - --http-port
    - "8080"
    image: registry.k8s.io/e2e-test-images/agnhost:2.39
    name: foo-app
---
kind: Service
apiVersion: v1
metadata:
  name: foo-service
spec:
  selector:
    app: foo
  ports:
  # Default port used by the image
  - port: 8080
---
kind: Pod
apiVersion: v1
metadata:
  name: bar-app
  labels:
    app: bar
spec:
  containers:
  - command:
    - /agnhost
    - netexec
    - --http-port
    - "8080"
    image: registry.k8s.io/e2e-test-images/agnhost:2.39
    name: bar-app
---
kind: Service
apiVersion: v1
metadata:
  name: bar-service
spec:
  selector:
    app: bar
  ports:
  # Default port used by the image
  - port: 8080
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  rules:
  - http:
      paths:
      - pathType: Prefix
        path: /foo(/|$)(.*)
        backend:
          service:
            name: foo-service
            port:
              number: 8080
      - pathType: Prefix
        path: /bar(/|$)(.*)
        backend:
          service:
            name: bar-service
            port:
              number: 8080
---
EOF
```

<!-- markdownlint-disable -->
<details>
  <summary>Fish shell equivalent</summary>
<!-- markdownlint-enable -->
```bash
kubectl apply --filename (echo '
kind: Pod
apiVersion: v1
metadata:
  name: foo-app
  labels:
    app: foo
spec:
  containers:
  - command:
    - /agnhost
    - netexec
    - --http-port
    - "8080"
    image: registry.k8s.io/e2e-test-images/agnhost:2.39
    name: foo-app
---
kind: Service
apiVersion: v1
metadata:
  name: foo-service
spec:
  selector:
    app: foo
  ports:
  # Default port used by the image
  - port: 8080
---
kind: Pod
apiVersion: v1
metadata:
  name: bar-app
  labels:
    app: bar
spec:
  containers:
  - command:
    - /agnhost
    - netexec
    - --http-port
    - "8080"
    image: registry.k8s.io/e2e-test-images/agnhost:2.39
    name: bar-app
---
kind: Service
apiVersion: v1
metadata:
  name: bar-service
spec:
  selector:
    app: bar
  ports:
  # Default port used by the image
  - port: 8080
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  rules:
  - http:
      paths:
      - pathType: Prefix
        path: /foo(/|$)(.*)
        backend:
          service:
            name: foo-service
            port:
              number: 8080
      - pathType: Prefix
        path: /bar(/|$)(.*)
        backend:
          service:
            name: bar-service
            port:
              number: 8080
---
' | psub)
```
<!-- markdownlint-disable -->
</details>
<!-- markdownlint-enable -->

> $ curl localhost:7080/foo/hostname
>
> should output "foo-app"
>
> $ curl localhost:7080/bar/hostname
>
> should output "bar-app"

Cleanup test resources:

```bash
kubectl delete pod foo-app
kubectl delete pod bar-app
kubectl delete svc foo-service
kubectl delete svc bar-service
kubectl delete ingress example-ingress
```
