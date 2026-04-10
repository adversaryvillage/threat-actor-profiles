// Adversary Threat Actor Encyclopedia - Frontend Logic

document.addEventListener('DOMContentLoaded', () => {
  // ---- SEARCH ----
  const searchInput = document.getElementById('actor-search');
  const cards = document.querySelectorAll('.actor-card');

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();
      cards.forEach(card => {
        const searchable = card.dataset.search || '';
        card.style.display = searchable.includes(query) ? '' : 'none';
      });
    });
  }

  // ---- FILTER PILLS ----
  const pills = document.querySelectorAll('.filter-pill');
  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      const isActive = pill.classList.contains('active');

      // If clicking "All", deactivate everything and show all
      if (pill.dataset.filter === 'all') {
        pills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        cards.forEach(card => card.style.display = '');
        return;
      }

      // Deactivate "All" pill
      pills.forEach(p => {
        if (p.dataset.filter === 'all') p.classList.remove('active');
      });

      if (isActive) {
        pill.classList.remove('active');
      } else {
        // Single select: deactivate others first
        pills.forEach(p => {
          if (p.dataset.filter !== 'all') p.classList.remove('active');
        });
        pill.classList.add('active');
      }

      // Check if any pill is active
      const activePills = document.querySelectorAll('.filter-pill.active');
      if (activePills.length === 0 || (activePills.length === 1 && activePills[0].dataset.filter === 'all')) {
        // No filter active, or "All" active, show all
        document.querySelector('.filter-pill[data-filter="all"]').classList.add('active');
        cards.forEach(card => card.style.display = '');
        return;
      }

      // Get active filter value
      const activeFilter = document.querySelector('.filter-pill.active:not([data-filter="all"])');
      if (!activeFilter) return;

      const filterType = activeFilter.dataset.filterType;
      const filterValue = activeFilter.dataset.filter.toLowerCase();

      cards.forEach(card => {
        let match = false;
        if (filterType === 'country') {
          match = (card.dataset.country || '').toLowerCase() === filterValue;
        } else if (filterType === 'type') {
          match = (card.dataset.type || '').toLowerCase().includes(filterValue);
        }
        card.style.display = match ? '' : 'none';
      });
    });
  });

  // ---- MATRIX TECHNIQUE TOOLTIPS ----
  const techniques = document.querySelectorAll('.matrix-technique');
  techniques.forEach(tech => {
    tech.addEventListener('mouseenter', () => {
      tech.style.position = 'relative';
    });
  });

  // ---- SMOOTH SCROLL for anchor links ----
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});
