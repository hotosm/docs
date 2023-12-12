# Modularization

HOT has many tools which have similar requirements for backend and
frontend functionality. To reduce long-term maintainance and code
duplication, it's better to have the shared functionality in
standalone modules. The other advantage of small sharable modules is
it's much easy to enhance or debug when not buried in much larger
prohects.

## Backend

Backend Python modules are released on
[PyPi](https://pypi.org) to be installed across multiple services.

See the [backend](modules/backend.md) page for more info.

## Frontend

As a form of standardization, we use [React](https://react.dev/) as
our frontend framework.

Many services have common UI components that can be shared (headers,
buttons, sidebars, etc).

We also use frontend map libraries extensively (obviously).

Currently we favour [OpenLayers](https://openlayers.org/) due to it's
breadth of functionality.

See the [frontend](modules/frontend.md) page for more info.
