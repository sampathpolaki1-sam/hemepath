// device_scale.js - Handles Phone Frame Scaling, Device Switching & Laptop Responsive Mode
(function() {
  const root = document.documentElement;
  const body = document.body;

  // Initialize Clock in Phone Status Bar
  function updateStatusBarTime() {
    const timeElem = document.getElementById('status-bar-time');
    if (timeElem) {
      const now = new Date();
      const hours = now.getHours().toString().padStart(2, '0');
      const minutes = now.getMinutes().toString().padStart(2, '0');
      timeElem.textContent = `${hours}:${minutes}`;
    }
  }
  updateStatusBarTime();
  setInterval(updateStatusBarTime, 10000);

  // Theme Management
  const savedTheme = localStorage.getItem('hemepath_theme') || 'light';
  root.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  const themeBtn = document.getElementById('theme-toggle-btn');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const current = root.getAttribute('data-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('hemepath_theme', next);
      updateThemeIcon(next);
    });
  }

  function updateThemeIcon(theme) {
    const icon = document.getElementById('theme-toggle-icon');
    const label = document.getElementById('theme-toggle-label');
    if (icon) {
      icon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
    if (label) {
      label.textContent = theme === 'dark' ? 'Light' : 'Dark';
    }
  }

  // Device Mode: Phone vs Laptop
  const savedMode = localStorage.getItem('hemepath_device_mode') || 'phone';
  setDeviceMode(savedMode);

  const phoneModeBtn = document.getElementById('mode-btn-phone');
  const laptopModeBtn = document.getElementById('mode-btn-laptop');

  if (phoneModeBtn) {
    phoneModeBtn.addEventListener('click', () => setDeviceMode('phone'));
  }
  if (laptopModeBtn) {
    laptopModeBtn.addEventListener('click', () => setDeviceMode('laptop'));
  }

  function setDeviceMode(mode) {
    if (mode === 'laptop') {
      body.classList.add('mode-laptop');
      body.classList.remove('mode-phone');
      if (laptopModeBtn) laptopModeBtn.classList.add('active');
      if (phoneModeBtn) phoneModeBtn.classList.remove('active');
    } else {
      body.classList.add('mode-phone');
      body.classList.remove('mode-laptop');
      if (phoneModeBtn) phoneModeBtn.classList.add('active');
      if (laptopModeBtn) laptopModeBtn.classList.remove('active');
    }
    localStorage.setItem('hemepath_device_mode', mode);
  }

  // Scale Controls (75% to 125%)
  const savedScale = localStorage.getItem('hemepath_phone_scale') || '1';
  setPhoneScale(parseFloat(savedScale));

  const scaleBtns = document.querySelectorAll('.scale-btn');
  scaleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const scaleVal = parseFloat(btn.getAttribute('data-scale'));
      setPhoneScale(scaleVal);
    });
  });

  function setPhoneScale(scale) {
    root.style.setProperty('--phone-scale', scale);
    localStorage.setItem('hemepath_phone_scale', scale);

    scaleBtns.forEach(btn => {
      if (parseFloat(btn.getAttribute('data-scale')) === scale) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  }

  // Auto-detect genuine mobile devices
  if (window.innerWidth <= 640) {
    setDeviceMode('phone');
  }
})();
