'use strict';
const filters = [...document.querySelectorAll('[data-filter]')];
const cards = [...document.querySelectorAll('.work-card')];
const status = document.querySelector('#filter-status');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
filters.forEach(button => button.addEventListener('click', () => {
  filters.forEach(filter => {
    const active = filter === button;
    filter.classList.toggle('active', active);
    filter.setAttribute('aria-pressed', String(active));
  });
  let visible = 0;
  cards.forEach(card => {
    card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter;
    if (!card.hidden) visible++;
  });
  status.textContent = `Showing ${visible} ${button.dataset.filter === 'all' ? 'floral' : button.textContent.trim()} designs`;
  if (!reducedMotion) document.querySelector('.portfolio').animate([{opacity: .4, transform:'translateY(8px)'},{opacity:1,transform:'translateY(0)'}],{duration:250,easing:'ease-out'});
}));
const dialog = document.querySelector('#lightbox');
let activePhoto = null;
let lastTrigger = null;
const visiblePhotos = () => cards.filter(card => !card.hidden).map(card => card.querySelector('.photo-button'));
function showPhoto(button) {
  activePhoto = button;
  const photo = document.querySelector('#lightbox-photo');
  photo.src = button.dataset.image;
  photo.alt = button.dataset.title;
  document.querySelector('#lightbox-title').textContent = button.dataset.title;
  document.querySelector('#lightbox-inquire').href = 'https://wa.me/917620644158?text=' + encodeURIComponent(`Hello Sagar Flower Shop, I would like to enquire about ${button.dataset.title}.`);
  const photos = visiblePhotos();
  document.querySelector('#lightbox-count').textContent = `${photos.indexOf(button) + 1} / ${photos.length} · SAGAR FLOWER SHOP`;
}
function nextPhoto(direction) {
  const photos = visiblePhotos();
  showPhoto(photos[(photos.indexOf(activePhoto) + direction + photos.length) % photos.length]);
}
document.querySelectorAll('.photo-button').forEach(button => button.addEventListener('click', () => {
  lastTrigger = button;
  showPhoto(button);
  dialog.showModal();
  document.body.classList.add('modal-open');
}));
document.querySelector('.lightbox-close').addEventListener('click', () => dialog.close());
document.querySelector('.lightbox-next').addEventListener('click', () => nextPhoto(1));
document.querySelector('.lightbox-prev').addEventListener('click', () => nextPhoto(-1));
dialog.addEventListener('click', event => {
  const rect = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
});
dialog.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  lastTrigger?.focus({preventScroll:true});
});
dialog.addEventListener('keydown', event => {
  if (event.key === 'ArrowRight') { event.preventDefault(); nextPhoto(1); }
  if (event.key === 'ArrowLeft') { event.preventDefault(); nextPhoto(-1); }
});
let touchStart = null;
document.querySelector('#lightbox-photo').addEventListener('touchstart', e => { touchStart = e.changedTouches[0].clientX; }, {passive:true});
document.querySelector('#lightbox-photo').addEventListener('touchend', e => {
  if (touchStart === null) return;
  const difference = e.changedTouches[0].clientX - touchStart;
  if (Math.abs(difference) > 55) nextPhoto(difference < 0 ? 1 : -1);
  touchStart = null;
}, {passive:true});
const navLinks = [...document.querySelectorAll('[data-section]')];
const sections = [...document.querySelectorAll('main section[id]')];
let framePending = false;
function updateScroll() {
  const y = window.scrollY;
  const scrollable = document.documentElement.scrollHeight - innerHeight;
  document.querySelector('.scroll-progress').style.transform = `scaleX(${scrollable > 0 ? y / scrollable : 0})`;
  let current = 'home';
  for (const section of sections) if (section.offsetTop <= y + innerHeight * .35) current = section.id;
  for (const link of navLinks) {
    const active = link.dataset.section === current || (current === 'story' && link.closest('.mobile-nav') && link.dataset.section === 'services');
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
  }
  framePending = false;
}
window.addEventListener('scroll', () => {
  if (!framePending) { framePending = true; requestAnimationFrame(updateScroll); }
}, {passive:true});
window.addEventListener('resize', updateScroll);
updateScroll();
if ('IntersectionObserver' in window && !reducedMotion) {
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.remove('pending'); observer.unobserve(entry.target); }
  }), {threshold:.08});
  document.querySelectorAll('.reveal').forEach(element => { element.classList.add('pending'); observer.observe(element); });
}
document.querySelector('#year').textContent = new Date().getFullYear();
