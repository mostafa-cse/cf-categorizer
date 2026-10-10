/**
 * Codeforces Categorizer Web Application Frontend Logic
 */

// Global State
const state = {
  taxonomy: [],
  stats: null,
  catalog: null, // Full catalog for instant client-side filtering on GitHub Pages
  activeMainTopic: null,
  activeSubtopic: null,
  activeSubsubtopicId: null,
  activeSubsubtopicObj: null,
  filters: {
    importance: 'all',
    minRating: null,
    maxRating: null,
    status: 'all',
    searchQuery: '',
    sortBy: 'rating_asc',
    page: 1,
    pageSize: 30
  },
  problems: [],
  pagination: { total: 0, page: 1, totalPages: 1 },
  userProgress: { solved: new Set(), bookmarked: new Set(), notes: {} },
  activeProblem: null,
  activeModalTab: 'statement',
  expandedTopics: new Set()
};

// Ratings Helpers
function getRatingClass(rating) {
  if (!rating) return 'cf-rating-gray';
  if (rating < 1200) return 'cf-rating-gray';
  if (rating < 1400) return 'cf-rating-green';
  if (rating < 1600) return 'cf-rating-cyan';
  if (rating < 1900) return 'cf-rating-blue';
  if (rating < 2200) return 'cf-rating-purple';
  if (rating < 2400) return 'cf-rating-orange';
  if (rating < 3000) return 'cf-rating-red';
  return 'cf-rating-legendary';
}

function getRatingTitle(rating) {
  if (!rating) return 'Unrated';
  if (rating < 1200) return 'Newbie';
  if (rating < 1400) return 'Pupil';
  if (rating < 1600) return 'Specialist';
  if (rating < 1900) return 'Expert';
  if (rating < 2200) return 'Candidate Master';
  if (rating < 2400) return 'Master';
  if (rating < 2600) return 'International Master';
  if (rating < 3000) return 'Grandmaster';
  return 'Legendary Grandmaster';
}

function getStarBadgeHtml(star) {
  if (star === '***') {
    return `<span class="px-2 py-0.5 rounded text-xs font-semibold star-badge-3 inline-flex items-center gap-1" title="Top-tier Masterpiece problem">★★★ Masterpiece</span>`;
  } else if (star === '**') {
    return `<span class="px-2 py-0.5 rounded text-xs font-medium star-badge-2 inline-flex items-center gap-1" title="Core Technique essential problem">★★ Core</span>`;
  } else {
    return `<span class="px-2 py-0.5 rounded text-xs star-badge-1 inline-flex items-center gap-1" title="Practice problem">★ Practice</span>`;
  }
}

// Initializer
document.addEventListener('DOMContentLoaded', async () => {
  setupEventListeners();
  await loadUserProgress();
  await Promise.all([loadTaxonomy(), loadStats()]);
  await loadProblems();
});

// Setup UI Listeners
function setupEventListeners() {
  // Global search input with debounce
  const searchInput = document.getElementById('global-search');
  let searchTimeout;
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        state.filters.searchQuery = e.target.value.trim();
        state.filters.page = 1;
        loadProblems();
      }, 250);
    });
  }

  // Taxonomy search
  const treeSearch = document.getElementById('taxonomy-search');
  if (treeSearch) {
    treeSearch.addEventListener('input', (e) => {
      filterTaxonomyTree(e.target.value.toLowerCase().trim());
    });
  }

  // Keyboard shortcut '/' to search & Escape to close modal
  window.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput?.focus();
    }
    if (e.key === 'Escape') {
      closeProblemModal();
    }
  });

  // Modal close when clicking backdrop
  const modal = document.getElementById('problem-modal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeProblemModal();
    });
  }
}

// Load User Progress (localStorage + API sync)
async function loadUserProgress() {
  try {
    const local = localStorage.getItem('cf_user_progress');
    if (local) {
      const parsed = JSON.parse(local);
      state.userProgress.solved = new Set(parsed.solved || []);
      state.userProgress.bookmarked = new Set(parsed.bookmarked || []);
      state.userProgress.notes = parsed.notes || {};
    }
  } catch (e) {
    console.warn('localStorage progress read error:', e);
  }

  // Optional background sync with backend if running locally
  try {
    const res = await fetch('/api/user/progress');
    if (res.ok) {
      const data = await res.json();
      (data.solved || []).forEach(id => state.userProgress.solved.add(id));
      (data.bookmarked || []).forEach(id => state.userProgress.bookmarked.add(id));
      state.userProgress.notes = { ...state.userProgress.notes, ...(data.notes || {}) };
      persistUserProgress();
    }
  } catch (err) {
    // Expected on static GitHub Pages
  }
  updateHeaderCounters();
}

function persistUserProgress() {
  try {
    const payload = {
      solved: Array.from(state.userProgress.solved),
      bookmarked: Array.from(state.userProgress.bookmarked),
      notes: state.userProgress.notes
    };
    localStorage.setItem('cf_user_progress', JSON.stringify(payload));
  } catch (e) {
    console.warn('localStorage persist error:', e);
  }
}

// Load Stats (Static fallback to API)
async function loadStats() {
  try {
    let res = await fetch('./data/stats.json');
    if (!res.ok) res = await fetch('/api/stats');
    if (res.ok) {
      const data = await res.json();
      state.stats = data;
      renderTopStats(data);
    }
  } catch (err) {
    console.error('Failed to load stats:', err);
  }
}

function renderTopStats(stats) {
  const totalBadge = document.getElementById('header-total-problems-count');
  if (totalBadge && stats.curriculum_quality_count) {
    totalBadge.textContent = `${stats.curriculum_quality_count.toLocaleString()} Problems`;
  }

  const container = document.getElementById('top-stats-container');
  if (!container) return;

  const solvedCount = state.userProgress.solved.size;
  const pct = ((solvedCount / (stats.curriculum_quality_count || 1)) * 100).toFixed(1);

  container.innerHTML = `
    <div class="flex items-center gap-3 text-xs font-medium text-slate-300">
      <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800">
        <span class="text-amber-400 font-bold">${stats.curriculum_quality_count?.toLocaleString()}</span>
        <span class="text-slate-400">Curated Problems</span>
      </div>
      <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800">
        <span class="text-amber-300 font-bold">${stats.stars?.['***']?.toLocaleString()}</span>
        <span class="text-slate-400">Masterpieces</span>
      </div>
      <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800">
        <span class="text-emerald-400 font-bold">${solvedCount}</span>
        <span class="text-slate-400">Solved (${pct}%)</span>
      </div>
    </div>
  `;
}

function updateHeaderCounters() {
  const solvedBadge = document.getElementById('header-solved-count');
  if (solvedBadge) solvedBadge.textContent = state.userProgress.solved.size;

  const bookmarkedBadge = document.getElementById('header-bookmarked-count');
  if (bookmarkedBadge) bookmarkedBadge.textContent = state.userProgress.bookmarked.size;

  if (state.stats) {
    renderTopStats(state.stats);
  }
}

// Load Taxonomy Tree
async function loadTaxonomy() {
  try {
    let res = await fetch('./data/taxonomy.json');
    if (!res.ok) res = await fetch('/api/taxonomy');
    if (res.ok) {
      const data = await res.json();
      state.taxonomy = data;
      renderTaxonomyTree();
    }
  } catch (err) {
    console.error('Failed to load taxonomy:', err);
  }
}

function renderTaxonomyTree() {
  const container = document.getElementById('taxonomy-tree-container');
  if (!container) return;

  const topicIcons = {
    'Basics': '⚡',
    'Data Structures (DS)': '🌲',
    'Graph Theory': '🕸️',
    'Number Theory': '🔢',
    'Combinatorics': '🎲',
    'Math': '📐',
    'Strings': '🔤',
    'Dynamic Programming (DP)': '🧩',
    'Game Theory': '♟️',
    'Geometry': '📏',
    'Miscellaneous': '🛠️'
  };

  let html = `
    <div class="mb-2">
      <button onclick="selectAllTopics()" class="w-full text-left px-3 py-2 rounded-xl text-xs font-semibold flex items-center justify-between transition-colors ${!state.activeMainTopic ? 'bg-sky-500/15 text-sky-300 border border-sky-500/30 font-bold' : 'text-slate-300 hover:bg-slate-900/60 border border-transparent'}">
        <span class="flex items-center gap-2"><span>📚</span> All Topics</span>
        <span class="text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono border border-slate-700/60">${state.stats?.curriculum_quality_count?.toLocaleString() || '28,338'}</span>
      </button>
    </div>
  `;

  state.taxonomy.forEach((main) => {
    const isMainActive = state.activeMainTopic === main.name && !state.activeSubtopic && !state.activeSubsubtopicId;
    const isExpanded = state.expandedTopics.has(main.name);
    const icon = topicIcons[main.name] || '📌';

    html += `
      <div class="mb-1 rounded-xl overflow-hidden border border-slate-800/80 bg-slate-900/40" data-topic-name="${main.name.toLowerCase()}">
        <div class="flex items-center justify-between px-3 py-2 cursor-pointer select-none transition-colors ${isMainActive ? 'bg-sky-500/15 text-sky-300 font-bold' : 'hover:bg-slate-800/50 text-slate-200'}" onclick="toggleMainTopicAccordion('${main.name}')">
          <div class="flex items-center gap-2 text-xs font-semibold">
            <span>${icon}</span>
            <span class="truncate">${main.name}</span>
          </div>
          <div class="flex items-center gap-1.5 text-xs">
            <span class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-mono text-[10px]">${main.total_problems}</span>
            <span class="text-slate-500 text-[10px] transition-transform duration-200 ${isExpanded ? 'rotate-90' : ''}">▶</span>
          </div>
        </div>

        <div class="subtopics-list pl-2 pr-1.5 py-1 space-y-1 bg-slate-950/40 border-t border-slate-800/50 ${isExpanded ? 'block' : 'hidden'}">
          ${main.subtopics.map(sub => {
            const isSubActive = state.activeMainTopic === main.name && state.activeSubtopic === sub.name && !state.activeSubsubtopicId;
            return `
              <div class="subtopic-node" data-subtopic-name="${sub.name.toLowerCase()}">
                <div class="flex items-center justify-between py-1 px-2 rounded-lg text-xs cursor-pointer ${isSubActive ? 'bg-sky-500/15 text-sky-300 font-bold' : 'text-slate-300 hover:text-white hover:bg-slate-800/40'}" onclick="selectSubtopic('${main.name}', '${sub.name}')">
                  <span class="truncate font-medium">${sub.name}</span>
                  <span class="text-[10px] text-slate-500 font-mono">${sub.total_problems}</span>
                </div>
                <div class="subsub-list pl-2 pt-0.5 space-y-0.5">
                  ${sub.subsubtopics.filter(sst => sst.problem_count > 0).map(sst => {
                    const isSstActive = state.activeSubsubtopicId === sst.id;
                    return `
                      <div onclick="selectSubsubtopic('${main.name}', '${sub.name}', ${sst.id})" 
                           class="flex items-center justify-between py-1 px-2 rounded-lg text-[11px] cursor-pointer transition-colors ${isSstActive ? 'bg-sky-500/25 text-sky-200 border border-sky-500/40 font-bold' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/30'}"
                           data-sst-name="${sst.name.toLowerCase()}">
                        <span class="truncate" title="${sst.full_title}">${sst.name}</span>
                        <div class="flex items-center gap-1 text-[10px] shrink-0">
                          ${sst.masterpiece_count > 0 ? `<span class="text-amber-400 font-mono">${sst.masterpiece_count}★</span>` : ''}
                          <span class="text-slate-500 font-mono">${sst.problem_count}</span>
                        </div>
                      </div>
                    `;
                  }).join('')}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function toggleMainTopicAccordion(mainTopicName) {
  if (state.expandedTopics.has(mainTopicName)) {
    state.expandedTopics.delete(mainTopicName);
  } else {
    state.expandedTopics.add(mainTopicName);
  }
  selectMainTopic(mainTopicName);
}

function toggleExpandAllTree() {
  const btn = document.getElementById('tree-expand-toggle-btn');
  if (state.expandedTopics.size >= state.taxonomy.length) {
    state.expandedTopics.clear();
    if (btn) btn.textContent = 'Expand All';
  } else {
    state.taxonomy.forEach(m => state.expandedTopics.add(m.name));
    if (btn) btn.textContent = 'Collapse All';
  }
  renderTaxonomyTree();
}

function filterTaxonomyTree(query) {
  const nodes = document.querySelectorAll('#taxonomy-tree-container [data-topic-name]');
  nodes.forEach(node => {
    const text = node.textContent.toLowerCase();
    if (!query || text.includes(query)) {
      node.style.display = 'block';
      const sublist = node.querySelector('.subtopics-list');
      if (query && sublist) {
        sublist.classList.remove('hidden');
      }
    } else {
      node.style.display = 'none';
    }
  });
}

// Topic Selection Handlers
function selectAllTopics() {
  state.activeMainTopic = null;
  state.activeSubtopic = null;
  state.activeSubsubtopicId = null;
  state.activeSubsubtopicObj = null;
  state.filters.page = 1;
  renderTaxonomyTree();
  updateBreadcrumbs();
  loadProblems();
}

function selectMainTopic(mainTopicName) {
  state.activeMainTopic = mainTopicName;
  state.activeSubtopic = null;
  state.activeSubsubtopicId = null;
  state.activeSubsubtopicObj = null;
  state.filters.page = 1;
  renderTaxonomyTree();
  updateBreadcrumbs();
  loadProblems();
}

function selectSubtopic(mainTopicName, subtopicName) {
  state.activeMainTopic = mainTopicName;
  state.activeSubtopic = subtopicName;
  state.activeSubsubtopicId = null;
  state.activeSubsubtopicObj = null;
  state.filters.page = 1;
  renderTaxonomyTree();
  updateBreadcrumbs();
  loadProblems();
}

function selectSubsubtopic(mainTopicName, subtopicName, sstId) {
  state.activeMainTopic = mainTopicName;
  state.activeSubtopic = subtopicName;
  state.activeSubsubtopicId = sstId;

  // Find the subsubtopic object
  for (const m of state.taxonomy) {
    if (m.name === mainTopicName) {
      for (const s of m.subtopics) {
        if (s.name === subtopicName) {
          state.activeSubsubtopicObj = s.subsubtopics.find(it => it.id === sstId);
          break;
        }
      }
    }
  }

  state.filters.page = 1;
  renderTaxonomyTree();
  updateBreadcrumbs();
  loadProblems();
}

function updateBreadcrumbs() {
  const container = document.getElementById('breadcrumbs-container');
  if (!container) return;

  let crumbs = [`<span onclick="selectAllTopics()" class="cursor-pointer hover:text-sky-400">All Topics</span>`];

  if (state.activeMainTopic) {
    crumbs.push(`<span onclick="selectMainTopic('${state.activeMainTopic}')" class="cursor-pointer hover:text-sky-400">${state.activeMainTopic}</span>`);
  }
  if (state.activeSubtopic) {
    crumbs.push(`<span onclick="selectSubtopic('${state.activeMainTopic}', '${state.activeSubtopic}')" class="cursor-pointer hover:text-sky-400">${state.activeSubtopic}</span>`);
  }
  if (state.activeSubsubtopicObj) {
    crumbs.push(`<span class="text-sky-400 font-semibold">${state.activeSubsubtopicObj.full_title}</span>`);
  }

  container.innerHTML = crumbs.join(' <span class="text-slate-600 font-bold">/</span> ');

  // Update Section Header Card
  const headerCard = document.getElementById('technique-header-card');
  if (headerCard) {
    if (state.activeSubsubtopicObj) {
      headerCard.classList.remove('hidden');
      headerCard.innerHTML = `
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <span class="px-2 py-0.5 rounded text-xs font-mono font-bold bg-sky-500/20 text-sky-300 border border-sky-500/30">#${state.activeSubsubtopicObj.id}</span>
              <h2 class="text-base sm:text-lg font-bold text-white">${state.activeSubsubtopicObj.name}</h2>
            </div>
            <p class="text-xs text-slate-400 mt-1">${state.activeMainTopic} &gt; ${state.activeSubtopic}</p>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-right">
              <div class="text-xs text-slate-400 font-medium">Curated Problems</div>
              <div class="text-sm sm:text-base font-bold text-white font-mono">
                ${state.activeSubsubtopicObj.problem_count} 
                <span class="text-xs font-normal text-amber-400">(${state.activeSubsubtopicObj.masterpiece_count} ★★★)</span>
              </div>
            </div>
          </div>
        </div>
      `;
    } else if (state.activeMainTopic) {
      headerCard.classList.remove('hidden');
      headerCard.innerHTML = `
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-base sm:text-lg font-bold text-white">${state.activeMainTopic}</h2>
            <p class="text-xs text-slate-400 mt-1">Viewing all curriculum problems in this main domain</p>
          </div>
        </div>
      `;
    } else {
      headerCard.classList.add('hidden');
    }
  }
}

async function ensureCatalogLoaded() {
  if (state.catalog && state.catalog.length > 0) return true;
  try {
    const res = await fetch('./data/problems_catalog.json');
    if (res.ok) {
      state.catalog = await res.json();
      return true;
    }
  } catch (e) {
    console.warn('Static catalog not available, falling back to API:', e);
  }
  return false;
}

// Load Problems API / Static In-Memory Engine
async function loadProblems() {
  const grid = document.getElementById('problems-container');
  if (!grid) return;

  grid.innerHTML = `
    <div class="col-span-full py-20 flex flex-col items-center justify-center text-slate-400">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-sky-500 mb-4"></div>
      <p class="text-sm font-medium">Loading problems from curriculum catalog...</p>
    </div>
  `;

  const catalogReady = await ensureCatalogLoaded();
  if (catalogReady && state.catalog) {
    let filtered = state.catalog;

    if (state.activeMainTopic) {
      filtered = filtered.filter(p => p.main_topic === state.activeMainTopic);
    }
    if (state.activeSubtopic) {
      filtered = filtered.filter(p => p.subtopic === state.activeSubtopic);
    }
    if (state.activeSubsubtopicId) {
      filtered = filtered.filter(p => p.subsubtopic_id === state.activeSubsubtopicId);
    }
    if (state.filters.importance !== 'all') {
      filtered = filtered.filter(p => p.importance === state.filters.importance);
    }
    if (state.filters.minRating) {
      filtered = filtered.filter(p => p.rating && p.rating >= state.filters.minRating);
    }
    if (state.filters.maxRating) {
      filtered = filtered.filter(p => p.rating && p.rating <= state.filters.maxRating);
    }
    if (state.filters.status === 'solved') {
      filtered = filtered.filter(p => state.userProgress.solved.has(p.id));
    } else if (state.filters.status === 'unsolved') {
      filtered = filtered.filter(p => !state.userProgress.solved.has(p.id));
    } else if (state.filters.status === 'bookmarked') {
      filtered = filtered.filter(p => state.userProgress.bookmarked.has(p.id));
    }
    if (state.filters.searchQuery) {
      const q = state.filters.searchQuery.toLowerCase();
      filtered = filtered.filter(p => {
        return p.id.toLowerCase().includes(q) ||
               (p.name && p.name.toLowerCase().includes(q)) ||
               (p.approach_summary && p.approach_summary.toLowerCase().includes(q)) ||
               (Array.isArray(p.tags) && p.tags.some(t => t.toLowerCase().includes(q)));
      });
    }

    // Sort
    const sortBy = state.filters.sortBy;
    filtered = [...filtered].sort((a, b) => {
      if (sortBy === 'rating_desc') {
        return (b.rating || 0) - (a.rating || 0) || (b.solved_count || 0) - (a.solved_count || 0);
      } else if (sortBy === 'solves_desc') {
        return (b.solved_count || 0) - (a.solved_count || 0) || (a.rating || 0) - (b.rating || 0);
      } else if (sortBy === 'id_asc') {
        return a.id.localeCompare(b.id, undefined, { numeric: true });
      } else if (sortBy === 'importance_desc') {
        const score = imp => imp === '***' ? 1 : (imp === '**' ? 2 : 3);
        return score(a.importance) - score(b.importance) || (a.rating || 0) - (b.rating || 0);
      } else { // rating_asc
        return (a.rating || 9999) - (b.rating || 9999) || (b.solved_count || 0) - (a.solved_count || 0);
      }
    });

    const total = filtered.length;
    const page = state.filters.page;
    const pageSize = state.filters.pageSize;
    const totalPages = Math.max(1, Math.ceil(total / pageSize));
    const pagedProblems = filtered.slice((page - 1) * pageSize, page * pageSize);

    state.problems = pagedProblems;
    state.pagination = { total, page, totalPages };

    renderProblems();
    renderPagination();
    return;
  }

  // Fallback to API if static catalog not available
  const params = new URLSearchParams();
  if (state.activeMainTopic) params.append('main_topic', state.activeMainTopic);
  if (state.activeSubtopic) params.append('subtopic', state.activeSubtopic);
  if (state.activeSubsubtopicId) params.append('subsubtopic_id', state.activeSubsubtopicId);
  if (state.filters.importance !== 'all') params.append('importance', state.filters.importance);
  if (state.filters.minRating) params.append('min_rating', state.filters.minRating);
  if (state.filters.maxRating) params.append('max_rating', state.filters.maxRating);
  if (state.filters.status !== 'all') params.append('status', state.filters.status);
  if (state.filters.searchQuery) params.append('q', state.filters.searchQuery);
  params.append('sort_by', state.filters.sortBy);
  params.append('page', state.filters.page);
  params.append('page_size', state.filters.pageSize);

  try {
    const res = await fetch(`/api/problems?${params.toString()}`);
    const data = await res.json();
    state.problems = data.problems || [];
    state.pagination = { total: data.total || 0, page: data.page || 1, totalPages: data.total_pages || 1 };

    renderProblems();
    renderPagination();
  } catch (err) {
    console.error('Failed to load problems:', err);
    grid.innerHTML = `<div class="col-span-full py-16 text-center text-rose-400 text-sm">Failed to fetch problems. Please try refreshing.</div>`;
  }
}

// Render Problem Cards
function renderProblems() {
  const container = document.getElementById('problems-container');
  const countBadge = document.getElementById('problems-count-badge');
  if (countBadge) {
    countBadge.textContent = `${state.pagination.total?.toLocaleString()} problems found`;
  }

  if (!container) return;

  if (state.problems.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-24 text-center glass-panel rounded-2xl p-8 border border-slate-800">
        <div class="text-4xl mb-3">🔍</div>
        <h3 class="text-base font-bold text-slate-200">No matching problems found</h3>
        <p class="text-xs text-slate-400 mt-1 max-w-md mx-auto">Try clearing search filters or broadening your rating range.</p>
        <button onclick="resetFilters()" class="mt-4 px-4 py-2 rounded-xl bg-sky-500/20 text-sky-400 text-xs font-semibold hover:bg-sky-500/30 transition-colors">Reset All Filters</button>
      </div>
    `;
    return;
  }

  container.innerHTML = state.problems.map(p => {
    const isSolved = state.userProgress.solved.has(p.id);
    const isBookmarked = state.userProgress.bookmarked.has(p.id);
    const ratingClass = getRatingClass(p.rating);
    const ratingTitle = getRatingTitle(p.rating);
    const starBadge = getStarBadgeHtml(p.importance);

    return `
      <div class="glass-card rounded-2xl p-4 flex flex-col justify-between relative group animate-fade-in ${isSolved ? 'border-emerald-500/40 bg-emerald-950/10' : ''}">
        <div>
          <!-- Header: Rating, ID, Star, Bookmark -->
          <div class="flex items-center justify-between gap-2 mb-2.5">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded text-xs font-mono font-bold ${ratingClass}" title="${ratingTitle}">
                ${p.rating || 'Unrated'}
              </span>
              <span class="text-xs font-mono font-bold text-slate-300">${p.id}</span>
            </div>
            <div class="flex items-center gap-1.5">
              ${starBadge}
              <button onclick="event.stopPropagation(); toggleBookmark('${p.id}')" class="p-1 rounded-lg hover:bg-slate-800 transition-colors ${isBookmarked ? 'text-amber-400' : 'text-slate-500 hover:text-slate-300'}" title="Toggle Bookmark">
                ★
              </button>
            </div>
          </div>

          <!-- Problem Title -->
          <h3 class="text-sm font-bold text-white group-hover:text-sky-300 transition-colors line-clamp-2 cursor-pointer mb-2" onclick="openProblemModal('${p.id}', 'statement')">
            ${p.name}
          </h3>

          <!-- Solution Approach Trick Preview -->
          <div class="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800/90 text-xs text-slate-300 leading-relaxed mb-3 line-clamp-3">
            <span class="text-amber-400 font-semibold">💡 Trick:</span> ${p.approach_summary || 'Apply standard techniques under this category.'}
          </div>

          <!-- Subtopic Tag Pill -->
          <div class="text-[11px] text-slate-400 flex items-center gap-1.5 mb-2 truncate">
            <span class="text-slate-500">📁</span>
            <span class="text-slate-300 truncate">${p.subsubtopic || `${p.main_topic} > ${p.subtopic}`}</span>
          </div>

          <!-- Tags -->
          <div class="flex flex-wrap gap-1 mb-3">
            ${(p.tags || []).slice(0, 3).map(t => `<span class="px-1.5 py-0.5 rounded text-[10px] bg-slate-800/80 text-slate-400 border border-slate-700/50">${t}</span>`).join('')}
            ${(p.tags || []).length > 3 ? `<span class="text-[10px] text-slate-500 self-center">+${p.tags.length - 3}</span>` : ''}
          </div>
        </div>

        <!-- Footer Actions -->
        <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs mt-auto">
          <div class="flex items-center gap-2">
            <label class="flex items-center gap-1 text-[11px] cursor-pointer text-slate-300 hover:text-emerald-400 select-none">
              <input type="checkbox" ${isSolved ? 'checked' : ''} onchange="toggleSolved('${p.id}')" class="rounded border-slate-700 text-emerald-500 focus:ring-0 bg-slate-800 cursor-pointer">
              <span>Solved</span>
            </label>
            <a href="${p.problem_url}" target="_blank" rel="noopener noreferrer" class="text-slate-400 hover:text-sky-400 text-[11px] flex items-center gap-0.5" title="Open on Codeforces">
              CF ↗
            </a>
          </div>

          <div class="flex items-center gap-1.5">
            <button onclick="openProblemModal('${p.id}', 'statement')" class="px-2.5 py-1 rounded-lg bg-sky-500/15 text-sky-400 hover:bg-sky-500/25 border border-sky-500/30 transition-colors font-medium text-[11px]">
              Statement
            </button>
            <button onclick="openProblemModal('${p.id}', 'editorial')" class="px-2.5 py-1 rounded-lg bg-purple-500/15 text-purple-300 hover:bg-purple-500/25 border border-purple-500/30 transition-colors font-medium text-[11px] flex items-center gap-1">
              <span>📖</span> Editorial
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// Render Pagination
function renderPagination() {
  const container = document.getElementById('pagination-container');
  if (!container) return;

  const { page, totalPages, total } = state.pagination;
  if (totalPages <= 1) {
    container.innerHTML = '';
    return;
  }

  container.innerHTML = `
    <div class="flex items-center justify-center gap-2 py-4">
      <button onclick="goToPage(1)" ${page <= 1 ? 'disabled class="opacity-30 cursor-not-allowed"' : 'class="hover:bg-slate-800"'} class="px-2.5 py-1.5 rounded-lg border border-slate-800 bg-slate-900 text-slate-300 text-xs font-medium transition-colors" title="First Page">
        ⇤
      </button>
      <button onclick="goToPage(${page - 1})" ${page <= 1 ? 'disabled class="opacity-30 cursor-not-allowed"' : 'class="hover:bg-slate-800"'} class="px-3 py-1.5 rounded-lg border border-slate-800 bg-slate-900 text-slate-300 text-xs font-medium transition-colors">
        ◀ Previous
      </button>
      <span class="px-3 py-1.5 text-xs text-slate-400 font-mono">
        Page <strong class="text-white">${page}</strong> of <strong class="text-white">${totalPages}</strong>
      </span>
      <button onclick="goToPage(${page + 1})" ${page >= totalPages ? 'disabled class="opacity-30 cursor-not-allowed"' : 'class="hover:bg-slate-800"'} class="px-3 py-1.5 rounded-lg border border-slate-800 bg-slate-900 text-slate-300 text-xs font-medium transition-colors">
        Next ▶
      </button>
      <button onclick="goToPage(${totalPages})" ${page >= totalPages ? 'disabled class="opacity-30 cursor-not-allowed"' : 'class="hover:bg-slate-800"'} class="px-2.5 py-1.5 rounded-lg border border-slate-800 bg-slate-900 text-slate-300 text-xs font-medium transition-colors" title="Last Page">
        ⇥
      </button>
    </div>
  `;
}

function goToPage(newPage) {
  if (newPage < 1 || newPage > state.pagination.totalPages) return;
  state.filters.page = newPage;
  loadProblems();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Filter Actions
function setImportanceFilter(imp) {
  state.filters.importance = imp;
  state.filters.page = 1;
  document.querySelectorAll('[data-filter-importance]').forEach(btn => {
    const val = btn.getAttribute('data-filter-importance');
    if (val === imp) {
      btn.className = "px-3 py-1.5 rounded-lg text-xs font-semibold bg-sky-500 text-white transition-colors shadow-sm";
    } else {
      btn.className = "px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 text-slate-300 hover:bg-slate-800 border border-slate-800 transition-colors";
    }
  });
  loadProblems();
}

function setStatusFilter(status) {
  state.filters.status = status;
  state.filters.page = 1;
  document.querySelectorAll('[data-filter-status]').forEach(btn => {
    const val = btn.getAttribute('data-filter-status');
    if (val === status) {
      btn.className = "px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-sky-500 text-white transition-colors shadow-sm";
    } else {
      btn.className = "px-2.5 py-1.5 rounded-lg text-xs font-medium bg-slate-900 text-slate-300 hover:bg-slate-800 border border-slate-800 transition-colors";
    }
  });
  loadProblems();
}

function setRatingPreset(min, max) {
  state.filters.minRating = min;
  state.filters.maxRating = max;
  state.filters.page = 1;
  const minInput = document.getElementById('filter-min-rating');
  const maxInput = document.getElementById('filter-max-rating');
  if (minInput) minInput.value = min || '';
  if (maxInput) maxInput.value = max || '';
  loadProblems();
}

function applyCustomRating() {
  const minInput = document.getElementById('filter-min-rating');
  const maxInput = document.getElementById('filter-max-rating');
  state.filters.minRating = minInput?.value ? parseInt(minInput.value) : null;
  state.filters.maxRating = maxInput?.value ? parseInt(maxInput.value) : null;
  state.filters.page = 1;
  loadProblems();
}

function setSortOrder(sortBy) {
  state.filters.sortBy = sortBy;
  state.filters.page = 1;
  loadProblems();
}

function setPageSize(size) {
  state.filters.pageSize = parseInt(size) || 30;
  state.filters.page = 1;
  loadProblems();
}

function resetFilters() {
  state.filters.importance = 'all';
  state.filters.minRating = null;
  state.filters.maxRating = null;
  state.filters.status = 'all';
  state.filters.searchQuery = '';
  state.filters.sortBy = 'rating_asc';
  state.filters.page = 1;
  state.filters.pageSize = 30;

  const searchInput = document.getElementById('global-search');
  if (searchInput) searchInput.value = '';
  const minInput = document.getElementById('filter-min-rating');
  const maxInput = document.getElementById('filter-max-rating');
  if (minInput) minInput.value = '';
  if (maxInput) maxInput.value = '';

  const sortSelect = document.getElementById('sort-by-select');
  if (sortSelect) sortSelect.value = 'rating_asc';
  const sizeSelect = document.getElementById('page-size-select');
  if (sizeSelect) sizeSelect.value = '30';

  setImportanceFilter('all');
  setStatusFilter('all');
  selectAllTopics();
}

// User Actions
async function toggleSolved(problemId) {
  const isCurrentlySolved = state.userProgress.solved.has(problemId);
  if (isCurrentlySolved) {
    state.userProgress.solved.delete(problemId);
  } else {
    state.userProgress.solved.add(problemId);
  }
  persistUserProgress();
  updateHeaderCounters();
  renderProblems();
  if (state.activeProblem && state.activeProblem.id === problemId) {
    state.activeProblem.is_solved = !isCurrentlySolved;
    updateModalActionButtons();
  }
  if (typeof syncProgressToVercel === 'function') {
    syncProgressToVercel(problemId, 'toggle_solved');
  }
  try {
    fetch(`/api/user/toggle_solved/${problemId}`, { method: 'POST' }).catch(() => {});
  } catch (err) {}
}

async function toggleBookmark(problemId) {
  const isCurrentlyBookmarked = state.userProgress.bookmarked.has(problemId);
  if (isCurrentlyBookmarked) {
    state.userProgress.bookmarked.delete(problemId);
  } else {
    state.userProgress.bookmarked.add(problemId);
  }
  persistUserProgress();
  updateHeaderCounters();
  renderProblems();
  if (state.activeProblem && state.activeProblem.id === problemId) {
    state.activeProblem.is_bookmarked = !isCurrentlyBookmarked;
    updateModalActionButtons();
  }
  if (typeof syncProgressToVercel === 'function') {
    syncProgressToVercel(problemId, 'toggle_bookmark');
  }
  try {
    fetch(`/api/user/toggle_bookmark/${problemId}`, { method: 'POST' }).catch(() => {});
  } catch (err) {}
}

async function saveNotes(problemId) {
  const textarea = document.getElementById('problem-notes-input');
  if (!textarea) return;
  const notes = textarea.value.trim();
  state.userProgress.notes[problemId] = notes;
  persistUserProgress();
  showToast('Notes saved successfully!');
  if (typeof syncNoteToVercel === 'function') {
    syncNoteToVercel(problemId, notes);
  }
  try {
    fetch(`/api/user/save_note/${problemId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notes })
    }).catch(() => {});
  } catch (err) {}
}

// Problem Modal View
async function openProblemModal(problemId, defaultTab = 'statement') {
  const modal = document.getElementById('problem-modal');
  const modalContent = document.getElementById('problem-modal-content');
  if (!modal || !modalContent) return;

  state.activeModalTab = defaultTab;
  modal.classList.remove('hidden');
  modalContent.innerHTML = `
    <div class="py-24 flex flex-col items-center justify-center text-slate-400">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-sky-500 mb-4"></div>
      <p class="text-sm font-medium">Loading problem statement, topic editorial & C++ solution...</p>
    </div>
  `;

  try {
    let p = null;
    try {
      let res = await fetch(`./data/problems/${encodeURIComponent(problemId)}.json`);
      if (!res.ok) res = await fetch(`/api/problems/${problemId}`);
      if (res.ok) p = await res.json();
    } catch (e) {
      try {
        const res = await fetch(`/api/problems/${problemId}`);
        if (res.ok) p = await res.json();
      } catch (err) {}
    }

    if (!p) {
      modalContent.innerHTML = `<div class="p-8 text-center text-rose-400">Failed to load problem statement.</div>`;
      return;
    }

    // Normalize topic_editorial from static JSON
    if (p.topic_editorial) {
      p.editorial_title = p.editorial_title || p.topic_editorial.title;
      p.editorial_key_invariant = p.editorial_key_invariant || p.topic_editorial.key_invariant;
      p.editorial_solution_walkthrough = p.editorial_solution_walkthrough || p.topic_editorial.solution_walkthrough;
      p.editorial_complexity_analysis = p.editorial_complexity_analysis || p.topic_editorial.complexity_analysis;
      p.editorial_cpp_code = p.editorial_cpp_code || p.topic_editorial.cpp_code;
    }

    // Attempt to load full markdown editorial if not present
    if (!p.editorial_full_markdown) {
      try {
        const mdRes = await fetch(`./data/editorials/${encodeURIComponent(problemId)}.md`);
        if (mdRes.ok) p.editorial_full_markdown = await mdRes.text();
      } catch (e) {}
    }

    state.activeProblem = p;

    const ratingClass = getRatingClass(p.rating);
    const ratingTitle = getRatingTitle(p.rating);
    const starBadge = getStarBadgeHtml(p.importance);
    const isSolved = state.userProgress.solved.has(p.id);
    const isBookmarked = state.userProgress.bookmarked.has(p.id);
    const currentNotes = state.userProgress.notes[p.id] || p.notes || '';

    let samplesHtml = '';
    if (Array.isArray(p.sample_testcases) && p.sample_testcases.length > 0) {
      samplesHtml = `
        <div class="mt-6">
          <h4 class="text-xs font-bold text-white uppercase tracking-wider mb-3">Sample Tests</h4>
          <div class="space-y-4">
            ${p.sample_testcases.map((sample, idx) => `
              <div class="rounded-xl border border-slate-800 bg-slate-950/70 overflow-hidden shadow-sm">
                <div class="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-800">
                  <div class="p-3">
                    <div class="flex items-center justify-between text-xs text-slate-400 mb-1.5">
                      <span class="font-semibold text-slate-300">Input ${idx + 1}</span>
                      <button onclick="copyToClipboard(\`${escapeForAttr(sample.input)}\`, 'Input copied!')" class="px-2 py-0.5 rounded text-[11px] bg-slate-800 text-sky-400 hover:bg-slate-700 transition-colors">Copy</button>
                    </div>
                    <pre class="text-xs text-slate-200 font-mono bg-slate-900/90 p-2.5 rounded-lg overflow-x-auto whitespace-pre">${escapeHtml(sample.input)}</pre>
                  </div>
                  <div class="p-3">
                    <div class="flex items-center justify-between text-xs text-slate-400 mb-1.5">
                      <span class="font-semibold text-slate-300">Output ${idx + 1}</span>
                      <button onclick="copyToClipboard(\`${escapeForAttr(sample.output)}\`, 'Output copied!')" class="px-2 py-0.5 rounded text-[11px] bg-slate-800 text-sky-400 hover:bg-slate-700 transition-colors">Copy</button>
                    </div>
                    <pre class="text-xs text-emerald-400 font-mono bg-slate-900/90 p-2.5 rounded-lg overflow-x-auto whitespace-pre">${escapeHtml(sample.output)}</pre>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    // Render Editorial content using marked if available
    let editorialBodyHtml = '';
    if (p.editorial_full_markdown && window.marked) {
      editorialBodyHtml = window.marked.parse(p.editorial_full_markdown);
    } else {
      editorialBodyHtml = `
        <div class="space-y-6">
          <div class="p-4 rounded-xl bg-gradient-to-r from-amber-500/15 via-amber-500/5 to-transparent border border-amber-500/30">
            <h3 class="text-amber-400 font-bold text-sm mb-1.5 flex items-center gap-1.5">
              <span>💡</span> The Core Invariant ("Aha!" Moment)
            </h3>
            <p class="text-sm leading-relaxed text-slate-200">${escapeHtml(p.editorial_key_invariant || p.approach_summary || '')}</p>
          </div>

          <div>
            <h3 class="text-sm font-bold text-white uppercase tracking-wider mb-2">Step-by-Step Walkthrough</h3>
            <div class="text-sm text-slate-200 leading-relaxed whitespace-pre-wrap">${escapeHtml(p.editorial_solution_walkthrough || '')}</div>
          </div>

          <div class="p-3.5 rounded-xl bg-slate-900/70 border border-slate-800">
            <h3 class="text-xs font-bold text-sky-400 uppercase tracking-wider mb-1">Complexity Analysis</h3>
            <div class="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap">${escapeHtml(p.editorial_complexity_analysis || '')}</div>
          </div>
        </div>
      `;
    }

    const cppCode = p.editorial_cpp_code || '// C++ solution placeholder';

    modalContent.innerHTML = `
      <!-- Modal Top Bar -->
      <div class="p-5 md:p-6 border-b border-slate-800 bg-slate-900/70 sticky top-0 z-20 backdrop-blur-md flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="px-2.5 py-1 rounded text-sm font-mono font-bold ${ratingClass}">${p.rating || 'Unrated'}</span>
            <span class="text-xs text-slate-400 font-medium">${ratingTitle}</span>
            <span class="text-slate-600">•</span>
            <span class="text-xs font-mono text-slate-300 font-bold">ID: ${p.id}</span>
            <span class="text-slate-600">•</span>
            ${starBadge}
            <span class="text-slate-600">•</span>
            <span class="text-xs text-slate-400">👥 ${p.solved_count?.toLocaleString()} solves</span>
          </div>
          <h2 class="text-lg md:text-xl font-extrabold text-white mt-1.5">${p.name}</h2>
          <div class="text-xs text-slate-400 mt-1">
            <span>${p.main_topic}</span> &gt; <span>${p.subtopic}</span> &gt; <span class="text-sky-400 font-semibold">${p.subsubtopic}</span>
          </div>
        </div>

        <div class="flex items-center gap-2 flex-wrap" id="modal-actions-container">
          <button onclick="toggleSolved('${p.id}')" class="px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors ${isSolved ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700'}">
            <span>${isSolved ? '✓ Solved' : 'Mark Solved'}</span>
          </button>
          <button onclick="toggleBookmark('${p.id}')" class="px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors ${isBookmarked ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700'}">
            <span>${isBookmarked ? '★ Bookmarked' : '☆ Bookmark'}</span>
          </button>
          <a href="${p.problem_url}" target="_blank" rel="noopener noreferrer" class="px-3 py-1.5 rounded-xl bg-sky-500 text-white text-xs font-semibold hover:bg-sky-400 transition-colors flex items-center gap-1">
            Solve on CF ↗
          </a>
          ${p.editorial_url ? `
            <a href="${p.editorial_url}" target="_blank" rel="noopener noreferrer" class="px-3 py-1.5 rounded-xl bg-purple-600/30 text-purple-300 border border-purple-500/40 text-xs font-semibold hover:bg-purple-600/40 transition-colors">
              CF Blog ↗
            </a>
          ` : ''}
          <button onclick="closeProblemModal()" class="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors text-base font-bold ml-1">
            ✕
          </button>
        </div>
      </div>

      <!-- Modal Tabs Header -->
      <div class="flex items-center gap-2 px-6 pt-3 border-b border-slate-800 bg-slate-900/40">
        <button id="modal-tab-btn-statement" onclick="switchModalTab('statement')" class="px-4 py-2.5 text-xs font-semibold rounded-t-xl transition-colors flex items-center gap-1.5 ${defaultTab === 'statement' ? 'border-b-2 border-sky-500 text-sky-400 bg-slate-800/80 font-bold' : 'border-b-2 border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'}">
          <span>📄</span> Problem Statement & Samples
        </button>
        <button id="modal-tab-btn-editorial" onclick="switchModalTab('editorial')" class="px-4 py-2.5 text-xs font-semibold rounded-t-xl transition-colors flex items-center gap-1.5 ${defaultTab === 'editorial' ? 'border-b-2 border-purple-500 text-purple-300 bg-slate-800/80 font-bold' : 'border-b-2 border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'}">
          <span>💡</span> Topic Editorial & Walkthrough
        </button>
        <button id="modal-tab-btn-solution" onclick="switchModalTab('solution')" class="px-4 py-2.5 text-xs font-semibold rounded-t-xl transition-colors flex items-center gap-1.5 ${defaultTab === 'solution' ? 'border-b-2 border-emerald-500 text-emerald-300 bg-slate-800/80 font-bold' : 'border-b-2 border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'}">
          <span>⚡</span> C++ Reference Implementation
        </button>
      </div>

      <!-- Tab 1: Statement Pane -->
      <div id="modal-tab-statement" class="${defaultTab === 'statement' ? '' : 'hidden'} p-6 md:p-8 space-y-6">
        <!-- Prominent Solution Trick & Technique Callout -->
        <div class="p-4 rounded-xl bg-gradient-to-r from-amber-500/10 via-amber-500/5 to-transparent border border-amber-500/30 text-slate-200">
          <div class="flex items-center gap-2 text-amber-400 font-bold text-xs mb-1.5">
            <span class="text-sm">💡</span>
            <span>Core Solution Invariant</span>
          </div>
          <p class="text-sm leading-relaxed text-amber-100/90 font-medium">
            ${p.approach_summary || 'Apply standard techniques under this category.'}
          </p>
        </div>

        <!-- Limits & Tags Bar -->
        <div class="flex flex-wrap items-center gap-3 text-xs text-slate-400 py-2 border-y border-slate-800/80">
          <div class="flex items-center gap-1.5">
            <span class="text-slate-500">⏱️ Time:</span>
            <span class="font-mono text-slate-200">${p.time_limit || '1.0s'}</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="text-slate-500">💾 Memory:</span>
            <span class="font-mono text-slate-200">${p.memory_limit || '256MB'}</span>
          </div>
          <div class="flex items-center gap-1.5 ml-auto">
            <span class="text-slate-500">Tags:</span>
            <div class="flex flex-wrap gap-1">
              ${(p.tags || []).map(t => `<span class="px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 text-[11px]">${t}</span>`).join('')}
            </div>
          </div>
        </div>

        <!-- Description -->
        <div>
          <h4 class="text-xs font-bold text-white uppercase tracking-wider mb-2">Statement</h4>
          <div class="text-slate-200 text-sm leading-relaxed whitespace-pre-wrap font-normal prose prose-invert max-w-none">
            ${escapeHtml(p.description || 'No statement available.')}
          </div>
        </div>

        <!-- Input Specification -->
        ${p.input_specification ? `
          <div>
            <h4 class="text-xs font-bold text-white uppercase tracking-wider mb-2">Input Specification</h4>
            <div class="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap bg-slate-900/40 p-3.5 rounded-xl border border-slate-800/80">
              ${escapeHtml(p.input_specification)}
            </div>
          </div>
        ` : ''}

        <!-- Output Specification -->
        ${p.output_specification ? `
          <div>
            <h4 class="text-xs font-bold text-white uppercase tracking-wider mb-2">Output Specification</h4>
            <div class="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap bg-slate-900/40 p-3.5 rounded-xl border border-slate-800/80">
              ${escapeHtml(p.output_specification)}
            </div>
          </div>
        ` : ''}

        <!-- Samples -->
        ${samplesHtml}

        <!-- Personal Notes Section -->
        <div class="mt-8 pt-6 border-t border-slate-800">
          <div class="flex items-center justify-between mb-2">
            <h4 class="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <span>📝</span> Personal Learning Notes
            </h4>
            <button onclick="saveNotes('${p.id}')" class="px-3 py-1 rounded-lg bg-sky-500 text-white text-xs font-semibold hover:bg-sky-400 transition-colors">
              Save Notes
            </button>
          </div>
          <textarea id="problem-notes-input" rows="3" placeholder="Write your own solution observations, tricky edge cases, or takeaways here..." class="w-full rounded-xl bg-slate-900 border border-slate-800 p-3 text-xs text-slate-200 focus:outline-none focus:border-sky-500 transition-colors font-mono">${escapeHtml(currentNotes)}</textarea>
        </div>
      </div>

      <!-- Tab 2: Topic-Based Editorial Pane -->
      <div id="modal-tab-editorial" class="${defaultTab === 'editorial' ? '' : 'hidden'} p-6 md:p-8 space-y-6">
        <!-- Technique Callout Bar -->
        <div class="flex items-center justify-between p-3.5 rounded-xl bg-purple-500/10 border border-purple-500/20 text-xs">
          <div class="flex items-center gap-2 text-purple-300 font-mono">
            <span>🎯 Technique:</span>
            <span class="font-bold text-white px-2 py-0.5 rounded bg-purple-900/60 border border-purple-600/40">${p.subsubtopic}</span>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="copyToClipboard(\`${escapeForAttr(p.editorial_full_markdown || '')}\`, 'Editorial Markdown copied!')" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-purple-300 text-xs font-medium transition-colors">
              Copy Markdown
            </button>
            <button onclick="switchModalTab('solution')" class="px-3 py-1 rounded-lg bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/30 transition-colors text-xs font-semibold flex items-center gap-1">
              <span>⚡</span> View C++ Code
            </button>
          </div>
        </div>

        <!-- Rendered Editorial Body -->
        <div class="prose prose-invert max-w-none text-slate-200 text-sm leading-relaxed space-y-4">
          ${editorialBodyHtml}
        </div>
      </div>

      <!-- Tab 3: C++ Solution Implementation Pane -->
      <div id="modal-tab-solution" class="${defaultTab === 'solution' ? '' : 'hidden'} p-6 md:p-8 space-y-6">
        <div class="rounded-2xl border border-slate-800 bg-slate-950 overflow-hidden shadow-2xl">
          <div class="flex items-center justify-between px-4 py-3 bg-slate-900/90 border-b border-slate-800">
            <div class="flex items-center gap-2 text-xs font-semibold text-slate-300 font-mono">
              <span class="text-emerald-400">⚡</span>
              <span>solution_${p.id}.cpp — (${p.subsubtopic})</span>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="downloadCode('${p.id}', \`${escapeForAttr(cppCode)}\`)" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium transition-colors flex items-center gap-1">
                <span>💾</span> Download .cpp
              </button>
              <button onclick="copyToClipboard(\`${escapeForAttr(cppCode)}\`, 'C++ Code copied!')" class="px-3 py-1 rounded-lg bg-sky-500 hover:bg-sky-400 text-white text-xs font-semibold transition-colors flex items-center gap-1 shadow-sm">
                <span>📋</span> Copy Code
              </button>
            </div>
          </div>
          <pre class="p-5 text-xs font-mono text-emerald-300 overflow-x-auto whitespace-pre leading-relaxed bg-[#060a12] select-all"><code>${escapeHtml(cppCode)}</code></pre>
        </div>
      </div>
    `;

    // Typeset LaTeX equations with MathJax
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([modalContent]).catch((err) => console.log('MathJax error:', err));
    }
  } catch (err) {
    console.error('Failed to load problem detail:', err);
    modalContent.innerHTML = `<div class="p-16 text-center text-rose-400">Failed to load problem statement and editorial.</div>`;
  }
}

function switchModalTab(tab) {
  state.activeModalTab = tab;
  const btnStatement = document.getElementById('modal-tab-btn-statement');
  const btnEditorial = document.getElementById('modal-tab-btn-editorial');
  const btnSolution = document.getElementById('modal-tab-btn-solution');

  const paneStatement = document.getElementById('modal-tab-statement');
  const paneEditorial = document.getElementById('modal-tab-editorial');
  const paneSolution = document.getElementById('modal-tab-solution');

  if (!btnStatement || !btnEditorial || !paneStatement || !paneEditorial) return;

  // Reset tab button states
  [btnStatement, btnEditorial, btnSolution].forEach(b => {
    if (b) b.className = 'px-4 py-2.5 text-xs font-semibold rounded-t-xl transition-colors flex items-center gap-1.5 border-b-2 border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40';
  });

  // Hide all panes
  [paneStatement, paneEditorial, paneSolution].forEach(p => {
    if (p) p.classList.add('hidden');
  });

  if (tab === 'statement') {
    btnStatement.className = 'px-4 py-2.5 text-xs font-bold rounded-t-xl transition-colors flex items-center gap-1.5 border-b-2 border-sky-500 text-sky-400 bg-slate-800/80';
    paneStatement.classList.remove('hidden');
  } else if (tab === 'editorial') {
    btnEditorial.className = 'px-4 py-2.5 text-xs font-bold rounded-t-xl transition-colors flex items-center gap-1.5 border-b-2 border-purple-500 text-purple-300 bg-slate-800/80';
    paneEditorial.classList.remove('hidden');
  } else if (tab === 'solution') {
    if (btnSolution) btnSolution.className = 'px-4 py-2.5 text-xs font-bold rounded-t-xl transition-colors flex items-center gap-1.5 border-b-2 border-emerald-500 text-emerald-300 bg-slate-800/80';
    if (paneSolution) paneSolution.classList.remove('hidden');
  }

  const activePane = tab === 'statement' ? paneStatement : (tab === 'editorial' ? paneEditorial : paneSolution);
  if (activePane && window.MathJax && window.MathJax.typesetPromise) {
    window.MathJax.typesetPromise([activePane]).catch(() => {});
  }
}

function updateModalActionButtons() {
  if (!state.activeProblem) return;
  const p = state.activeProblem;
  const isSolved = state.userProgress.solved.has(p.id);
  const isBookmarked = state.userProgress.bookmarked.has(p.id);

  const container = document.getElementById('modal-actions-container');
  if (!container) return;

  const buttons = container.querySelectorAll('button');
  if (buttons.length >= 2) {
    buttons[0].className = `px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors ${isSolved ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700'}`;
    buttons[0].innerHTML = `<span>${isSolved ? '✓ Solved' : 'Mark Solved'}</span>`;

    buttons[1].className = `px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors ${isBookmarked ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700'}`;
    buttons[1].innerHTML = `<span>${isBookmarked ? '★ Bookmarked' : '☆ Bookmark'}</span>`;
  }
}

function closeProblemModal() {
  const modal = document.getElementById('problem-modal');
  if (modal) modal.classList.add('hidden');
  state.activeProblem = null;
}

// Random Problem Picker
function pickRandomProblem() {
  if (state.problems.length > 0) {
    const randomIdx = Math.floor(Math.random() * state.problems.length);
    openProblemModal(state.problems[randomIdx].id, 'statement');
  }
}

// Clipboard Helper
function copyToClipboard(text, message = 'Copied to clipboard!') {
  navigator.clipboard.writeText(text).then(() => {
    showToast(message);
  }).catch(() => {
    showToast('Failed to copy');
  });
}

// Download Code Helper
function downloadCode(problemId, code) {
  const blob = new Blob([code], { type: 'text/x-c++src' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `solution_${problemId}.cpp`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast(`solution_${problemId}.cpp downloaded!`);
}

function showToast(msg) {
  const toast = document.createElement('div');
  toast.className = 'fixed bottom-6 right-6 z-50 px-4 py-2.5 rounded-xl bg-slate-800/95 border border-slate-700 text-white text-xs font-medium shadow-2xl animate-fade-in flex items-center gap-2 backdrop-blur-md';
  toast.innerHTML = `<span class="text-emerald-400">✓</span> <span>${msg}</span>`;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 2500);
}

// Escape Helpers
function escapeHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function escapeForAttr(str) {
  if (!str) return '';
  return str.replace(/`/g, '\\`').replace(/\$/g, '\\$');
}
