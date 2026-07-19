/* ────────────────────────────────────────────
   MERIDIAN BLOG — app.js
──────────────────────────────────────────── */

/* ── NAVBAR SCROLL BEHAVIOR ── */
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  }, { passive: true });
}


/* ── HAMBURGER MENU ── */
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');

if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('mobile-open');
    const open = navLinks.classList.contains('mobile-open');
    hamburger.setAttribute('aria-expanded', open);
  });
}

document.addEventListener('click', (e) => {
  if (navbar && navLinks && !navbar.contains(e.target)) {
    navLinks.classList.remove('mobile-open');
  }
});


/* ── SEARCH OVERLAY ── */
const searchBtn     = document.getElementById('searchBtn');
const searchOverlay = document.getElementById('searchOverlay');
const searchClose   = document.getElementById('searchClose');
const searchInput   = document.getElementById('searchInput');

function openSearch() {
  if (!searchOverlay || !searchInput) return;
  searchOverlay.classList.add('open');
  setTimeout(() => searchInput.focus(), 50);
}
function closeSearch() {
  if (!searchOverlay || !searchInput) return;
  searchOverlay.classList.remove('open');
  searchInput.value = '';
}

if (searchBtn) searchBtn.addEventListener('click', openSearch);
if (searchClose) searchClose.addEventListener('click', closeSearch);

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && searchOverlay && searchOverlay.classList.contains('open')) closeSearch();
  if ((e.metaKey || e.ctrlKey) && e.key === 'k' && searchOverlay) { e.preventDefault(); openSearch(); }
});


/* ── CATEGORY FILTER ── */
const filterBtns = document.querySelectorAll('.filter-btn');
const articles   = document.querySelectorAll('.article-card[data-cat]');

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const filter = btn.dataset.filter;
    articles.forEach(card => {
      if (filter === 'all' || card.dataset.cat === filter) {
        card.style.display = '';
        card.style.animation = 'fadeIn 0.25s ease';
      } else {
        card.style.display = 'none';
      }
    });
  });
});


/* ── SORT ── */
const sortSelect  = document.getElementById('sortSelect');
const articleFeed = document.getElementById('articleFeed');

const articleData = [
  { el: 0, views: 14200, minutes: 9,  date: new Date('2026-06-20') },
  { el: 1, views: 9800,  minutes: 11, date: new Date('2026-06-18') },
  { el: 2, views: 7100,  minutes: 7,  date: new Date('2026-06-15') },
  { el: 3, views: 18500, minutes: 13, date: new Date('2026-06-12') },
  { el: 4, views: 11300, minutes: 8,  date: new Date('2026-06-10') },
  { el: 5, views: 6900,  minutes: 10, date: new Date('2026-06-08') },
];

if (sortSelect && articleFeed) {
  sortSelect.addEventListener('change', () => {
    const cards = Array.from(articleFeed.querySelectorAll('.article-card[data-cat]'));
    const loadBtn = articleFeed.querySelector('.load-more-wrap');

    const sorted = [...articleData].sort((a, b) => {
      if (sortSelect.value === 'popular') return b.views - a.views;
      if (sortSelect.value === 'long')    return b.minutes - a.minutes;
      return b.date - a.date;
    });

    sorted.forEach(d => {
      if (!cards[d.el]) return;
      articleFeed.insertBefore(cards[d.el], loadBtn);
    });
  });
}


/* ── NEWSLETTER FORM ── */
function handleSubscribe(e) {
  e.preventDefault();
  const input = e.target.querySelector('input');
  const email = input.value.trim();
  if (!email) return;
  input.value = '';
  showToast('✓ You\'re subscribed! Check your inbox.');
}

window.handleSubscribe = handleSubscribe;


/* ── TOAST ── */
let toastTimer;
function showToast(msg) {
  let toast = document.querySelector('.toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span class="toast-dot"></span><span class="toast-msg"></span>`;
    document.body.appendChild(toast);
  }
  toast.querySelector('.toast-msg').textContent = msg;
  clearTimeout(toastTimer);
  toast.classList.add('show');
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3500);
}


/* ── LOAD MORE (simulated) ── */
const loadMoreBtn = document.getElementById('loadMore');
const moreArticles = [
  { cat: 'technology', title: 'The API Economy Is Eating Software', author: 'David Park', date: 'June 6', mins: 7, views: '5.2k' },
  { cat: 'culture',    title: 'What Vinyl Records Tell Us About Nostalgia', author: 'Cleo Martin', date: 'June 4', mins: 5, views: '4.8k' },
  { cat: 'science',    title: 'CRISPR Enters Its Second Act', author: 'Dr. Ana Reyes', date: 'June 2', mins: 12, views: '8.1k' },
];
let loaded = false;

if (loadMoreBtn && articleFeed) {
  loadMoreBtn.addEventListener('click', () => {
    if (loaded) return;
    loaded = true;
    loadMoreBtn.textContent = 'Loading…';
    loadMoreBtn.disabled = true;

    setTimeout(() => {
      const wrap = loadMoreBtn.closest('.load-more-wrap');
      moreArticles.forEach(data => {
        const article = document.createElement('article');
        article.className = 'article-card';
        article.dataset.cat = data.cat;
        article.style.animation = 'fadeIn 0.35s ease both';
        article.innerHTML = `
          <a href="#" class="card-img-wrap">
            <div class="card-img ${data.cat}-img"><div class="img-abstract img-a1"></div></div>
            <span class="card-badge" style="text-transform:capitalize">${data.cat}</span>
          </a>
          <div class="card-content">
            <h2 class="card-title"><a href="#">${data.title}</a></h2>
            <p class="card-excerpt">A thoughtful exploration of ideas that challenge the way we understand our world, written with clarity and depth.</p>
            <div class="card-footer">
              <div class="card-author">
                <div class="avatar sm av3">${data.author.split(' ').map(n=>n[0]).join('')}</div>
                <span>${data.author}</span>
              </div>
              <div class="card-stats">
                <span class="stat">${data.date}</span>
                <span class="stat-sep">·</span>
                <span class="stat">${data.mins} min</span>
                <span class="stat-sep">·</span>
                <span class="stat views">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  ${data.views}
                </span>
              </div>
            </div>
          </div>`;
        articleFeed.insertBefore(article, wrap);
      });
      if (wrap) wrap.remove();
    }, 600);
  });
}


/* ── HERO ABSTRACT ART ── */
(function drawHeroArt() {
  const el = document.getElementById('heroArt');
  if (!el) return;

  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'width:100%;height:100%;display:block;';
  el.appendChild(canvas);

  function resize() {
    const rect = el.getBoundingClientRect();
    canvas.width  = rect.width  || 420;
    canvas.height = rect.height || 315;
    draw();
  }

  function draw() {
    const W = canvas.width, H = canvas.height;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = '#0d0e18';
    ctx.fillRect(0, 0, W, H);

    // Grid lines
    ctx.strokeStyle = 'rgba(60,70,120,0.18)';
    ctx.lineWidth = 0.5;
    const grid = 32;
    for (let x = 0; x <= W; x += grid) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
    }
    for (let y = 0; y <= H; y += grid) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }

    // Glow orbs
    const orbs = [
      { x: 0.3, y: 0.35, r: 0.28, c1: 'rgba(50,80,200,0.25)', c2: 'transparent' },
      { x: 0.72, y: 0.6,  r: 0.22, c1: 'rgba(180,120,30,0.18)', c2: 'transparent' },
      { x: 0.5,  y: 0.8,  r: 0.18, c1: 'rgba(30,60,160,0.15)', c2: 'transparent' },
    ];
    orbs.forEach(o => {
      const grd = ctx.createRadialGradient(o.x*W, o.y*H, 0, o.x*W, o.y*H, o.r*W);
      grd.addColorStop(0, o.c1);
      grd.addColorStop(1, o.c2);
      ctx.fillStyle = grd;
      ctx.fillRect(0, 0, W, H);
    });

    // Floating dots
    ctx.fillStyle = 'rgba(212, 168, 83, 0.55)';
    const dots = [[0.18,0.22],[0.55,0.14],[0.82,0.32],[0.1,0.7],[0.7,0.75],[0.42,0.88],[0.9,0.6]];
    dots.forEach(([x,y]) => {
      ctx.beginPath();
      ctx.arc(x*W, y*H, 2, 0, Math.PI*2);
      ctx.fill();
    });

    // Connecting lines
    ctx.strokeStyle = 'rgba(212,168,83,0.12)';
    ctx.lineWidth = 0.8;
    const lineNodes = dots.map(([x,y]) => [x*W, y*H]);
    const connections = [[0,1],[1,2],[2,5],[0,3],[3,6],[4,5],[1,4],[2,6]];
    connections.forEach(([a,b]) => {
      ctx.beginPath();
      ctx.moveTo(lineNodes[a][0], lineNodes[a][1]);
      ctx.lineTo(lineNodes[b][0], lineNodes[b][1]);
      ctx.stroke();
    });

    // Central geometric shape
    ctx.strokeStyle = 'rgba(212,168,83,0.2)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    const cx = W * 0.5, cy = H * 0.45, R = Math.min(W,H) * 0.18;
    for (let i = 0; i < 6; i++) {
      const angle = (Math.PI / 3) * i - Math.PI / 6;
      const x = cx + R * Math.cos(angle);
      const y = cy + R * Math.sin(angle);
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.stroke();

    // Inner hexagon
    ctx.strokeStyle = 'rgba(212,168,83,0.1)';
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
      const angle = (Math.PI / 3) * i - Math.PI / 6;
      const x = cx + (R * 0.55) * Math.cos(angle);
      const y = cy + (R * 0.55) * Math.sin(angle);
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.stroke();

    // Radial lines from center
    ctx.strokeStyle = 'rgba(212,168,83,0.07)';
    for (let i = 0; i < 12; i++) {
      const angle = (Math.PI / 6) * i;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + R * 1.6 * Math.cos(angle), cy + R * 1.6 * Math.sin(angle));
      ctx.stroke();
    }

    // Text label overlay
    ctx.font = '500 10px JetBrains Mono, monospace';
    ctx.fillStyle = 'rgba(212,168,83,0.4)';
    ctx.fillText('FEATURED / 2026', W * 0.06, H * 0.92);
    ctx.fillStyle = 'rgba(255,255,255,0.08)';
    ctx.fillText('VOL.12', W * 0.82, H * 0.07);
  }

  const ro = new ResizeObserver(resize);
  ro.observe(el);
  resize();
})();


/* ── FADE-IN ANIMATION (CSS injection) ── */
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .article-card { animation: fadeIn 0.3s ease both; }
`;
document.head.appendChild(style);


/* ── INTERSECTION OBSERVER for scroll reveals ── */
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.pick-card, .sidebar-widget').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(16px)';
  el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
  observer.observe(el);
});
