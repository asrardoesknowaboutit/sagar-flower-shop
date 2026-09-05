from pathlib import Path
import json, re, html
from urllib.parse import quote

R = Path(__file__).resolve().parents[1]
source = (R / 'scripts/site-base.html').read_text()
items = json.loads((R / 'assets/collection.json').read_text())

# Mix occasions in the first screen; every original upload remains in the collection.
priority = ['new-2', 'new-21', 'new-10', 'new-7', 'new-28', 'new-33', 'new-22', 'new-5', 'new-8', 'new-26', 'new-31', 'new-11']
items.sort(key=lambda i: priority.index(i['id']) if i['id'] in priority else 100)
(R / 'assets/collection.json').write_text(json.dumps(items, ensure_ascii=False, indent=2))

wa = lambda title: 'https://wa.me/917620644158?text=' + quote('नमस्कार! मला ' + title + ' याबद्दल माहिती हवी आहे. / Hello, I would like to enquire about ' + title + '.')

def image(i, eager=False, sizes='(max-width: 600px) 48vw, (max-width: 900px) 45vw, 30vw'):
    if 'copies' in i:
        srcset = ', '.join(f"{v['path']} {v['width']}w" for v in i['copies'].values())
    else:
        srcset = f"{i['thumb']} 640w, {i['src']} {i['width']}w"
    return f'''<img src="{i['thumb']}" srcset="{srcset}" sizes="{sizes}" width="{i['width']}" height="{i['height']}" alt="{html.escape(i['title'])} — Sagar Flower Shop" {'fetchpriority="high"' if eager else 'loading="lazy"'} decoding="async">'''

def watermark():
    return '<span class="watermark" aria-hidden="true">SAGAR · 7620644158</span>'

logo = '<img class="shop-logo" src="assets/brand/sagar-logo.webp" alt="सागर फूल सेंटर — Sagar Flower Shop" width="420" height="211">'

# Preload hero video poster
head = source[:source.index('<body>')].replace('assets/images/bouquets/bouquets-25.webp', 'assets/videos/delivery-poster.webp')
head = re.sub(r'<link rel="preload" as="image"[^>]+>', '<link rel="preload" as="image" href="assets/videos/delivery-poster.webp">', head)

ticker = 'सागर फ्लॉवर सेंटर, परळी वैजनाथ मध्ये आपले स्वागत आहे! ऑर्डर देण्यासाठी कृपया संपर्क साधा :'

parts = [head, f'''<body><a class="skip" href="#main">Skip to content</a>
<div class="welcome-bar">
  <div class="ticker" aria-label="{ticker} 7620644158">
    <div class="ticker-track">
      <span lang="mr">✿ &nbsp; {ticker} &nbsp; <a href="tel:+917620644158">7620644158</a> &nbsp; · &nbsp; ताजी फुले, लग्नहार, बुके, गाडी सजावट व घरपोच डिलिव्हरी &nbsp; ✿ &nbsp;</span>
      <span aria-hidden="true" lang="mr">✿ &nbsp; {ticker} &nbsp; <b>7620644158</b> &nbsp; · &nbsp; ताजी फुले, लग्नहार, बुके, गाडी सजावट व घरपोच डिलिव्हरी &nbsp; ✿ &nbsp;</span>
    </div>
  </div>
  <button id="ticker-toggle" aria-label="Pause welcome ticker" aria-pressed="false">Ⅱ</button>
</div>
<header class="header">
  <a class="brand" href="#home" aria-label="Sagar Flower Shop home">
    {logo}
  </a>
  <nav class="desktop-nav" aria-label="Main navigation">
    <a href="#collection" data-section="collection">आमचे काम (Collection)</a>
    <a href="#films" data-section="films">व्हिडिओ झलक (Stories)</a>
    <a href="#inspiration" data-section="inspiration">शाही रचना (Signature)</a>
    <a href="#services" data-section="services">सेवा (Services)</a>
    <a href="#contact" data-section="contact">भेट द्या (Visit us)</a>
  </nav>
  <a class="button header-order" href="{wa('फुलांची थेट ऑर्डर')}" target="_blank" rel="noopener noreferrer">
    <span>💬 WhatsApp वर ऑर्डर</span><span aria-hidden="true">↗</span>
  </a>
  <div class="scroll-progress" aria-hidden="true"></div>
</header>
<main id="main">

<section class="hero wrap" id="home">
  <div class="hero-copy">
    <p class="eyebrow">📍 सागर फ्लॉवर सेंटर · PARLI, MAHARASHTRA <span>✳</span> FAST DOORSTEP DELIVERY</p>
    <h1>ताजी फुले.<br><em>शुभ क्षणांची साथ.</em></h1>
    <p class="hero-description">Fresh wedding garlands, handcrafted celebration bouquets, haldi swing decorations & wedding car decor. Made fresh every day with tradition and love in Parli.</p>
    <div class="hero-actions">
      <a class="button button-wa-hero" href="{wa('फुलांची थेट ऑर्डर')}" target="_blank" rel="noopener noreferrer">
        <span>💬 WhatsApp वर ऑर्डर करा</span> <span aria-hidden="true">↗</span>
      </a>
      <a class="hero-call-btn" href="tel:+917620644158">
        <span>📞 76206 44158 ↗</span>
      </a>
    </div>
    <div class="hero-tags">
      <span>🌸 लग्नहार</span>
      <span>💐 बुके</span>
      <span>🚗 गाडी सजावट</span>
      <span>⚡ घरपोच डिलिव्हरी</span>
    </div>
  </div>

  <div class="hero-video-showcase">
    <div class="hero-video-card">
      <video class="hero-video" id="hero-delivery-video" src="assets/videos/delivery.mp4" poster="assets/videos/delivery-poster.webp" autoplay muted loop playsinline preload="auto" aria-label="Flowers on their way to customers in Parli"></video>
      <div class="hero-video-live-badge">
        <span class="live-dot" aria-hidden="true"></span>
        <span>Flowers, on their way · फुले, तुमच्या दारी</span>
      </div>
      <button class="sound-toggle-btn" id="hero-sound-toggle" aria-label="Toggle hero video sound" title="Toggle sound">
        <span class="sound-icon">🔇</span>
      </button>
    </div>
    <div class="hero-video-caption">
      <div>
        <span class="eyebrow">SAGAR SPECIAL DELIVERY</span>
        <p>Flowers, on their way <small lang="mr">परळी व जवळच्या परिसरात ताजी फुले वेळेवर घरपोच मिळतील</small></p>
      </div>
      <a class="hero-caption-cta" href="{wa('घरपोच डिलिव्हरी बद्दल माहिती')}" target="_blank" rel="noopener noreferrer">
        डिलिव्हरी बुक करा ↗
      </a>
    </div>
  </div>
</section>

<div class="values-strip">
  <span>🌸 १००% ताजी फुले</span>
  <i>✳</i>
  <span>💍 आकर्षक लग्नहार व वरमाला</span>
  <i>✳</i>
  <span>🚗 गाडी व मंडप सजावट</span>
  <i>✳</i>
  <span>⚡ परळी व परिसरात जलद डिलिव्हरी</span>
</div>

<section id="collection" class="collection wrap section">
  <div class="section-heading">
    <div>
      <p class="eyebrow">THE FLOWER EDIT · आमची फुलांची दुनिया</p>
      <h2>Let the flowers<br><em>do the talking.</em></h2>
    </div>
    <p>Find a design you love. Tap to see every detail in full resolution.<br><span lang="mr">तुमची आवडती डिझाईन निवडा, ऑर्डर WhatsApp वर द्या.</span></p>
  </div>

  <!-- NEUMORPHIC CONNECTED CONTOUR FILTER BAR -->
  <div class="neo-filter-container">
    <div class="neo-filter-shelf">
      <div class="neo-filter-track" role="group" aria-label="Filter floral collection">
        <div class="neo-glider" aria-hidden="true"></div>''']

category_labels = [
    ('all', 'All designs', 'सर्व फुले', '🌸'),
    ('garlands', 'Wedding garlands', 'लग्नहार व वरमाला', '🌺'),
    ('bouquets', 'Bouquets', 'आकर्षक बुके', '💐'),
    ('decor', 'Car & stage décor', 'गाडी व स्टेज सजावट', '🚗'),
    ('belts', 'Floral jewellery', 'गजरा व कंबरपट्टा', '🌼')
]

for key, en, mr, icon in category_labels:
    is_active = (key == 'all')
    parts.append(f'''<button data-filter="{key}" aria-pressed="{str(is_active).lower()}" class="neo-btn{" active" if is_active else ""}">
        <span class="neo-icon" aria-hidden="true">{icon}</span>
        <span class="neo-text">
          <span class="neo-mr" lang="mr">{mr}</span>
          <span class="neo-en">{en}</span>
        </span>
      </button>''')

parts.append(f'''      </div>
    </div>
  </div>
  <div class="gallery-toolbar">
    <p id="filter-status" role="status" aria-live="polite">{len(items)} floral designs</p>
    <span>फोटोवर टॅप करून मोठा फोटो पहा ↗</span>
  </div>
  <div class="portfolio">''')

for i in items:
    parts.append(f'''<article class="work-card" data-category="{i['category']}"><button class="photo-button" data-image="{i['src']}" data-title="{i['title']}" data-marathi="{i['marathi']}" data-group="collection" aria-label="View {i['title']}">{image(i)}{watermark()}<span class="expand" aria-hidden="true" title="मोठा फोटो पहा">↗</span></button><div class="card-info"><div class="card-meta"><span class="category-pill">{i['label']}</span></div><h3 class="card-title-mr" lang="mr">{i['marathi']}</h3><p class="card-title-en">{i['title']}</p><a class="inquire" href="{wa(i['marathi'] + ' / ' + i['title'])}" target="_blank" rel="noopener noreferrer"><span>💬 WhatsApp वर ऑर्डर</span><span class="inquire-arrow" aria-hidden="true">↗</span></a></div></article>''')

parts.append(f'''</div>
<div class="collection-footer">
  <button id="show-more" class="button button-outline" hidden>अधिक डिझाईन्स पहा <span>↓</span></button>
  <p>तुमच्या आवडीचे रंग, बजेट किंवा खास कल्पना आहे का?</p>
  <a class="text-link" href="{wa('कस्टम फुलांची ऑर्डर / Custom order')}" target="_blank" rel="noopener noreferrer">आम्हाला सांगा, आम्ही तयार करू ↗</a>
</div>
</section>

<section id="films" class="films section">
  <div class="wrap">
    <div class="section-heading">
      <div>
        <p class="eyebrow">फुलांची थेट व्हिडिओ झलक · FLOWER STORIES</p>
        <h2>Flowers, <em>in motion.</em></h2>
      </div>
      <p lang="mr">लग्नहार आणि ताज्या फुलांची खास व्हिडिओ झलक.<br><span lang="en">Live celebration moments from Sagar Flower Shop.</span></p>
    </div>
    <div class="film-rail" tabindex="0" aria-label="Flower videos, swipe to explore">''')

videos = json.loads((R / 'assets/videos.json').read_text())
# Include all 3 videos looping seamlessly without buttons
for v in [videos[1], videos[2], videos[0]]:
    parts.append(f'''<article class="film-card">
  <div class="film-frame">
    <video class="story-video" src="{v['src']}" poster="{v['poster']}" autoplay muted loop playsinline preload="auto" aria-label="{v['title']}"></video>
    <div class="story-video-overlay">
      <span class="story-tag">{v['marathi']}</span>
      <button class="sound-toggle-btn story-sound-toggle" aria-label="Toggle sound" title="Toggle audio">
        <span class="sound-icon">🔇</span>
      </button>
    </div>
    {watermark()}
  </div>
  <div class="film-caption">
    <h3>{v['title']}</h3>
    <p lang="mr">{v['marathi']}</p>
    <a class="story-order-btn" href="{wa(v['title'] + ' - ' + v['marathi'])}" target="_blank" rel="noopener noreferrer">
      <span>💬 WhatsApp वर ऑर्डर द्या ↗</span>
    </a>
  </div>
</article>''')

parts.append('''</div>
<div class="rail-footer">
  <span>← डावीकडे/उजवीकडे स्वाइप करा (Swipe to explore) →</span>
  <div>
    <button class="film-prev" aria-label="Scroll to previous video">←</button>
    <button class="film-next" aria-label="Scroll to next video">→</button>
  </div>
</div>
</div>
</section>

<section id="inspiration" class="inspiration section wrap">
  <div class="section-heading">
    <div>
      <p class="eyebrow">खास ऑर्डर व शाही रचना · SIGNATURE CREATIONS</p>
      <h2>Bespoke <em>Celebration Edits.</em><br>शाही लग्नहार व सोहळा सजावट.</h2>
    </div>
    <p>Exclusive floral styling for grand weddings and special celebrations.<br><span lang="mr">तुमच्या पसंतीनुसार आणि बजेटनुसार खास डिझाईन करून मिळतील.</span></p>
  </div>
  <div class="inspiration-grid">''')

signature_edits = [
    ('varmala', 'The Royal Rose & Lotus Varmala', 'शाही गुलाब व कमळांचा लग्नहार', 'शाही लग्नहार · ROYAL EDIT'),
    ('haldi', 'Golden Haldi Celebration Swing', 'हळदीचा सोनेरी झोपाळा व सजावट', 'हळदी विशेष · HALDI SPECIAL')
]

for name, title, mr, badge in signature_edits:
    parts.append(f'''<article class="inspiration-card">
  <button class="photo-button" data-image="assets/images/inspiration/{name}-960.webp" data-title="{title}" data-marathi="{mr}" data-group="inspiration" aria-label="View {title}">
    <img src="assets/images/inspiration/{name}-480.webp" srcset="assets/images/inspiration/{name}-480.webp 480w, assets/images/inspiration/{name}-960.webp 960w" sizes="(max-width: 600px) 90vw, 45vw" width="960" height="1280" alt="{title} — Sagar Flower Shop" loading="lazy">
    <span class="inspiration-badge">{badge}</span>
    <span class="expand" aria-hidden="true">↗</span>
  </button>
  <div class="inspiration-caption">
    <h3 lang="mr">{mr}</h3>
    <p>{title}</p>
    <a class="text-link" href="{wa(mr + ' (' + title + ')')}" target="_blank" rel="noopener noreferrer">या डिझाईनची ऑर्डर द्या (Book on WhatsApp) ↗</a>
  </div>
</article>''')

parts.append('</div></section>')

# Retain verified business and service content from the base version.
services = re.search(r'<section id="services".*?(?=<section id="story")', source, re.S).group()
story = re.search(r'<section id="story".*?(?=<section class="process)', source, re.S).group()

# Present the garland photograph cleanly
story = re.sub(
    r'<div class="story-image reveal">.*?</div>',
    '<div class="story-image"><img src="assets/images/garlands/collection-21-640.webp" width="640" height="1044" alt="Traditional rose and ivory garland by Sagar Flower Shop" loading="lazy">' + watermark() + '<div class="story-tag">परंपरेचा सुगंध.</div></div>',
    story, count=1, flags=re.S
)
story = story.replace('</div></div><div class="story-copy', '</div><div class="story-copy')

contact = re.search(r'<section id="contact".*?</section>', source, re.S).group()

parts.extend([services, story, contact, '</main>'])

parts.append(f'''<footer>
  <div class="wrap footer-top">
    <a class="brand" href="#home">{logo}</a>
    <p lang="mr">तुमच्या प्रत्येक आनंदात, फुलांची खास साथ.</p>
    <a href="#home">वर जा (Back to top) ↑</a>
  </div>
  <div class="wrap footer-bottom">
    <span>© <span id="year">2026</span> सागर फ्लॉवर सेंटर · Sagar Flower Shop</span>
    <span>परळी वैजनाथ, महाराष्ट्र. From Parli, with love. ✿</span>
  </div>
</footer>''')

parts.append(re.search(r'<a class="floating-wa".*?(?=<nav class="mobile-nav")', source, re.S).group())

parts.append('''<nav class="mobile-nav" aria-label="Mobile navigation">
  <a href="#home" data-section="home" class="active"><span aria-hidden="true">⌂</span>होम</a>
  <a href="#collection" data-section="collection"><span aria-hidden="true">❀</span>फुले</a>
  <a href="#films" data-section="films"><span aria-hidden="true">▷</span>व्हिडिओ</a>
  <a href="#contact" data-section="contact"><span aria-hidden="true">♡</span>संपर्क</a>
</nav>

<dialog id="lightbox" aria-labelledby="lightbox-title">
  <button class="lightbox-close" aria-label="Close photo">×</button>
  <div class="lightbox-image">
    <button class="lightbox-prev" aria-label="Previous photo">‹</button>
    <img alt="" id="lightbox-photo">
    <span class="watermark" aria-hidden="true">SAGAR · 7620644158</span>
    <button class="lightbox-next" aria-label="Next photo">›</button>
  </div>
  <div class="lightbox-bottom">
    <div>
      <span id="lightbox-count" class="eyebrow"></span>
      <h2 id="lightbox-title"></h2>
    </div>
    <a class="button button-whatsapp-modal" id="lightbox-inquire" target="_blank" rel="noopener noreferrer">💬 WhatsApp वर ऑर्डर ↗</a>
  </div>
  <p class="lightbox-tip">स्वाइप करा किंवा बाणांचा वापर करा · दोन्ही बोटांनी झूम करू शकता</p>
</dialog>
</body>
</html>
''')

(R / 'index.html').write_text(''.join(parts))
print('Built upgraded portfolio with neumorphic connected contour filter bar')
