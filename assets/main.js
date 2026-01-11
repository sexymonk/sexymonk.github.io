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

  const btn = document.getElementById('printBtn');
  if (btn) btn.addEventListener('click', () => window.print());

  const langToggle = document.getElementById('langToggle');
  if (langToggle) {
    langToggle.addEventListener('click', () => {
      const next = document.body.classList.contains('lang-zh') ? 'en' : 'zh';
      setLang(next);
    });
  }
})();
