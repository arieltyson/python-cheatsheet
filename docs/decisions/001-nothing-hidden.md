# 001: Nothing on the page is hidden

## Context

The page is used mid-interview, in a narrow window, with Cmd+F. The
browser's find only searches text that is rendered. Collapsed sections,
tabs, lazy loading and menus hide text from it.

## Decision

All content is plain text in the first HTML response. No accordions,
tabs, `display: none` content, lazy loading or client-side rendering of
content. The table of contents moves above the content on narrow
screens instead of collapsing behind a menu button. JavaScript only adds
controls (jump list, copy buttons, theme toggle).

## Consequence

The page is long. That is accepted: length costs nothing when every
lookup is a search. A build test fails if content inside `<main>` is
hidden.
