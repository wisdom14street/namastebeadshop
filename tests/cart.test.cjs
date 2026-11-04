const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const { test } = require('node:test');
const vm = require('node:vm');
const source = readFileSync(join(__dirname, '../src/assets/cart.js'), 'utf8');

// Run the actual cart handlers with storage and network isolated from real shoppers.
function cart(initial = [], analytics = 'record') {
  const handlers = {}, events = [], storage = new Map();
  const key = 'ni_cart_v1:namastebeadshop.com';
  storage.set(key, JSON.stringify(initial));
  const window = { NI_CART: { shop: 'https://namastebookshop.com', domain: 'namastebeadshop.com',
    brand: 'Namaste Bead Shop', ref: 'namastebeadshop', attr: '?attributes%5BStorefront%5D=Namaste%20Bead%20Shop' },
    addEventListener() {} };
  if (analytics === 'record') window.gtag = (...args) => events.push(args);
  if (analytics === 'throw') window.gtag = () => { throw Error('Analytics blocked'); };
  const document = { querySelector: () => null, querySelectorAll: () => [],
    addEventListener: (name, fn) => { handlers[name] = fn; } };
  vm.runInNewContext(source, { window, document, localStorage: {
    getItem: k => storage.get(k), setItem: (k, v) => storage.set(k, v) },
    // Keep stock fetch pending so these assertions isolate quantity calculations.
    fetch: () => new Promise(() => {}), setTimeout: () => 0, URL, console });
  function click(items, checkout = false) {
    const attrs = checkout ? { 'data-checkout': '' } : { 'data-atc-items': JSON.stringify(items) };
    const button = { hasAttribute: k => Object.hasOwn(attrs, k), getAttribute: k => attrs[k],
      classList: { add() {}, remove() {} }, textContent: 'Add to cart' };
    handlers.click({ target: { closest: () => button }, preventDefault() {} });
    return button;
  }
  return { click, events, items: () => JSON.parse(storage.get(key)), url: () => window.NI_CART_URL() };
}
const item = { v: '101', h: 'fixture-mala', t: 'Fixture Mala', p: 24.99, q: 1, max: 2 };

test('a capped item does not emit a successful addition', () => {
  const c = cart([{ ...item, q: 2 }]);
  c.click([item]);
  assert.equal(c.items()[0].q, 2);
  assert.equal(c.events.length, 0);
});

test('a partially capped addition reports only the accepted quantity and value', () => {
  const c = cart([item]);
  c.click([{ ...item, q: 5 }]);
  assert.equal(c.items()[0].q, 2);
  assert.equal(c.events.length, 1);
  assert.equal(c.events[0][1], 'add_to_cart');
  assert.equal(c.events[0][2].items[0].quantity, 1);
  assert.equal(c.events[0][2].value, 24.99);
});

test('bundles report only items actually added', () => {
  const c = cart([{ ...item, q: 2 }]);
  c.click([item, { ...item, v: '202', h: 'fixture-bell', p: 12.99 }]);
  assert.equal(c.events.length, 1);
  assert.equal(c.events[0][2].items.length, 1);
  assert.equal(c.events[0][2].items[0].item_id, '202');
  assert.equal(c.events[0][2].value, 12.99);
});

test('checkout retains item quantities and all existing referral fields, excluding sold-out items', () => {
  const c = cart([{ ...item, q: 2 }, { ...item, v: '202', out: true }]);
  const url = new URL(c.click(null, true).href);
  assert.equal(url.origin, 'https://namastebookshop.com');
  assert.equal(url.pathname, '/cart/101:2');
  assert.equal(url.searchParams.get('attributes[Storefront]'), 'Namaste Bead Shop');
  assert.equal(url.searchParams.get('attributes[Site]'), 'namastebeadshop.com');
  assert.equal(url.searchParams.get('ref'), 'namastebeadshop');
  assert.equal(url.searchParams.get('note'), 'Ordered on Namaste Bead Shop (namastebeadshop.com)');
  assert.equal(c.events.length, 1);
  assert.equal(c.events[0][1], 'begin_checkout');
  assert.equal(c.events[0][2].value, 49.98);
  assert.equal(c.events[0][2].items.length, 1);
});

test('empty carts cannot create a checkout or checkout event', () => {
  const c = cart();
  c.click(null, true);
  assert.equal(c.url(), '');
  assert.equal(c.events.length, 0);
});

test('missing or failing analytics never blocks cart persistence or checkout', () => {
  for (const state of ['missing', 'throw']) {
    const c = cart([], state);
    c.click([item]);
    assert.equal(c.items()[0].q, 1);
    assert.ok(c.click(null, true).href.startsWith('https://namastebookshop.com/cart/101:1?'));
  }
});
