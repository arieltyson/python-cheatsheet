"use strict";

// Progressive enhancement only: the page is complete without this file.

function markCurrentSection() {
  const links = new Map(
    [...document.querySelectorAll(".toc ol ol a")].map((link) => [
      link.hash.slice(1),
      link,
    ]),
  );
  let current = null;
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        current?.removeAttribute("aria-current");
        current = links.get(entry.target.id) ?? null;
        current?.setAttribute("aria-current", "location");
      }
    },
    { rootMargin: "-10% 0px -85% 0px" },
  );
  for (const section of document.querySelectorAll("main .section")) {
    observer.observe(section);
  }
}

markCurrentSection();
