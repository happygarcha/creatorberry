# Store audit (read from the live storefront)

- Store: Drapewell, Surrey BC. Currency CAD. Plan: Basic.
- Sells: home textiles and decor, outdoor, pet supplies, desk and hobby, fashion accessories, kitchen, bathroom, car accessories, seasonal (Christmas).
- Categories: Bathroom (Shower Curtains, Bath Mats), Beauty, Bedroom, Car Accessories, Desk & Hobby, Fashion, Kitchen, Living Room, Outdoors, Pet Supplies, Seasonal (Christmas Table Runners), Tech.
- Typical prices: CA$13-65.
- Shipping: Canada 13-25 days from CA$9.99; US 10-20 days; tracked; duties included on US orders; 30-day damaged/wrong item policy.
- Existing features to keep: announcement bar, "Buy 2, save 10%" offer, cart drawer, Judge.me reviews, trust row, shipping estimate, size guide.

## Test theme file layout (Drapewell Website Test)
- layout: theme.liquid, GemPages blank/header/footer variants
- sections: home, collection, product, cart, search, list-collections, page, not-found, side-feeds, gp-variant-selected
- snippets: product-card, price, rating-stars, reviews, trust-row, ship-estimate, size-guide, offer-flag, offer-nudge, cart-drawer, checkout-strip, hero-slide, home-row, breadcrumbs, seo-meta, policy-links, gp-head
- assets: theme.css, theme.js, motion.js, gp-global.css, fonts (archivo, inter)
- templates: index, collection, product, cart, search, page, 404, list-collections, llms.txt

Note: GemPages templates and SEO snippets exist; keep `seo-meta.liquid` and `llms.txt.liquid` behaviour intact when redesigning.
