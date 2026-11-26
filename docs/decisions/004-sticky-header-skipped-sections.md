# 004: Sticky header on wide screens, off-screen sections skipped

## Context

The section links scrolled away on a page tens of thousands of pixels
tall, and every theme switch or resize re-laid out all of it.

## Decision

From 68.75rem up, the header is sticky and opaque (no blur, which
would be redrawn on every scroll frame). `app.js` measures its height
into `--header-height` with a `ResizeObserver`, which feeds the TOC's
`top`, and `scroll-padding-top` so jumps and focus land below it.
Phones keep it in the flow. Each `.section` has
`content-visibility: auto`, so off-screen sections skip style, layout
and paint. Cmd+F, the jump list and printing still reach all of it, so
decision 001 holds.

## Consequence

In headless Chrome at 1280 px, the first layout fell from about 41 ms to
6 ms and a theme switch from 7.4 ms to 0.2 ms. A section is its own
layout box, so its top gap sits on the section, and an 8 px inline
padding keeps outlines and highlights from clipping. Ported from Swift
CheatSheet.
