# Use script-aware fonts for user interfaces

## Context and Problem Statement

HOT tools support many languages and scripts. HOT's brand fonts, Archivo and
Barlow, keep Latin text visually consistent but do not cover scripts such as
Arabic, Devanagari, Ethiopic, Bengali, Tamil, Telugu, Thai, CJK, or Cyrillic.

Pages may also mix scripts, for example a French interface showing a Nepali
project name. We need readable multilingual text without giving up visual
consistency or making every user download a large font package.

## Considered Options

- Use system sans-serif fonts everywhere.
- Use Archivo with a generic system fallback.
- Use a large multilingual font family such as Noto everywhere.
- Use the brand fonts for supported scripts and choose fallbacks per language
  or script.

## Decision Outcome

We will use Archivo, plus Barlow for headings and variants, for Latin text and
script-aware fallbacks for unsupported scripts.

- Start each font stack with the brand font, followed by system fonts with broad
  script coverage: Helvetica on Apple platforms, Noto on Android and ChromeOS,
  then `sans-serif`. The tokens live in
  [hotosm/ui-design `hot.css`](https://github.com/hotosm/ui-design/blob/main/css/dist/hot.css)
  and are shipped by `@hotosm/ui`.
- When adding a non-Latin language, test it on the
  [font test page](https://hotosm.github.io/ui-design/html/font-test.html).
  Add CSS `:lang()` rules only where needed to adjust the font, line height
  (for example, Devanagari and Thai), letter spacing (none for Arabic), or CJK
  font choice.
- Add correct `lang` attributes to content when its language differs from the
  page language, including user-created names and descriptions where known.
- If system fonts render a script poorly, add a suitable script-specific font,
  such as a Noto family from Fontsource, which ships pre-split files.
- Use `unicode-range` to subset self-hosted brand fonts and any fonts added, so
  browsers download only the glyphs needed for the page.
- Bake product wordmarks into logo SVGs when they must look identical across
  devices.

This approach prioritises readable, reliable interfaces in every supported
language while retaining HOT's visual identity where practical.

## Consequences

- ✅ Archivo and Barlow keep Latin-script interfaces visually consistent.
- ✅ Other scripts receive typography suited to their language.
- ✅ New languages can be supported incrementally.
- ✅ Font subsets limit downloads on slow or expensive connections.
- ❌ Typography may still vary between operating systems until a script-specific
  font is added.
- ❌ Each new script needs testing and may require a small amount of CSS.
- ❌ Mixed-language content must be marked with the correct `lang` attribute to
  receive the intended styling.
