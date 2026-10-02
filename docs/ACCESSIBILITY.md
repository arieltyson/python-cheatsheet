# Accessibility

[Python CheatSheet](https://arieltyson.github.io/python-cheatsheet/)
is designed to keep its interview reference readable, searchable,
and usable with a keyboard.

## Implemented

- All reference content is present in one static page, including when
  JavaScript is disabled. Use Cmd+F or Ctrl+F to search the full page.
- A skip link, named contents navigation, main landmark, and ordered
  headings support navigation through the document.
- Code is selectable text. Lines wrap, and text sizes use relative
  units so they follow the reader's font size.
- Keyboard controls have focus styles. With JavaScript enabled, the
  jump list opens with `/` or the Jump to button; arrow keys move
  through results, Enter selects a result, and Escape closes it.
  Selecting a result moves focus to its heading.
- Copy buttons have labels that identify the entry. Code can also be
  selected and copied manually.
- Light and dark appearance follow the system preference, with an
  optional manual theme control.
- The heading highlight transition is disabled when the system
  requests reduced motion.

## Verified automatically

[Contrast tests](../tests/test_contrast.py) check the configured text
and syntax colours against their specified backgrounds in both themes
for a contrast ratio of at least 4.5:1.

[Built-page tests](../tests/test_page.py) check that every entry is
present, main content is not hidden, heading levels do not skip,
static buttons have names, IDs are unique, and the page declares its
language as English. These checks run in the repository's CI.

## Limitations and remaining checks

These checks do not establish full WCAG conformance. Manual assessment
is still needed for screen-reader navigation and announcements,
including the jump list and copy feedback, as well as high zoom,
increased text spacing, forced colours, and touch interaction across
browsers. The static-page tests do not exercise JavaScript controls.

The jump list, copy buttons, and manual theme control require
JavaScript. The reference content and contents links remain available
without it.

## Report an accessibility problem

[Open an issue](https://github.com/arieltyson/python-cheatsheet/issues/new)
with the entry link, what you tried, what happened, and what you
expected. Include your browser, operating system, assistive technology,
and zoom or text-size settings when relevant.
