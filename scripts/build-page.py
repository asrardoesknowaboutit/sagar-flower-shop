import json, html
from urllib.parse import quote
from pathlib import Path

R = Path(__file__).resolve().parents[1]

with open(R / 'assets/collection.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open(R / 'assets/videos.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

wa = lambda text: f"https://wa.me/917620644158?text={quote(text)}"

def make_card(item, index):
    is_hidden = index >= 8
    eager = index < 2
    
    if 'copies' in item and item['copies']:
        srcset = ', '.join(f"{c['path']} {c['width']}w" for c in item['copies'].values())
    else:
        srcset = f"{item['thumb']} 640w, {item['src']} {item['width']}w"
        
    sizes = "(max-width: 600px) 48vw, (max-width: 900px) 31vw, 23vw"
    
    wa_msg = f"नमस्कार! मला {item['marathi']} ({item['title']}) याबद्दल माहिती हवी आहे. / Hello, I would like to order {item['title']}."
    wa_link = wa(wa_msg)
    
    loading_attr = 'fetchpriority="high"' if eager else 'loading="lazy"'
    hidden_attr = ' hidden' if is_hidden else ''
    
    return f'''      <article class="work-card"{hidden_attr} data-category="{item['category']}">
        <button class="photo-button" style="aspect-ratio: {item['width']} / {item['height']};" data-image="{item['src']}" data-title="{html.escape(item['title'])}" data-marathi="{html.escape(item['marathi'])}" data-group="collection" aria-label="View {html.escape(item['title'])}">
          <img src="{item['thumb']}" srcset="{srcset}" sizes="{sizes}" width="{item['width']}" height="{item['height']}" style="aspect-ratio: {item['width']} / {item['height']};" alt="{html.escape(item['marathi'])} — {html.escape(item['title'])}" {loading_attr} decoding="async">
          <span class="watermark" aria-hidden="true">SAGAR · 7620644158</span>
          <span class="expand-badge" aria-hidden="true" title="मोठा फोटो पहा">⤢</span>
        </button>
        <div class="card-info">
          <span class="category-pill">{item['label']}</span>
          <h3 class="card-title-mr" lang="mr">{html.escape(item['marathi'])}</h3>
          <p class="card-title-en">{html.escape(item['title'])}</p>
          <a class="card-inquire-btn" href="{wa_link}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp वर ऑर्डर - {html.escape(item['marathi'])}">
            <svg class="wa-icon" viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/></svg>
            <span>WhatsApp ऑर्डर</span>
          </a>
        </div>
      </article>'''

cards_html = '\n'.join(make_card(item, idx) for idx, item in enumerate(items))

reel_cards = []
for v in videos[:3]:
    wa_reel = wa(f"नमस्कार! मला {v['title']} - {v['marathi']} (व्हिडिओ पाहून ऑर्डर) याबद्दल माहिती हवी आहे. / Hello, I would like to enquire about {v['title']}.")
    reel_cards.append(f'''        <article class="film-card {v.get('theme', '')}" data-video-id="{v['id']}">
          <div class="film-frame">
            <video class="story-video" src="{v['src']}" poster="{v['poster']}" muted loop playsinline preload="none" aria-label="{v['title']}"></video>
            <div class="story-video-top">
              <span class="story-tag-pill">{v['tag']}</span>
              <button class="sound-toggle-btn story-sound-toggle" aria-label="Toggle audio" title="आवाज चालू/बंद करा">
                <span class="sound-icon">🔇</span>
              </button>
            </div>
            <div class="film-watermark">
              <span class="wm-brand">🌸 SAGAR FLOWER SHOP</span>
              <span class="wm-loc">· PARLI</span>
            </div>
          </div>
          <div class="film-caption">
            <div class="film-caption-text">
              <span class="film-eyebrow">SAGAR SIGNATURE REEL</span>
              <h3 class="film-title">{v['title']}</h3>
              <p class="film-desc" lang="mr">{v['marathi']}</p>
            </div>
            <a class="film-wa-btn" href="{wa_reel}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp वर ऑर्डर - {v['title']}">
              <svg class="wa-icon" viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/></svg>
              <span>WhatsApp वर ऑर्डर</span>
            </a>
          </div>
        </article>''')

reels_html = '\n'.join(reel_cards)

header_wa_link = wa('नमस्कार! मला फुलांची थेट ऑर्डर याबद्दल माहिती हवी आहे. / Hello, I would like to order flowers.')
hero_wa_link = wa('नमस्कार! मला फुलांची थेट ऑर्डर करायची आहे. / Hello, I would like to order flowers.')
delivery_wa_link = wa('नमस्कार! मला परळीत फुलांची होम डिलिव्हरी बुक करायची आहे. / Hello, I want to book flower delivery in Parli.')
varmala_wa_link = wa('नमस्कार! मला शाही गुलाब व कमळांचा लग्नहार (The Royal Rose & Lotus Varmala) याबद्दल माहिती हवी आहे. / Hello, I would like to order The Royal Rose & Lotus Varmala.')
haldi_wa_link = wa('नमस्कार! मला हळदीचा सोनेरी झोपाळा व सजावट (Golden Haldi Celebration Swing) याबद्दल माहिती हवी आहे. / Hello, I would like to order Golden Haldi Celebration Swing.')
contact_wa_link = wa('नमस्कार! मला फुलांची चौकशी करायची आहे. / Hello, I would like to enquire about flowers.')
maps_wa_link = wa('नमस्कार! मला सागर फ्लॉवर सेंटरचे लोकेशन पाठवा. / Hello, please share Sagar Flower Shop location.')

html_content = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#0d2b1f">
  <title>Sagar Flower Shop | Garlands, Bouquets & Wedding Décor in Parli</title>
  <meta name="description" content="Flowers for life's beautiful moments. Explore Sagar Flower Shop's wedding garlands, bouquets, floral belts and event decorations in Parli. Order on WhatsApp or Call.">
  <link rel="canonical" href="https://sagarflowershopparli.github.io/sagar-flower-shop/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Sagar Flower Shop — Made for your moments">
  <meta property="og:description" content="Wedding garlands, thoughtful bouquets & beautiful celebrations in Parli, Maharashtra.">
  <meta property="og:url" content="https://sagarflowershopparli.github.io/sagar-flower-shop/">
  <meta property="og:image" content="https://sagarflowershopparli.github.io/sagar-flower-shop/assets/videos/delivery-poster.webp">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="styles.css">
  <link rel="preload" as="image" href="assets/brand/sagar-logo.webp">
  <link rel="preload" as="image" href="assets/videos/delivery-poster.webp">
  <script src="app.js" defer></script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Florist",
    "name": "Sagar Flower Shop",
    "alternateName": "सागर फूल सेंटर",
    "url": "https://sagarflowershopparli.github.io/sagar-flower-shop/",
    "image": "https://sagarflowershopparli.github.io/sagar-flower-shop/assets/videos/delivery-poster.webp",
    "telephone": "+917620644158",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "Near Maharashtra Shoe Mart",
      "addressLocality": "Parli",
      "addressRegion": "Maharashtra",
      "addressCountry": "IN"
    }},
    "hasOfferCatalog": {{
      "@type": "OfferCatalog",
      "name": "Floral services",
      "itemListElement": [
        {{"@type": "OfferCatalog", "name": "Wedding garlands"}},
        {{"@type": "OfferCatalog", "name": "Bouquets"}},
        {{"@type": "OfferCatalog", "name": "Car and event decorations"}},
        {{"@type": "OfferCatalog", "name": "Floral waist belts"}}
      ]
    }}
  }}
  </script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>

  <!-- STICKY HEADER (Mobile-first, compact & fast) -->
  <header class="header">
    <a class="brand" href="#home" aria-label="Sagar Flower Shop home">
      <img class="shop-logo" src="assets/brand/sagar-logo.webp" alt="सागर फूल सेंटर — Sagar Flower Shop" width="130" height="65">
    </a>

    <!-- Desktop Nav: Hidden on mobile, flex on desktop (min-width: 768px) -->
    <nav class="desktop-nav" aria-label="Main navigation">
      <div class="nav-links">
        <a href="#collection" data-section="collection" class="nav-pill"><span>आमचे काम</span> <small>Collection</small></a>
        <a href="#films" data-section="films" class="nav-pill"><span>व्हिडिओ</span> <small>Stories</small></a>
        <a href="#inspiration" data-section="inspiration" class="nav-pill"><span>शाही रचना</span> <small>Signature</small></a>
        <a href="#services" data-section="services" class="nav-pill"><span>सेवा</span> <small>Services</small></a>
        <a href="#contact" data-section="contact" class="nav-pill"><span>भेट द्या</span> <small>Visit us</small></a>
      </div>
    </nav>

    <a class="header-wa-btn" href="{header_wa_link}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp वर ऑर्डर">
      <svg class="header-wa-icon" viewBox="0 0 24 24" width="17" height="17" fill="currentColor" aria-hidden="true"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/></svg>
      <span>WhatsApp ऑर्डर</span>
    </a>

    <div class="scroll-progress" aria-hidden="true"></div>
  </header>

  <main id="main">
    <!-- HERO SECTION (Mobile-First Architecture) -->
    <section class="hero wrap" id="home">
      <div class="hero-content">
        <div class="hero-location-badge">
          <span class="live-dot" aria-hidden="true"></span>
          <span>📍 परळी, महाराष्ट्र · जलद घरपोच डिलिव्हरी</span>
        </div>

        <h1 class="hero-title">
          <span class="hero-title-main" lang="mr">ताजी फुले.</span>
          <span class="hero-title-sub" lang="mr">शुभ क्षणांची साथ.</span>
          <span class="hero-title-en">Fresh Flowers. Made for Your Moments.</span>
        </h1>

        <p class="hero-desc">
          लग्नहार, आकर्षक बुके, हळदीचा झोपाळा व गाडी सजावट. परळीमध्ये दररोज ताजी फुले आणि वेळेवर घरपोच डिलिव्हरी.
        </p>

        <!-- Primary Action Pod: High-contrast, easy thumb reach -->
        <div class="hero-actions">
          <a class="btn btn-wa-hero" href="{hero_wa_link}" target="_blank" rel="noopener noreferrer">
            <svg class="wa-icon" viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/></svg>
            <span>WhatsApp वर ऑर्डर करा</span>
          </a>
          <a class="btn btn-call-hero" href="tel:+917620644158">
            <span aria-hidden="true">📞</span>
            <span>कॉल करा: 76206 44158</span>
          </a>
        </div>

        <!-- Trust Chips -->
        <div class="hero-trust-chips" role="region" aria-label="Key highlights">
          <a class="trust-chip" href="#collection" data-filter-trigger="garlands">
            <span class="chip-icon">🌸</span>
            <span>१००% ताजी फुले</span>
          </a>
          <a class="trust-chip" href="{delivery_wa_link}" target="_blank" rel="noopener noreferrer">
            <span class="chip-icon">⚡</span>
            <span>परळीत थेट डिलिव्हरी</span>
          </a>
          <a class="trust-chip" href="#services">
            <span class="chip-icon">💍</span>
            <span>लग्न व सर्व कार्यक्रम</span>
          </a>
        </div>
      </div>

      <!-- Hero Video Preview (Optimized, lightweight, preload=metadata) -->
      <div class="hero-media">
        <div class="hero-video-card">
          <video class="hero-video" id="hero-delivery-video" src="assets/videos/delivery.mp4" poster="assets/videos/delivery-poster.webp" muted loop playsinline preload="metadata" aria-label="Flowers on their way to customers in Parli"></video>
          <div class="hero-video-badge">
            <span class="live-dot" aria-hidden="true"></span>
            <span>फुले, तुमच्या दारी · Fast Delivery</span>
          </div>
          <button class="sound-toggle-btn" id="hero-sound-toggle" aria-label="Toggle hero video sound" title="आवाज चालू/बंद करा">
            <span class="sound-icon">🔇</span>
          </button>
        </div>
        <div class="hero-media-caption">
          <div>
            <span class="caption-eyebrow">SAGAR SPECIAL DELIVERY</span>
            <p>परळी व जवळच्या परिसरात ताजी फुले वेळेवर घरपोच मिळतील.</p>
          </div>
          <a class="btn-caption-cta" href="{delivery_wa_link}" target="_blank" rel="noopener noreferrer">
            डिलिव्हरी बुक करा ↗
          </a>
        </div>
      </div>
    </section>

    <!-- COLLECTION SECTION (#collection) -->
    <section class="collection wrap section" id="collection">
      <div class="section-header">
        <span class="eyebrow">आमची फुलांची दुनिया · THE FLOWER EDIT</span>
        <h2>तुमच्या खास क्षणांसाठी <em>ताजी फुले.</em></h2>
        <p>आवडती डिझाईन निवडा. फोटोवर टॅप करून मोठा फोटो पहा. WhatsApp वर थेट ऑर्डर द्या.</p>
      </div>

      <!-- Mobile-First Horizontal Swipeable Filter Ribbon -->
      <div class="filter-ribbon-wrap" role="region" aria-label="Floral Category Filter">
        <div class="filter-ribbon">
          <button class="filter-pill active" data-filter="all" aria-pressed="true">
            <span class="pill-icon">✨</span>
            <span>सर्व फुले</span>
          </button>
          <button class="filter-pill" data-filter="garlands" aria-pressed="false">
            <span class="pill-icon">🌸</span>
            <span>लग्नहार</span>
          </button>
          <button class="filter-pill" data-filter="bouquets" aria-pressed="false">
            <span class="pill-icon">💐</span>
            <span>बुके</span>
          </button>
          <button class="filter-pill" data-filter="decor" aria-pressed="false">
            <span class="pill-icon">🚗</span>
            <span>सजावट</span>
          </button>
          <button class="filter-pill" data-filter="belts" aria-pressed="false">
            <span class="pill-icon">🎀</span>
            <span>कंबरपट्टे</span>
          </button>
        </div>
      </div>

      <p class="filter-status" id="filter-status" role="status" aria-live="polite">दाखवत आहोत: 8 / 40 डिझाईन्स</p>

      <!-- 2-Column Responsive Product Grid -->
      <div class="portfolio" id="portfolio-grid">
{cards_html}
      </div>

      <!-- Load More Button -->
      <div class="load-more-wrap">
        <button class="btn btn-show-more" id="show-more">
          <span>आणखी डिझाईन्स पहा</span>
          <span class="show-more-count" id="show-more-count">+32</span>
        </button>
      </div>
    </section>

    <!-- VIDEO REELS SECTION (#films) -->
    <section class="films section" id="films">
      <div class="wrap">
        <div class="section-header">
          <span class="eyebrow">व्हिडिओ स्टोरीज · FLOWER STORIES</span>
          <h2>थेट व्हिडिओ <em>झलक.</em></h2>
          <p lang="mr">लग्नहार आणि ताज्या फुलांची खास व्हिडिओ झलक. स्वस्त आणि दर्जेदार फुलांची खात्री.</p>
        </div>

        <div class="film-rail" tabindex="0" aria-label="Flower videos, swipe to explore">
{reels_html}
        </div>
      </div>
    </section>

    <!-- SIGNATURE CREATIONS SECTION (#inspiration) -->
    <section class="inspiration wrap section" id="inspiration">
      <div class="section-header">
        <span class="eyebrow">खास शाही रचना · SIGNATURE EDITS</span>
        <h2>Bespoke <em>Celebration Edits.</em></h2>
        <p>शाही लग्नहार व सोहळा सजावट. तुमच्या पसंतीनुसार आणि बजेटनुसार खास डिझाईन करून मिळतील.</p>
      </div>

      <div class="inspiration-grid">
        <article class="inspiration-card">
          <button class="photo-button" style="aspect-ratio: 3 / 4;" data-image="assets/images/inspiration/varmala-960.webp" data-title="The Royal Rose & Lotus Varmala" data-marathi="शाही गुलाब व कमळांचा लग्नहार" data-group="inspiration" aria-label="View The Royal Rose & Lotus Varmala">
            <img src="assets/images/inspiration/varmala-480.webp" srcset="assets/images/inspiration/varmala-480.webp 480w, assets/images/inspiration/varmala-960.webp 960w" sizes="(max-width: 600px) 90vw, 45vw" width="960" height="1280" style="aspect-ratio: 3 / 4;" alt="The Royal Rose & Lotus Varmala — Sagar Flower Shop" loading="lazy">
            <span class="inspiration-badge">शाही लग्नहार · ROYAL EDIT</span>
            <span class="expand-badge" aria-hidden="true">⤢</span>
          </button>
          <div class="inspiration-caption">
            <h3 lang="mr">शाही गुलाब व कमळांचा लग्नहार</h3>
            <p class="caption-en">The Royal Rose & Lotus Varmala</p>
            <a class="btn btn-inspire" href="{varmala_wa_link}" target="_blank" rel="noopener noreferrer">
              <span>या डिझाईनची ऑर्डर द्या (Book on WhatsApp)</span>
              <span aria-hidden="true">↗</span>
            </a>
          </div>
        </article>

        <article class="inspiration-card">
          <button class="photo-button" style="aspect-ratio: 3 / 4;" data-image="assets/images/inspiration/haldi-960.webp" data-title="Golden Haldi Celebration Swing" data-marathi="हळदीचा सोनेरी झोपाळा व सजावट" data-group="inspiration" aria-label="View Golden Haldi Celebration Swing">
            <img src="assets/images/inspiration/haldi-480.webp" srcset="assets/images/inspiration/haldi-480.webp 480w, assets/images/inspiration/haldi-960.webp 960w" sizes="(max-width: 600px) 90vw, 45vw" width="960" height="1280" style="aspect-ratio: 3 / 4;" alt="Golden Haldi Celebration Swing — Sagar Flower Shop" loading="lazy">
            <span class="inspiration-badge">हळदी विशेष · HALDI SPECIAL</span>
            <span class="expand-badge" aria-hidden="true">⤢</span>
          </button>
          <div class="inspiration-caption">
            <h3 lang="mr">हळदीचा सोनेरी झोपाळा व सजावट</h3>
            <p class="caption-en">Golden Haldi Celebration Swing</p>
            <a class="btn btn-inspire" href="{haldi_wa_link}" target="_blank" rel="noopener noreferrer">
              <span>या डिझाईनची ऑर्डर द्या (Book on WhatsApp)</span>
              <span aria-hidden="true">↗</span>
            </a>
          </div>
        </article>
      </div>
    </section>

    <!-- SERVICES SECTION (#services) -->
    <section class="services section" id="services">
      <div class="wrap">
        <div class="section-header">
          <span class="eyebrow">आमच्या सेवा · OUR SERVICES</span>
          <h2>सर्व समारंभांसाठी <em>फुलांची साथ.</em></h2>
          <p>साध्या बुकेपासून ते मोठ्या लग्न मंडप सजावटीपर्यंत, आम्ही तुमची प्रत्येक कल्पना सुंदर फुलांमध्ये साकार करतो.</p>
        </div>

        <div class="service-grid">
          <article class="service-card">
            <span class="service-num">01 / THE WEDDING EDIT</span>
            <h3>शाही लग्न सोहळा</h3>
            <p>लग्नहार, सेहरा, फुलांचे कंबरपट्टे आणि लग्न मंडप व बेड सजावट. परंपरेला साजेसा देखणा थाट.</p>
            <a class="service-link" href="{wa('Hello, I want to enquire about wedding flowers.')}" target="_blank" rel="noopener noreferrer">
              <span>लग्न फुलांची चौकशी करा ↗</span>
            </a>
          </article>

          <article class="service-card">
            <span class="service-num">02 / JUST BECAUSE</span>
            <h3>आकर्षक बुके व भेटवस्तू</h3>
            <p>वाढदिवस, अभिनंदन, सरप्राईज किंवा कोणत्याही खास क्षणासाठी ताजे व सुगंधी फुलांचे बुके.</p>
            <a class="service-link" href="{wa('Hello, I want to order a bouquet.')}" target="_blank" rel="noopener noreferrer">
              <span>सुंदर बुके निवडा ↗</span>
            </a>
          </article>

          <article class="service-card">
            <span class="service-num">03 / LET’S CELEBRATE</span>
            <h3>इव्हेंट व कार डेकोरेशन</h3>
            <p>लग्न कार सजावट, स्टेज स्टाइलिंग, बर्थडे डेकोर व हळदी झोपाळा सजावट. देखणी आणि वेळेवर सेवा.</p>
            <a class="service-link" href="{wa('Hello, I want to enquire about event decoration.')}" target="_blank" rel="noopener noreferrer">
              <span>इव्हेंट सजावटीबद्दल बोला ↗</span>
            </a>
          </article>
        </div>

        <div class="service-notes">
          <div class="note-item">
            <strong>तुमची पसंती व बजेट</strong>
            <span>तुमचे रंग, तारीख व बजेट सांगा; आम्ही योग्य डिझाईन सुचवू.</span>
          </div>
          <div class="note-item">
            <strong>आधी बुकिंग करणे सोयीचे</strong>
            <span>विशेष लग्नहार आणि इव्हेंट सजावटीसाठी कृपया आधी संपर्क साधा.</span>
          </div>
          <div class="note-item">
            <strong>परळी परिसरात डिलिव्हरी</strong>
            <span>परळी व जवळच्या भागात वेळेवर थेट होम डिलिव्हरी उपलब्ध आहे.</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ORDERING PROCESS (3 EASY STEPS) -->
    <section class="process wrap section" id="process">
      <div class="section-header">
        <span class="eyebrow">सोपी पद्धत · HOW TO ORDER</span>
        <h2>फक्त ३ सोप्या पायऱ्यांमध्ये <em>ऑर्डर करा.</em></h2>
      </div>

      <div class="process-grid">
        <div class="process-step">
          <span class="step-num">01</span>
          <h3>डिझाईन निवडा</h3>
          <p>आमच्या गॅलरीमधील डिझाईन निवडा किंवा तुमचा स्वतःचा आवडता फोटो WhatsApp वर पाठवा.</p>
        </div>
        <div class="process-step">
          <span class="step-num">02</span>
          <h3>WhatsApp वर संपर्क</h3>
          <p>तारीख, ठिकाण आणि तुमची गरज सांगा. आम्ही तत्काळ किंमत आणि खात्रीशीर वेळ कळवू.</p>
        </div>
        <div class="process-step">
          <span class="step-num">03</span>
          <h3>ताजी डिलिव्हरी मिळवा</h3>
          <p>वेळेवर ताजी फुले थेट तुमच्या पत्त्यावर किंवा दुकानातून वेळेत घेऊन जा.</p>
        </div>
      </div>
    </section>

    <!-- STORE LOCATION & VISIT US (#contact) -->
    <section class="contact wrap section" id="contact">
      <div class="section-header">
        <span class="eyebrow">भेट द्या व संपर्क · VISIT & ENQUIRE</span>
        <h2>सागर फ्लॉवर सेंटर, <em>परळी.</em></h2>
        <p>कोणताही प्रश्न असो किंवा फुलांची ऑर्डर, आम्ही एका फोन किंवा WhatsApp मेसेजवर उपलब्ध आहोत.</p>
      </div>

      <div class="contact-layout">
        <!-- Contact Info Card -->
        <div class="contact-card">
          <a class="btn btn-wa-full" href="{contact_wa_link}" target="_blank" rel="noopener noreferrer">
            <svg class="wa-icon" viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/></svg>
            <span>WhatsApp वर थेट चॅट करा</span>
          </a>

          <div class="phone-box">
            <span class="info-label">थेट फोन करा (Call us directly):</span>
            <a class="primary-phone" href="tel:+917620644158">📞 +91 76206 44158</a>
            <div class="alt-phones">
              <span>इतर संपर्क:</span>
              <a href="tel:+919960142943">99601 42943</a>
              <span>/</span>
              <a href="tel:+919763553185">97635 53185</a>
            </div>
          </div>

          <div class="address-box">
            <span class="info-label">दुकान पत्ता (Store Address):</span>
            <p><strong>सागर फ्लॉवर सेंटर (Sagar Flower Shop)</strong><br>Near Maharashtra Shoe Mart, Parli, Maharashtra 431515</p>
            <span class="hours-tag">
              <span class="live-dot" aria-hidden="true"></span> चालू आहे: सर्व ७ दिवस · सकाळी ६ ते रात्री १०
            </span>
          </div>
        </div>

        <!-- Maps Location Window -->
        <div class="maps-box">
          <div class="maps-header">
            <div class="maps-title-wrap">
              <span class="radar-dot" aria-hidden="true"></span>
              <span>थेट लोकेशन · LIVE STORE GPS</span>
            </div>
            <a class="maps-open-link" href="https://www.google.com/maps/search/?api=1&query=Sagar+Flower+Shop+near+Maharashtra+Shoe+Mart+Parli+Maharashtra" target="_blank" rel="noopener noreferrer">
              Google Maps वर उघडा ↗
            </a>
          </div>

          <div class="maps-frame-container">
            <iframe class="maps-iframe" 
              src="https://maps.google.com/maps?q=Near+Maharashtra+Shoe+Mart+Parli+Maharashtra&t=&z=16&ie=UTF8&iwloc=&output=embed" 
              loading="lazy" 
              allowfullscreen 
              referrerpolicy="no-referrer-when-downgrade" 
              title="Sagar Flower Shop Parli Google Maps Location">
            </iframe>
          </div>

          <div class="maps-actions">
            <a class="btn btn-maps-dir" href="https://www.google.com/maps/dir/?api=1&destination=Sagar+Flower+Shop+near+Maharashtra+Shoe+Mart+Parli+Maharashtra" target="_blank" rel="noopener noreferrer">
              <span aria-hidden="true">🚗</span>
              <span>मार्ग दाखवा (Directions)</span>
            </a>
            <a class="btn btn-maps-wa" href="{maps_wa_link}" target="_blank" rel="noopener noreferrer">
              <span aria-hidden="true">💬</span>
              <span>WhatsApp लोकेशन</span>
            </a>
            <a class="btn btn-maps-call" href="tel:+917620644158">
              <span aria-hidden="true">📞</span>
              <span>कॉल करा</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- FOOTER -->
  <footer class="footer">
    <div class="wrap footer-content">
      <div class="footer-brand">
        <img class="footer-logo" src="assets/brand/sagar-logo.webp" alt="सागर फूल सेंटर" width="120" height="60">
        <p>ताजी फुले. शुभ क्षणांची साथ. परळी, महाराष्ट्र.</p>
      </div>
      <div class="footer-links">
        <a href="#home">होम</a>
        <a href="#collection">गॅलरी</a>
        <a href="#films">व्हिडिओ</a>
        <a href="#services">सेवा</a>
        <a href="#contact">पत्ता</a>
      </div>
      <div class="footer-copy">
        <p>© <span id="year">2026</span> Sagar Flower Shop. All rights reserved.</p>
        <a class="back-to-top" href="#home" aria-label="Back to top">वर जा ↑</a>
      </div>
    </div>
  </footer>

  <!-- FLOATING WHATSAPP BUTTON (Positioned safely above bottom dock on mobile) -->
  <a class="floating-wa" href="{hero_wa_link}" aria-label="WhatsApp वर थेट बोला" target="_blank" rel="noopener noreferrer">
    <div class="floating-wa-icon-box" aria-hidden="true">
      <svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/></svg>
      <span class="floating-wa-pulse" aria-hidden="true"></span>
    </div>
    <span class="floating-wa-label">WhatsApp ऑर्डर</span>
  </a>

  <!-- MOBILE BOTTOM NAVIGATION DOCK (Thumb-zone friendly, hidden on desktop) -->
  <nav class="mobile-bottom-dock" aria-label="Mobile quick navigation">
    <div class="dock-track">
      <a href="#home" data-section="home" class="dock-item active">
        <span class="dock-icon" aria-hidden="true">🏠</span>
        <span class="dock-label">होम</span>
      </a>
      <a href="#collection" data-section="collection" class="dock-item">
        <span class="dock-icon" aria-hidden="true">🌸</span>
        <span class="dock-label">फुले</span>
      </a>
      <a href="#films" data-section="films" class="dock-item">
        <span class="dock-icon" aria-hidden="true">🎬</span>
        <span class="dock-label">व्हिडिओ</span>
      </a>
      <a href="#contact" data-section="contact" class="dock-item">
        <span class="dock-icon" aria-hidden="true">📍</span>
        <span class="dock-label">पत्ता</span>
      </a>
    </div>
  </nav>

  <!-- ACCESSIBLE LIGHTBOX DIALOG -->
  <dialog id="lightbox" aria-labelledby="lightbox-title">
    <button class="lightbox-close" aria-label="Close photo">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
    </button>
    <div class="lightbox-image-container">
      <button class="lightbox-nav lightbox-prev" aria-label="Previous photo">‹</button>
      <img alt="" id="lightbox-photo">
      <span class="watermark" aria-hidden="true">SAGAR · 7620644158</span>
      <button class="lightbox-nav lightbox-next" aria-label="Next photo">›</button>
    </div>
    <div class="lightbox-footer">
      <div class="lightbox-info">
        <span id="lightbox-count" class="lightbox-count"></span>
        <h2 id="lightbox-title" class="lightbox-title"></h2>
      </div>
      <a class="btn btn-wa-lightbox" id="lightbox-inquire" target="_blank" rel="noopener noreferrer">
        <svg class="wa-icon" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/></svg>
        <span>WhatsApp वर ऑर्डर</span>
      </a>
    </div>
    <p class="lightbox-hint">स्वाइप करा किंवा बाणांचा वापर करा</p>
  </dialog>
</body>
</html>
'''

(R / 'index.html').write_text(html_content, encoding='utf-8')
print("Successfully generated high-performance mobile-first index.html!")
