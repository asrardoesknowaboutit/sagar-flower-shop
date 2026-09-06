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

const storyVideos = $$('.story-video');

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
    status.textContent = `Showing ${count} of ${matches.length} designs · डिझाईन्स`;
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
    const active = item.dataset.filter === currentFilter;
    item.classList.toggle('active', active);
    if (item.tagName === 'BUTTON') item.setAttribute('aria-pressed', String(active));
  });
  centerActiveButton($(`.fluid-filter-pill[data-filter="${currentFilter}"]`));
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

// Native video controls allow play, pause and sound without autoplay on mobile.
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => { if (!entry.isIntersecting) entry.target.pause(); });
  }, { threshold: 0.15 });
  storyVideos.forEach(video => observer.observe(video));
}
document.addEventListener('visibilitychange', () => {
  if (document.hidden) storyVideos.forEach(video => video.pause());
});

// Initialize
renderCollection();
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

