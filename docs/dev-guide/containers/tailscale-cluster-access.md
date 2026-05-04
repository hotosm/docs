# Using Tailscale to Access Kubernetes Clusters

We use Tailscale to keep Kubernetes control planes off the public internet.

Instead of opening the Kubernetes API to public IP addresses, approved devices
join a private HOT network called a tailnet. `kubectl` can then reach the
control plane through its Tailscale IP.

Tailscale only handles the network path. Kubernetes access is still controlled
by your kubeconfig and Kubernetes RBAC permissions.

## Access Model

Cluster access has three layers:

- Tailscale account access: you must be allowed into the HOT tailnet.
- Device approval: your laptop must be approved by a tailnet admin.
- Kubernetes access: your kubeconfig and RBAC permissions decide what you can do.

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
- A kubeconfig from a cluster admin.
- Device approval from a Tailscale admin.

Keep your kubeconfig private. It is the credential that tells Kubernetes who you
are and what you can access.

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

7. Add the kubeconfig provided by the cluster admin.
8. Make sure the kubeconfig points to the cluster control plane Tailscale IP.
9. Test access:

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
5. Add the kubeconfig provided for your work.
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
- Check that the kubeconfig server address is the cluster control plane
  Tailscale IP.

If `kubectl` connects but says `Forbidden`, the network is working. Ask a
cluster admin to check your Kubernetes RBAC permissions.

If you no longer need access, ask a Tailscale admin to remove your device from
the tailnet.
