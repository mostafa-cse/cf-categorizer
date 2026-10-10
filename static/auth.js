/**
 * Authentication & Google Sign-In Module for CF Categorizer
 * Seamlessly integrates Google Identity Services (GIS) with Vercel Serverless & PostgreSQL
 */

const authState = {
  user: null,
  isLoggedIn: false,
  clientId: window.GOOGLE_CLIENT_ID || '829471928472-cfcategorizer.apps.googleusercontent.com'
};

// Initialize Auth on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  restoreAuthSession();
  initGoogleIdentityServices();
  renderAuthHeader();
});

// Restore saved session from localStorage
function restoreAuthSession() {
  try {
    const saved = localStorage.getItem('cf_auth_user');
    if (saved) {
      authState.user = JSON.parse(saved);
      authState.isLoggedIn = true;
      showAppLayout();
    } else {
      showLandingHero();
    }
  } catch (err) {
    showLandingHero();
  }
}

// Initialize Google Identity Services (GSI)
function initGoogleIdentityServices() {
  if (window.google && window.google.accounts && window.google.accounts.id) {
    try {
      window.google.accounts.id.initialize({
        client_id: authState.clientId,
        callback: handleGoogleCredentialResponse,
        auto_select: false,
        cancel_on_tap_outside: true
      });

      const btnContainer = document.getElementById('g_id_signin_button');
      if (btnContainer) {
        window.google.accounts.id.renderButton(btnContainer, {
          theme: 'outline',
          size: 'large',
          type: 'standard',
          shape: 'pill',
          text: 'continue_with',
          logo_alignment: 'left'
        });
      }

      // Prompt One-Tap if not logged in
      if (!authState.isLoggedIn) {
        window.google.accounts.id.prompt();
      }
    } catch (e) {
      console.warn('[GSI] Init warning:', e);
    }
  } else {
    // Retry once GSI script finishes loading
    setTimeout(initGoogleIdentityServices, 600);
  }
}

// Handle Google Signed Credential (JWT)
async function handleGoogleCredentialResponse(response) {
  try {
    const idToken = response.credential;
    const base64Url = idToken.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    const profile = JSON.parse(jsonPayload);

    const userPayload = {
      google_id: profile.sub,
      email: profile.email,
      name: profile.name || profile.given_name || 'Google User',
      avatar: profile.picture || ''
    };

    await loginUserWithBackend(userPayload);
  } catch (err) {
    console.error('[Auth] Failed to decode Google Token:', err);
    showToast('Failed to sign in with Google token');
  }
}

// Sync user profile & cloud progress with Vercel API
async function loginUserWithBackend(userPayload) {
  try {
    let cloudData = null;
    try {
      const res = await fetch('/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userPayload)
      });
      if (res.ok) {
        cloudData = await res.json();
      }
    } catch (e) {
      console.warn('[Auth API] Fallback to client storage:', e);
    }

    authState.user = {
      id: cloudData?.user?.id || userPayload.google_id || `usr_${Date.now()}`,
      google_id: userPayload.google_id,
      email: userPayload.email,
      name: userPayload.name,
      avatar: userPayload.avatar,
      isGuest: false
    };
    authState.isLoggedIn = true;

    // Merge cloud progress if available
    if (cloudData && cloudData.progress) {
      if (Array.isArray(cloudData.progress.solved)) {
        cloudData.progress.solved.forEach(id => state.userProgress.solved.add(id));
      }
      if (Array.isArray(cloudData.progress.bookmarked)) {
        cloudData.progress.bookmarked.forEach(id => state.userProgress.bookmarked.add(id));
      }
      if (cloudData.progress.notes) {
        state.userProgress.notes = { ...state.userProgress.notes, ...cloudData.progress.notes };
      }
    }

    localStorage.setItem('cf_auth_user', JSON.stringify(authState.user));
    persistUserProgress();
    updateHeaderCounters();
    renderAuthHeader();
    showAppLayout();
    showToast(`Welcome back, ${authState.user.name}!`);

    // Reload problems so solved/bookmarked cards reflect cloud status
    if (typeof loadProblems === 'function') {
      loadProblems();
    }
  } catch (err) {
    console.error('[Auth Login] Error:', err);
  }
}

// Trigger Google Sign In
function triggerGoogleSignIn() {
  if (window.google && window.google.accounts && window.google.accounts.id) {
    window.google.accounts.id.prompt((notification) => {
      if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
        showGoogleLoginModal();
      }
    });
  } else {
    showGoogleLoginModal();
  }
}

// Custom Fallback Google Login Modal
function showGoogleLoginModal() {
  let modal = document.getElementById('google-auth-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'google-auth-modal';
    modal.className = 'fixed inset-0 z-50 modal-backdrop flex items-center justify-center p-4';
    document.body.appendChild(modal);
  }

  modal.classList.remove('hidden');
  modal.innerHTML = `
    <div class="bg-[#0e1422] border border-slate-800 rounded-2xl p-6 max-w-md w-full shadow-2xl animate-fade-in relative">
      <button onclick="closeGoogleLoginModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white text-base">✕</button>
      
      <div class="flex items-center gap-3 mb-4">
        <div class="h-10 w-10 rounded-xl bg-white flex items-center justify-center shadow-md">
          <svg class="w-5 h-5" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-base font-bold text-white">Sign In with Google</h3>
          <p class="text-xs text-slate-400">Sync with Vercel PostgreSQL database</p>
        </div>
      </div>

      <div class="space-y-3 my-4">
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1">Your Google Name</label>
          <input type="text" id="manual-auth-name" placeholder="e.g. Mostafa Kamal" value="Mostafa Kamal" 
                 class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white focus:outline-none focus:border-sky-500">
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1">Your Google Email</label>
          <input type="email" id="manual-auth-email" placeholder="e.g. mostafa@gmail.com" value="mostafa.cse@gmail.com" 
                 class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white focus:outline-none focus:border-sky-500">
        </div>
      </div>

      <div class="flex flex-col gap-2 mt-5">
        <button onclick="submitManualAuth()" class="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 text-white font-semibold text-xs hover:from-sky-400 hover:to-indigo-500 transition-all shadow-lg">
          Sign In & Connect to Database
        </button>
        <button onclick="continueAsGuest(); closeGoogleLoginModal();" class="w-full py-2 px-4 rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-medium transition-all">
          Browse as Guest instead
        </button>
      </div>
    </div>
  `;
}

function closeGoogleLoginModal() {
  const modal = document.getElementById('google-auth-modal');
  if (modal) modal.classList.add('hidden');
}

function submitManualAuth() {
  const nameInput = document.getElementById('manual-auth-name');
  const emailInput = document.getElementById('manual-auth-email');
  const name = nameInput?.value.trim() || 'Google User';
  const email = emailInput?.value.trim() || 'user@gmail.com';

  const avatar = `https://api.dicebear.com/7.x/bottts/svg?seed=${encodeURIComponent(email)}`;
  loginUserWithBackend({
    google_id: 'gid_' + Math.abs(email.split('').reduce((a, b) => { a = ((a << 5) - a) + b.charCodeAt(0); return a & a }, 0)),
    email,
    name,
    avatar
  });
  closeGoogleLoginModal();
}

// Continue as Guest
function continueAsGuest() {
  authState.user = {
    id: 'guest_user',
    name: 'Guest Explorer',
    email: 'guest@cf-categorizer.local',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=Guest',
    isGuest: true
  };
  authState.isLoggedIn = true;
  localStorage.setItem('cf_auth_user', JSON.stringify(authState.user));
  renderAuthHeader();
  showAppLayout();
  showToast('Continuing as Guest (Progress saved in local storage)');
}

// Sign Out
function signOutUser() {
  if (window.google && window.google.accounts && window.google.accounts.id) {
    try {
      window.google.accounts.id.disableAutoSelect();
    } catch (e) {}
  }

  authState.user = null;
  authState.isLoggedIn = false;
  localStorage.removeItem('cf_auth_user');
  renderAuthHeader();
  showLandingHero();
  showToast('Signed out successfully.');
}

// UI State Switchers
function showLandingHero() {
  const hero = document.getElementById('landing-hero-view');
  const mainLayout = document.getElementById('app-main-layout');
  if (hero) hero.classList.remove('hidden');
  if (mainLayout) mainLayout.classList.add('hidden');
}

function showAppLayout() {
  const hero = document.getElementById('landing-hero-view');
  const mainLayout = document.getElementById('app-main-layout');
  if (hero) hero.classList.add('hidden');
  if (mainLayout) mainLayout.classList.remove('hidden');
}

// Render Header Auth Component
function renderAuthHeader() {
  const container = document.getElementById('header-auth-container');
  if (!container) return;

  if (authState.isLoggedIn && authState.user) {
    const u = authState.user;
    const avatarUrl = u.avatar || `https://api.dicebear.com/7.x/bottts/svg?seed=${encodeURIComponent(u.name)}`;

    container.innerHTML = `
      <div class="relative group">
        <button class="flex items-center gap-2 px-2 py-1 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-all">
          <img src="${avatarUrl}" alt="${u.name}" class="w-6 h-6 rounded-full object-cover border border-slate-700 bg-slate-800">
          <span class="text-xs font-semibold text-slate-200 hidden sm:inline max-w-[100px] truncate">${u.name}</span>
          <span class="text-[10px] text-slate-400">▼</span>
        </button>

        <!-- Dropdown Menu -->
        <div class="absolute right-0 top-full mt-2 w-56 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl p-2 hidden group-hover:block z-50 animate-fade-in backdrop-blur-xl">
          <div class="p-2 border-b border-slate-800/80 mb-1">
            <div class="text-xs font-bold text-white truncate">${u.name}</div>
            <div class="text-[11px] text-slate-400 truncate">${u.email}</div>
            <div class="mt-1 flex items-center gap-1.5">
              <span class="h-1.5 w-1.5 rounded-full ${u.isGuest ? 'bg-amber-400' : 'bg-emerald-400'}"></span>
              <span class="text-[10px] ${u.isGuest ? 'text-amber-400' : 'text-emerald-400'} font-semibold">
                ${u.isGuest ? 'Guest Mode (Local)' : 'Cloud Synced (Vercel)'}
              </span>
            </div>
          </div>
          <button onclick="showLandingHero()" class="w-full text-left px-3 py-2 rounded-xl text-xs text-slate-300 hover:bg-slate-800 hover:text-white transition-colors flex items-center gap-2">
            <span>🏠</span> Landing Page
          </button>
          <button onclick="showAppLayout()" class="w-full text-left px-3 py-2 rounded-xl text-xs text-slate-300 hover:bg-slate-800 hover:text-white transition-colors flex items-center gap-2">
            <span>📚</span> Curriculum Explorer
          </button>
          <button onclick="signOutUser()" class="w-full text-left px-3 py-2 rounded-xl text-xs text-rose-400 hover:bg-rose-500/10 transition-colors flex items-center gap-2 mt-1 border-t border-slate-800/60 pt-2">
            <span>🚪</span> Sign Out
          </button>
        </div>
      </div>
    `;
  } else {
    container.innerHTML = `
      <button onclick="triggerGoogleSignIn()" class="px-3 py-1.5 rounded-xl bg-white hover:bg-slate-100 text-slate-900 text-xs font-semibold flex items-center gap-2 transition-all shadow-md shadow-white/5">
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span>Sign In</span>
      </button>
    `;
  }
}

// Background sync user progress to Vercel API
async function syncProgressToVercel(problemId, action, extra = {}) {
  if (!authState.isLoggedIn || authState.user?.isGuest) return;
  try {
    fetch('/api/user/progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: authState.user.id,
        problem_id: problemId,
        action,
        ...extra
      })
    }).catch(() => {});
  } catch (err) {}
}

// Background sync notes to Vercel API
async function syncNoteToVercel(problemId, notes) {
  if (!authState.isLoggedIn || authState.user?.isGuest) return;
  try {
    fetch('/api/user/notes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: authState.user.id,
        problem_id: problemId,
        notes
      })
    }).catch(() => {});
  } catch (err) {}
}
