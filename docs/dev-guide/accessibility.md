# Accessibility

Accessibility in this context means making your app as easy as possible to
use for users with impairments of any kind.

In the context of web this would typically only involve visual and cognitive
impairments, or low literacy levels.

With this in mind, an application should:

- Have ARIA labels in the UI component (must be included in development).
- Have large print / contrast options (this can typically be covered by
  any modern web browser).
- Using icons rather than text where possible.
- Making application usage as intuitive as possible.

## ARIA & Component Design

The following sections will describe how to make a web UI as accessible
as possible.

W3 maintains a guide on
[ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)

### Keyboard Interaction

- The component can be selected using a keyboard button (e.g. tab key).
- Add `tabindex='0'` to your control or possibly `aria-activedescendant`.

### Visually Intuitive States

- When a component changes state, e.g. `focus`, `hover`, `active`, the UI
  change should be clearly defined by a distinctive styling.

### ARIA Labels For State

- When a component changes state, there are often ARIA labels to help
  describe this.
- `aria-expanded` can be used when a modal is toggled open or closed.
- A multiline textbox can have `aria-multiline` to better communicate this.
- `aria-selected` can be attached to each item in a dropdown to indicate
  selected state.
- Full W3 guide [here](https://www.w3.org/TR/wai-aria-1.1/)

### ARIA Labels For Function

- A component can be labeled with it's stated function.
- For example a button may save your work, so should be labelled `Save`.
- Sometimes the labelled is implicit, for example if the button is defined
  as such `<button>Save</button>`, then the text content will be used.
- `aria-label` is used in all other cases, or to override the label.
  `<button aria-label="Save">Save The Thing</button>`
- `aria-labelledby` is used when we want to refer to another component
  for labelling:

  ```html
  <input type="search" aria-labelledby="this" />
  <button id="this">Search</button>
  ```

This is far from an exhaustive list on available accessibility options!
