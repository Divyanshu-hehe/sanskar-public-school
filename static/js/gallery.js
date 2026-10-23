/**
 * SANSKAR PUBLIC SCHOOL — Gallery Lightbox & Filtering Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  const galleryItems = document.querySelectorAll('.gallery-card');
  let currentIndex = 0;
  const images = [];

  // Populate images list
  galleryItems.forEach((card, index) => {
    const img = card.querySelector('img');
    const title = card.querySelector('.gallery-card-title')?.innerText || '';
    const caption = card.querySelector('.gallery-card-caption')?.innerText || '';

    if (img) {
      images.push({
        src: img.src,
        title: title,
        caption: caption
      });

      card.addEventListener('click', () => {
        openLightbox(index);
      });
    }
  });

  // Lightbox Elements
  function openLightbox(index) {
    currentIndex = index;
    let lightbox = document.getElementById('gallery-lightbox-modal');
    if (!lightbox) {
      lightbox = document.createElement('div');
      lightbox.id = 'gallery-lightbox-modal';
      lightbox.className = 'lightbox-overlay';
      lightbox.innerHTML = `
        <div class="lightbox-content">
          <button class="lightbox-btn lightbox-close" id="lightbox-close">&times;</button>
          <button class="lightbox-btn lightbox-prev" id="lightbox-prev">&#10094;</button>
          <button class="lightbox-btn lightbox-next" id="lightbox-next">&#10095;</button>
          <div class="lightbox-image-wrap">
            <img src="" id="lightbox-img" alt="Gallery Photo">
          </div>
          <div class="lightbox-caption-wrap">
            <h4 id="lightbox-title"></h4>
            <p id="lightbox-caption"></p>
            <span id="lightbox-counter" class="lightbox-counter"></span>
          </div>
        </div>
      `;
      document.body.appendChild(lightbox);

      // Event Listeners
      lightbox.querySelector('#lightbox-close').addEventListener('click', closeLightbox);
      lightbox.querySelector('#lightbox-prev').addEventListener('click', prevImage);
      lightbox.querySelector('#lightbox-next').addEventListener('click', nextImage);
      
      lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) closeLightbox();
      });

      document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('active')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') prevImage();
        if (e.key === 'ArrowRight') nextImage();
      });
    }

    updateLightbox();
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function updateLightbox() {
    if (images.length === 0) return;
    const current = images[currentIndex];
    const imgEl = document.getElementById('lightbox-img');
    const titleEl = document.getElementById('lightbox-title');
    const captionEl = document.getElementById('lightbox-caption');
    const counterEl = document.getElementById('lightbox-counter');

    if (imgEl) imgEl.src = current.src;
    if (titleEl) titleEl.innerText = current.title;
    if (captionEl) captionEl.innerText = current.caption;
    if (counterEl) counterEl.innerText = `${currentIndex + 1} of ${images.length}`;
  }

  function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateLightbox();
  }

  function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    updateLightbox();
  }

  function closeLightbox() {
    const lightbox = document.getElementById('gallery-lightbox-modal');
    if (lightbox) {
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
    }
  }
});
