// chat.js - Topic-Limited MBBS Hematology Chatbot Interface
(function() {
  window.HemeChat = {
    currentMode: 'mbbs_exam',

    init: function() {
      const modeChips = document.querySelectorAll('.chat-mode-chip');
      modeChips.forEach(chip => {
        chip.addEventListener('click', () => {
          modeChips.forEach(c => c.classList.remove('active'));
          chip.classList.add('active');
          this.currentMode = chip.getAttribute('data-mode');
          HemeApp.showToast(`Switched mode to: ${chip.textContent.trim()}`);
        });
      });

      const input = document.getElementById('chat-input-field');
      if (input) {
        input.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') this.sendMessage();
        });
      }
    },

    setPrompt: function(text) {
      const input = document.getElementById('chat-input-field');
      if (input) {
        input.value = text;
        this.sendMessage();
      }
    },

    sendMessage: function() {
      const input = document.getElementById('chat-input-field');
      const text = input ? input.value.trim() : '';
      if (!text) return;

      input.value = '';
      this.appendBubble(text, 'user');

      // Add loading bubble
      const loadingId = 'loading-' + Date.now();
      this.appendLoading(loadingId);

      fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          mode: this.currentMode
        })
      })
      .then(res => res.json())
      .then(data => {
        this.removeLoading(loadingId);
        this.appendBubble(data.reply, 'bot', data.citations);
      })
      .catch(() => {
        this.removeLoading(loadingId);
        this.appendBubble('⚠️ Unable to connect to tutor service. Please check your connection.', 'bot');
      });
    },

    appendBubble: function(content, sender, citations = []) {
      const messagesContainer = document.getElementById('chat-messages-list');
      if (!messagesContainer) return;

      const bubble = document.createElement('div');
      bubble.className = `chat-bubble ${sender}`;

      // Convert basic markdown to html
      let formatted = content
        .replace(/### (.*?)\n/g, '<h4 style="margin:6px 0; font-size:14px; font-weight:700;">$1</h4>')
        .replace(/#### (.*?)\n/g, '<h5 style="margin:4px 0; font-size:13px; font-weight:600; color:var(--heme-indigo);">$1</h5>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n- /g, '<br>• ');

      // Citation tags
      if (citations && citations.length > 0) {
        formatted += `<div style="margin-top:8px; padding-top:6px; border-top:1px dashed rgba(255,255,255,0.15); font-size:10px; color:var(--text-muted);">
          📚 <strong>Sources</strong>: ${citations.join(', ')}
        </div>`;
      }

      bubble.innerHTML = formatted;
      messagesContainer.appendChild(bubble);
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    },

    appendLoading: function(id) {
      const messagesContainer = document.getElementById('chat-messages-list');
      if (!messagesContainer) return;
      const bubble = document.createElement('div');
      bubble.id = id;
      bubble.className = 'chat-bubble bot';
      bubble.innerHTML = `<em>Consulting medical literature...</em> <span style="animation:pulse 1s infinite;">⏳</span>`;
      messagesContainer.appendChild(bubble);
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    },

    removeLoading: function(id) {
      const el = document.getElementById(id);
      if (el) el.remove();
    },

    clearChat: function() {
      const list = document.getElementById('chat-messages-list');
      if (list) {
        list.innerHTML = `
          <div class="chat-bubble bot">
            <strong>👋 HemePath Tutor Cleared.</strong>
            <p style="font-size:12px; margin-top:4px;">How can I assist your hematology study today?</p>
          </div>
        `;
      }
    }
  };

  document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('chat-messages-list')) {
      HemeChat.init();
    }
  });
})();
