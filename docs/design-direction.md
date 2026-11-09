# Design direction: bright and friendly (approved)

Keep all existing wording; change the design.

- **Feel:** bright, warm, trustworthy; real product photos carry the page.
- **Palette:** light background, near-black text, one friendly accent colour plus a soft secondary (to be proposed in the first build).
- **Type:** rounded/friendly sans for headings, clean sans for body.
- **Header:** announcement bar (shipping line), search, cart, mega-menu for the 12 categories.
- **Homepage:** seasonal hero, category tiles, new arrivals, featured picks, "Buy 2, save 10%" strip, pet and home spotlights, trust row, newsletter.
- **Collection:** clean grid, filters, skeleton loading, offer badges.
- **Product:** sticky gallery, mobile bottom-sheet variants, sticky add-to-cart, delivery estimate and trust row near the button, Judge.me reviews, add-to-cart toast.
- **Cart:** drawer with offer nudge and delivery reminder.
- **Footer:** large wordmark, grouped links, newsletter above links, shipping/returns row.
- **Motion:** subtle fades and hover zoom, reduced-motion safe.

## Build order
1. Design tokens (colours, type, spacing) in `assets/theme.css`
2. Header, footer
3. Homepage
4. Collection and product cards
5. Product page
6. Cart drawer
7. QA on mobile and desktop, then launch checklist
