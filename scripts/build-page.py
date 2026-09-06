"""Build the static portfolio from the maintained template and collection catalog."""
from pathlib import Path
import json
from html import escape
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
items = json.loads((ROOT / 'assets/collection.json').read_text())
filters = [('all', 'All flowers', 'सर्व'), ('bouquets', 'Bouquets', 'बुके'),
           ('garlands', 'Garlands', 'लग्नहार'), ('decor', 'Décor', 'सजावट'),
           ('belts', 'Floral belts', 'कमरपट्टा')]
filter_html = ''.join(
    f'<button class="fluid-filter-pill{" active" if key == "all" else ""}" '
    f'data-filter="{key}" aria-pressed="{str(key == "all").lower()}">'
    f'{en}<span lang="mr">{mr}</span></button>' for key, en, mr in filters)
cards = []
for item in items:
    title, mr = escape(item['title'], quote=True), escape(item.get('marathi', ''), quote=True)
    copies = item.get('copies', {})
    srcset = ', '.join(f"{v['path']} {v['width']}w" for v in copies.values())
    if not srcset:
        srcset = f"{item['thumb']} 640w, {item['src']} {item['width']}w"
    url = 'https://wa.me/917620644158?text=' + quote(f"नमस्कार! मला {item.get('marathi', '')} ({item['title']}) याबद्दल माहिती हवी आहे. / Hello, I would like to enquire about {item['title']}.")
    cards.append(f'''<article class="work-card" data-category="{item['category']}">
<button class="photo-button" data-image="{item['src']}" data-title="{title}" data-marathi="{mr}" data-group="collection" aria-label="View {title}">
<img src="{item['thumb']}" srcset="{srcset}" sizes="(min-width: 1000px) 23vw, (min-width: 700px) 30vw, 46vw" width="{item['width']}" height="{item['height']}" alt="{title} — Sagar Flower Shop" loading="lazy" decoding="async"><span class="expand" aria-hidden="true">↗</span></button>
<div class="card-info"><p class="card-category">{escape(item['label'])}</p><h3>{title}</h3><p class="card-title-mr" lang="mr">{mr}</p><a class="inquire" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Enquire about {title}">Enquire <span aria-hidden="true">↗</span></a></div></article>''')
page = (ROOT / 'scripts/site-base.html').read_text()
page = page.replace('{{FILTERS}}', filter_html).replace('{{COLLECTION}}', '\n'.join(cards))
(ROOT / 'index.html').write_text(page)
print(f'Built mobile-first portfolio with {len(items)} designs.')
