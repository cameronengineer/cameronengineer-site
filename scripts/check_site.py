#!/usr/bin/env python3
"""Check static page links, fragments, canonical URLs and profile data."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlparse
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]/'site'
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__();self.links=[];self.ids=set();self.canonical=None;self.h1=0;self.json_text=None;self.graphs=[]
        self.feed(path.read_text())
    def handle_starttag(self,t,a):
        d=dict(a)
        if d.get('id'):self.ids.add(d['id'])
        if t=='h1':self.h1+=1
        if t=='link' and d.get('rel')=='canonical':self.canonical=d['href']
        if t=='script' and d.get('type')=='application/ld+json':self.json_text=''
        for k in ('href','src'):
            if d.get(k):self.links.append(d[k])
    def handle_data(self,data):
        if self.json_text is not None:self.json_text+=data
    def handle_endtag(self,t):
        if t=='script' and self.json_text is not None:
            self.graphs.append(json.loads(self.json_text));self.json_text=None
pages={p.resolve():Page(p) for p in ROOT.rglob('*.html')}
for source,page in pages.items():
    assert page.h1==1,source
    assert page.canonical.startswith('https://cameronengineer.com/'),source
    for link in page.links:
        u=urlparse(link)
        if u.scheme or u.netloc:continue
        target=ROOT/unquote(u.path.lstrip('/')) if u.path.startswith('/') else source.parent/unquote(u.path)
        if not u.path:target=source
        if target.is_dir():target/='index.html'
        assert target.exists(),(source,link)
        if u.fragment and target.resolve() in pages:assert unquote(u.fragment) in pages[target.resolve()].ids,(source,link)
    if source.name!='404.html':
        graph=page.graphs[0]['@graph']
        person=next(n for n in graph if n['@type']=='Person')
        assert person['name']=='Cameron Mitchell'
        assert person['homeLocation']['address']['addressLocality']=='Melbourne'
        assert 'https://github.com/cameronengineer' in person['sameAs']
        assert 'https://www.linkedin.com/in/cameronengineer/' in person['sameAs']
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
for node in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns):
    path=ROOT/urlparse(node.text).path.lstrip('/')/'index.html'
    assert path.exists(),path
print(f'Passed: {len(pages)} pages, internal links, fragments, canonical URLs, profile metadata and sitemap')
