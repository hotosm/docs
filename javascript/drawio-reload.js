document$.subscribe(({ _body }) => {
  GraphViewer.processElements();
});
