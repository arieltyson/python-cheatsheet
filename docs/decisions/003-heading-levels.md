# 003: Entries are h4, not h3

## Context

The Design plan said "part h2, section and entry h3". Screen reader
users navigate by heading level, and entries sit inside sections.

## Decision

Reversed: page title h1, part h2, section h3, entry h4.
`tests/test_page.py` asserts that heading levels never skip.

## Consequence

The heading outline matches the visual nesting, and "next h3" moves
between sections while "next h4" moves between entries.
