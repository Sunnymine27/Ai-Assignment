/**
 * AI Employee Check-in/Check-out System
 * Frontend JavaScript — Clock, sidebar toggle, and utilities.
 */

// ─── Clock ──────────────────────────────────────────────────────────────
function updateClock() {
    const now = new Date();

    const timeEl = document.getElementById('currentTime');
    if (timeEl) {
        timeEl.textContent = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        });
    }

    const dateEl = document.getElementById('currentDate');
    if (dateEl) {
        dateEl.textContent = now.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
}

// Update clock immediately and every second
updateClock();
setInterval(updateClock, 1000);


// ─── Sidebar Toggle ─────────────────────────────────────────────────────
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

// Close sidebar on outside click (mobile)
document.addEventListener('click', function(e) {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('sidebarToggle');

    if (sidebar && sidebar.classList.contains('open')) {
        if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
            sidebar.classList.remove('open');
        }
    }
});


// ─── Auto-dismiss Flash Messages ────────────────────────────────────────
document.querySelectorAll('.flash-message').forEach(function(msg) {
    setTimeout(function() {
        msg.style.animation = 'flash-in 0.3s ease reverse';
        setTimeout(function() { msg.remove(); }, 300);
    }, 5000);
});


// ─── Page Load Animation ────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
    // Animate stat cards
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(function(card, index) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(function() {
            card.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + index * 80);
    });

    // Animate cards
    const cards = document.querySelectorAll('.card, .employee-card');
    cards.forEach(function(card, index) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(15px)';
        setTimeout(function() {
            card.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 200 + index * 60);
    });
});
