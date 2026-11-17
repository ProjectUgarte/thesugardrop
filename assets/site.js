(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.menu-toggle');
  var links = document.querySelector('.nav-links');

  if (toggle) toggle.addEventListener('click', function () {
    var open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
  });

  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- Gallery ---------- */
  var grid = document.getElementById('grid');
  if (grid) {
    var filterRow = document.getElementById('filters');
    var galleries = [], shown = [], lbIndex = 0;
    var lb = document.getElementById('lightbox');
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('figcaption');
    var lastFocus = null;

    var path = function (g, n, thumb) { return 'assets/img/' + g + '/' + (thumb ? 't/' : '') + n + '.webp'; };

    (function (data) {
      galleries = data.galleries;
      var total = galleries.reduce(function (s, g) { return s + g.count; }, 0);
      var chips = [{ slug: 'all', short: 'All', count: total }].concat(galleries);
      filterRow.innerHTML = chips.map(function (g) {
        return '<button class="filter" type="button" data-slug="' + g.slug + '" aria-pressed="false">' +
          g.short + '<small>' + g.count + '</small></button>';
      }).join('');
      filterRow.addEventListener('click', function (e) {
        var b = e.target.closest('.filter');
        if (b) select(b.dataset.slug, true);
      });
      var start = location.hash.slice(1);
      select(galleries.some(function (g) { return g.slug === start; }) ? start : 'all', false);
    })(window.GALLERY_DATA);

    function select(slug, push) {
      filterRow.querySelectorAll('.filter').forEach(function (b) {
        var on = b.dataset.slug === slug;
        b.setAttribute('aria-pressed', on);
        if (on && push) b.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
      });
      shown = [];
      var html = '';
      galleries.forEach(function (g) {
        if (slug !== 'all' && g.slug !== slug) return;
        if (slug === 'all') html += '<div class="gallery-group" style="grid-column:1/-1"><h2>' + g.title + '</h2></div>';
        g.items.forEach(function (it, i) {
          var idx = shown.length;
          shown.push({ g: g, it: it, i: i });
          html += '<button class="tile" type="button" data-i="' + idx + '" aria-label="Open ' + g.title + ' photo ' + (i + 1) + ' of ' + g.count + '">' +
            '<img src="' + path(g.slug, it.n, true) + '" width="600" height="750" loading="lazy" decoding="async" alt="' + g.title + ' by The Sugar Drop">' +
            '</button>';
        });
      });
      grid.innerHTML = html;
      if (push) {
        history.replaceState(null, '', slug === 'all' ? location.pathname : '#' + slug);
        var top = grid.getBoundingClientRect().top + scrollY - 170;
        if (scrollY > top) scrollTo({ top: top, behavior: 'smooth' });
      }
    }

    grid.addEventListener('click', function (e) {
      var t = e.target.closest('.tile');
      if (t) open(+t.dataset.i);
    });

    function show(i) {
      lbIndex = (i + shown.length) % shown.length;
      var s = shown[lbIndex];
      lbImg.src = path(s.g.slug, s.it.n);
      lbImg.width = s.it.w; lbImg.height = s.it.h;
      lbImg.alt = s.g.title + ' by The Sugar Drop';
      lbCap.textContent = s.g.title + '  ·  ' + (s.i + 1) + ' / ' + s.g.count;
      [1, -1].forEach(function (d) {
        var n = shown[(lbIndex + d + shown.length) % shown.length];
        new Image().src = path(n.g.slug, n.it.n);
      });
    }
    function open(i) {
      lastFocus = document.activeElement;
      show(i);
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
      lb.querySelector('.lb-close').focus();
    }
    function close() {
      lb.classList.remove('open');
      document.body.style.overflow = '';
      lbImg.removeAttribute('src');
      if (lastFocus) lastFocus.focus();
    }
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function () { show(lbIndex - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { show(lbIndex + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.tagName === 'FIGURE') close(); });
    addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight') show(lbIndex + 1);
      else if (e.key === 'ArrowLeft') show(lbIndex - 1);
      else if (e.key === 'Tab') {
        var f = lb.querySelectorAll('button'), first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    var x0 = null;
    lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 45) show(lbIndex + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  }

  /* ---------- Inquiry form ---------- */
  var form = document.getElementById('inquiry');
  if (form) {
    var status = document.getElementById('status'), btn = form.querySelector('button[type=submit]');
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (form.action.indexOf('YOUR_FORM_ID') > -1) {
        status.className = 'status err';
        status.textContent = 'This form isn’t connected yet — the Formspree endpoint still needs to be added.';
        return;
      }
      btn.disabled = true; btn.textContent = 'Sending…';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.reset();
          status.className = 'status ok';
          status.textContent = 'Thank you! Your inquiry is on its way — I’ll be in touch soon.';
        })
        .catch(function () {
          status.className = 'status err';
          status.textContent = 'Something went wrong sending your inquiry. Please try again in a moment.';
        })
        .finally(function () { btn.disabled = false; btn.textContent = 'Send inquiry'; });
    });
  }
})();
