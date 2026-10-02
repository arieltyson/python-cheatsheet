# 002: Colours are data

## Context

Contrast claims in comments drift as colours change.

## Decision

Every colour is defined once in `web/tokens.toml` as a `[light, dark]`
pair. The build emits CSS custom properties with `light-dark()`, and
`tests/test_contrast.py` reads the same file and asserts WCAG AA (4.5:1)
for every text and syntax colour on every background it appears on.

## Consequence

A colour literal anywhere else in the CSS is a defect. Changing a
colour that fails contrast fails the build.
