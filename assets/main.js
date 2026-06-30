(() => {
  const getQueryLang = () => {
    try {
      const url = new URL(window.location.href);
      const v = (url.searchParams.get('lang') || '').toLowerCase();
      if (v === 'zh' || v === 'zh-cn' || v === 'cn') return 'zh';
      if (v === 'en' || v === 'en-us' || v === 'us') return 'en';
    } catch {
      // ignore
    }
    return null;
  };

  const getDefaultLang = () => {
    const q = getQueryLang();
    if (q) return q;

    const stored = (localStorage.getItem('lang') || '').toLowerCase();
    if (stored === 'zh' || stored === 'en') return stored;

    const nav = (navigator.language || '').toLowerCase();
    return nav.startsWith('zh') ? 'zh' : 'en';
  };

  const setLang = (lang) => {
    const safe = lang === 'zh' ? 'zh' : 'en';
    document.body.classList.toggle('lang-zh', safe === 'zh');
    document.body.classList.toggle('lang-en', safe === 'en');
    document.documentElement.lang = safe === 'zh' ? 'zh-CN' : 'en';
    localStorage.setItem('lang', safe);
  };

  setLang(getDefaultLang());

  const langToggle = document.getElementById('langToggle');
  if (langToggle) {
    langToggle.addEventListener('click', () => {
      const next = document.body.classList.contains('lang-zh') ? 'en' : 'zh';
      setLang(next);
    });
  }

  const parseRgb = (value) => {
    const match = String(value || '').match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/i);
    return match ? [Number(match[1]), Number(match[2]), Number(match[3])] : [255, 255, 255];
  };

  const pageIsDark = () => {
    const [r, g, b] = parseRgb(getComputedStyle(document.body).backgroundColor);
    return (r * 299 + g * 587 + b * 114) / 1000 < 128;
  };

  const updateActivityImages = () => {
    const dark = pageIsDark();
    document.querySelectorAll('.activity-thumb[data-light-src][data-dark-src]').forEach((img) => {
      const next = dark ? img.dataset.darkSrc : img.dataset.lightSrc;
      if (next && img.getAttribute('src') !== next) img.setAttribute('src', next);
    });
  };

  const getDefaultTheme = () => {
    const stored = (localStorage.getItem('theme') || '').toLowerCase();
    return stored === 'dark' ? 'dark' : 'light';
  };

  const setTheme = (theme) => {
    const safe = theme === 'dark' ? 'dark' : 'light';
    document.body.classList.toggle('theme-dark', safe === 'dark');
    localStorage.setItem('theme', safe);
    updateActivityImages();
  };

  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const next = document.body.classList.contains('theme-dark') ? 'light' : 'dark';
      setTheme(next);
    });
  }

  setTheme(getDefaultTheme());
  updateActivityImages();
  window.refreshActivityImages = updateActivityImages;
  const scheme = window.matchMedia?.('(prefers-color-scheme: dark)');
  if (scheme) scheme.addEventListener('change', updateActivityImages);
})();
