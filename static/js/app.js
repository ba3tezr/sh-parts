// Theme handling: apply and persist
(function(){
  var supportedThemes = ['dark-blue','light','day-blue','camel-dune','olive-sage'];
  function applyTheme(theme){
    if (supportedThemes.indexOf(theme) === -1) {
      theme = 'dark-blue';
    }
    var html = document.documentElement;
    var body = document.body;
    if(theme){
      html.setAttribute('data-theme', theme);
      body && body.setAttribute('data-theme', theme);
      try { localStorage.setItem('theme', theme); } catch(e){}
    }
    // toggle active dot
    document.querySelectorAll('.theme-btn').forEach(function(btn){
      var t = btn.getAttribute('data-theme');
      if(t === theme){ btn.classList.add('active'); } else { btn.classList.remove('active'); }
    });
  }
  document.addEventListener('DOMContentLoaded', function(){
    var saved = null;
    try { saved = localStorage.getItem('theme'); } catch(e){}
  applyTheme(saved || 'dark-blue');
    document.querySelectorAll('.theme-btn').forEach(function(btn){
      btn.addEventListener('click', function(){
        var t = btn.getAttribute('data-theme');
        applyTheme(t);
      });
    });
    // Sync currency symbol from server if provided on body dataset
    try {
      var sym = document.body && document.body.dataset && document.body.dataset.currencySymbol;
      if (sym && window.app && app.getSettings && app.setSettings) {
        var s = app.getSettings(); s.currency_symbol = sym; app.setSettings(s);
      }
    } catch(e){}
    // Wire language switch buttons if present
    document.querySelectorAll('.lang-btn').forEach(function(btn){
      btn.addEventListener('click', function(){
        var lang = btn.getAttribute('data-lang');
        if (window.app && app.setLanguage) app.setLanguage(lang);
      });
    });
  });
})();



// Global app helpers (formatting, settings)
window.app = window.app || {};

(function(app){
  app.getSettings = function(){
    try { return JSON.parse(localStorage.getItem('app_settings')) || {}; } catch(e){ return {}; }
  };
  app.setSettings = function(s){ try { localStorage.setItem('app_settings', JSON.stringify(s||{})); } catch(e){} };
  app.formatNumber = function(n){ try { return new Intl.NumberFormat(undefined, { maximumFractionDigits: 0 }).format(n||0); } catch(e){ return String(n||0); } };
  app.formatCurrency = function(a){ var sym = (app.getSettings()||{}).currency_symbol || (document.body && document.body.dataset && document.body.dataset.currencySymbol) || '﷼';
    try { return sym + ' ' + new Intl.NumberFormat(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 2 }).format(a||0); } catch(e){ return sym + ' ' + String(a||0); } };
  app.getCookie = function(name){
    const value = `; ${document.cookie}`; const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  };
  app.setLanguage = function(lang){
    try {
      fetch('/i18n/setlang/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': app.getCookie('csrftoken') },
        body: new URLSearchParams({ language: lang, next: window.location.pathname })
      }).then(function(){ window.location.reload(); });
    } catch(e){}
  };
})(window.app);


// Lightweight global loading and notifications used by pages
(function(app){
  let overlay = null;
  app.showLoading = function(message){
    if (!overlay){
      overlay = document.createElement('div');
      overlay.id = 'globalLoadingOverlay';
      overlay.style.cssText = 'position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.35);z-index:2000;';
      overlay.innerHTML = '<div class="text-center bg-dark text-white p-4 rounded"><div class="spinner-border text-info"></div><div class="mt-2">'+(message||'...')+'</div></div>';
      document.body.appendChild(overlay);
    }
  };
  app.hideLoading = function(){ if(overlay){ overlay.remove(); overlay=null; } };
  app.showNotification = function(message, type){ app.showAlert(message, type); };
})(window.app || (window.app = {}));
