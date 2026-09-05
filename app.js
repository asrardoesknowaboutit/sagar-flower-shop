'use strict';
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const connection = navigator.connection;
const saveData = Boolean(connection?.saveData || /(^|-)2g$/.test(connection?.effectiveType || ''));
const animate = () => !motion.matches && !saveData;
const smooth = () => animate() ? 'smooth' : 'auto';
const whatsapp = title => 'https://wa.me/917620644158?text=' + encodeURIComponent(`नमस्कार! मला ${title} याबद्दल माहिती हवी आहे. / Hello, I would like to enquire about ${title}.`);

// Render only a small first page. The complete collection is readable without JS.
const cards = $$('.work-card');
const filterButtons = $$('[data-filter]');
const batchSize = () => innerWidth >= 900 ? 9 : 8;
let filter = 'all', limit = batchSize();
const matchingCards = () => cards.filter(card => filter === 'all' || card.dataset.category === filter);
function renderCollection() {
  const matches = matchingCards();
  cards.forEach(card => { card.hidden = !matches.includes(card) || matches.indexOf(card) >= limit; });
  const count = Math.min(limit, matches.length);
  $('#filter-status').textContent = `Showing ${count} of ${matches.length} designs`;
  $('#show-more').hidden = count >= matches.length;
  $('#show-more').innerHTML = `Discover more designs <span>↓</span><small>${Math.max(0, matches.length - count)} more</small>`;
  requestScrollUpdate();
}
filterButtons.forEach(button => button.addEventListener('click', () => {
  filter = button.dataset.filter; limit = batchSize();
  filterButtons.forEach(item => {
    const active = item === button; item.classList.toggle('active', active); item.setAttribute('aria-pressed', String(active));
  });
  renderCollection();
  if (animate()) $('.portfolio').animate([{opacity:.5,transform:'translateY(6px)'},{opacity:1,transform:'none'}],{duration:220,easing:'ease-out'});
}));
$('#show-more').addEventListener('click', () => {
  const firstNew = matchingCards()[limit]; limit += batchSize(); renderCollection();
  const photo = $('.photo-button', firstNew);
  photo.focus({preventScroll:true}); firstNew.scrollIntoView({behavior:smooth(),block:'start'});
});

// Full-photo modal: native focus trap, Escape, arrow keys, touch swipe, and focus return.
const dialog = $('#lightbox');
let activePhoto, lastTrigger, photoGroup = [];
let imageVersion = 0;
function showPhoto(button) {
  activePhoto = button;
  const photo = $('#lightbox-photo');
  photo.src = button.dataset.image; photo.alt = button.dataset.title;
  $('#lightbox-title').textContent = button.dataset.title;
  $('#lightbox-inquire').href = whatsapp(button.dataset.title);
  $('#lightbox-count').textContent = `${photoGroup.indexOf(button) + 1} / ${photoGroup.length} · SAGAR FLOWER SHOP`;
  const version = ++imageVersion;
  photo.decode().catch(() => {}).then(() => {
    if (version === imageVersion && animate()) photo.animate([{opacity:.5},{opacity:1}],{duration:160});
  });
}
function nextPhoto(direction) {
  showPhoto(photoGroup[(photoGroup.indexOf(activePhoto) + direction + photoGroup.length) % photoGroup.length]);
}
$$('.photo-button[data-image]').forEach(button => button.addEventListener('click', () => {
  lastTrigger = button;
  photoGroup = button.dataset.group === 'collection'
    ? matchingCards().map(card => $('.photo-button', card))
    : $$(`.photo-button[data-group="${button.dataset.group}"]`);
  showPhoto(button); dialog.showModal(); document.body.classList.add('modal-open'); scheduleHero();
}));
$('.lightbox-close').addEventListener('click', () => dialog.close());
$('.lightbox-next').addEventListener('click', () => nextPhoto(1));
$('.lightbox-prev').addEventListener('click', () => nextPhoto(-1));
dialog.addEventListener('click', event => {
  const r = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom)) dialog.close();
});
dialog.addEventListener('close', () => { document.body.classList.remove('modal-open'); lastTrigger?.focus({preventScroll:true}); scheduleHero(); });
dialog.addEventListener('keydown', event => {
  if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') { event.preventDefault(); nextPhoto(event.key === 'ArrowRight' ? 1 : -1); }
});
function onSwipe(element, callback) {
  let start = null;
  element.addEventListener('touchstart', event => {
    start = event.touches.length === 1 ? {x:event.touches[0].clientX,y:event.touches[0].clientY} : null;
  },{passive:true});
  element.addEventListener('touchend', event => {
    if (!start) return;
    const dx = event.changedTouches[0].clientX - start.x, dy = event.changedTouches[0].clientY - start.y;
    if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.5) callback(dx < 0 ? 1 : -1);
    start = null;
  },{passive:true});
}
onSwipe($('#lightbox-photo'), nextPhoto);

// Only the active slide is downloaded at first; later slides hydrate on demand.
const hero = $('.hero-carousel'), slides = $$('.hero-slide'), dots = $$('[data-slide]');
let slideIndex = 0, heroTimer, heroVisible = false, heroPaused = false, heroHover = false, heroFocus = false, slideVersion = 0;
function scheduleHero() {
  clearTimeout(heroTimer);
  if (heroVisible && !heroPaused && !heroHover && !heroFocus && !document.hidden && !dialog.open && animate())
    heroTimer = setTimeout(() => changeSlide(slideIndex + 1), 6500);
}
async function changeSlide(index) {
  const next = (index + slides.length) % slides.length;
  const version = ++slideVersion;
  const img = $('img', slides[next]);
  if (img.dataset.src) {
    if (img.dataset.srcset) img.srcset = img.dataset.srcset;
    img.src = img.dataset.src; delete img.dataset.src; delete img.dataset.srcset;
  }
  try { await img.decode(); } catch { scheduleHero(); return; }
  if (version !== slideVersion) return;
  slideIndex = next;
  slides.forEach((slide, i) => {
    slide.classList.toggle('is-active', i === next); slide.inert = i !== next; slide.setAttribute('aria-hidden', String(i !== next));
    dots[i].classList.toggle('active', i === next); dots[i].setAttribute('aria-pressed', String(i === next));
  });
  $('#hero-caption').textContent = $('.photo-button', slides[next]).dataset.title;
  scheduleHero();
}
function manualSlide(index) { heroPaused = true; syncHeroPause(); changeSlide(index); }
function syncHeroPause() {
  $('#hero-pause').textContent = heroPaused || !animate() ? '▶' : 'Ⅱ';
  $('#hero-pause').setAttribute('aria-label', heroPaused || !animate() ? 'Play featured slideshow' : 'Pause featured slideshow');
  $('#hero-pause').setAttribute('aria-pressed', String(heroPaused || !animate())); scheduleHero();
}
$('.hero-prev').addEventListener('click', () => manualSlide(slideIndex - 1));
$('.hero-next').addEventListener('click', () => manualSlide(slideIndex + 1));
dots.forEach(dot => dot.addEventListener('click', () => manualSlide(Number(dot.dataset.slide))));
$('#hero-pause').addEventListener('click', () => { heroPaused = !heroPaused; syncHeroPause(); });
hero.addEventListener('mouseenter', () => { heroHover = true; scheduleHero(); });
hero.addEventListener('mouseleave', () => { heroHover = false; scheduleHero(); });
hero.addEventListener('focusin', () => { heroFocus = true; scheduleHero(); });
hero.addEventListener('focusout', event => { if (!hero.contains(event.relatedTarget)) { heroFocus = false; scheduleHero(); } });
onSwipe($('.hero-slides'), direction => manualSlide(slideIndex + direction));

// CSS-only ticker movement, with pause and reduced-motion support.
let tickerPaused = false, tickerVisible = true;
function syncTicker() {
  $('.ticker-track').classList.toggle('stopped', tickerPaused || !tickerVisible || document.hidden || !animate());
  $('#ticker-toggle').textContent = tickerPaused || !animate() ? '▶' : 'Ⅱ';
  $('#ticker-toggle').setAttribute('aria-label', tickerPaused || !animate() ? 'Play welcome ticker' : 'Pause welcome ticker');
  $('#ticker-toggle').setAttribute('aria-pressed', String(tickerPaused || !animate()));
}
$('#ticker-toggle').addEventListener('click', () => { tickerPaused = !tickerPaused; syncTicker(); });

// Videos never fetch media until the visitor presses play. Only one plays at a time.
const videos = $$('video');
videos.forEach(video => {
  const card = video.closest('.film-card'), play = $('.video-play',card);
  play.addEventListener('click', async () => {
    videos.forEach(other => { if (other !== video) other.pause(); });
    play.disabled = true; play.classList.add('loading');
    if (!video.src) video.src = video.dataset.src;
    video.controls = true;
    try { await video.play(); card.classList.add('playing'); }
    catch { $('.video-play small',card).textContent = 'TAP TO TRY AGAIN'; }
    finally { play.disabled = false; play.classList.remove('loading'); }
  });
  video.addEventListener('play', () => { videos.forEach(other => { if (other !== video) other.pause(); }); card.classList.add('playing'); });
  video.addEventListener('pause', () => card.classList.remove('playing'));
  video.addEventListener('ended', () => card.classList.remove('playing'));
});
const rail = $('.film-rail');
function scrollFilms(direction) { rail.scrollBy({left:direction * ($('.film-card',rail).offsetWidth + 20),behavior:smooth()}); }
$('.film-prev').addEventListener('click', () => scrollFilms(-1));
$('.film-next').addEventListener('click', () => scrollFilms(1));
rail.addEventListener('keydown', event => {
  if (event.target === rail && ['ArrowLeft','ArrowRight'].includes(event.key)) { event.preventDefault(); scrollFilms(event.key === 'ArrowRight' ? 1 : -1); }
});

// A single passive listener schedules at most one navigation update per frame.
const navLinks = $$('[data-section]'), sections = $$('main section[id]');
let framePending = false;
function requestScrollUpdate() { if (!framePending) { framePending = true; requestAnimationFrame(updateScroll); } }
function updateScroll() {
  const y = scrollY, scrollable = document.documentElement.scrollHeight - innerHeight;
  $('.scroll-progress').style.transform = `scaleX(${scrollable > 0 ? y / scrollable : 0})`;
  let current = 'home';
  for (const section of sections) if (section.offsetTop <= y + innerHeight * .35) current = section.id;
  const mobileMap = {inspiration:'films',services:'films',story:'films'};
  navLinks.forEach(link => {
    const target = link.closest('.mobile-nav') ? (mobileMap[current] || current) : current;
    const active = link.dataset.section === target; link.classList.toggle('active',active);
    if (active) link.setAttribute('aria-current','location'); else link.removeAttribute('aria-current');
  });
  framePending = false;
}
addEventListener('scroll', requestScrollUpdate, {passive:true});
addEventListener('resize', requestScrollUpdate);
if ('IntersectionObserver' in window) {
  new IntersectionObserver(entries => { heroVisible = entries[0].isIntersecting; scheduleHero(); },{threshold:.15}).observe(hero);
  new IntersectionObserver(entries => { tickerVisible = entries[0].isIntersecting; syncTicker(); }).observe($('.welcome-bar'));
  const videoObserver = new IntersectionObserver(entries => entries.forEach(entry => { if (!entry.isIntersecting) entry.target.pause(); }), {threshold:.1});
  videos.forEach(video => videoObserver.observe(video));
}
document.addEventListener('visibilitychange', () => { if (document.hidden) videos.forEach(v => v.pause()); scheduleHero(); syncTicker(); });
motion.addEventListener('change', () => { syncHeroPause(); syncTicker(); });
if (saveData) document.body.classList.add('save-data');
renderCollection(); syncHeroPause(); syncTicker(); requestScrollUpdate();
$('#year').textContent = new Date().getFullYear();
