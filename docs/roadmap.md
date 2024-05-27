# Brief Roadmap

The HOT Tech Team is working to improve the user experience across
multiple tools, and working towards an end to end data flow between
projects. Since often a disaster response, or humanitarian mapping
campaign, a project manager or mapper may use the [Tasking
Manager](https://hotosm.github.io/tasking-manager/), [Export Tool](https://hotosm.github.io/osm-export-tool/),
[fAIr](https://fair-dev.hotosm.org/),
[FMTM](https://hotosm.github.io/fmtm/), etc... For more information,
here's a short [E2E Presentation](techdoc/e2e.pdf).

To improve maintainability of the code base, the Text Team has been
working on modularizing all of our projects. Rather than duplicating
functionality used by multiple projects, that functionality has been
migrated to standalone python modules so they can be shared. There is
more detailed information on modularization [here](modules.md).

## Block Model Diagram

![block-model](./images/hot-tools-block-model.png)

## Overall Architecture

![detailed-e2e](./images/hot-components-model.png)
