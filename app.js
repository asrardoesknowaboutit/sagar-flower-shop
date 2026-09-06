'use strict';

// --------------------------------------------------------------------------
// DOM Helpers & State
// --------------------------------------------------------------------------
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const smooth = () => motion.matches ? 'auto' : 'smooth';

const whatsapp = (title, marathi = '') => {
  const item = marathi ? `${marathi} (${title})` : title;
  return 'https://wa.me/917620644158?text=' + encodeURIComponent(`नमस्कार! मला ${item} याबद्दल माहिती हवी आहे. / Hello, I would like to order ${item}.`);
};

// --------------------------------------------------------------------------
// HERO & STORY VIDEOS (Lazy, Performance-Optimized Autoplay)
// --------------------------------------------------------------------------
const heroVideo = $('#hero-delivery-video');
const heroSoundBtn = $('#hero-sound-toggle');
const storyVideos = $$('.story-video');

if (heroVideo && heroSoundBtn) {
  heroSoundBtn.addEventListener('click', () => {
    heroVideo.muted = !heroVideo.muted;
    heroSoundBtn.querySelector('.sound-icon').textContent = heroVideo.muted ? '🔇' : '🔊';
    heroSoundBtn.setAttribute('aria-label', heroVideo.muted ? 'Unmute hero video' : 'Mute hero video');
  });
}

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
        // Mute all other videos when one is unmuted
        storyVideos.forEach(v => {
          if (v !== video) {
            v.muted = true;
            const otherBtn = v.closest('.film-card')?.querySelector('.story-sound-toggle .sound-icon');
            if (otherBtn) otherBtn.textContent = '🔇';
          }
        });
        if (heroVideo) {
          heroVideo.muted = true;
          const heroIcon = heroSoundBtn?.querySelector('.sound-icon');
          if (heroIcon) heroIcon.textContent = '🔇';
        }
      }
      video.muted = willMute;
      const icon = soundBtn.querySelector('.sound-icon');
      if (icon) icon.textContent = willMute ? '🔇' : '🔊';
    });
  }

  video.addEventListener('click', () => {
    soundBtn?.click();
  });
});

// Single IntersectionObserver for zero-lag video playback
if ('IntersectionObserver' in window) {
  const videoObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const video = entry.target;
      if (entry.isIntersecting) {
        video.play().catch(() => {});
      } else {
        video.pause();
      }
    });
  }, { threshold: 0.35 });

  if (heroVideo) videoObserver.observe(heroVideo);
  storyVideos.forEach(v => videoObserver.observe(v));
}

// Pause videos on background tab to save battery and memory
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    if (heroVideo) heroVideo.pause();
    storyVideos.forEach(v => v.pause());
  } else {
    // Re-check visible videos
    if (heroVideo && isElementInViewport(heroVideo)) heroVideo.play().catch(() => {});
    storyVideos.forEach(v => {
      if (isElementInViewport(v)) v.play().catch(() => {});
    });
  }
});

function isElementInViewport(el) {
  const rect = el.getBoundingClientRect();
  return (
    rect.top < window.innerHeight &&
    rect.bottom > 0
  );
}

// --------------------------------------------------------------------------
// PORTFOLIO FILTERING & PAGINATION
// --------------------------------------------------------------------------
const cards = $$('.work-card');
const filterButtons = $$('.filter-pill');
const filterContainer = $('.filter-ribbon-wrap');
const batchSize = () => window.innerWidth >= 768 ? 12 : 8;
let currentFilter = 'all';
let limit = batchSize();

function getMatchingCards() {
  return cards.filter(card => currentFilter === 'all' || card.dataset.category === currentFilter);
}

function centerActiveFilterButton(btn) {
  if (!filterContainer || !btn) return;
  const cRect = filterContainer.getBoundingClientRect();
  const bRect = btn.getBoundingClientRect();
  const scrollTarget = filterContainer.scrollLeft + (bRect.left - cRect.left) - (filterContainer.clientWidth / 2) + (bRect.width / 2);
  filterContainer.scrollTo({ left: Math.max(0, scrollTarget), behavior: smooth() });
}

function renderCollection() {
  const matches = getMatchingCards();
  cards.forEach(card => {
    const index = matches.indexOf(card);
    card.hidden = index === -1 || index >= limit;
  });

  const count = Math.min(limit, matches.length);
  const status = $('#filter-status');
  if (status) {
    status.textContent = `दाखवत आहोत: ${count} / ${matches.length} डिझाईन्स`;
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
}

filterButtons.forEach(button => {
  button.addEventListener('click', () => {
    currentFilter = button.dataset.filter || 'all';
    limit = batchSize();
    filterButtons.forEach(btn => {
      const active = btn === button;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-pressed', String(active));
    });
    centerActiveFilterButton(button);
    renderCollection();
  });
});

// Quick trigger from trust chips or hero tags
$$('[data-filter-trigger]').forEach(el => {
  el.addEventListener('click', (e) => {
    const cat = el.dataset.filterTrigger;
    if (cat) {
      const targetBtn = $(`.filter-pill[data-filter="${cat}"]`);
      if (targetBtn) {
        targetBtn.click();
      }
    }
  });
});

// Show more button
$('#show-more')?.addEventListener('click', () => {
  const matches = getMatchingCards();
  const oldLimit = limit;
  const firstNew = matches[oldLimit];
  limit += batchSize();
  renderCollection();

  if (firstNew) {
    const photo = $('.photo-button', firstNew);
    photo?.focus({ preventScroll: true });
    firstNew.scrollIntoView({ behavior: smooth(), block: 'nearest' });
  }
});

// --------------------------------------------------------------------------
// LIGHTBOX MODAL (Touch-friendly, Full-Resolution, Fast)
// --------------------------------------------------------------------------
const dialog = $('#lightbox');
let activePhoto = null;
let lastTrigger = null;
let photoGroup = [];

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
}

function nextPhoto(direction) {
  if (!photoGroup.length) return;
  const currentIndex = photoGroup.indexOf(activePhoto);
  const nextIndex = (currentIndex + direction + photoGroup.length) % photoGroup.length;
  showPhoto(photoGroup[nextIndex]);
}

$$('.photo-button[data-image]').forEach(button => {
  button.addEventListener('click', () => {
    lastTrigger = button;
    photoGroup = button.dataset.group === 'collection'
      ? getMatchingCards().map(card => $('.photo-button', card)).filter(Boolean)
      : $$(`.photo-button[data-group="${button.dataset.group}"]`);
    showPhoto(button);
    dialog.showModal();
    document.body.classList.add('modal-open');
  });
});

$('.lightbox-close')?.addEventListener('click', () => dialog.close());
$('.lightbox-next')?.addEventListener('click', () => nextPhoto(1));
$('.lightbox-prev')?.addEventListener('click', () => nextPhoto(-1));

dialog?.addEventListener('click', (event) => {
  const r = dialog.getBoundingClientRect();
  if (
    event.target === dialog &&
    (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom)
  ) {
    dialog.close();
  }
});

dialog?.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  lastTrigger?.focus({ preventScroll: true });
});

dialog?.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
    event.preventDefault();
    nextPhoto(event.key === 'ArrowRight' ? 1 : -1);
  }
});

// Touch Swipe on Lightbox
(function initLightboxSwipe() {
  const target = $('#lightbox-photo');
  if (!target) return;
  let startX = 0, startY = 0;

  target.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1) {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
    }
  }, { passive: true });

  target.addEventListener('touchend', (e) => {
    if (!startX) return;
    const dx = e.changedTouches[0].clientX - startX;
    const dy = e.changedTouches[0].clientY - startY;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.3) {
      nextPhoto(dx < 0 ? 1 : -1);
    }
    startX = 0;
    startY = 0;
  }, { passive: true });
})();

// --------------------------------------------------------------------------
// SCROLL PROGRESS & ACTIVE DOCK NAVIGATION (Passive, zero-lag)
// --------------------------------------------------------------------------
const sections = $$('main section[id]');
const dockLinks = $$('.dock-item');
const navLinks = $$('.nav-pill');
const progressBar = $('.scroll-progress');
let scrollPending = false;

function onScroll() {
  if (!scrollPending) {
    scrollPending = true;
    requestAnimationFrame(updateScroll);
  }
}

function updateScroll() {
  scrollPending = false;
  const y = window.scrollY;
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;

  if (progressBar && scrollable > 0) {
    progressBar.style.transform = `scaleX(${y / scrollable})`;
  }

  // Active section detection
  let currentId = 'home';
  const triggerOffset = y + 140;
  for (let i = 0; i < sections.length; i++) {
    const sec = sections[i];
    if (sec.offsetTop <= triggerOffset) {
      currentId = sec.id;
    }
  }

  // Map sub-sections to primary navigation keys
  const mapSection = {
    inspiration: 'collection',
    services: 'collection',
    process: 'collection'
  };
  const activeId = mapSection[currentId] || currentId;

  dockLinks.forEach(link => {
    const isCurrent = link.dataset.section === activeId;
    link.classList.toggle('active', isCurrent);
  });

  navLinks.forEach(link => {
    const isCurrent = link.dataset.section === currentId;
    link.classList.toggle('active', isCurrent);
  });
}

window.addEventListener('scroll', onScroll, { passive: true });

// --------------------------------------------------------------------------
// INITIALIZE
// --------------------------------------------------------------------------
renderCollection();
updateScroll();

const yearEl = $('#year');
if (yearEl) yearEl.textContent = new Date().getFullYear();
