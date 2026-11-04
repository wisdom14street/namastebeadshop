#!/usr/bin/env python3
"""Check generated local destinations and metadata before publishing. No network requests."""
import collections
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.social = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        field = {'a': 'href', 'link': 'href', 'img': 'src', 'script': 'src', 'form': 'action'}.get(tag)
        if field and attrs.get(field):
            self.links.append(attrs[field])
        if tag == 'meta':
            key = attrs.get('property') or attrs.get('name', '')
            if key.startswith(('og:', 'twitter:')):
                self.social.append(key)


def check(root):
    root = Path(root)
    errors = []
    pages = list(root.rglob('*.html'))
    if not pages:
        return ['No generated HTML pages found']
    for file in pages:
        page = Page()
        page.feed(file.read_text())
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            dest = root / path.lstrip('/') if path.startswith('/') else file.parent / path
            if path.endswith('/'):
                dest /= 'index.html'
            if not dest.is_file():
                errors.append(f'{file.relative_to(root)}: missing {path}')
        for key, n in collections.Counter(page.social).items():
            if n > 1:
                errors.append(f'{file.relative_to(root)}: duplicate {key}')
    meta = json.loads((root / 'data/meta.json').read_text())
    for key in meta.get('stone_pages', []):
        if not (root / 'stones' / key / 'index.html').is_file():
            errors.append(f'Search suggests missing stone page: {key}')
    return errors


if __name__ == '__main__':
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'dist'
    errors = check(root)
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(f'Checked {len(list(root.rglob("*.html")))} pages: local links, assets and social metadata passed')
