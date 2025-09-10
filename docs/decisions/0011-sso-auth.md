# Use Hanko for shared auth SSO solution across HOT apps

## Context and Problem Statement

We need a form of shared authentication to:

- Have shared login between apps, so if I login into one HOT tool,
  I am automatically logged into the others.
- Reduce code duplication across tools, where we have custom logic
  to login via various OAuth providers. This is for both the
  frontend and the backend code.
- Centralise OAuth config for a single app to connect to OSM / Google
  etc, for easier management. No need to configure credentials for
  every single app.
- Have a consistent login flow for all apps, making for better user
  experience, and developer experience (we can bundle config in hotosm/ui).
- It would also be nice to integrate modern passwordless logins such as
  passkeys with biometrics (bonus).

Other requirements:

- An option to delete user profiles when requested.
- Easy way for self-hosters of our tool to include Hanko.

## Considered Options

- Authelia
- Authentik
- Auth0
- Keycloak
- Hanko

## Decision Outcome

Auth0 is closed source. Keycloak is antiquated Java and too heavyweight.

Authelia and Authentik are both similar tools, with a preference for Athelia,
written in Golang and extremely simple to run + resource efficient.

However Authelia is primarily focused around acting as auth for reverse proxied
apps. Typically the entire web UI / interface is placed behind the reverse
proxy, with authelia there to check if the user is authenticated. The request
is intercepted and the users is redirected to login, then can access the app
afterwards - **this is not what we want**.

Instead, we need a true Identity Provider that issues and verifies tokens,
which our APIs can validate independently. The IdP does not sit 'in front' of
services like a reverse proxy — it just handles the login flow:

- The frontend is public.
- The user clicks to 'log in' and does an OAuth redirect flow.
- The user is returned to the web frontend, with a JWT set in a secure cookie.
- The cookie is sent to the API, verifying that the user is logged in.

In order to delete a user profile, this is still done per-app database (not changed).
The user info stored in the Hanko db from OAuth is minimal and does not need to be
considered.

As for self-hosting, we can provide the lightweight Hanko binary / container as part
of the docker compose config for self-hosters to include (the binary footprint is
minimal / microservice). HOT will use a single centralized Hanko instance, while
self-hosters will primarily have a bundled Hanko instance per tool (it's unlikely
they will be deploying all of our tools together).

## Consequences

- ✅ Reduced developer overhead: code and key management.
- ✅ Better user experience, with only a single login required.
- ✅ Easy configuration of any OAuth provider we want underneath,
  rolled out to all apps at the same time. Self-hosters can also
  use any combination of providers they wish.
- ✅ We rely on standard OIDC flows: the frontend does PKCE with
  the IdP, gets a JWT, stores it in an HttpOnly cookie, sends it to
  the API, which verifies the JWT signature and claims.
- ❌ Adds a single point of failure for auth (mitigated by running in
  kubernetes with multiple replicas).
- ❌ Increases complexity of deployment slightly. The HOT deployment
  relies on the centralised `login.hotosm.org` provider. For self-hosters,
  we will have to provide a config that bundles the small Hanko binary
  to host their own IdP.
