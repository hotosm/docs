# Using Tailscale to Access Kubernetes Clusters

We use Tailscale to keep Kubernetes control planes off the public internet.

Instead of opening the Kubernetes API to public IP addresses, approved devices
join a private HOT network called a tailnet. `kubectl` then reaches the
cluster through the Tailscale operator's API server proxy.

The proxy identifies you by your Tailscale identity, and the tailnet policy
maps your group to Kubernetes RBAC permissions. No personal credentials are
stored in your kubeconfig.

## Access Model

Cluster access has three layers:

- Tailscale account access: you must be allowed into the HOT tailnet.
- Device approval: your laptop must be approved by a tailnet admin.
- Kubernetes access: your tailnet group (e.g. admin, read-only, contractor)
  decides your RBAC permissions.

## Privacy And Device Access

Installing Tailscale does not give everyone access to your laptop.

- Other users do not automatically get SSH, file, screen, or browser access.
- SSH access must be explicitly enabled and allowed by Tailscale policy.
- Normal SSH also requires an SSH server, a local user, and valid credentials.
- Kubernetes permissions are separate from Tailscale. Being on the tailnet does
  not grant cluster admin access.
- Tailnet admins can see device metadata such as device name, account, tailnet
  IP, operating system, and connection status. This is needed to manage access.
- Tailnet admins cannot see your local files, screen, browser history, or
  non-Tailscale traffic through the admin console.
- You can disconnect Tailscale when you are not working with cluster resources.

Use a clear device name such as `first-last-laptop`. Avoid putting private
details in the device name, since it may be visible in the tailnet.

## Before You Start

You need:

- Tailscale installed on your machine.
- `kubectl` installed.
- Access to the correct HOT GitHub account or organization.
- Device approval from a Tailscale admin.

## Connecting As Staff

1. Install Tailscale from <https://tailscale.com/download>.
2. Open Tailscale and sign in with GitHub.
3. Select the `user@hotosm` tailnet.
4. Make sure you are not connected to a personal or private tailnet.
5. Ask a Tailscale admin to approve your device.
6. Confirm you are connected:

```bash
tailscale status
```

7. Generate your kubeconfig. This adds a context for the cluster to
   `~/.kube/config` and switches to it:

```bash
tailscale configure kubeconfig hotosm-k8s-operator
```

8. Test access:

```bash
kubectl get namespaces
```

If the command works, you can use the cluster according to your Kubernetes RBAC
permissions.

## Connecting As A Contractor

Contractor access is more restricted than staff access.

1. Install Tailscale from <https://tailscale.com/download>.
2. Open Tailscale and sign in with the GitHub account provided for the contract.
3. Select the `hotosm-contractors@hotosm` tailnet.
4. Ask a Tailscale admin to approve your device.
5. Generate your kubeconfig:

```bash
tailscale configure kubeconfig hotosm-k8s-operator
```

6. Test access:

```bash
kubectl get namespaces
```

Contractor access is usually read-only by default. Edit access can be granted for
specific namespaces when needed.

## Troubleshooting

If `kubectl` cannot connect:

- Check that Tailscale is running.
- Check that you joined the correct tailnet.
- Check that your device has been approved.
- Check that your current context is the operator
  (`kubectl config current-context`), pointing at
  `https://hotosm-k8s-operator.banded-armadillo.ts.net`.

If `kubectl` connects but says `Forbidden`, the network is working. Ask a
Tailscale admin to check you are in the right tailnet group.

If you no longer need access, ask a Tailscale admin to remove your device from
the tailnet.
