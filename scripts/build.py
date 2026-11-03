#!/usr/bin/env python3
"""Build the academic website and optional GitHub profile using only Python's standard library."""
from pathlib import Path
from html import escape
from string import Template
from urllib.parse import urlsplit
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'site'


def h(value):
    return escape(str(value), quote=True)


def url(value):
    if urlsplit(value).scheme not in {'https', 'mailto'}:
        raise ValueError(f'Use an https: or mailto: URL: {value}')
    return h(value)


def link(item, cls='text-link'):
    return f'<a class="{cls}" href="{url(item["url"])}">{h(item["label"])} <span aria-hidden="true">↗</span></a>'


def build():
    data = json.loads((ROOT / 'content/profile.json').read_text())
    p = data['person']
    # Fail before writing if the most frequently edited content is incomplete.
    for item in data['news']:
        for key in ['period', 'title', 'text']:
            if not item.get(key):
                raise ValueError(f'Each news item needs {key}.')
    for item in data['publications']:
        for key in ['year', 'venue', 'title', 'category', 'role', 'summary', 'links']:
            if key not in item:
                raise ValueError(f'Each publication needs {key}.')
        if not isinstance(item['year'], int):
            raise ValueError('Publication years must be numbers.')
    news = ''.join(f'<li><span class="date">{h(n["period"])}</span><div><h3>{h(n["title"])}</h3><p>{h(n["text"])}</p></div></li>' for n in data['news'][:4])
    if len(data['news']) > 4:
        older = ''.join(f'<li><span class="date">{h(n["period"])}</span><div><h3>{h(n["title"])}</h3><p>{h(n["text"])}</p></div></li>' for n in data['news'][4:])
        news_archive = f'<details class="news-archive"><summary>Earlier updates</summary><ol class="news-list">{older}</ol></details>'
    else:
        news_archive = ''
    research = ''.join(f'<article class="research-card"><span class="card-number">{h(r["number"])}</span><h3>{h(r["title"])}</h3><p>{h(r["text"])}</p><div class="tags">' + ''.join(f'<span>{h(t)}</span>' for t in r['tags']) + '</div></article>' for r in data['research'])
    publications = []
    for item in sorted(data['publications'], key=lambda x: -x['year']):
        publications.append(f'<article class="publication" data-category="{h(item["category"])}" data-search="{h((item["title"]+" "+item["venue"]+" "+str(item["year"])+" "+item["category"]).lower())}"><div class="pub-meta"><span class="venue">{h(item["venue"])}</span><span>{h(item["year"])}</span></div><div class="pub-body"><h3>{h(item["title"])}</h3><p class="pub-role">{h(item["role"])}</p><p class="pub-description">{h(item["summary"])}</p><div class="pub-links">'+''.join(link(l) for l in item['links'])+'</div></div></article>')
    categories = list(dict.fromkeys(item['category'] for item in data['publications']))
    filters = '<button type="button" class="filter active" data-filter="All" aria-pressed="true">All work</button>' + ''.join(f'<button type="button" class="filter" data-filter="{h(c)}" aria-pressed="false">{h(c)}</button>' for c in categories)
    service = ''.join(f'<li><span class="date">{h(s["period"])}</span><div><h3>{h(s["title"])}</h3><p>{h(s["organisation"])}</p></div></li>' for s in data['service'])
    education = ''.join(f'<li><span class="date">{h(e["year"])}</span><div><h3>{h(e["degree"])}</h3><p>{h(e["institution"])}</p></div></li>' for e in data['education'])
    courses = ''.join(f'<li><span class="course-code">{h(c["code"])}</span><h3>{h(c["name"])}</h3><p>{h(c["detail"])}</p></li>' for c in data['teaching']['courses'])
    opensource = ''.join(f'<a class="code-card" href="{url(o["url"])}"><div class="code-top"><span class="code-icon" aria-hidden="true">&lt;/&gt;</span><span aria-hidden="true">↗</span></div><h3>{h(o["title"])}</h3><p class="code-subtitle">{h(o["subtitle"])}</p><p>{h(o["text"])}</p><span class="code-label">Explore the repository</span></a>' for o in data['opensource'])
    bio = ''.join(f'<p>{h(b)}</p>' for b in data['bio'])
    appointments = ''.join(f'<div><span class="mini-label">Academic service · {h(s["period"])}</span><p><strong>{h(s["title"])}</strong><span>{h(s["organisation"])}</span></p></div>' for s in data['service'][:2])
    scholar = next((l['url'] for l in p['links'] if l['label'] == 'Google Scholar'), p['website'])
    values = dict(name=h(p['name']), role=h(p['role_short']), institution=h(p['institution']), intro=h(data['intro']), headline='<br>'.join(h(x) for x in data['headline'].split('\n')), bio=bio, research=research, news=news, news_archive=news_archive, publications=''.join(publications), filters=filters, publication_count=len(publications), service=service, appointments=appointments, scholar_url=url(scholar), education=education, courses=courses, teaching=h(data['teaching']['text']), opensource=opensource, profile_links=''.join(link(l) for l in p['links']), email=h(p['email']), github_url=url(f'https://github.com/{p["github_username"]}'), updated=h(data['updated']))
    values.update(title=h(p['title']), description=h(f'{p["name"]} — {p["role_short"]} at {p["institution"]}. {data["intro"]}'))
    rendered = Template((ROOT/'templates/index.html').read_text()).substitute(values)
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'assets', OUT/'assets', dirs_exist_ok=True)
    (OUT/'index.html').write_text(rendered)
    (OUT/'.nojekyll').write_text('')
    (OUT/'profile-README.md').write_text(profile_readme(data))
    print(f'Built {OUT.relative_to(ROOT)}/index.html: {len(publications)} publications, {len(data["news"])} updates.')


def profile_readme(data):
    p = data['person']
    lines = [f'# {p["name"]}', '', f'**{p["role_short"]} · {p["institution"]}**', '', 'CVSSP · Surrey Institute for People-Centred Artificial Intelligence', '', data['intro'], '', '## News', '']
    lines += [f'- **{n["period"]}** — {n["text"]}' for n in data['news'][:4]]
    lines += ['', '## Research', '']
    lines += [f'- **{r["title"]}:** {r["text"]}' for r in data['research']]
    lines += ['', '## Selected publications', '']
    for q in sorted(data['publications'],key=lambda q:-q['year'])[:7]:
        title = f'[{q["title"]}]({q["links"][0]["url"]})' if q['links'] else q['title']
        lines.append(f'- **{q["venue"]} {q["year"]}** · {title}')
    lines += ['', '## Open-source research', '']
    lines += [f'- [{o["title"]}]({o["url"]}) — {o["subtitle"]}' for o in data['opensource']]
    lines += ['', '## Academic service', '']
    lines += [f'- {s["title"]}, {s["organisation"]} ({s["period"]})' for s in data['service']]
    lines += ['', '## Find me', '']
    lines += [' · '.join(f'[{l["label"]}]({l["url"]})' for l in p['links']), '', f'Email: [{p["email"]}](mailto:{p["email"]})', '', '<!-- Generated from content/profile.json with scripts/build.py. -->', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    build()
