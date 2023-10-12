# Modularization

HOT has many tools and services, of which there is potential for code duplication.

Modularization of backend and frontend components allows us to avoid repeating code.

## Backend

Backend Python modules are released on
[PyPi](https://pypi.org) to be installed across multiple services.

See the [backend](https://hotosm.github.io/docs/modules_backend) page for more info.

## Frontend

As a form of standardisation,
we use [React](https://react.dev/) as our frontend framework.

Many services have common UI components that
can be shared (headers, buttons, sidebars, etc).

We also use frontend map libraries extensively (obviously).

Currently we favour [OpenLayers](https://openlayers.org/)
due to it's breadth of functionality

See the [frontend](https://hotosm.github.io/docs/modules_frontend)
page for more info.
