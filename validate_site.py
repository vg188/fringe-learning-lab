"""Read-only checks before publishing; standard library only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
course=json.loads((ROOT/'course.json').read_text(encoding='utf-8'))
assert len(course['chapters'])==20
assert len({c['id'] for c in course['chapters']})==20
labs=set()
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        for attr in ('src','href'):
            value=attrs.get(attr,'')
            if not value or value.startswith('#') or urlparse(value).scheme: continue
            target=(ROOT/unquote(value.split('#')[0])).resolve()
            assert target.is_relative_to(ROOT),value
            assert target.is_file(),value
for c in course['chapters']:
    assert 0<=c['quiz']['answer']<len(c['quiz']['options'])
    assert '../lw/' not in c['body']
    assert not re.search(r'[A-Z]:[\\/]|33128|Publish-Version|gh[pousr]_[A-Za-z0-9]{20,}',c['body'])
    Links().feed(c['body'])
    labs.update(re.findall(r'data-lab="([^"]+)"',c['body']))
assert labs=={'wave','psp','unwrap','conv','phasor','unet'}
Links().feed((ROOT/'index.html').read_text(encoding='utf-8'))
for f in (ROOT/'assets').glob('*.svg'):ET.parse(f)
for f in ROOT.rglob('*'):
    if not f.is_file() or '.git' in f.parts:continue
    assert f.suffix.lower() not in ('.pdf','.zip'),str(f)
for link in re.findall(r'url\(([^)]+)\)',(ROOT/'vendor/katex/katex.min.css').read_text(encoding='utf-8')):
    assert (ROOT/'vendor/katex'/link.strip('"\'')).is_file(),link
assert (ROOT/'.nojekyll').is_file()
print('PASS: 20 chapters / 6 labs / local assets / SVG XML / formula fonts / no local paper references')
