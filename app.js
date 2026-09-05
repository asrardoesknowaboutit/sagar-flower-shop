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

  // Sync depth of field for unhidden cards
  if (typeof focalObserver !== 'undefined' && focalObserver) {
    const vh = window.innerHeight;
    cards.forEach(card => {
      if (!card.hidden && !card.classList.contains('focal-settled')) {
        card.classList.add('cinematic-dof');
        const rect = card.getBoundingClientRect();
        if (rect.top < vh * 0.92 && rect.bottom > 0) {
          card.classList.add('focal-in', 'focal-settled');
        } else {
          focalObserver.observe(card);
        }
      }
    });
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

// --- MARATHI TICKER TOGGLE ---
let tickerPaused = false;
const tickerToggle = $('#ticker-toggle');
function syncTicker() {
  const track = $('.ticker-track');
  if (track) track.classList.toggle('stopped', tickerPaused || document.hidden || !animate());
  if (tickerToggle) {
    tickerToggle.textContent = tickerPaused || !animate() ? '▶' : 'Ⅱ';
    tickerToggle.setAttribute('aria-label', tickerPaused || !animate() ? 'Play welcome ticker' : 'Pause welcome ticker');
    tickerToggle.setAttribute('aria-pressed', String(tickerPaused || !animate()));
  }
}
tickerToggle?.addEventListener('click', () => {
  tickerPaused = !tickerPaused;
  syncTicker();
});

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

  const mobileMap = { inspiration: 'collection', services: 'collection', story: 'collection' };
  navLinks.forEach(link => {
    const target = link.closest('.mobile-nav') ? (mobileMap[current] || current) : current;
    const active = link.dataset.section === target;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });

  // Cinematic hero optical recession on scroll
  const heroShowcase = $('.hero-video-showcase');
  if (heroShowcase) {
    if (y > 90) {
      heroShowcase.classList.add('hero-receding');
    } else {
      heroShowcase.classList.remove('hero-receding');
    }
  }

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
  syncTicker();
});

motion.addEventListener('change', syncTicker);

// Initialize
renderCollection();
syncTicker();
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

// --- CINEMATIC SCROLL-DRIVEN DEPTH OF FIELD & PROGRESSIVE FOCUS REVEAL ---
let focalObserver = null;

function initCinematicDepthOfField() {
  const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const targets = $$('.section-heading, .work-card, .film-card, .inspiration-card, .service-grid article, .process-card, .review-card, .values-strip');

  if (isReducedMotion) {
    targets.forEach(el => el.classList.add('cinematic-dof', 'focal-in', 'focal-settled'));
    return;
  }

  if ('IntersectionObserver' in window) {
    focalObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const el = entry.target;
        if (entry.isIntersecting) {
          el.classList.add('focal-in');
          // Free GPU filter cache after optical transition finishes
          setTimeout(() => {
            if (el.classList.contains('focal-in')) {
              el.classList.add('focal-settled');
            }
          }, 460);
        }
      });
    }, {
      rootMargin: '0px 0px -5% 0px',
      threshold: [0, 0.12]
    });
  }

  const vh = window.innerHeight;
  targets.forEach(el => {
    el.classList.add('cinematic-dof');
    const rect = el.getBoundingClientRect();
    // Pre-focus visible above-the-fold content immediately (0 latency, 0 loading)
    if (rect.top < vh * 0.92 && rect.bottom > 0) {
      el.classList.add('focal-in', 'focal-settled');
    } else if (focalObserver) {
      focalObserver.observe(el);
    }
  });

  // Reel Rail Horizontal Focus Tracking
  initRailFocusTracking();
}

function initRailFocusTracking() {
  const rail = $('.film-rail');
  if (!rail) return;
  const cards = $$('.film-card', rail);
  if (!cards.length) return;

  let railPending = false;
  function updateRailFocus() {
    railPending = false;
    const railRect = rail.getBoundingClientRect();
    const railCenter = railRect.left + railRect.width / 2;

    let closestCard = null;
    let minDistance = Infinity;

    cards.forEach(card => {
      const cardRect = card.getBoundingClientRect();
      const cardCenter = cardRect.left + cardRect.width / 2;
      const dist = Math.abs(railCenter - cardCenter);
      if (dist < minDistance) {
        minDistance = dist;
        closestCard = card;
      }
    });

    cards.forEach(card => {
      const isFocused = card === closestCard;
      card.classList.toggle('rail-in-focus', isFocused);
      card.classList.toggle('rail-out-of-focus', !isFocused);
    });
  }

  rail.addEventListener('scroll', () => {
    if (!railPending) {
      railPending = true;
      requestAnimationFrame(updateRailFocus);
    }
  }, { passive: true });

  updateRailFocus();
}

// Start Depth of Field Controller
initCinematicDepthOfField();

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



