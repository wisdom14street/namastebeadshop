# namastebeadshop.com

Namaste Bead Shop: static storefront built daily from the public namastebookshop.com catalog and deployed to GitHub Pages.
Namaste Bead Shop is a brand of Wealth Edge Ventures Inc.

- `site/config.json`: site settings. Set `REVIEW_URL` (Google review link) to show the "Review us on Google" button and QR code; set `GOOGLE_SITE_VERIFICATION` to the Search Console HTML-tag value. Both stay hidden while empty. `kinds`, `max_price` and `best_collections` limit what the daily pickup and best-seller checks fetch.
- `site/sitecopy.py`: aisles, product mix rules and all copy for this site.
- `site/theme.css`, `site/favicon.svg`: this site's design.
- `scripts/`: shared jewelry/bead engine (fetch with pagination and 429 backoff, Shopify pickup check, best sellers, build).
- Checkout: Add-to-cart buttons keep a local basket. Checkout passes its variants and quantities to `namastebookshop.com/cart/<variant>:<quantity>,...` with `attributes[Storefront]=Namaste Bead Shop`, `attributes[Site]=namastebeadshop.com`, the existing order note, and `ref=namastebeadshop`. These are source markers, not proof that a purchase completed or a Shopify order tag was created. Confirm them on the resulting order before attributing revenue. See [Shopify's cart permalink documentation](https://shopify.dev/docs/apps/build/checkout/create-cart-permalinks).
- Analytics: GA4 is already configured through `GA_MEASUREMENT_ID`. Do not add another tag. `view_item`, `add_to_cart`, `begin_checkout` and contact/directions events describe activity on this storefront; `begin_checkout` records the handoff click, not a completed purchase. Additions at the cart quantity limit do not count as new items. This code sends no `purchase` event. Filter reports by hostname `namastebeadshop.com`; verify checkout-side measurement and cross-domain settings in the existing GA4/Shopify setup before reporting conversion rates. Preview builds disable GA4. Counts can differ from all visitors when analytics is blocked or unavailable.
- Bookshop links: the footer and About page point to `https://namastebookshop.com/?ref=namastebeadshop`; no new storage or visitor identifiers are added.

Validation runs before each daily or push deployment:

```sh
python3 -m unittest discover -s tests
node --test tests/cart.test.cjs
python3 scripts/check_site.py  # after scripts/build.py
```

The offline fixtures cover sparse inventories, missing stone pages, analytics isolation and quantity limits. The generated-site check rejects broken local destinations, missing assets and duplicate social metadata. Source products, images, prices, inventory and pickup availability remain supplied by Namaste Bookshop. Search Console verification is optional configuration; an empty verification tag alone does not establish whether DNS verification exists.
