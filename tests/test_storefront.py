"""Inventory-boundary regressions. Fixtures are synthetic and never contact Shopify."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_site import check


def product(index, title):
    return {'id': index, 'handle': f'fixture-{index}', 'title': title, 'vendor': '',
            'product_type': 'Brass Singing Bowl' if 'Bowl' in title else '', 'created_at': '2026-01-01', 'body_html': '',
            'images': [{'src': f'https://example.com/fixture-{index}.jpg'}],
            'variants': [{'id': index * 10, 'title': 'Default Title', 'price': '24.99',
                          'available': True, 'sku': f'TEST-{index}'}]}


class StorefrontTest(unittest.TestCase):
    def build(self, products, preview=False):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        for name in ('scripts', 'src', 'site'):
            shutil.copytree(ROOT / name, root / name, ignore=shutil.ignore_patterns('__pycache__'))
        (root / 'data').mkdir()
        (root / 'data/all_products.json').write_text(json.dumps(products))
        command = [sys.executable, str(root / 'scripts/build.py')]
        if preview:
            command.append('--preview')
        result = subprocess.run(command, cwd=root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(check(root / 'dist'), [])
        return root / 'dist'

    def test_sparse_inventory_keeps_navigation_valid(self):
        for title in ('Chakra Singing Bowl', 'Rudraksha 108 Bead Mala', 'Amethyst Chakra Bracelet'):
            with self.subTest(title=title):
                self.build([product(1, title)])

    def test_search_only_suggests_generated_stone_pages(self):
        products = [product(i, 'Rudraksha 108 Bead Mala') for i in range(1, 4)]
        products.append(product(4, 'Amethyst Chakra Bracelet'))
        dist = self.build(products)
        meta = json.loads((dist / 'data/meta.json').read_text())
        self.assertIn('amethyst', meta['fams'])
        self.assertNotIn('amethyst', meta['stone_pages'])
        self.assertIn('rudraksha', meta['stone_pages'])

    def test_existing_tracking_and_checkout_config_are_preserved(self):
        dist = self.build([product(1, 'Rudraksha 108 Bead Mala')])
        for file in dist.rglob('*.html'):
            text = file.read_text()
            self.assertEqual(text.count('googletagmanager.com/gtag/js?id=G-Y7R5K9NMW0'), 1)
            self.assertEqual(text.count('gtag("config","G-Y7R5K9NMW0"'), 1)
            self.assertEqual(text.count('src="/assets/ga.js"'), 1)
            self.assertIn('href="https://namastebookshop.com/?ref=namastebeadshop"', text)
            self.assertIn('"shop": "https://namastebookshop.com"', text)
            self.assertIn('?attributes%5BStorefront%5D=Namaste%20Bead%20Shop', text)
        catalog = json.loads((dist / 'data/catalog.json').read_text())
        self.assertEqual((catalog[0]['v'], catalog[0]['p']), (10, 24.99))

    def test_preview_sends_no_analytics(self):
        dist = self.build([product(1, 'Rudraksha 108 Bead Mala')], preview=True)
        for file in dist.rglob('*.html'):
            text = file.read_text()
            self.assertNotIn('googletagmanager.com', text)
            self.assertNotIn('src="/assets/ga.js"', text)
            self.assertIn('noindex,nofollow', text)


if __name__ == '__main__':
    unittest.main()
