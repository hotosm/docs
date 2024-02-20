# Overarching Architecture Folder
While today HOT architecture consists of a wide range of applications
and modules, the vision for the future is a more unified ecosystem.

The key features of this architecture are:
* An integrated set of back-end modules
* A common data model based on standards and only extending as required
* Fit for purpose front-ends, built on REACT

Please refer to the [decisions](/decisions) log for details about HOT
architecture decisions.

## HOT Overarching View
This is an overarching view of the HOT ecosystem of solutions. It
includes some key non-HOT components for context and because they
serve an important role in the ecosystem.</br></br>

[LibreOffice Source](HOT%20Overarching%20Block%20Diagram.odg)<br/>
![Overarching](HOT%20Overarching%20Block%20Diagram.png)

## Solution User View
This solution user view provides a user-centric view of the HOT
architecture showing the key user roles and what activities they will
perform using the solution. You can learn more about the diagram and
notation
[here](https://github.com/hotosm/techdoc/wiki/Architecture-Documents-Walkthrough#solution-user-diagram).<br/><br/>
[LibreOffice Source](HOT%20Solution%20User.odg)<br/>
![Solution User View](HOT%20Solution%20User.png)

## Information Flow
This information flow is a dynamic view that shows the flow of
information (in high level business terms) between the HOT ecosystem
components. You can learn more about the diagram and notation
[here](https://github.com/hotosm/techdoc/wiki/Architecture-Documents-Walkthrough#information-flow).<br/><br/>
[LibreOffice Source](HOT%20Information%20Flow.odg)<br/>
![Information Flow Diagram](HOT%20Information%20Flow.png)

## Component Model
This component model is a static view that shows how the HOT ecosystem
components connect to one another. You can learn more about the
diagram and notation
[here](https://github.com/hotosm/techdoc/wiki/Architecture-Documents-Walkthrough#component-model).<br/><br/>
[LibreOffice Source](HOT%20Component%20Diagram.odg)<br/>
![Component Diagram](HOT%20Component%20Diagram.jpg)

## E2E Data Integration Diagrams
This is the high level concept for the E2E data integration
approach. The TD Admin components in the center are not actually a hub
instance, but a set of shared modules used for connectivity.<br/><br/>
[LibreOffice Source](E2E%20Data%20Integration%20Layer.odg)<br/>
![Conceptual Data Model](E2E%20Data%20Integration%20Layer.jpg)
<br/>
Here is a zoom in showing how that would work between two components.<br/>
![Conceptual Data Model](E2E%20Data%20Integration%20Layer%20-%20Zoom.png))

## E2E Integration Sequence Diagrams
These show the interactions between multiple components at a more detailed level.
|  |  |
|--|--|
| <img src="OSDs/Overarching%20OSD%20-%20TM%20User%20Profiles%20to%20FTM.png" width="90%"/> | <img src="OSDs/Overarching%20OSD%20-%20TM%20Org%20Profiles%20to%20FTM.png" width="90%"/> |
| <img src="OSDs/Overarching%20OSD%20-%20TM%20Projects%20to%20FTM.png" width="90%"/> | . |

## E2E Conceptual Data Model
This is a conceptual data model, illustrating the key entities and relationship in the data model.
[LibreOffice Source](Overarching%20Data%20Model.odg)<br/>
![Conceptual Data Model](E2E%20Draft%20Data%20Model.png)
