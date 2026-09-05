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

  if (soundBtn) {
    soundBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const willMute = !video.muted;
      if (!willMute) {
        storyVideos.forEach(v => {
          if (v !== video) {
            v.muted = true;
            const otherBtn = v.closest('.film-card')?.querySelector('.story-sound-toggle .sound-icon');
            if (otherBtn) otherBtn.textContent = '🔇';
          }
        });
        if (heroVideo) {
          heroVideo.muted = true;
          if (heroSoundBtn) heroSoundBtn.querySelector('.sound-icon').textContent = '🔇';
        }
      }
      video.muted = willMute;
      soundBtn.querySelector('.sound-icon').textContent = willMute ? '🔇' : '🔊';
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

// --- PORTFOLIO FILTERING & NEUMORPHIC FLUID GLIDER ---
const cards = $$('.work-card');
const filterButtons = $$('[data-filter]');
const filterBar = $('.neo-filter-track') || $('.filter-pill-bar');
const filterGlider = $('.neo-glider') || $('.filter-glider');
const filterContainer = $('.neo-filter-container') || $('.filter-flow-wrapper');
const batchSize = () => window.innerWidth >= 900 ? 12 : 8;
let currentFilter = 'all', limit = batchSize();

function syncPrevActive() {
  const activeIdx = filterButtons.findIndex(btn => btn.classList.contains('active'));
  filterButtons.forEach((btn, idx) => {
    btn.classList.toggle('prev-active', idx === activeIdx - 1);
  });
}

function updateGlider(activeBtn, immediate = false) {
  if (!filterBar || !filterGlider || !activeBtn) return;
  const barRect = filterBar.getBoundingClientRect();
  const btnRect = activeBtn.getBoundingClientRect();
  const left = btnRect.left - barRect.left;
  const width = btnRect.width;

  if (immediate || !animate()) {
    filterGlider.style.transition = 'none';
  } else {
    filterGlider.style.transition = 'transform 0.42s cubic-bezier(0.34, 1.25, 0.64, 1), width 0.36s cubic-bezier(0.34, 1.15, 0.64, 1)';
  }

  filterGlider.style.transform = `translateX(${left}px)`;
  filterGlider.style.width = `${width}px`;

  // Center the active button smoothly on mobile
  if (filterContainer && filterContainer.scrollWidth > filterContainer.clientWidth) {
    const containerRect = filterContainer.getBoundingClientRect();
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
    showMore.hidden = count >= matches.length;
    showMore.innerHTML = `अधिक डिझाईन्स पहा <span>↓</span><small> (${matches.length - count} आणखी)</small>`;
  }
  requestScrollUpdate();
}

filterButtons.forEach(button => button.addEventListener('click', () => {
  currentFilter = button.dataset.filter;
  limit = batchSize();
  filterButtons.forEach(item => {
    const active = item === button;
    item.classList.toggle('active', active);
    item.setAttribute('aria-pressed', String(active));
  });
  syncPrevActive();
  updateGlider(button);
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
  const firstNew = matches[limit];
  limit += batchSize();
  renderCollection();
  if (firstNew) {
    const photo = $('.photo-button', firstNew);
    photo?.focus({ preventScroll: true });
    firstNew.scrollIntoView({ behavior: smooth(), block: 'start' });
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
requestScrollUpdate();

const initialActiveBtn = $('.neo-btn.active') || $('.filter-pill.active');
if (initialActiveBtn) {
  syncPrevActive();
  requestAnimationFrame(() => updateGlider(initialActiveBtn, true));
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(() => updateGlider(initialActiveBtn, true));
  }
}
window.addEventListener('resize', () => {
  const currentBtn = $('.neo-btn.active') || $('.filter-pill.active');
  if (currentBtn) updateGlider(currentBtn, true);
});

const yearEl = $('#year');
if (yearEl) yearEl.textContent = new Date().getFullYear();
