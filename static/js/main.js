// ========== NAVBAR SCROLL EFFECT ==========
window.addEventListener('scroll', function() {
    const nav = document.getElementById('mainNav');
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 50);
});

// ========== AUTO DISMISS ALERTS ==========
setTimeout(function() {
    document.querySelectorAll('.alert').forEach(function(alert) {
        alert.style.transition = 'opacity 0.5s';
        alert.style.opacity = '0';
        setTimeout(function() { alert.remove(); }, 500);
    });
}, 3000);

// ========== LIVE SEARCH ==========
const searchInput = document.getElementById('searchInput');
const searchDropdown = document.getElementById('searchDropdown');
if (searchInput) {
    let timeout = null;
    searchInput.addEventListener('input', function() {
        clearTimeout(timeout);
        const q = this.value.trim();
        if (q.length < 2) { searchDropdown.style.display = 'none'; return; }
        timeout = setTimeout(function() {
            fetch('/search/suggestions/?q=' + encodeURIComponent(q))
                .then(r => r.json())
                .then(data => {
                    if (!data.results.length) { searchDropdown.style.display = 'none'; return; }
                    searchDropdown.innerHTML = data.results.map(m =>
                        '<a href="/movie/' + m.id + '/" class="search-suggestion-item">' +
                        '<i class="fas fa-' + (m.type === 'series' ? 'tv' : 'film') + ' text-success"></i>' +
                        '<span>' + m.title + '</span>' +
                        '<small class="ms-auto" style="color:#6a6a6a;">' + m.year + '</small></a>'
                    ).join('');
                    searchDropdown.style.display = 'block';
                });
        }, 300);
    });
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target))
            searchDropdown.style.display = 'none';
    });
}

// ========== HERO SLIDESHOW ==========
(function() {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot');
    const prevBtn = document.getElementById('heroPrev');
    const nextBtn = document.getElementById('heroNext');
    if (!slides.length) return;

    let current = 0;
    let autoPlay = null;

    function goTo(index) {
        slides[current].classList.remove('active');
        dots[current] && dots[current].classList.remove('active');
        current = (index + slides.length) % slides.length;
        slides[current].classList.add('active');
        dots[current] && dots[current].classList.add('active');
    }

    function startAuto() {
        autoPlay = setInterval(function() { goTo(current + 1); }, 6000);
    }

    function stopAuto() {
        clearInterval(autoPlay);
    }

    if (prevBtn) prevBtn.addEventListener('click', function() { stopAuto(); goTo(current - 1); startAuto(); });
    if (nextBtn) nextBtn.addEventListener('click', function() { stopAuto(); goTo(current + 1); startAuto(); });

    dots.forEach(function(dot, i) {
        dot.addEventListener('click', function() { stopAuto(); goTo(i); startAuto(); });
    });

    // Swipe support
    let touchStartX = 0;
    const slideshow = document.getElementById('heroSlideshow');
    if (slideshow) {
        slideshow.addEventListener('touchstart', function(e) { touchStartX = e.touches[0].clientX; });
        slideshow.addEventListener('touchend', function(e) {
            const diff = touchStartX - e.changedTouches[0].clientX;
            if (Math.abs(diff) > 50) { stopAuto(); goTo(current + (diff > 0 ? 1 : -1)); startAuto(); }
        });
    }

    startAuto();
})();

// ========== SECTION SLIDE-IN ANIMATIONS ==========
const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.content-section').forEach(function(section, i) {
    section.style.opacity = '0';
    section.style.transform = 'translateY(35px)';
    section.style.transition = 'opacity 0.6s ease ' + (i * 0.08) + 's, transform 0.6s ease ' + (i * 0.08) + 's';
    observer.observe(section);
});

// ========== STAGGERED CARD ANIMATION ==========
window.addEventListener('load', function() {
    document.querySelectorAll('.cards-scroll .poster-card, .cards-scroll .top10-card').forEach(function(card, i) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.4s ease ' + ((i % 12) * 0.05) + 's, transform 0.4s ease ' + ((i % 12) * 0.05) + 's';
        setTimeout(function() {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 200 + (i % 12) * 50);
    });
});

// ========== SMOOTH HORIZONTAL SCROLL ==========
document.querySelectorAll('.cards-scroll').forEach(function(scroll) {
    scroll.addEventListener('wheel', function(e) {
        if (e.deltaY !== 0) { e.preventDefault(); scroll.scrollLeft += e.deltaY * 2.5; }
    }, { passive: false });
});
