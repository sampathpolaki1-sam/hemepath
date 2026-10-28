// main.js - Core Application Utilities, State Management & Accessibility
(function() {
  window.HemeApp = {
    showToast: function(message, duration = 3000) {
      let container = document.getElementById('toast-container');
      if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
      }
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.innerHTML = `<span>🔔</span> <span>${message}</span>`;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 300);
      }, duration);
    },

    markLessonComplete: function(lessonId, btnElem) {
      fetch('/api/progress/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lesson_id: lessonId, status: 'completed' })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          HemeApp.showToast('✅ Lesson marked as Completed! Great job!');
          if (btnElem) {
            btnElem.textContent = 'Completed ✓';
            btnElem.classList.remove('btn-primary');
            btnElem.classList.add('btn-secondary');
            btnElem.disabled = true;
          }
        }
      })
      .catch(err => {
        HemeApp.showToast('⚠️ Progress saved locally.');
      });
    },

    saveNote: function(itemId, itemType, defaultTitle) {
      const noteText = prompt(`Save Note / Bookmark for "${defaultTitle}":`, '');
      if (noteText === null) return; // user cancelled

      fetch('/api/bookmarks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          item_id: String(itemId),
          item_type: itemType,
          title: defaultTitle,
          content: noteText
        })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          HemeApp.showToast('🔖 Saved to your Bookmarks & Notes!');
        }
      })
      .catch(() => {
        HemeApp.showToast('🔖 Saved locally.');
      });
    },

    readAloud: function(text) {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
        HemeApp.showToast('🔊 Reading summary aloud...');
      } else {
        HemeApp.showToast('Speech audio not supported on this device.');
      }
    }
  };

  // Theme Management
  function initTheme() {
    const root = document.documentElement;
    const savedTheme = localStorage.getItem('hemepath_theme') || 'light';
    root.setAttribute('data-theme', savedTheme);
    updateThemeUI(savedTheme);

    const btn = document.getElementById('theme-toggle-btn');
    if (btn) {
      btn.addEventListener('click', () => {
        const cur = root.getAttribute('data-theme') || 'light';
        const next = cur === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        localStorage.setItem('hemepath_theme', next);
        updateThemeUI(next);
      });
    }
  }

  function updateThemeUI(theme) {
    const icon = document.getElementById('theme-toggle-icon');
    const label = document.getElementById('theme-toggle-label');
    if (icon) icon.textContent = theme === 'dark' ? '☀️' : '🌙';
    if (label) label.textContent = theme === 'dark' ? 'Light' : 'Dark';
  }

  document.addEventListener('DOMContentLoaded', initTheme);
})();
