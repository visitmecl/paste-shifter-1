#!/usr/bin/env python3
"""Validate crawlable site files and consistency of social metadata without dependencies."""
import json
import re
import struct
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / 'Store' / 'Site'
BASE = 'https://pasteshifter.bastianhidalgo.cl'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}
        self.canonical = []
        self.refs = []
        self.ids = []
        self.h1s = 0

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'meta':
            key = attrs.get('property') or attrs.get('name')
            if key:
                assert key not in self.meta, f'Duplicate metadata: {key}'
                self.meta[key] = attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs.get('href'))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'h1':
            self.h1s += 1
        self.refs.extend(attrs[key] for key in ('href', 'src') if key in attrs)

locations = [entry.text for entry in ET.parse(ROOT / 'sitemap.xml').findall('.//{*}loc')]
expected = {BASE + '/', *(BASE + '/' + name for name in ('product.html', 'support.html', 'privacy.html'))}
assert set(locations) == expected and len(locations) == len(expected), 'Sitemap URLs differ from public pages'
robots = (ROOT / 'robots.txt').read_text()
assert 'User-agent: *' in robots and 'Allow: /' in robots
assert 'Sitemap: ' + BASE + '/sitemap.xml' in robots
for url in locations:
    path = urlsplit(url).path
    file = ROOT / ('index.html' if path == '/' else path.lstrip('/'))
    source = file.read_text()
    page = Page()
    page.feed(source)
    assert page.h1s == 1, f'{file.name}: expected one H1'
    assert page.canonical == [url], f'{file.name}: canonical mismatch'
    assert len(page.ids) == len(set(page.ids)), f'{file.name}: duplicate IDs'
    assert 'noindex' not in page.meta.get('robots', '').lower()
    for key in ('description', 'og:title', 'og:description', 'og:type', 'og:locale', 'og:site_name', 'og:image:alt', 'twitter:title', 'twitter:description', 'twitter:image:alt'):
        assert page.meta.get(key), f'{file.name}: missing {key}'
    assert page.meta['og:url'] == url
    assert page.meta['twitter:card'] == 'summary_large_image'
    assert page.meta['og:image'] == page.meta['twitter:image'] == BASE + '/assets/social-card.png'
    assert (page.meta['og:image:width'], page.meta['og:image:height']) == ('1200', '630')
    structured = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
    assert len(structured) == 1, f'{file.name}: missing or duplicate JSON-LD'
    data = json.loads(structured[0])
    assert data['@context'] == 'https://schema.org' and data['url'] == url
    for ref in page.refs:
        parsed = urlsplit(ref)
        if parsed.scheme and parsed.netloc != urlsplit(BASE).netloc:
            continue
        local = parsed.path
        target = ROOT / local.lstrip('/') if local.startswith('/') else file.parent / local
        if not local or local == '/':
            target = file if not local else ROOT / 'index.html'
        if target.is_dir():
            target = target / 'index.html'
        assert target.exists(), f'{file.name}: missing target {ref}'
        if parsed.fragment and target.suffix == '.html':
            linked = Page()
            linked.feed(target.read_text())
            assert unquote(parsed.fragment) in linked.ids, f'{file.name}: missing anchor {ref}'
    print(file.name + ': canonical, metadata, JSON-LD, links and anchors OK')
image = (ROOT / 'assets/social-card.png').read_bytes()
assert image[:8] == b'\x89PNG\r\n\x1a\n'
assert struct.unpack('>II', image[16:24]) == (1200, 630), 'Social image size mismatch'
llms = (ROOT / 'llms.txt').read_text()
for url in locations:
    assert url in llms, f'Missing documentation link: {url}'
print('robots.txt, sitemap.xml, llms.txt and 1200x630 social image OK')
