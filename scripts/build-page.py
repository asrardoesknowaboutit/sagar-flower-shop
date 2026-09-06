from pathlib import Path
import json, re, html
from urllib.parse import quote

R = Path(__file__).resolve().parents[1]
source = (R / 'scripts/site-base.html').read_text()
items = json.loads((R / 'assets/collection.json').read_text())

# Bouquets are top priority in the floral collection
bouquet_order = [
    'new-2', 'new-7', 'new-5', 'new-4', 'new-16', 'new-31', 
    'new-6', 'new-14', 'new-3', 'new-17', 'new-12', 'new-34', 
    'new-35', 'new-18', 'new-19', 'original-25', 'original-37'
]

def sort_key(item):
    if item['category'] == 'bouquets':
        try:
            return (0, bouquet_order.index(item['id']))
        except ValueError:
            return (0, 99)
    elif item['category'] == 'garlands':
        return (1, 0)
    elif item['category'] == 'decor':
        return (2, 0)
    elif item['category'] == 'belts':
        return (3, 0)
    return (4, 0)

items.sort(key=sort_key)
(R / 'assets/collection.json').write_text(json.dumps(items, ensure_ascii=False, indent=2))

wa = lambda title: 'https://wa.me/917620644158?text=' + quote('नमस्कार! मला ' + title + ' याबद्दल माहिती हवी आहे. / Hello, I would like to enquire about ' + title + '.')

def image(i, eager=False, sizes='(max-width: 600px) 48vw, (max-width: 900px) 45vw, 30vw'):
    if 'copies' in i:
        srcset = ', '.join(f"{v['path']} {v['width']}w" for v in i['copies'].values())
    else:
        srcset = f"{i['thumb']} 640w, {i['src']} {i['width']}w"
    return f'''<img src="{i['thumb']}" srcset="{srcset}" sizes="{sizes}" width="{i['width']}" height="{i['height']}" style="aspect-ratio: {i['width']} / {i['height']};" alt="{html.escape(i['title'])} — Sagar Flower Shop" {'fetchpriority="high"' if eager else 'loading="lazy"'} decoding="async">'''

def watermark():
    return '<span class="watermark" aria-hidden="true">SAGAR · 7620644158</span>'

logo = '<img class="shop-logo" src="assets/brand/sagar-logo.webp" alt="सागर फूल सेंटर — Sagar Flower Shop" width="420" height="211">'

# Preload hero video poster
head = source[:source.index('<body>')].replace('assets/images/bouquets/bouquets-25.webp', 'assets/videos/delivery-poster.webp')
head = re.sub(r'<link rel="preload" as="image"[^>]+>', '<link rel="preload" as="image" href="assets/videos/delivery-poster.webp">', head)

parts = [head, f'''<body><a class="skip" href="#main">Skip to content</a>
<header class="header">
  <a class="brand" href="#home" aria-label="Sagar Flower Shop home">
    {logo}
  </a>
  <nav class="desktop-nav" aria-label="Main navigation">
    <div class="fluid-nav-track">
      <a href="#collection" data-section="collection" class="fluid-nav-pill"><span>आमचे काम</span> <small>Collection</small></a>
      <a href="#films" data-section="films" class="fluid-nav-pill"><span>व्हिडिओ</span> <small>Stories</small></a>
      <a href="#inspiration" data-section="inspiration" class="fluid-nav-pill"><span>शाही रचना</span> <small>Signature</small></a>
      <a href="#services" data-section="services" class="fluid-nav-pill"><span>सेवा</span> <small>Services</small></a>
      <a href="#contact" data-section="contact" class="fluid-nav-pill"><span>भेट द्या</span> <small>Visit us</small></a>
    </div>
  </nav>
  <a class="header-fluid-order" href="{wa('फुलांची थेट ऑर्डर')}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp वर ऑर्डर">
    <div class="header-order-wa">
      <svg class="header-wa-icon" viewBox="0 0 24 24" width="17" height="17" fill="currentColor">
        <path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/>
      </svg>
      <span>WhatsApp ऑर्डर</span>
    </div>
    <div class="header-order-arrow" aria-hidden="true">
      <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
        <line x1="5" y1="12" x2="19" y2="12"></line>
        <polyline points="12 5 19 12 12 19"></polyline>
      </svg>
    </div>
  </a>
  <div class="scroll-progress" aria-hidden="true"></div>
</header>
<main id="main">

<section class="hero wrap" id="home">
  <!-- Living Typography Synchronized Backdrop (Cinematic crossfade + scale) -->
  <div class="hero-living-backdrop" aria-hidden="true">
    <div class="living-bg-slide active" data-service="bouquets" style="background-image: url('assets/images/bouquets/collection-02-1280.webp');"></div>
    <div class="living-bg-slide" data-service="garlands" style="background-image: url('assets/images/garlands/collection-20-1280.webp');"></div>
    <div class="living-bg-slide" data-service="wedding" style="background-image: url('assets/images/inspiration/varmala-960.webp');"></div>
    <div class="living-bg-slide" data-service="decor" style="background-image: url('assets/images/decor/collection-10-1280.webp');"></div>
    <div class="living-bg-slide" data-service="gifts" style="background-image: url('assets/images/bouquets/collection-34-1280.webp');"></div>
    <div class="living-backdrop-scrim"></div>
  </div>

  <!-- LIVING TYPOGRAPHY COMPOSITION -->
  <div class="living-typography-stage" role="region" aria-label="Living Typography - Florist Services">
    <div class="living-typography-row" aria-live="polite">
      <!-- 1: Bouquets -->
      <a class="living-word-slot active" href="#collection" data-service="bouquets" data-filter="bouquets" aria-label="Bouquets - आकर्षक बुके">
        <span class="living-word">
          <span class="living-word-text">Bouquets</span>
          <span class="living-word-mr" lang="mr">बुके</span>
        </span>
      </a>
      <span class="living-dot-sep" aria-hidden="true">·</span>

      <!-- 2: Garlands -->
      <a class="living-word-slot" href="#collection" data-service="garlands" data-filter="garlands" aria-label="Garlands - लग्नहार">
        <span class="living-word">
          <span class="living-word-text">Garlands</span>
          <span class="living-word-mr" lang="mr">लग्नहार</span>
        </span>
      </a>
      <span class="living-dot-sep" aria-hidden="true">·</span>

      <!-- 3: Wedding Flowers -->
      <a class="living-word-slot" href="#collection" data-service="wedding" data-filter="garlands" aria-label="Wedding Flowers - वरमाला">
        <span class="living-word">
          <span class="living-word-text">Wedding Flowers</span>
          <span class="living-word-mr" lang="mr">वरमाला</span>
        </span>
      </a>
      <span class="living-dot-sep" aria-hidden="true">·</span>

      <!-- 4: Decorations -->
      <a class="living-word-slot" href="#collection" data-service="decor" data-filter="decor" aria-label="Decorations - सजावट">
        <span class="living-word">
          <span class="living-word-text">Decorations</span>
          <span class="living-word-mr" lang="mr">सजावट</span>
        </span>
      </a>
      <span class="living-dot-sep" aria-hidden="true">·</span>

      <!-- 5: Gifts -->
      <a class="living-word-slot" href="#collection" data-service="gifts" data-filter="belts" aria-label="Gifts - भेटवस्तू">
        <span class="living-word">
          <span class="living-word-text">Gifts</span>
          <span class="living-word-mr" lang="mr">भेटवस्तू</span>
        </span>
      </a>
    </div>
  </div>

  <div class="hero-copy">
    <p class="eyebrow">📍 सागर फ्लॉवर सेंटर · PARLI, MAHARASHTRA <span>✳</span> FAST DOORSTEP DELIVERY</p>
    
    <h1 class="hero-headline hero-ticker-wrap" aria-live="polite">
      <div class="hero-ticker-viewport">
        <!-- Slide 1: Marathi (ताजी फुले) -->
        <div class="hero-ticker-slide active" data-index="0">
          <span class="ticker-headline-primary devanagari-text" lang="mr">ताजी फुले.</span>
          <em class="ticker-headline-accent devanagari-text" lang="mr">शुभ क्षणांची साथ.</em>
        </div>
        <!-- Slide 2: Hindi (ताज़े फूल) -->
        <div class="hero-ticker-slide" data-index="1">
          <span class="ticker-headline-primary devanagari-text" lang="hi">ताज़े फूल.</span>
          <em class="ticker-headline-accent devanagari-text" lang="hi">खुशियों में साथ.</em>
        </div>
        <!-- Slide 3: English (Fresh Flowers) -->
        <div class="hero-ticker-slide" data-index="2">
          <span class="ticker-headline-primary english-text" lang="en">Fresh Flowers.</span>
          <em class="ticker-headline-accent english-text" lang="en">Made for Your Moments.</em>
        </div>
        <!-- Slide 4: Marathi (शाही लग्नहार) -->
        <div class="hero-ticker-slide" data-index="3">
          <span class="ticker-headline-primary devanagari-text" lang="mr">शाही लग्नहार.</span>
          <em class="ticker-headline-accent devanagari-text" lang="mr">परंपरेचा खरा सुगंध.</em>
        </div>
        <!-- Slide 5: Hindi (शाही वरमाला) -->
        <div class="hero-ticker-slide" data-index="4">
          <span class="ticker-headline-primary devanagari-text" lang="hi">शाही वरमाला.</span>
          <em class="ticker-headline-accent devanagari-text" lang="hi">हर उत्सव की शान.</em>
        </div>
        <!-- Slide 6: English (Royal Garlands) -->
        <div class="hero-ticker-slide" data-index="5">
          <span class="ticker-headline-primary english-text" lang="en">Royal Garlands.</span>
          <em class="ticker-headline-accent english-text" lang="en">Pure Tradition & Love.</em>
        </div>
      </div>
    </h1>

    <p class="hero-description">Fresh wedding garlands, handcrafted celebration bouquets, haldi swing decorations & wedding car decor. Made fresh every day with tradition and love in Parli.</p>

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
  <div class="reference-actions" aria-label="Order flowers and explore services">
    <!-- FLUID CONNECTED ACTION POD (WhatsApp + Call) -->
    <div class="fluid-action-pod-wrap">
      <div class="fluid-action-pod">
        <!-- WhatsApp Unit -->
        <a class="fluid-unit fluid-unit-wa" href="{wa('फुलांची थेट ऑर्डर')}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp वर ऑर्डर करा - Chat now • Fast response">
          <div class="fluid-badge wa-badge" aria-hidden="true">
            <svg class="wa-svg" viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
              <path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/>
            </svg>
          </div>
          <div class="fluid-text-group">
            <span class="fluid-title">WhatsApp वर ऑर्डर करा</span>
            <span class="fluid-sub">Chat now • Fast response</span>
          </div>
          <div class="fluid-circle-arrow wa-arrow-btn" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </div>
        </a>

        <!-- Organic Fluid Waist Bridge -->


        <!-- Call Unit -->
        <a class="fluid-unit fluid-unit-call" href="tel:+917620644158" aria-label="76206 44158 - Call us directly">
          <div class="fluid-badge call-badge" aria-hidden="true">
            <svg class="call-svg" viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
              <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 0 0-1.01.24l-2.2 2.2a15.053 15.053 0 0 1-6.59-6.59l2.2-2.21a.96.96 0 0 0 .25-1A11.36 11.36 0 0 1 8.5 3.99c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-.99-1.11z"/>
            </svg>
          </div>
          <div class="fluid-text-group">
            <span class="fluid-title call-number">76206 44158</span>
            <span class="fluid-sub call-sub">Call us directly</span>
          </div>
          <div class="fluid-circle-arrow call-arrow-btn" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </div>
        </a>
      </div>
    </div>

    <!-- FLUID CONNECTED TAGS RIBBON (लग्नहार ~ बुके ~ गाडी सजावट ~ घरपोच डिलिव्हरी) -->
    <div class="fluid-tags-ribbon-wrap">
      <div class="fluid-tags-ribbon" role="region" aria-label="Quick Categories">
        <!-- Tag 1: लग्नहार (Garlands) -->
        <a class="fluid-tag-pill tag-garlands" href="#collection" data-filter-trigger="garlands">
          <img class="button-sticker tag-sticker" src="assets/stickers/sticker-garland.webp" alt="" width="22" height="22">
          <span class="tag-label">लग्नहार</span>
          <span class="tag-arrow" aria-hidden="true">›</span>
        </a>

        <!-- Organic Fluid Tag Waist 1-2 -->


        <!-- Tag 2: बुके (Bouquets) -->
        <a class="fluid-tag-pill tag-bouquets" href="#collection" data-filter-trigger="bouquets">
          <img class="button-sticker tag-sticker" src="assets/stickers/sticker-bouquet.webp" alt="" width="22" height="22">
          <span class="tag-label">बुके</span>
          <span class="tag-arrow" aria-hidden="true">›</span>
        </a>

        <!-- Organic Fluid Tag Waist 2-3 -->


        <!-- Tag 3: गाडी सजावट (Car Decor) -->
        <a class="fluid-tag-pill tag-decor" href="#collection" data-filter-trigger="decor">
          <img class="button-sticker tag-sticker" src="assets/stickers/sticker-decor.webp" alt="" width="22" height="22">
          <span class="tag-label">गाडी सजावट</span>
          <span class="tag-arrow" aria-hidden="true">›</span>
        </a>

        <!-- Organic Fluid Tag Waist 3-4 -->


        <!-- Tag 4: घरपोच डिलिव्हरी (Doorstep Delivery) -->
        <a class="fluid-tag-pill tag-delivery" href="{wa('घरपोच डिलिव्हरी बद्दल माहिती')}" target="_blank" rel="noopener noreferrer">
          <img class="button-sticker tag-sticker" src="assets/stickers/sticker-delivery.webp" alt="" width="22" height="22">
          <span class="tag-label">घरपोच डिलिव्हरी</span>
          <span class="tag-arrow" aria-hidden="true">›</span>
        </a>
      </div>
    </div>
  </div>

</section>

<div class="values-strip">
  <div class="fluid-values-ribbon-wrap">
    <div class="fluid-values-ribbon" role="region" aria-label="Sagar Highlights">
      <!-- Value 1: १००% ताजी फुले -->
      <a class="fluid-val-pill val-fresh" href="#collection" data-filter-trigger="all" aria-label="१००% ताजी फुले - सर्व ताजी फुले पहा">
        <img class="button-sticker val-sticker" src="assets/stickers/sticker-blossom.webp" alt="" width="22" height="22">
        <span class="val-label">१००% ताजी फुले</span>
        <span class="val-arrow" aria-hidden="true">›</span>
      </a>

      <!-- Organic Fluid Waist 1-2 (Rose to Mint) -->
      <div class="fluid-val-waist val-waist-1" aria-hidden="true">
        <svg class="val-waist-svg" viewBox="0 0 28 46" preserveAspectRatio="none">
          <defs>
            <linearGradient id="valWaistGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="35%" stop-color="#fff0f5"/>
              <stop offset="70%" stop-color="#f0fdf4"/>
              <stop offset="100%" stop-color="#ffffff"/>
            </linearGradient>
          </defs>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0 L 28,46 C 21,46 18,37 14,37 C 10,37 7,46 0,46 Z" fill="url(#valWaistGrad1)"/>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0" fill="none" stroke="rgba(255, 255, 255, 0.95)" stroke-width="1.5"/>
          <path d="M 0,46 C 7,46 10,37 14,37 C 18,37 21,46 28,46" fill="none" stroke="rgba(255, 255, 255, 0.9)" stroke-width="1.5"/>
        </svg>
      </div>

      <!-- Value 2: आकर्षक लग्नहार व वरमाला -->
      <a class="fluid-val-pill val-wedding" href="#collection" data-filter-trigger="garlands" aria-label="आकर्षक लग्नहार व वरमाला">
        <img class="button-sticker val-sticker" src="assets/stickers/sticker-rings.webp" alt="" width="22" height="22">
        <span class="val-label"><span class="val-text-full">आकर्षक लग्नहार व वरमाला</span><span class="val-text-short">लग्नहार व वरमाला</span></span>
        <span class="val-arrow" aria-hidden="true">›</span>
      </a>

      <!-- Organic Fluid Waist 2-3 (Mint to Coral) -->
      <div class="fluid-val-waist val-waist-2" aria-hidden="true">
        <svg class="val-waist-svg" viewBox="0 0 28 46" preserveAspectRatio="none">
          <defs>
            <linearGradient id="valWaistGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="35%" stop-color="#f0fdf4"/>
              <stop offset="70%" stop-color="#fff5f5"/>
              <stop offset="100%" stop-color="#ffffff"/>
            </linearGradient>
          </defs>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0 L 28,46 C 21,46 18,37 14,37 C 10,37 7,46 0,46 Z" fill="url(#valWaistGrad2)"/>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0" fill="none" stroke="rgba(255, 255, 255, 0.95)" stroke-width="1.5"/>
          <path d="M 0,46 C 7,46 10,37 14,37 C 18,37 21,46 28,46" fill="none" stroke="rgba(255, 255, 255, 0.9)" stroke-width="1.5"/>
        </svg>
      </div>

      <!-- Value 3: गाडी व मंडप सजावट -->
      <a class="fluid-val-pill val-decor" href="#collection" data-filter-trigger="decor" aria-label="गाडी व मंडप सजावट">
        <img class="button-sticker val-sticker" src="assets/stickers/sticker-decor.webp" alt="" width="22" height="22">
        <span class="val-label"><span class="val-text-full">गाडी व मंडप सजावट</span><span class="val-text-short">गाडी व मंडप सजावट</span></span>
        <span class="val-arrow" aria-hidden="true">›</span>
      </a>

      <!-- Organic Fluid Waist 3-4 (Coral to Gold) -->
      <div class="fluid-val-waist val-waist-3" aria-hidden="true">
        <svg class="val-waist-svg" viewBox="0 0 28 46" preserveAspectRatio="none">
          <defs>
            <linearGradient id="valWaistGrad3" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="35%" stop-color="#fff5f5"/>
              <stop offset="70%" stop-color="#fefce8"/>
              <stop offset="100%" stop-color="#ffffff"/>
            </linearGradient>
          </defs>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0 L 28,46 C 21,46 18,37 14,37 C 10,37 7,46 0,46 Z" fill="url(#valWaistGrad3)"/>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0" fill="none" stroke="rgba(255, 255, 255, 0.95)" stroke-width="1.5"/>
          <path d="M 0,46 C 7,46 10,37 14,37 C 18,37 21,46 28,46" fill="none" stroke="rgba(255, 255, 255, 0.9)" stroke-width="1.5"/>
        </svg>
      </div>

      <!-- Value 4: परळी व परिसरात जलद डिलिव्हरी -->
      <a class="fluid-val-pill val-delivery" href="{wa('परळी व परिसरात जलद घरपोच डिलिव्हरी बद्दल माहिती')}" target="_blank" rel="noopener noreferrer" aria-label="परळी व परिसरात जलद डिलिव्हरी">
        <img class="button-sticker val-sticker" src="assets/stickers/sticker-delivery.webp" alt="" width="22" height="22">
        <span class="val-label"><span class="val-text-full">परळी व परिसरात जलद डिलिव्हरी</span><span class="val-text-short">जलद घरपोच डिलिव्हरी</span></span>
        <span class="val-arrow" aria-hidden="true">›</span>
      </a>
    </div>
  </div>
</div>

<section id="collection" class="collection wrap section">
  <div class="section-heading">
    <div>
      <p class="eyebrow">THE FLOWER EDIT · आमची फुलांची दुनिया</p>
      <h2>Let the flowers<br><em>do the talking.</em></h2>
    </div>
    <p>Find a design you love. Tap to see every detail in full resolution.<br><span lang="mr">तुमची आवडती डिझाईन निवडा, ऑर्डर WhatsApp वर द्या.</span></p>
  </div>

  <!-- FLUID CONNECTED CATEGORY FILTER RIBBON (MATCHING HERO VALUES RIBBON) -->
  <div class="fluid-filter-ribbon-wrap">
    <div class="fluid-filter-ribbon" role="region" aria-label="Floral Category Filter">
      <!-- Category 1: सर्व फुले -->
      <button data-filter="all" aria-pressed="true" class="fluid-filter-pill filter-all active" aria-label="सर्व फुले - All Designs">
        <img class="button-sticker filter-sticker" src="assets/stickers/sticker-blossom.webp" alt="" width="22" height="22">
        <span class="filter-label">सर्व फुले</span>
        <span class="filter-arrow" aria-hidden="true">›</span>
      </button>

      <!-- Organic Fluid Waist 1-2 (Rose to Mint) -->
      <div class="fluid-filter-waist waist-1" aria-hidden="true">
        <svg class="filter-waist-svg" viewBox="0 0 28 46" preserveAspectRatio="none">
          <defs>
            <linearGradient id="catWaistGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="35%" stop-color="#fff0f5"/>
              <stop offset="70%" stop-color="#f0fdf4"/>
              <stop offset="100%" stop-color="#ffffff"/>
            </linearGradient>
          </defs>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0 L 28,46 C 21,46 18,37 14,37 C 10,37 7,46 0,46 Z" fill="url(#catWaistGrad1)"/>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0" fill="none" stroke="rgba(255, 255, 255, 0.95)" stroke-width="1.5"/>
          <path d="M 0,46 C 7,46 10,37 14,37 C 18,37 21,46 28,46" fill="none" stroke="rgba(255, 255, 255, 0.9)" stroke-width="1.5"/>
        </svg>
      </div>

      <!-- Category 2: लग्नहार व वरमाला -->
      <button data-filter="garlands" aria-pressed="false" class="fluid-filter-pill filter-garlands" aria-label="लग्नहार व वरमाला - Wedding Garlands">
        <img class="button-sticker filter-sticker" src="assets/stickers/sticker-garland.webp" alt="" width="22" height="22">
        <span class="filter-label"><span class="filter-text-full">लग्नहार व वरमाला</span><span class="filter-text-short">लग्नहार</span></span>
        <span class="filter-arrow" aria-hidden="true">›</span>
      </button>

      <!-- Organic Fluid Waist 2-3 (Mint to Sky) -->
      <div class="fluid-filter-waist waist-2" aria-hidden="true">
        <svg class="filter-waist-svg" viewBox="0 0 28 46" preserveAspectRatio="none">
          <defs>
            <linearGradient id="catWaistGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="35%" stop-color="#f0fdf4"/>
              <stop offset="70%" stop-color="#f0f9ff"/>
              <stop offset="100%" stop-color="#ffffff"/>
            </linearGradient>
          </defs>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0 L 28,46 C 21,46 18,37 14,37 C 10,37 7,46 0,46 Z" fill="url(#catWaistGrad2)"/>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0" fill="none" stroke="rgba(255, 255, 255, 0.95)" stroke-width="1.5"/>
          <path d="M 0,46 C 7,46 10,37 14,37 C 18,37 21,46 28,46" fill="none" stroke="rgba(255, 255, 255, 0.9)" stroke-width="1.5"/>
        </svg>
      </div>

      <!-- Category 3: आकर्षक बुके -->
      <button data-filter="bouquets" aria-pressed="false" class="fluid-filter-pill filter-bouquets" aria-label="आकर्षक बुके - Bouquets">
        <img class="button-sticker filter-sticker" src="assets/stickers/sticker-bouquet.webp" alt="" width="22" height="22">
        <span class="filter-label"><span class="filter-text-full">आकर्षक बुके</span><span class="filter-text-short">बुके</span></span>
        <span class="filter-arrow" aria-hidden="true">›</span>
      </button>

      <!-- Organic Fluid Waist 3-4 (Sky to Coral) -->
      <div class="fluid-filter-waist waist-3" aria-hidden="true">
        <svg class="filter-waist-svg" viewBox="0 0 28 46" preserveAspectRatio="none">
          <defs>
            <linearGradient id="catWaistGrad3" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="35%" stop-color="#f0f9ff"/>
              <stop offset="70%" stop-color="#fff5f5"/>
              <stop offset="100%" stop-color="#ffffff"/>
            </linearGradient>
          </defs>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0 L 28,46 C 21,46 18,37 14,37 C 10,37 7,46 0,46 Z" fill="url(#catWaistGrad3)"/>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0" fill="none" stroke="rgba(255, 255, 255, 0.95)" stroke-width="1.5"/>
          <path d="M 0,46 C 7,46 10,37 14,37 C 18,37 21,46 28,46" fill="none" stroke="rgba(255, 255, 255, 0.9)" stroke-width="1.5"/>
        </svg>
      </div>

      <!-- Category 4: गाडी व स्टेज सजावट -->
      <button data-filter="decor" aria-pressed="false" class="fluid-filter-pill filter-decor" aria-label="गाडी व स्टेज सजावट - Car & Stage Decor">
        <img class="button-sticker filter-sticker" src="assets/stickers/sticker-decor.webp" alt="" width="22" height="22">
        <span class="filter-label"><span class="filter-text-full">गाडी व स्टेज सजावट</span><span class="filter-text-short">गाडी सजावट</span></span>
        <span class="filter-arrow" aria-hidden="true">›</span>
      </button>

      <!-- Organic Fluid Waist 4-5 (Coral to Gold) -->
      <div class="fluid-filter-waist waist-4" aria-hidden="true">
        <svg class="filter-waist-svg" viewBox="0 0 28 46" preserveAspectRatio="none">
          <defs>
            <linearGradient id="catWaistGrad4" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="35%" stop-color="#fff5f5"/>
              <stop offset="70%" stop-color="#fefce8"/>
              <stop offset="100%" stop-color="#ffffff"/>
            </linearGradient>
          </defs>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0 L 28,46 C 21,46 18,37 14,37 C 10,37 7,46 0,46 Z" fill="url(#catWaistGrad4)"/>
          <path d="M 0,0 C 7,0 10,9 14,9 C 18,9 21,0 28,0" fill="none" stroke="rgba(255, 255, 255, 0.95)" stroke-width="1.5"/>
          <path d="M 0,46 C 7,46 10,37 14,37 C 18,37 21,46 28,46" fill="none" stroke="rgba(255, 255, 255, 0.9)" stroke-width="1.5"/>
        </svg>
      </div>

      <!-- Category 5: गजरा व कंबरपट्टा -->
      <button data-filter="belts" aria-pressed="false" class="fluid-filter-pill filter-belts" aria-label="गजरा व कंबरपट्टा - Floral Jewellery">
        <img class="button-sticker filter-sticker" src="assets/stickers/sticker-belt.webp" alt="" width="22" height="22">
        <span class="filter-label"><span class="filter-text-full">गजरा व कंबरपट्टा</span><span class="filter-text-short">कंबरपट्टा</span></span>
        <span class="filter-arrow" aria-hidden="true">›</span>
      </button>
    </div>
  </div>
  <div class="gallery-toolbar">
    <p id="filter-status" role="status" aria-live="polite">{len(items)} floral designs</p>
    <span>फोटोवर टॅप करून मोठा फोटो पहा ↗</span>
  </div>
  <div class="portfolio">''']

for idx, i in enumerate(items):
    aspect = f"{i['width']} / {i['height']}"
    is_eager = (idx < 6)
    priority_class = " priority-item" if idx < 12 else ""
    parts.append(f'''<article class="work-card{priority_class}" data-category="{i['category']}"><button class="photo-button" style="aspect-ratio: {aspect};" data-image="{i['src']}" data-title="{i['title']}" data-marathi="{i['marathi']}" data-group="collection" aria-label="View {i['title']}">{image(i, eager=is_eager)}{watermark()}<span class="expand" aria-hidden="true" title="मोठा फोटो पहा">↗</span></button><div class="card-info"><div class="card-meta"><span class="category-pill">{i['label']}</span></div><h3 class="card-title-mr" lang="mr">{i['marathi']}</h3><p class="card-title-en">{i['title']}</p><a class="inquire fluid-card-inquire" href="{wa(i['marathi'] + ' / ' + i['title'])}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp वर ऑर्डर - {i['marathi']}"><div class="inquire-wa-part"><svg class="inquire-wa-svg" viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/></svg><span>WhatsApp वर ऑर्डर</span></div><span class="inquire-arrow-pod" aria-hidden="true"><svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg></span></a></div></article>''')

parts.append(f'''</div>
<div class="collection-footer">
  <button id="show-more" class="neo-load-more" hidden aria-label="अधिक सुंदर डिझाईन्स उघडा">
    <span class="load-more-halo" aria-hidden="true"></span>
    <span class="load-more-content">
      <span class="load-more-icon-wrap" aria-hidden="true">
        <span class="load-more-flower">🌸</span>
      </span>
      <span class="load-more-text">
        <span class="load-more-primary" lang="mr">अधिक सुंदर डिझाईन्स उघडा</span>
        <span class="load-more-secondary">Explore more floral designs</span>
      </span>
      <span class="load-more-chip">
        <span class="chip-pulse" aria-hidden="true"></span>
        <span class="chip-count" id="show-more-count">+28</span>
        <span class="chip-label" lang="mr">आणखी</span>
      </span>
      <span class="load-more-arrow-wrap" aria-hidden="true">
        <span class="load-more-arrow">↓</span>
      </span>
    </span>
    <span class="load-more-shimmer" aria-hidden="true"></span>
  </button>
  <p>तुमच्या आवडीचे रंग, बजेट किंवा खास कल्पना आहे का?</p>
  <a class="text-link" href="{wa('कस्टम फुलांची ऑर्डर / Custom order')}" target="_blank" rel="noopener noreferrer">आम्हाला सांगा, आम्ही तयार करू ↗</a>
</div>
</section>

<!-- Elastic Section Boundary 1: Collection to Films (Bends & Stretches on Scroll) -->
<div class="elastic-boundary-wrap boundary-collection-to-films" data-boundary="col-to-films" aria-hidden="true">
  <svg class="elastic-boundary-svg" viewBox="0 0 1440 140" preserveAspectRatio="none">
    <defs>
      <linearGradient id="edgeSilverMint" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="rgba(255, 255, 255, 0.15)"/>
        <stop offset="25%" stop-color="rgba(255, 255, 255, 0.85)"/>
        <stop offset="50%" stop-color="rgba(167, 243, 208, 0.95)"/>
        <stop offset="75%" stop-color="rgba(255, 255, 255, 0.85)"/>
        <stop offset="100%" stop-color="rgba(255, 255, 255, 0.15)"/>
      </linearGradient>
    </defs>
    <path class="elastic-boundary-fill" d="M 0,75 C 440,135 1000,15 1440,70 L 1440,140 L 0,140 Z" fill="#062216"/>
    <path class="elastic-boundary-edge" d="M 0,75 C 440,135 1000,15 1440,70" fill="none" stroke="url(#edgeSilverMint)" stroke-width="2.5"/>
  </svg>
</div>

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
# Include Rose varmala, Lotus varmala, and Bouquet reel
for v in videos[:3]:
    theme = v.get('theme', 'theme-rose')
    tag = v.get('tag', v['marathi'])
    parts.append(f'''<article class="film-card {theme}" data-video-id="{v['id']}">
  <div class="film-frame">
    <video class="story-video" src="{v['src']}" poster="{v['poster']}" autoplay muted loop playsinline preload="auto" aria-label="{v['title']}"></video>
    <div class="film-ambient-aura" aria-hidden="true"></div>
    <div class="story-video-overlay">
      <span class="story-tag fluid-story-pill">
        <span class="story-tag-dot" aria-hidden="true"></span>
        <span class="story-tag-text">{tag}</span>
      </span>
      <button class="sound-toggle-btn story-sound-toggle" aria-label="Toggle audio" title="आवाज चालू/बंद करा">
        <span class="sound-icon">🔇</span>
      </button>
    </div>
    <div class="film-progress-bar" aria-hidden="true">
      <div class="film-progress-fill"></div>
    </div>
    <div class="film-watermark">
      <span class="wm-brand">🌸 SAGAR FLOWER SHOP</span>
      <span class="wm-loc">· PARLI</span>
    </div>
  </div>
  <div class="film-caption">
    <div class="film-caption-header">
      <span class="film-eyebrow">SAGAR SIGNATURE REEL</span>
      <h3 class="film-title">{v['title']}</h3>
      <p class="film-desc" lang="mr">{v['marathi']}</p>
    </div>
    <a class="story-order-btn fluid-card-inquire" href="{wa(v['title'] + ' - ' + v['marathi'] + ' (व्हिडिओ पाहून ऑर्डर)')}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp वर ऑर्डर - {v['title']}">
      <div class="inquire-wa-part">
        <svg class="inquire-wa-svg" viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/></svg>
        <span>WhatsApp वर ऑर्डर द्या</span>
      </div>
      <span class="inquire-arrow-pod" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
          <line x1="5" y1="12" x2="19" y2="12"></line>
          <polyline points="12 5 19 12 12 19"></polyline>
        </svg>
      </span>
    </a>
  </div>
</article>''')

parts.append('''</div>
<div class="rail-footer">
  <span class="rail-hint">← स्वाइप करा किंवा बटणाने पुढे जा (Swipe to explore) →</span>
  <div class="fluid-reel-controls" role="group" aria-label="व्हिडिओ नेव्हिगेशन (Video controls)">
    <button class="film-prev fluid-ctrl-pill" aria-label="मागील व्हिडिओ (Previous video)">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
      <span>मागील</span>
    </button>
    <div class="fluid-ctrl-waist" aria-hidden="true">
      <svg class="ctrl-waist-svg" viewBox="0 0 20 42" preserveAspectRatio="none">
        <defs>
          <linearGradient id="ctrlWaistGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#ffffff"/>
            <stop offset="50%" stop-color="#f2f7f4"/>
            <stop offset="100%" stop-color="#ffffff"/>
          </linearGradient>
        </defs>
        <path d="M 0,0 C 5,0 7,8 10,8 C 13,8 15,0 20,0 L 20,42 C 15,42 13,34 10,34 C 7,34 5,42 0,42 Z" fill="url(#ctrlWaistGrad)"/>
        <path d="M 0,0 C 5,0 7,8 10,8 C 13,8 15,0 20,0" fill="none" stroke="rgba(255,255,255,0.95)" stroke-width="1.5"/>
        <path d="M 0,42 C 5,42 7,34 10,34 C 13,34 15,42 20,42" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="1.5"/>
      </svg>
    </div>
    <button class="film-next fluid-ctrl-pill" aria-label="पुढील व्हिडिओ (Next video)">
      <span>पुढील</span>
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
    </button>
  </div>
</div>
  <!-- Elastic Section Boundary 2: Films to Inspiration (Cream Wave Pulls Up) -->
  <div class="elastic-boundary-wrap boundary-films-to-inspiration" data-boundary="films-to-inspire" aria-hidden="true">
    <svg class="elastic-boundary-svg" viewBox="0 0 1440 140" preserveAspectRatio="none">
      <defs>
        <linearGradient id="edgeSilverGold" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="rgba(255, 255, 255, 0.15)"/>
          <stop offset="30%" stop-color="rgba(255, 255, 255, 0.9)"/>
          <stop offset="55%" stop-color="rgba(254, 240, 138, 0.9)"/>
          <stop offset="80%" stop-color="rgba(255, 255, 255, 0.9)"/>
          <stop offset="100%" stop-color="rgba(255, 255, 255, 0.15)"/>
        </linearGradient>
      </defs>
      <path class="elastic-boundary-fill" d="M 0,65 C 480,15 960,130 1440,60 L 1440,140 L 0,140 Z" fill="var(--paper)"/>
      <path class="elastic-boundary-edge" d="M 0,65 C 480,15 960,130 1440,60" fill="none" stroke="url(#edgeSilverGold)" stroke-width="2.5"/>
    </svg>
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
  <button class="photo-button" style="aspect-ratio: 3 / 4;" data-image="assets/images/inspiration/{name}-960.webp" data-title="{title}" data-marathi="{mr}" data-group="inspiration" aria-label="View {title}">
    <img src="assets/images/inspiration/{name}-480.webp" srcset="assets/images/inspiration/{name}-480.webp 480w, assets/images/inspiration/{name}-960.webp 960w" sizes="(max-width: 600px) 90vw, 45vw" width="960" height="1280" style="aspect-ratio: 3 / 4;" alt="{title} — Sagar Flower Shop" loading="lazy">
    <span class="inspiration-badge fluid-gold-pill">{badge}</span>
    <span class="expand" aria-hidden="true">↗</span>
  </button>
  <div class="inspiration-caption">
    <h3 lang="mr">{mr}</h3>
    <p>{title}</p>
    <a class="fluid-inspire-cta" href="{wa(mr + ' (' + title + ')')}" target="_blank" rel="noopener noreferrer">
      <span>या डिझाईनची ऑर्डर द्या (Book on WhatsApp)</span>
      <span class="fluid-circle-arrow" aria-hidden="true">↗</span>
    </a>
  </div>
</article>''')

parts.append('</div></section>')

# Elastic Section Boundary 3: Inspiration to Services (Beige Wave Pulls Up)
parts.append('''<div class="elastic-boundary-wrap boundary-inspiration-to-services" data-boundary="inspire-to-services" aria-hidden="true">
  <svg class="elastic-boundary-svg" viewBox="0 0 1440 140" preserveAspectRatio="none">
    <defs>
      <linearGradient id="edgeSilverStone1" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="rgba(255, 255, 255, 0.25)"/>
        <stop offset="50%" stop-color="rgba(255, 255, 255, 0.95)"/>
        <stop offset="100%" stop-color="rgba(255, 255, 255, 0.25)"/>
      </linearGradient>
    </defs>
    <path class="elastic-boundary-fill" d="M 0,70 C 400,120 1040,25 1440,65 L 1440,140 L 0,140 Z" fill="#f2eee3"/>
    <path class="elastic-boundary-edge" d="M 0,70 C 400,120 1040,25 1440,65" fill="none" stroke="url(#edgeSilverStone1)" stroke-width="2"/>
  </svg>
</div>''')

# Retain verified business and service content from the base version.
services = re.search(r'<section id="services".*?(?=<section id="story")', source, re.S).group()
# Upgrade service links to fluid pill buttons and numbers to fluid pills
services = re.sub(
    r'<a href="([^"]+)" target="_blank" rel="noopener noreferrer">([^<]+)</a>',
    r'<a class="fluid-service-pill" href="\1" target="_blank" rel="noopener noreferrer"><span>\2</span><span class="fluid-circle-arrow" aria-hidden="true">↗</span></a>',
    services
)
services = re.sub(
    r'<span class="service-number">([^<]+)</span>',
    r'<span class="service-number fluid-num-pill">\1</span>',
    services
)

# Insert Elastic Section Boundary 4: Services to Story (Cream Wave Pulls Up) at end of services
services_boundary = '''  <div class="elastic-boundary-wrap boundary-services-to-story" data-boundary="services-to-story" aria-hidden="true">
    <svg class="elastic-boundary-svg" viewBox="0 0 1440 140" preserveAspectRatio="none">
      <defs>
        <linearGradient id="edgeSilverStone2" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="rgba(255, 255, 255, 0.25)"/>
          <stop offset="50%" stop-color="rgba(255, 255, 255, 0.95)"/>
          <stop offset="100%" stop-color="rgba(255, 255, 255, 0.25)"/>
        </linearGradient>
      </defs>
      <path class="elastic-boundary-fill" d="M 0,60 C 500,20 940,120 1440,70 L 1440,140 L 0,140 Z" fill="var(--paper)"/>
      <path class="elastic-boundary-edge" d="M 0,60 C 500,20 940,120 1440,70" fill="none" stroke="url(#edgeSilverStone2)" stroke-width="2"/>
    </svg>
  </div>
</section>'''
services = re.sub(r'</section>\s*$', services_boundary, services.strip())

story = re.search(r'<section id="story".*?(?=<section class="process)', source, re.S).group()

# Present the garland photograph cleanly
story = re.sub(
    r'<div class="story-image reveal">.*?</div>',
    '<div class="story-image"><img src="assets/images/garlands/collection-21-640.webp" width="640" height="1044" style="aspect-ratio: 640 / 1044;" alt="Traditional rose and ivory garland by Sagar Flower Shop" loading="lazy">' + watermark() + '<div class="story-tag fluid-story-pill">🌸 परंपरेचा सुगंध.</div></div>',
    story, count=1, flags=re.S
)
story = story.replace('</div></div><div class="story-copy', '</div><div class="story-copy')

# Contact Section with Creative Google Maps Location Window
contact = f'''<section id="contact" class="contact section wrap">
  <div class="contact-intro reveal">
    <p class="eyebrow">भेट द्या व संपर्क · VISIT & ENQUIRE</p>
    <h2>Let’s make<br>something <em>lovely.</em></h2>
    <p>A question, a celebration, or just a love of flowers.<br>We’re a call or a message away.</p>
    
    <a class="fluid-contact-wa-btn" href="{wa('फुलांची चौकशी / Flower booking & enquiry')}" target="_blank" rel="noopener noreferrer">
      <div class="wa-contact-left">
        <svg class="wa-svg" viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/></svg>
        <span>WhatsApp वर थेट चॅट करा</span>
      </div>
      <span class="fluid-circle-arrow" aria-hidden="true">↗</span>
    </a>
    <p class="marathi" lang="mr">तुमची आवड सांगा, फुलांची सजावट आम्ही करू.</p>

    <div class="contact-info-cards">
      <div class="contact-quick-card">
        <span class="eyebrow">LET’S TALK FLOWERS · थेट फोन करा</span>
        <a class="contact-phone fluid-phone-primary" href="tel:+917620644158"><span>📞 +91 76206 44158</span></a>
        <div class="other-phones fluid-phone-group">
          <span>इतर क्रमांक:</span>
          <a href="tel:+919960142943">99601 42943</a>
          <span>/</span>
          <a href="tel:+919763553185">97635 53185</a>
        </div>
      </div>

      <div class="contact-quick-card">
        <span class="eyebrow">BEFORE YOU VISIT · भेट देण्यापूर्वी</span>
        <p>ताजी फुले आणि डिझाईन उपलब्धतेसाठी आधी कॉल करू शकता. परळी परिसरात घरपोच डिलिव्हरी उपलब्ध आहे.</p>
      </div>
    </div>
  </div>

  <div class="contact-maps-showcase reveal">
    <!-- Creative Google Maps Location Window -->
    <div class="maps-location-window">
      <div class="maps-window-titlebar">
        <div class="window-controls-cluster" aria-hidden="true">
          <span class="window-dot dot-close"></span>
          <span class="window-dot dot-min"></span>
          <span class="window-dot dot-zoom"></span>
        </div>
        <div class="maps-live-indicator">
          <span class="radar-dot" aria-hidden="true"></span>
          <span class="live-full-tag">थेट गुगल मॅप्स लोकेशन · LIVE STORE GPS</span>
          <span class="live-short-tag">थेट लोकेशन · LIVE GPS</span>
        </div>
        <a class="maps-nav-action-btn" href="https://www.google.com/maps/search/?api=1&query=Sagar+Flower+Shop+near+Maharashtra+Shoe+Mart+Parli+Maharashtra" target="_blank" rel="noopener noreferrer" aria-label="Open in Google Maps">
          <span>Google Maps वर उघडा</span>
          <span aria-hidden="true">↗</span>
        </a>
      </div>

      <div class="maps-viewport-stage">
        <!-- Stylized Cartographic Fallback / Ambient Background -->
        <div class="map-carto-layer" aria-hidden="true">
          <div class="carto-area-green"></div>
          <div class="carto-road-main"></div>
          <div class="carto-road-cross"></div>
          <div class="carto-beacon-hub">
            <div class="beacon-ripple-ring"></div>
            <div class="beacon-pin-head">
              <span class="beacon-flower">🌸</span>
            </div>
            <span class="beacon-tag">SAGAR FLOWER SHOP</span>
          </div>
        </div>

        <iframe class="maps-iframe" 
          src="https://maps.google.com/maps?q=Near+Maharashtra+Shoe+Mart+Parli+Maharashtra&t=&z=16&ie=UTF8&iwloc=&output=embed" 
          loading="lazy" 
          allowfullscreen 
          referrerpolicy="no-referrer-when-downgrade" 
          title="Sagar Flower Shop Parli Google Maps Location">
        </iframe>

        <!-- Floating Glassmorphic HUD Location Card -->
        <div class="maps-hud-card">
          <div class="hud-badge-row">
            <div class="hud-flower-icon" aria-hidden="true">🌸</div>
            <div class="hud-title-wrap">
              <h4>सागर फ्लॉवर सेंटर</h4>
              <span>Sagar Flower Shop · Parli</span>
            </div>
          </div>
          <p class="hud-address">📍 Near Maharashtra Shoe Mart, Parli, Maharashtra 431515</p>
          <span class="hud-hours-tag">
            <span class="status-live-dot" aria-hidden="true">●</span> चालू आहे (Open All 7 Days · सकाळी ६ ते रात्री १०)
          </span>
        </div>
      </div>

      <div class="maps-window-footer">
        <div class="footer-fluid-dock">
          <a class="footer-fluid-pill primary-dir" href="https://www.google.com/maps/dir/?api=1&destination=Sagar+Flower+Shop+near+Maharashtra+Shoe+Mart+Parli+Maharashtra" target="_blank" rel="noopener noreferrer">
            <img class="button-sticker maps-btn-sticker" src="assets/stickers/sticker-decor.webp" alt="" width="18" height="18">
            <span class="pill-full-text">मार्ग दाखवा (Directions)</span>
            <span class="pill-short-text">मार्ग (Directions)</span>
          </a>
          <a class="footer-fluid-pill" href="https://wa.me/917620644158?text=%E0%A4%A8%E0%A4%AE%E0%A4%B8%E0%A5%8D%E0%A4%95%E0%A4%BE%E0%A4%B0!%20%E0%A4%AE%E0%A4%B2%E0%A4%BE%20%E0%A4%B8%E0%A4%BE%E0%A4%97%E0%A4%B0%20%E0%A4%AB%E0%A5%8D%E0%A4%B2%E0%A5%89%E0%A4%B4%E0%A4%B0%20%E0%A4%B8%E0%A5%87%E0%A4%82%E0%A4%9F%E0%A4%B0%E0%A4%9A%E0%A5%87%20%E0%A4%B2%E0%A5%8B%E0%A4%95%E0%A5%87%E0%A4%B6%E0%A4%A8%20%E0%A4%AA%E0%A4%BE%E0%A4%A0%E0%A4%B5%E0%A4%BE." target="_blank" rel="noopener noreferrer">
            <span aria-hidden="true">💬</span>
            <span class="pill-full-text">WhatsApp लोकेशन</span>
            <span class="pill-short-text">WhatsApp</span>
          </a>
          <a class="footer-fluid-pill" href="tel:+917620644158">
            <span aria-hidden="true">📞</span>
            <span class="pill-full-text">कॉल करा</span>
            <span class="pill-short-text">कॉल</span>
          </a>
        </div>
        <div class="footer-delivery-pill">
          <img class="button-sticker val-sticker" src="assets/stickers/sticker-delivery.webp" alt="" width="18" height="18">
          <span>परळी शहरात जलद घरपोच डिलिव्हरी</span>
        </div>
      </div>
    </div>
  </div>
</section>'''

parts.extend([services, story, contact, '</main>'])

# Elastic Section Boundary 5: Contact to Footer (Footer Stone Wave Pulls Up)
parts.append('''<div class="elastic-boundary-wrap boundary-contact-to-footer" data-boundary="contact-to-footer" aria-hidden="true">
  <svg class="elastic-boundary-svg" viewBox="0 0 1440 140" preserveAspectRatio="none">
    <defs>
      <linearGradient id="edgeSilverFooter" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="rgba(255, 255, 255, 0.25)"/>
        <stop offset="50%" stop-color="rgba(255, 255, 255, 0.95)"/>
        <stop offset="100%" stop-color="rgba(255, 255, 255, 0.25)"/>
      </linearGradient>
    </defs>
    <path class="elastic-boundary-fill" d="M 0,70 C 450,125 990,30 1440,65 L 1440,140 L 0,140 Z" fill="#f1ede2"/>
    <path class="elastic-boundary-edge" d="M 0,70 C 450,125 990,30 1440,65" fill="none" stroke="url(#edgeSilverFooter)" stroke-width="2"/>
  </svg>
</div>''')

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

parts.append(f'''<div class="floating-wa-wrap">
  <a class="floating-wa fluid-floating-pill" href="https://wa.me/917620644158?text={quote('नमस्कार! मला फुलांची थेट ऑर्डर करायची आहे. / Hello, I would like to book flowers.')}" aria-label="Chat with Sagar Flower Shop on WhatsApp" target="_blank" rel="noopener noreferrer">
    <div class="floating-wa-icon-box" aria-hidden="true">
      <svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
        <path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/>
      </svg>
      <span class="floating-wa-pulse" aria-hidden="true"></span>
    </div>
    <div class="floating-wa-copy">
      <span class="floating-wa-mr" lang="mr">WhatsApp वर बोला</span>
      <span class="floating-wa-en">Order & Inquire ↗</span>
    </div>
  </a>
</div>''')

parts.append('''<nav class="mobile-nav" aria-label="Mobile navigation">
  <div class="fluid-mobile-dock">
    <a href="#home" data-section="home" class="fluid-mobile-item active"><span class="dock-icon" aria-hidden="true">⌂</span><span class="dock-text">होम</span></a>
    <a href="#collection" data-section="collection" class="fluid-mobile-item"><span class="dock-icon" aria-hidden="true">❀</span><span class="dock-text">फुले</span></a>
    <a href="#films" data-section="films" class="fluid-mobile-item"><span class="dock-icon" aria-hidden="true">▷</span><span class="dock-text">व्हिडिओ</span></a>
    <a href="#contact" data-section="contact" class="fluid-mobile-item"><span class="dock-icon" aria-hidden="true">♡</span><span class="dock-text">संपर्क</span></a>
  </div>
</nav>

<dialog id="lightbox" aria-labelledby="lightbox-title">
  <button class="lightbox-close fluid-modal-close" aria-label="Close photo">
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
  </button>
  <div class="lightbox-image">
    <button class="lightbox-prev fluid-modal-nav" aria-label="Previous photo">‹</button>
    <img alt="" id="lightbox-photo">
    <span class="watermark" aria-hidden="true">SAGAR · 7620644158</span>
    <button class="lightbox-next fluid-modal-nav" aria-label="Next photo">›</button>
  </div>
  <div class="lightbox-bottom">
    <div>
      <span id="lightbox-count" class="eyebrow"></span>
      <h2 id="lightbox-title"></h2>
    </div>
    <a class="fluid-card-inquire lightbox-inquire-btn" id="lightbox-inquire" target="_blank" rel="noopener noreferrer">
      <div class="inquire-wa-part">
        <svg class="inquire-wa-svg" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41c-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.02.79.81-2.94-.19-.3a8.21 8.21 0 0 1-1.26-4.56c0-4.54 3.7-8.24 8.24-8.24zm4.51 11.64c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.02-1.24-.75-.67-1.25-1.49-1.4-1.74-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43l-.48-.01c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.53.61.2 1.16.17 1.6-.1.49-.3 1.47-1.2 1.68-1.75.2-.55.2-1.02.14-1.12-.06-.1-.23-.16-.48-.28z"/></svg>
        <span>WhatsApp वर ऑर्डर</span>
      </div>
      <span class="inquire-arrow-pod" aria-hidden="true">↗</span>
    </a>
  </div>
  <p class="lightbox-tip">स्वाइप करा किंवा बाणांचा वापर करा · दोन्ही बोटांनी झूम करू शकता</p>
</dialog>
</body>
</html>
''')

(R / 'index.html').write_text(''.join(parts))
print('Built upgraded portfolio with neumorphic connected contour filter bar')
