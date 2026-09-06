'use strict';

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const animate = () => !motion.matches;
const smooth = () => animate() ? 'smooth' : 'auto';

const whatsapp = (title, marathi = '') => {
  const item = marathi ? `${marathi} (${title})` : title;
  return 'https://wa.me/917620644158?text=' + encodeURIComponent(`नमस्कार! मला ${item} याबद्दल माहिती हवी आहे. / Hello, I would like to order ${item}.`);
};

// --- HERO VIDEO SOUND TOGGLE ---
const heroVideo = $('#hero-delivery-video');
const heroSoundBtn = $('#hero-sound-toggle');
if (heroVideo && heroSoundBtn) {
  heroSoundBtn.addEventListener('click', () => {
    heroVideo.muted = !heroVideo.muted;
    heroSoundBtn.querySelector('.sound-icon').textContent = heroVideo.muted ? '🔇' : '🔊';
    heroSoundBtn.setAttribute('aria-label', heroVideo.muted ? 'Unmute hero video' : 'Mute hero video');
  });
}

// --- STORY REEL VIDEOS (AUTOPLAY IN LOOP WITHOUT PLAY BUTTONS) ---
const storyVideos = $$('.story-video');
storyVideos.forEach(video => {
  video.loop = true;
  video.muted = true;
  video.playsInline = true;

  const card = video.closest('.film-card');
  const soundBtn = card?.querySelector('.story-sound-toggle');
  const progressFill = card?.querySelector('.film-progress-fill');

  // Track progress bar smoothly
  video.addEventListener('timeupdate', () => {
    if (progressFill && video.duration) {
      const pct = (video.currentTime / video.duration) * 100;
      progressFill.style.width = `${pct}%`;
    }
  });

  if (soundBtn) {
    soundBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const willMute = !video.muted;
      if (!willMute) {
        storyVideos.forEach(v => {
          if (v !== video) {
            v.muted = true;
            const otherBtn = v.closest('.film-card')?.querySelector('.story-sound-toggle');
            if (otherBtn) {
              const icon = otherBtn.querySelector('.sound-icon');
              if (icon) icon.textContent = '🔇';
              otherBtn.classList.remove('unmuted');
            }
          }
        });
        if (heroVideo) {
          heroVideo.muted = true;
          if (heroSoundBtn) heroSoundBtn.querySelector('.sound-icon').textContent = '🔇';
        }
      }
      video.muted = willMute;
      soundBtn.querySelector('.sound-icon').textContent = willMute ? '🔇' : '🔊';
      soundBtn.classList.toggle('unmuted', !willMute);
    });
  }

  video.addEventListener('click', () => {
    soundBtn?.click();
  });
});

// Film rail horizontal scroll controls
const rail = $('.film-rail');
if (rail) {
  const scrollFilms = direction => {
    const card = $('.film-card', rail);
    const cardWidth = card ? card.offsetWidth + 20 : 300;
    rail.scrollBy({ left: direction * cardWidth, behavior: smooth() });
  };
  $('.film-prev')?.addEventListener('click', () => scrollFilms(-1));
  $('.film-next')?.addEventListener('click', () => scrollFilms(1));
  rail.addEventListener('keydown', event => {
    if (event.target === rail && ['ArrowLeft', 'ArrowRight'].includes(event.key)) {
      event.preventDefault();
      scrollFilms(event.key === 'ArrowRight' ? 1 : -1);
    }
  });
}

// --- PORTFOLIO FILTERING & FLUID CONNECTED PILL RIBBON ---
const cards = $$('.work-card');
const filterButtons = $$('[data-filter]');
const filterContainer = $('.fluid-filter-ribbon-wrap') || $('.dynamic-island-ticker-wrap') || $('.neo-filter-container') || $('.filter-flow-wrapper');
const batchSize = () => window.innerWidth >= 900 ? 12 : 8;
let currentFilter = 'all', limit = batchSize();

function centerActiveButton(activeBtn) {
  if (!filterContainer || !activeBtn) return;
  if (filterContainer.scrollWidth > filterContainer.clientWidth) {
    const containerRect = filterContainer.getBoundingClientRect();
    const btnRect = activeBtn.getBoundingClientRect();
    const scrollTarget = filterContainer.scrollLeft + (btnRect.left - containerRect.left) - (filterContainer.clientWidth / 2) + (btnRect.width / 2);
    filterContainer.scrollTo({ left: Math.max(0, scrollTarget), behavior: smooth() });
  }
}

const getMatchingCards = () => cards.filter(card => currentFilter === 'all' || card.dataset.category === currentFilter);

function renderCollection() {
  const matches = getMatchingCards();
  cards.forEach(card => {
    const index = matches.indexOf(card);
    card.hidden = index === -1 || index >= limit;
  });
  const count = Math.min(limit, matches.length);
  const status = $('#filter-status');
  if (status) {
    status.textContent = `दाखवत आहोत: ${count} / ${matches.length} डिझाईन्स (Showing ${count} of ${matches.length})`;
  }
  const showMore = $('#show-more');
  if (showMore) {
    const remaining = matches.length - count;
    showMore.hidden = remaining <= 0;
    const countEl = $('#show-more-count');
    if (countEl) {
      countEl.textContent = `+${remaining}`;
    }
  }

  requestScrollUpdate();
}

filterButtons.forEach(button => button.addEventListener('click', () => {
  currentFilter = button.dataset.filter;
  limit = batchSize();
  if (filterContainer) filterContainer.dataset.activeFilter = currentFilter;
  filterButtons.forEach(item => {
    const active = item === button;
    item.classList.toggle('active', active);
    item.setAttribute('aria-pressed', String(active));
  });
  centerActiveButton(button);
  renderCollection();
  if (animate()) {
    const portfolio = $('.portfolio');
    if (portfolio) {
      portfolio.animate([
        { opacity: 0.5, transform: 'translateY(8px)' },
        { opacity: 1, transform: 'none' }
      ], { duration: 240, easing: 'cubic-bezier(0.16, 1, 0.3, 1)' });
    }
  }
}));

$('#show-more')?.addEventListener('click', () => {
  const matches = getMatchingCards();
  const oldLimit = limit;
  const firstNew = matches[oldLimit];
  limit += batchSize();
  renderCollection();

  if (animate()) {
    const newlyRevealed = matches.slice(oldLimit, limit);
    newlyRevealed.forEach((card, idx) => {
      card.style.animationDelay = `${idx * 45}ms`;
      card.classList.remove('card-revealing');
      void card.offsetWidth;
      card.classList.add('card-revealing');
    });
  }

  if (firstNew) {
    const photo = $('.photo-button', firstNew);
    photo?.focus({ preventScroll: true });
    firstNew.scrollIntoView({ behavior: smooth(), block: 'nearest' });
  }
});

// --- LIGHTBOX MODAL (100% Full uncropped view) ---
const dialog = $('#lightbox');
let activePhoto, lastTrigger, photoGroup = [];
let imageVersion = 0;

function showPhoto(button) {
  if (!button || !dialog) return;
  activePhoto = button;
  const photo = $('#lightbox-photo');
  const title = button.dataset.title || '';
  const marathi = button.dataset.marathi || '';
  const displayTitle = marathi ? `${marathi} · ${title}` : title;

  photo.src = button.dataset.image;
  photo.alt = displayTitle;
  $('#lightbox-title').textContent = displayTitle;
  $('#lightbox-inquire').href = whatsapp(title, marathi);
  $('#lightbox-count').textContent = `${photoGroup.indexOf(button) + 1} / ${photoGroup.length} · सागर फ्लॉवर सेंटर, परळी`;

  const version = ++imageVersion;
  photo.decode().catch(() => {}).then(() => {
    if (version === imageVersion && animate()) {
      photo.animate([{ opacity: 0.6 }, { opacity: 1 }], { duration: 160 });
    }
  });
}

function nextPhoto(direction) {
  if (!photoGroup.length) return;
  const currentIndex = photoGroup.indexOf(activePhoto);
  const nextIndex = (currentIndex + direction + photoGroup.length) % photoGroup.length;
  showPhoto(photoGroup[nextIndex]);
}

$$('.photo-button[data-image]').forEach(button => button.addEventListener('click', () => {
  lastTrigger = button;
  photoGroup = button.dataset.group === 'collection'
    ? getMatchingCards().map(card => $('.photo-button', card))
    : $$(`.photo-button[data-group="${button.dataset.group}"]`);
  showPhoto(button);
  dialog.showModal();
  document.body.classList.add('modal-open');
}));

$('.lightbox-close')?.addEventListener('click', () => dialog.close());
$('.lightbox-next')?.addEventListener('click', () => nextPhoto(1));
$('.lightbox-prev')?.addEventListener('click', () => nextPhoto(-1));

dialog?.addEventListener('click', event => {
  const r = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom)) {
    dialog.close();
  }
});
dialog?.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  lastTrigger?.focus({ preventScroll: true });
});
dialog?.addEventListener('keydown', event => {
  if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
    event.preventDefault();
    nextPhoto(event.key === 'ArrowRight' ? 1 : -1);
  }
});

function onSwipe(element, callback) {
  if (!element) return;
  let start = null;
  element.addEventListener('touchstart', event => {
    start = event.touches.length === 1 ? { x: event.touches[0].clientX, y: event.touches[0].clientY } : null;
  }, { passive: true });
  element.addEventListener('touchend', event => {
    if (!start) return;
    const dx = event.changedTouches[0].clientX - start.x;
    const dy = event.changedTouches[0].clientY - start.y;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.4) {
      callback(dx < 0 ? 1 : -1);
    }
    start = null;
  }, { passive: true });
}
onSwipe($('#lightbox-photo'), nextPhoto);

// --- BILINGUAL HERO HEADLINE TICKER (MARATHI & HINDI) ---
function initHeroHeadlineTicker() {
  const wrap = $('.hero-ticker-wrap');
  if (!wrap) return;

  const slides = $$('.hero-ticker-slide', wrap);
  if (slides.length <= 1) return;

  const DURATION = 3200; // 3.2 seconds per rotation
  let currentIndex = 0;
  let tickerTimer = null;
  let isHovered = false;

  function goToSlide(newIndex) {
    if (newIndex === currentIndex) return;

    const currentSlide = slides[currentIndex];
    const nextSlide = slides[newIndex];

    slides.forEach(s => {
      s.classList.remove('leaving-up', 'leaving-down');
    });

    if (currentSlide && animate()) {
      currentSlide.classList.remove('active');
      currentSlide.classList.add('leaving-up');
      setTimeout(() => {
        currentSlide.classList.remove('leaving-up');
      }, 600);
    } else if (currentSlide) {
      currentSlide.classList.remove('active');
    }

    if (nextSlide) {
      nextSlide.classList.add('active');
    }

    currentIndex = newIndex;
  }

  function advanceTicker() {
    const nextIdx = (currentIndex + 1) % slides.length;
    goToSlide(nextIdx);
  }

  function startCycle() {
    stopCycle();
    if (!isHovered && !document.hidden && animate()) {
      tickerTimer = setInterval(advanceTicker, DURATION);
    }
  }

  function stopCycle() {
    if (tickerTimer) {
      clearInterval(tickerTimer);
      tickerTimer = null;
    }
  }

  // Hover handlers: pause while reading
  wrap.addEventListener('mouseenter', () => {
    isHovered = true;
    stopCycle();
  });

  wrap.addEventListener('mouseleave', () => {
    isHovered = false;
    startCycle();
  });

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      stopCycle();
    } else {
      startCycle();
    }
  });

  motion.addEventListener('change', () => {
    if (!animate()) {
      stopCycle();
    } else {
      startCycle();
    }
  });

  // Start rotation
  startCycle();
}

// --- NAVIGATION & SCROLL PROGRESS ---
const navLinks = $$('[data-section]');
const sections = $$('main section[id]');
let framePending = false;

function requestScrollUpdate() {
  if (!framePending) {
    framePending = true;
    requestAnimationFrame(updateScroll);
  }
}

function updateScroll() {
  const y = window.scrollY;
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  const progress = $('.scroll-progress');
  if (progress) {
    progress.style.transform = `scaleX(${scrollable > 0 ? y / scrollable : 0})`;
  }

  let current = 'home';
  for (const section of sections) {
    if (section.offsetTop <= y + window.innerHeight * 0.35) {
      current = section.id;
    }
  }

  const mobileMap = { inspiration: 'collection', 'maternity-jewellery': 'collection', services: 'collection', story: 'collection' };
  navLinks.forEach(link => {
    const target = link.closest('.mobile-nav') ? (mobileMap[current] || current) : current;
    const active = link.dataset.section === target;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });

  framePending = false;
}

window.addEventListener('scroll', requestScrollUpdate, { passive: true });
window.addEventListener('resize', requestScrollUpdate);

// --- INTERSECTION OBSERVER FOR POWER OPTIMIZATION ---
if ('IntersectionObserver' in window) {
  const videoObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.play().catch(() => {});
      } else {
        entry.target.pause();
      }
    });
  }, { threshold: 0.15 });

  if (heroVideo) videoObserver.observe(heroVideo);
  storyVideos.forEach(video => videoObserver.observe(video));
}

document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    if (heroVideo) heroVideo.pause();
    storyVideos.forEach(v => v.pause());
  } else {
    if (heroVideo) heroVideo.play().catch(() => {});
    storyVideos.forEach(v => v.play().catch(() => {}));
  }
});


// Initialize
renderCollection();
initHeroHeadlineTicker();
requestScrollUpdate();

const initialActiveBtn = $('.fluid-filter-pill.active') || $('.island-btn.active') || $('.neo-btn.active') || $('.filter-pill.active');
if (initialActiveBtn) {
  if (filterContainer) filterContainer.dataset.activeFilter = initialActiveBtn.dataset.filter || 'all';
  centerActiveButton(initialActiveBtn);
}
window.addEventListener('resize', () => {
  const currentBtn = $('.fluid-filter-pill.active') || $('.island-btn.active') || $('.neo-btn.active') || $('.filter-pill.active');
  if (currentBtn) centerActiveButton(currentBtn);
});

// Quick filter click from fluid tags ribbon & values ribbon
$$('.fluid-tag-pill[data-filter-trigger], .fluid-val-pill[data-filter-trigger]').forEach(tag => {
  tag.addEventListener('click', () => {
    const filter = tag.dataset.filterTrigger;
    if (filter) {
      const targetBtn = $(`.fluid-filter-pill[data-filter="${filter}"]`) || $(`.island-btn[data-filter="${filter}"]`) || $(`.neo-btn[data-filter="${filter}"]`) || $(`.filter-pill[data-filter="${filter}"]`);
      if (targetBtn) {
        targetBtn.click();
      }
    }
  });
});

const yearEl = $('#year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// --- LIVING TYPOGRAPHY HERO AUTO-ANIMATION & SYNCHRONIZED BACKDROP ---
function initLivingTypography() {
  const stage = $('.living-typography-stage');
  if (!stage) return;

  const slots = $$('.living-word-slot', stage);
  const slides = $$('.living-bg-slide');
  if (!slots.length) return;

  const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (isReducedMotion) {
    slots.forEach(slot => slot.classList.remove('active'));
    return;
  }

  const SERVICES = ['bouquets', 'garlands', 'wedding', 'decor', 'gifts'];
  let currentIndex = 0;
  let timerId = null;
  let isPaused = false;

  const STAND_DURATION = 1800; // 1.8s per service
  const RESET_PAUSE = 700;     // ~700ms intentional pause when all sit down

  function setService(index) {
    // If index is -1: all five words become equal and sit down
    if (index === -1) {
      slots.forEach(slot => {
        slot.classList.remove('active');
        slot.setAttribute('aria-current', 'false');
      });
      // Gently dim backdrops during reset
      slides.forEach(slide => slide.classList.remove('active'));
      return;
    }

    const serviceId = SERVICES[index];
    slots.forEach((slot, idx) => {
      const isActive = (idx === index);
      slot.classList.toggle('active', isActive);
      slot.setAttribute('aria-current', isActive ? 'true' : 'false');
    });

    slides.forEach(slide => {
      const match = (slide.dataset.service === serviceId);
      slide.classList.toggle('active', match);
    });
  }

  function nextStep() {
    if (isPaused) return;

    if (currentIndex < SERVICES.length - 1) {
      currentIndex++;
      setService(currentIndex);
      timerId = setTimeout(nextStep, STAND_DURATION);
    } else {
      // Step: after Gifts sits down, have all five words briefly become equal, pause for ~700ms
      setService(-1);
      timerId = setTimeout(() => {
        if (!isPaused) {
          currentIndex = 0;
          setService(currentIndex); // Bouquets starts again!
          timerId = setTimeout(nextStep, STAND_DURATION);
        }
      }, RESET_PAUSE);
    }
  }

  // Interactive Hover / Tap exploration
  slots.forEach((slot, idx) => {
    slot.addEventListener('mouseenter', () => {
      isPaused = true;
      clearTimeout(timerId);
      currentIndex = idx;
      setService(idx);
    });

    slot.addEventListener('mouseleave', () => {
      isPaused = false;
      clearTimeout(timerId);
      timerId = setTimeout(nextStep, STAND_DURATION);
    });

    slot.addEventListener('click', () => {
      const filter = slot.dataset.filter;
      if (filter) {
        const targetBtn = $(`.fluid-filter-pill[data-filter="${filter}"]`) || $(`.island-btn[data-filter="${filter}"]`) || $(`.neo-btn[data-filter="${filter}"]`) || $(`.filter-pill[data-filter="${filter}"]`);
        if (targetBtn) targetBtn.click();
      }
    });
  });

  // Power optimization on visibility change
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      isPaused = true;
      clearTimeout(timerId);
    } else {
      isPaused = false;
      clearTimeout(timerId);
      timerId = setTimeout(nextStep, 1000);
    }
  });

  // Initial Start: Bouquets stands up
  setService(0);
  timerId = setTimeout(nextStep, STAND_DURATION);
}

// Start Living Typography
initLivingTypography();

// --- ELASTIC SECTION BOUNDARIES PHYSICS ENGINE ---
// dividing edges subtly bend/stretch before settling organically on scroll
function initElasticBoundaries() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const boundaries = [
    {
      id: 'col-to-films',
      fillEl: document.querySelector('.boundary-collection-to-films .elastic-boundary-fill'),
      edgeEl: document.querySelector('.boundary-collection-to-films .elastic-boundary-edge'),
      container: document.querySelector('.boundary-collection-to-films'),
      base: { x0: 0, y0: 75, cp1x: 440, cp1y: 135, cp2x: 1000, cp2y: 15, x1: 1440, y1: 70 },
      factors: { cp1: 1.35, cp2: -0.9, y0: 0.2, y1: -0.2 },
      currentStretch: 0,
      targetStretch: 0,
      velocity: 0,
      stiffness: 0.1,
      damping: 0.76
    },
    {
      id: 'films-to-inspire',
      fillEl: document.querySelector('.boundary-films-to-inspiration .elastic-boundary-fill'),
      edgeEl: document.querySelector('.boundary-films-to-inspiration .elastic-boundary-edge'),
      container: document.querySelector('.boundary-films-to-inspiration'),
      base: { x0: 0, y0: 65, cp1x: 480, cp1y: 15, cp2x: 960, cp2y: 130, x1: 1440, y1: 60 },
      factors: { cp1: -0.95, cp2: 1.25, y0: -0.2, y1: 0.2 },
      currentStretch: 0,
      targetStretch: 0,
      velocity: 0,
      stiffness: 0.1,
      damping: 0.76
    },
    {
      id: 'inspire-to-services',
      fillEl: document.querySelector('.boundary-inspiration-to-services .elastic-boundary-fill'),
      edgeEl: document.querySelector('.boundary-inspiration-to-services .elastic-boundary-edge'),
      container: document.querySelector('.boundary-inspiration-to-services'),
      base: { x0: 0, y0: 70, cp1x: 400, cp1y: 120, cp2x: 1040, cp2y: 25, x1: 1440, y1: 65 },
      factors: { cp1: 1.1, cp2: -0.85, y0: 0.15, y1: -0.15 },
      currentStretch: 0,
      targetStretch: 0,
      velocity: 0,
      stiffness: 0.11,
      damping: 0.78
    },
    {
      id: 'services-to-story',
      fillEl: document.querySelector('.boundary-services-to-story .elastic-boundary-fill'),
      edgeEl: document.querySelector('.boundary-services-to-story .elastic-boundary-edge'),
      container: document.querySelector('.boundary-services-to-story'),
      base: { x0: 0, y0: 60, cp1x: 500, cp1y: 20, cp2x: 940, cp2y: 120, x1: 1440, y1: 70 },
      factors: { cp1: -0.85, cp2: 1.1, y0: -0.15, y1: 0.15 },
      currentStretch: 0,
      targetStretch: 0,
      velocity: 0,
      stiffness: 0.11,
      damping: 0.78
    },
    {
      id: 'contact-to-footer',
      fillEl: document.querySelector('.boundary-contact-to-footer .elastic-boundary-fill'),
      edgeEl: document.querySelector('.boundary-contact-to-footer .elastic-boundary-edge'),
      container: document.querySelector('.boundary-contact-to-footer'),
      base: { x0: 0, y0: 70, cp1x: 450, cp1y: 125, cp2x: 990, cp2y: 30, x1: 1440, y1: 65 },
      factors: { cp1: 1.1, cp2: -0.85, y0: 0.15, y1: -0.15 },
      currentStretch: 0,
      targetStretch: 0,
      velocity: 0,
      stiffness: 0.11,
      damping: 0.78
    }
  ].filter(b => b.fillEl && b.edgeEl && b.container);

  if (!boundaries.length) return;

  function renderBoundary(b) {
    const s = b.currentStretch;
    const y0 = Math.round((b.base.y0 + s * b.factors.y0) * 10) / 10;
    const cp1y = Math.round((b.base.cp1y + s * b.factors.cp1) * 10) / 10;
    const cp2y = Math.round((b.base.cp2y + s * b.factors.cp2) * 10) / 10;
    const y1 = Math.round((b.base.y1 + s * b.factors.y1) * 10) / 10;

    const curve = `M ${b.base.x0},${y0} C ${b.base.cp1x},${cp1y} ${b.base.cp2x},${cp2y} ${b.base.x1},${y1}`;
    const fillPath = `${curve} L 1440,140 L 0,140 Z`;

    b.edgeEl.setAttribute('d', curve);
    b.fillEl.setAttribute('d', fillPath);
  }

  // Initial render of all natural resting curves
  boundaries.forEach(renderBoundary);

  let lastScrollY = window.scrollY;
  let lastTime = performance.now();
  let isSpringActive = false;

  function springStep() {
    let hasMotion = false;
    const vh = window.innerHeight;

    for (let i = 0; i < boundaries.length; i++) {
      const b = boundaries[i];
      
      const rect = b.container.getBoundingClientRect();
      const inViewport = rect.top < vh + 100 && rect.bottom > -100;

      // Spring physics: force = displacement * stiffness
      const force = (b.targetStretch - b.currentStretch) * b.stiffness;
      b.velocity = (b.velocity + force) * b.damping;
      b.currentStretch += b.velocity;

      // Organic relaxation of target towards equilibrium
      b.targetStretch *= 0.88;
      if (Math.abs(b.targetStretch) < 0.01) b.targetStretch = 0;

      if (inViewport) {
        renderBoundary(b);
      }

      if (Math.abs(b.velocity) > 0.008 || Math.abs(b.currentStretch - b.targetStretch) > 0.01) {
        hasMotion = true;
      }
    }

    if (hasMotion) {
      requestAnimationFrame(springStep);
    } else {
      isSpringActive = false;
      boundaries.forEach(b => {
        b.currentStretch = 0;
        b.velocity = 0;
        renderBoundary(b);
      });
    }
  }

  function onScroll() {
    const now = performance.now();
    const dt = Math.max(8, now - lastTime);
    const scrollY = window.scrollY;
    const delta = scrollY - lastScrollY;
    lastScrollY = scrollY;
    lastTime = now;

    // Normalize impulse by time delta
    const speed = delta / (dt / 16.67);
    const impulse = Math.max(-34, Math.min(34, speed * 1.6));

    for (let i = 0; i < boundaries.length; i++) {
      const b = boundaries[i];
      b.targetStretch += impulse;
      b.targetStretch = Math.max(-44, Math.min(44, b.targetStretch));
    }

    if (!isSpringActive) {
      isSpringActive = true;
      requestAnimationFrame(springStep);
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
}

// Start Elastic Section Boundaries
initElasticBoundaries();




// Fluid bridges live in the gallery gutters, behind the photo cards.
(() => {
  const gallery = $('.portfolio');
  if (!gallery) return;
  const ns = 'http://www.w3.org/2000/svg';
  const layer = document.createElementNS(ns, 'svg');
  layer.classList.add('gallery-fluid-connections');
  layer.setAttribute('aria-hidden', 'true');
  layer.setAttribute('focusable', 'false');
  gallery.append(layer);
  let pending = false;
  function schedule() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(draw);
  }
  function draw() {
    pending = false;
    const origin = gallery.getBoundingClientRect();
    if (!origin.width || !origin.height) return;
    layer.setAttribute('viewBox', `0 0 ${origin.width} ${origin.height}`);
    layer.setAttribute('width', origin.width);
    layer.setAttribute('height', origin.height);
    layer.replaceChildren();
    const defs = document.createElementNS(ns, 'defs');
    defs.innerHTML = '<linearGradient id="gallery-fluid-tint" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffefa"/><stop offset=".5" stop-color="#e5f1e7"/><stop offset="1" stop-color="#fffefa"/></linearGradient>';
    layer.append(defs);
    const visible = cards.filter(card => !card.hidden).map(card => {
      const r = card.getBoundingClientRect();
      const photo = $('.photo-button', card).getBoundingClientRect();
      return { left: r.left - origin.left, right: r.right - origin.left,
        top: r.top - origin.top, bottom: r.bottom - origin.top,
        photoTop: photo.top - origin.top, photoBottom: photo.bottom - origin.top };
    });
    const columns = [];
    visible.forEach(rect => {
      let column = columns.find(c => Math.abs(c[0].left - rect.left) < 3);
      if (!column) columns.push(column = []);
      column.push(rect);
    });
    columns.sort((a, b) => a[0].left - b[0].left);
    columns.forEach(column => column.sort((a, b) => a.top - b.top));
    function bridge(x, y, length, vertical = false) {
      if (length < 1 || length > 50) return;
      const half = Math.min(23, origin.width * .05);
      const path = document.createElementNS(ns, 'path');
      path.setAttribute('d', `M -1 ${-half} C ${length*.3} ${-half} ${length*.28} -5 ${length/2} -5 C ${length*.72} -5 ${length*.7} ${-half} ${length+1} ${-half} L ${length+1} ${half} C ${length*.7} ${half} ${length*.72} 5 ${length/2} 5 C ${length*.28} 5 ${length*.3} ${half} -1 ${half} Z`);
      path.setAttribute('transform', `translate(${x} ${y})${vertical ? ' rotate(90)' : ''}`);
      path.setAttribute('fill', 'url(#gallery-fluid-tint)');
      path.setAttribute('stroke', '#fffefa');
      path.setAttribute('stroke-width', '1');
      layer.append(path);
    }
    if (columns.length === 1) {
      columns[0].forEach((rect, i, column) => {
        if (i) bridge((rect.left + rect.right)/2, column[i-1].bottom, rect.top-column[i-1].bottom, true);
      });
    } else {
      columns.slice(0, -1).forEach((column, i) => {
        const used = new Set();
        column.forEach(left => {
          const candidates = columns[i+1].map(right => ({ right,
            top: Math.max(left.photoTop, right.photoTop) + 28,
            bottom: Math.min(left.photoBottom, right.photoBottom) - 28
          })).filter(c => c.bottom > c.top && !used.has(c.right));
          candidates.sort((a, b) => (b.bottom-b.top)-(a.bottom-a.top));
          const match = candidates[0];
          if (match) {
            used.add(match.right);
            bridge(left.right, (match.top+match.bottom)/2, match.right.left-left.right);
          }
        });
      });
    }
  }
  const observer = new ResizeObserver(schedule);
  observer.observe(gallery);
  cards.forEach(card => observer.observe(card));
  new MutationObserver(schedule).observe(gallery, { subtree: true, attributes: true, attributeFilter: ['hidden'] });
  gallery.addEventListener('load', schedule, true);
  gallery.addEventListener('animationend', schedule);
  gallery.addEventListener('transitionend', schedule);
  window.addEventListener('resize', schedule);
  schedule();
})();

// Premium editorial carousel: light, touch-friendly morphing deck.
(() => {
  const root = document.querySelector('.premium-carousel');
  if (!root) return;
  const slides = [...root.querySelectorAll('[data-premium-slide]')];
  const dots = [...root.querySelectorAll('[data-premium-dot]')];
  const prev = root.querySelector('[data-premium-prev]');
  const next = root.querySelector('[data-premium-next]');
  if (!slides.length) return;
  let current = 0;
  let timer;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const render = index => {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => slide.classList.toggle('is-active', i === current));
    dots.forEach((dot, i) => {
      const active = i === current;
      dot.classList.toggle('is-active', active);
      dot.setAttribute('aria-selected', String(active));
    });
  };
  const stop = () => { if (timer) window.clearInterval(timer); timer = undefined; };
  const start = () => { stop(); if (!reduceMotion.matches) timer = window.setInterval(() => render(current + 1), 5200); };
  prev?.addEventListener('click', () => { render(current - 1); start(); });
  next?.addEventListener('click', () => { render(current + 1); start(); });
  dots.forEach(dot => dot.addEventListener('click', () => { render(Number(dot.dataset.premiumDot)); start(); }));
  root.addEventListener('mouseenter', stop);
  root.addEventListener('mouseleave', start);
  root.addEventListener('focusin', stop);
  root.addEventListener('focusout', start);
  root.addEventListener('touchstart', stop, { passive: true });
  root.addEventListener('touchend', start, { passive: true });
  reduceMotion.addEventListener?.('change', start);
  render(0);
  start();
})();

// ==========================================================================
// MATERNITY & CEREMONIAL KAMAR PATTA CONTINUOUS MORPHING CAROUSEL
// Continuous 60fps liquid progress, touch drag gestures, and lightbox link.
// ==========================================================================
(() => {
  const root = document.querySelector('[data-maternity-carousel]');
  if (!root) return;

  const slides = [...root.querySelectorAll('[data-maternity-slide]')];
  const dots = [...root.querySelectorAll('[data-maternity-dot]')];
  const prevBtn = root.querySelector('[data-maternity-prev]');
  const nextBtn = root.querySelector('[data-maternity-next]');
  const progressFill = root.querySelector('[data-maternity-progress]');
  const track = root.querySelector('[data-maternity-track]');
  if (!slides.length) return;

  let current = 0;
  let isPaused = false;
  const duration = 5400; // ms per slide
  let startTime = null;
  let pausedElapsed = 0;
  let animFrameId = null;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  const render = (index) => {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      const active = i === current;
      slide.classList.toggle('is-active', active);
      slide.setAttribute('aria-hidden', String(!active));
      if (active) {
        slide.removeAttribute('inert');
      } else {
        slide.setAttribute('inert', '');
      }
    });

    dots.forEach((dot, i) => {
      const active = i === current;
      dot.classList.toggle('is-active', active);
      dot.setAttribute('aria-selected', String(active));
    });

    resetTimer();
  };

  function tick(timestamp) {
    if (reduceMotion.matches) return;
    if (!startTime) startTime = timestamp;

    if (!isPaused) {
      const elapsed = timestamp - startTime + pausedElapsed;
      const pct = Math.min(100, (elapsed / duration) * 100);
      if (progressFill) progressFill.style.width = pct + '%';

      if (elapsed >= duration) {
        startTime = null;
        pausedElapsed = 0;
        render(current + 1);
      }
    }
    animFrameId = requestAnimationFrame(tick);
  }

  function resetTimer() {
    startTime = null;
    pausedElapsed = 0;
    if (progressFill) progressFill.style.width = '0%';
  }

  function pause() {
    if (isPaused) return;
    isPaused = true;
    if (startTime) {
      pausedElapsed += performance.now() - startTime;
      startTime = performance.now();
    }
  }

  function resume() {
    if (!isPaused) return;
    isPaused = false;
    startTime = performance.now();
  }

  prevBtn?.addEventListener('click', () => { render(current - 1); });
  nextBtn?.addEventListener('click', () => { render(current + 1); });

  dots.forEach(dot => {
    dot.addEventListener('click', () => {
      render(Number(dot.dataset.maternityDot));
    });
  });

  // Smartphone touch drag & swipe handling
  let touchStartX = 0;
  let touchStartY = 0;
  let touchDeltaX = 0;
  let isSwiping = false;

  track?.addEventListener('touchstart', e => {
    if (e.touches.length !== 1) return;
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
    touchDeltaX = 0;
    isSwiping = true;
    pause();
  }, { passive: true });

  track?.addEventListener('touchmove', e => {
    if (!isSwiping || e.touches.length !== 1) return;
    const currentX = e.touches[0].clientX;
    const currentY = e.touches[0].clientY;
    touchDeltaX = currentX - touchStartX;
    const deltaY = currentY - touchStartY;

    // Detect horizontal swipe intent
    if (Math.abs(touchDeltaX) > Math.abs(deltaY) && Math.abs(touchDeltaX) > 8) {
      const dragPx = Math.max(-48, Math.min(48, touchDeltaX * 0.28));
      track.style.setProperty('--maternity-drag-x', dragPx + 'px');
    }
  }, { passive: true });

  const finishTouch = () => {
    if (!isSwiping) return;
    isSwiping = false;
    track.style.setProperty('--maternity-drag-x', '0px');
    if (touchDeltaX < -38) {
      render(current + 1);
    } else if (touchDeltaX > 38) {
      render(current - 1);
    }
    setTimeout(resume, 1200);
  };

  track?.addEventListener('touchend', finishTouch, { passive: true });
  track?.addEventListener('touchcancel', finishTouch, { passive: true });

  // Hover & Focus controls
  root.addEventListener('mouseenter', pause);
  root.addEventListener('mouseleave', resume);
  root.addEventListener('focusin', pause);
  root.addEventListener('focusout', resume);

  // Keyboard navigation
  track?.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      render(current - 1);
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      render(current + 1);
    }
  });

  render(0);
  if (!reduceMotion.matches) {
    animFrameId = requestAnimationFrame(tick);
  }

  reduceMotion.addEventListener?.('change', () => {
    if (reduceMotion.matches) {
      if (animFrameId) cancelAnimationFrame(animFrameId);
      if (progressFill) progressFill.style.width = '0%';
    } else {
      resetTimer();
      animFrameId = requestAnimationFrame(tick);
    }
  });
})();
