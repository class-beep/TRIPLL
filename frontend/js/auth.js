/**
 * TRIPPL Travel Planner - Authentication & Session Management Utility
 */

const API_BASE_URL = window.API_BASE_URL || "http://localhost:8000";

// --- Session Persistence ---
function getAuthToken() {
    return localStorage.getItem("trippl_token");
}

function getAuthUser() {
    try {
        const userStr = localStorage.getItem("trippl_user");
        return userStr ? JSON.parse(userStr) : null;
    } catch (e) {
        console.error("Error parsing stored user data", e);
        return null;
    }
}

function setAuthSession(token, user) {
    if (token) localStorage.setItem("trippl_token", token);
    if (user) localStorage.setItem("trippl_user", JSON.stringify(user));
    window.dispatchEvent(new Event("trippl_auth_changed"));
}

function clearAuthSession() {
    localStorage.removeItem("trippl_token");
    localStorage.removeItem("trippl_user");
    window.dispatchEvent(new Event("trippl_auth_changed"));
}

function isLoggedIn() {
    return !!getAuthToken() && !!getAuthUser();
}

// --- Authenticated API Request Wrapper ---
async function apiFetch(url, options = {}) {
    const token = getAuthToken();
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const fullUrl = url.startsWith("http") ? url : `${API_BASE_URL}${url}`;

    try {
        const response = await fetch(fullUrl, {
            ...options,
            headers
        });

        if (response.status === 401) {
            // Token expired or invalid
            clearAuthSession();
            if (!window.location.pathname.endsWith("login.html")) {
                window.location.href = "login.html?session_expired=1";
            }
        }

        return response;
    } catch (error) {
        console.warn("API Request failed (Backend may be offline):", error);
        throw error;
    }
}

// --- Auth API Actions ---
async function loginUser(email, password) {
    try {
        const res = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.detail || "Login failed. Please check your credentials.");
        }

        setAuthSession(data.access_token, data.user);
        return { success: true, data };
    } catch (err) {
        if (err.name === "TypeError" && err.message.includes("Failed to fetch")) {
            throw new Error("Unable to connect to authentication server. Please ensure the backend is running.");
        }
        throw err;
    }
}

async function registerUser(userData) {
    try {
        const res = await fetch(`${API_BASE_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userData)
        });

        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.detail || "Registration failed. Please try again.");
        }

        setAuthSession(data.access_token, data.user);
        return { success: true, data };
    } catch (err) {
        if (err.name === "TypeError" && err.message.includes("Failed to fetch")) {
            throw new Error("Unable to connect to authentication server. Please ensure the backend is running.");
        }
        throw err;
    }
}

function logoutUser() {
    clearAuthSession();
    window.location.href = "login.html?logged_out=1";
}

// --- Dynamic Navigation Header Sync ---
function syncNavigationHeader() {
    const user = getAuthUser();
    const headers = document.querySelectorAll("header");

    headers.forEach(header => {
        const authActionContainer = header.querySelector(".flex.items-center.gap-4");
        if (!authActionContainer) return;

        // Check if container already updated
        let userMenu = authActionContainer.querySelector("#user-nav-profile");

        if (user) {
            const initials = user.full_name
                ? user.full_name.split(" ").map(n => n[0]).join("").toUpperCase().substring(0, 2)
                : "U";

            const userAvatarHtml = user.profile_image
                ? `<img src="${user.profile_image}" alt="${user.full_name}" class="w-full h-full object-cover">`
                : `<span class="font-bold text-sm text-primary">${initials}</span>`;

            if (!userMenu) {
                userMenu = document.createElement("div");
                userMenu.id = "user-nav-profile";
                userMenu.className = "relative group flex items-center gap-3";

                userMenu.innerHTML = `
                    <div class="relative group/menu">
                        <button id="user-menu-btn" class="flex items-center gap-2 py-1 px-2 rounded-full hover:bg-surface-container transition-all border border-outline-variant focus:outline-none">
                            <div class="w-9 h-9 rounded-full bg-primary-container/20 overflow-hidden flex items-center justify-center border border-primary/30">
                                ${userAvatarHtml}
                            </div>
                            <span class="hidden lg:inline text-sm font-semibold text-on-surface max-w-[120px] truncate">${user.full_name || 'My Account'}</span>
                            <span class="material-symbols-outlined text-sm text-on-surface-variant transition-transform group-hover/menu:rotate-180">expand_more</span>
                        </button>
                        
                        <!-- Dropdown Menu -->
                        <div class="absolute right-0 mt-2 w-56 bg-surface-container-lowest rounded-2xl shadow-xl border border-outline-variant py-2 hidden group-hover/menu:block hover:block z-50 animate-fadeIn">
                            <div class="px-4 py-3 border-b border-outline-variant/60">
                                <p class="text-xs text-on-surface-variant font-medium">Signed in as</p>
                                <p class="text-sm font-bold text-on-surface truncate">${user.email || ''}</p>
                            </div>
                            <a href="profile.html" class="flex items-center gap-3 px-4 py-2.5 text-sm text-on-surface hover:bg-surface-container transition-colors">
                                <span class="material-symbols-outlined text-primary text-lg">person</span>
                                My Profile
                            </a>
                            <a href="planning.html" class="flex items-center gap-3 px-4 py-2.5 text-sm text-on-surface hover:bg-surface-container transition-colors">
                                <span class="material-symbols-outlined text-primary text-lg">luggage</span>
                                My Trips
                            </a>
                            <a href="booking.html" class="flex items-center gap-3 px-4 py-2.5 text-sm text-on-surface hover:bg-surface-container transition-colors">
                                <span class="material-symbols-outlined text-primary text-lg">confirmation_number</span>
                                My Bookings
                            </a>
                            <div class="border-t border-outline-variant/60 my-1"></div>
                            <button onclick="logoutUser()" class="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-error hover:bg-error-container/30 transition-colors text-left font-medium">
                                <span class="material-symbols-outlined text-error text-lg">logout</span>
                                Sign Out
                            </button>
                        </div>
                    </div>
                `;

                // Remove existing profile icon link if any
                const oldProfileBtn = authActionContainer.querySelector("a[href='profile.html']");
                if (oldProfileBtn && oldProfileBtn.parentElement === authActionContainer) {
                    oldProfileBtn.remove();
                }

                // Append the dynamic user menu
                authActionContainer.appendChild(userMenu);
            }
        } else {
            // Unauthenticated state
            if (userMenu) userMenu.remove();

            let loginBtn = authActionContainer.querySelector("#nav-login-btn");
            if (!loginBtn && !window.location.pathname.endsWith("login.html")) {
                loginBtn = document.createElement("a");
                loginBtn.id = "nav-login-btn";
                loginBtn.href = "login.html";
                loginBtn.className = "px-5 py-2 text-primary font-semibold hover:bg-primary/10 rounded-full text-sm transition-all duration-150 border border-primary/30";
                loginBtn.textContent = "Log In";
                
                // Remove old static profile icon if any
                const oldProfileBtn = authActionContainer.querySelector("a[href='profile.html']");
                if (oldProfileBtn) oldProfileBtn.remove();

                authActionContainer.appendChild(loginBtn);
            }
        }
    });
}

// Execute header sync when DOM is ready
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", syncNavigationHeader);
} else {
    syncNavigationHeader();
}

window.addEventListener("trippl_auth_changed", syncNavigationHeader);
