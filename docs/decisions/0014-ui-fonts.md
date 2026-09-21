# Use script-aware fonts for user interfaces

## Context and Problem Statement

HOT tools support many languages and scripts. Archivo provides consistent HOT
branding for Latin text, but does not cover scripts such as Arabic, Devanagari,
Ethiopic, Bengali, Tamil, Telugu, Thai, CJK, or Cyrillic.

Pages may also mix scripts, for example a French interface showing a Nepali
project name. We need readable multilingual text without giving up visual
consistency or making every user download a large font package.

## Considered Options

- Use system sans-serif fonts everywhere.
- Use Archivo with a generic system fallback.
- Use a large multilingual font family such as Noto everywhere.
- Use Archivo for supported scripts and choose fallbacks per language or script.

## Decision Outcome

We will use Archivo for Latin text and script-aware fallbacks for text that
Archivo does not support.

- Start with Archivo followed by a named list of suitable system fonts.
- Use CSS `:lang()` rules to adjust fonts, line height, letter spacing, and
  other typography where a script needs it.
- Add correct `lang` attributes to content when its language differs from the
  page language, including user-created names and descriptions where known.
- If system fonts render a script poorly, add a suitable font such as a Noto
  family for that script.
- Subset added fonts with `unicode-range` so browsers download only the glyphs
  needed for the page.
- Bake product wordmarks into logo SVGs when they must look identical across
  devices.

This approach prioritises readable, reliable interfaces in every supported
language while retaining HOT's visual identity where practical.

## Consequences

- ✅ Archivo keeps Latin-script interfaces visually consistent.
- ✅ Other scripts receive typography suited to their language.
- ✅ New languages can be supported incrementally.
- ✅ Font subsets limit downloads on slow or expensive connections.
- ❌ Typography may still vary between operating systems until a script-specific
  font is added.
- ❌ Each new script needs testing and may require a small amount of CSS.
- ❌ Mixed-language content must be marked with the correct `lang` attribute to
  receive the intended styling.
