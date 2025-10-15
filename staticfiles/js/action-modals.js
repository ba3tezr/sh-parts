// Modal and API utilities
window.app = window.app || {};

(function(app){
  function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  app.apiRequest = async function(url, options){
    options = options || {};
    const headers = Object.assign({ 'Accept': 'application/json' }, options.headers||{});
    if (!headers['Content-Type'] && options.body) headers['Content-Type'] = 'application/json';
    const csrftoken = getCookie('csrftoken');
    if (csrftoken) headers['X-CSRFToken'] = csrftoken;
    const resp = await fetch(url, Object.assign({}, options, { headers }));
    if (!resp.ok) {
      let msg = `HTTP ${resp.status}`;
      try { const data = await resp.json(); msg = data.detail || data.message || msg; } catch(e){}
      throw new Error(msg);
    }
    try { return await resp.json(); } catch(e){ return {}; }
  };

  app.showAlert = function(message, type){
    type = type || 'info';
    const alert = document.createElement('div');
    alert.className = `position-fixed top-0 start-50 translate-middle-x mt-3 alert alert-${type}`;
    alert.style.zIndex = 1080;
    alert.innerHTML = `${message}`;
    document.body.appendChild(alert);
    setTimeout(()=>{ alert.classList.add('show'); }, 10);
    setTimeout(()=>{ alert.classList.remove('show'); alert.remove(); }, 2500);
  };

  let activeModal = null;

  window.showFormModal = function(title, formHtml, onSubmit){
    closeModal();
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
<div class="modal fade" tabindex="-1">
  <div class="modal-dialog modal-lg modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">${title}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        ${formHtml}
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
        <button type="button" class="btn btn-primary" id="modalSubmitBtn">حفظ</button>
      </div>
    </div>
  </div>
</div>`;
    document.body.appendChild(wrapper);
    const modalEl = wrapper.querySelector('.modal');
    const modal = new bootstrap.Modal(modalEl, { backdrop: 'static' });
    activeModal = { wrapper, modal };
    modal.show();

    wrapper.querySelector('#modalSubmitBtn').addEventListener('click', async function(){
      const form = wrapper.querySelector('form');
      const fd = new FormData(form);
      try { await onSubmit(fd); modal.hide(); wrapper.remove(); activeModal=null; } catch(err){ app.showAlert(err.message || 'خطأ', 'danger'); }
    });

    modalEl.addEventListener('hidden.bs.modal', function(){ wrapper.remove(); if(activeModal&&activeModal.wrapper===wrapper) activeModal=null; });
  };

  window.showLoadingModal = function(message){
    closeModal();
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
<div class="modal fade" tabindex="-1">
  <div class="modal-dialog modal-sm modal-dialog-centered">
    <div class="modal-content" style="text-align:center; padding: 24px;">
      <div class="spinner-border text-primary" role="status"></div>
      <div class="mt-3">${message||'جارٍ التحميل...'}</div>
    </div>
  </div>
</div>`;
    document.body.appendChild(wrapper);
    const modalEl = wrapper.querySelector('.modal');
    const modal = new bootstrap.Modal(modalEl, { backdrop: 'static', keyboard: false });
    activeModal = { wrapper, modal };
    modal.show();
  };

  window.closeModal = function(){ if(activeModal){ activeModal.modal.hide(); activeModal.wrapper.remove(); activeModal=null; } };

})(window.app);


// Unified Action Modals API + confirm/info helpers
(function(){
  function buildModal(html){
    const wrapper = document.createElement('div');
    wrapper.innerHTML = html.trim();
    document.body.appendChild(wrapper);
    const modalEl = wrapper.querySelector('.modal');
    const modal = new bootstrap.Modal(modalEl, { backdrop: 'static' });
    modal.show();
    modalEl.addEventListener('hidden.bs.modal', function(){ wrapper.remove(); });
    return { wrapper, modal, modalEl };
  }

  // Info modal (success/warning/error)
  window.actionModals = window.actionModals || {};
  window.actionModals.showInfoModal = function(opts){
    const title = opts.title || 'Info';
    const message = opts.message || '';
    const type = opts.type || 'info';
    const okText = opts.okText || 'حسناً';
    const { modal, wrapper } = buildModal(`
      <div class="modal fade" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">${title}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <div class="alert alert-${type}">${message}</div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-primary" data-bs-dismiss="modal">${okText}</button>
            </div>
          </div>
        </div>
      </div>
    `);
    if (opts.onClose) {
      wrapper.querySelector('.modal').addEventListener('hidden.bs.modal', opts.onClose);
    }
    return modal;
  };

  // Simple dynamic form modal generator (options-based)
  window.actionModals.showFormModal = function(opts){
    const title = opts.title || '';
    const fields = Array.isArray(opts.fields) ? opts.fields : [];
    const submitText = opts.submitText || 'حفظ';
    const cancelText = opts.cancelText || 'إلغاء';

    function renderField(f){
      const name = f.name || '';
      const label = f.label || '';
      const type = (f.type||'text').toLowerCase();
      const required = f.required ? 'required' : '';
      const value = (f.value!=null ? f.value : '');
      if (type === 'select'){
        const optsHtml = (f.options||[]).map(o => `<option value="${o.value}">${o.label}</option>`).join('');
        return `
          <div class="mb-3">
            <label class="form-label" for="${name}">${label}</label>
            <select class="form-select" id="${name}" name="${name}" ${required}>${optsHtml}</select>
          </div>`;
      }
      return `
        <div class="mb-3">
          <label class="form-label" for="${name}">${label}</label>
          <input class="form-control" type="${type}" id="${name}" name="${name}" value="${value}" ${required} />
        </div>`;
    }

    const formHtml = `
      <form id="__dynForm">
        ${fields.map(renderField).join('')}
      </form>`;

    // Use the global form modal and adapt onSubmit signature
    window.showFormModal(title, formHtml, async function(fd){
      const data = {};
      fd.forEach((v,k)=>{ data[k]=v; });
      if (opts.onSubmit) return await opts.onSubmit(data);
    });

    // Swap footer button labels if provided
    try{
      const submitBtn = document.getElementById('modalSubmitBtn');
      if (submitBtn && submitText) submitBtn.textContent = submitText;
      const footer = submitBtn?.closest('.modal-footer');
      const cancelBtn = footer?.querySelector('[data-bs-dismiss="modal"]');
      if (cancelBtn && cancelText) cancelBtn.textContent = cancelText;
    }catch(e){}
  };


  // Confirm modal used by pages (e.g., vehicles delete)
  window.showConfirmModal = function(title, message, onConfirm){
    const { modal, wrapper } = buildModal(`
      <div class="modal fade" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">${title||'تأكيد'}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">${message||''}</div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
              <button type="button" class="btn btn-danger" id="__confirmBtn">تأكيد</button>
            </div>
          </div>
        </div>
      </div>
    `);
    wrapper.querySelector('#__confirmBtn').addEventListener('click', async function(){
      try { if (onConfirm) await onConfirm(); } finally { modal.hide(); }
    });
  };

  // Confirm modal that returns a Promise
  window.actionModals.showConfirmModal = function(opts){
    return new Promise((resolve) => {
      const title = opts.title || 'تأكيد';
      const message = opts.message || '';
      const confirmText = opts.confirmText || 'تأكيد';
      const cancelText = opts.cancelText || 'إلغاء';

      const { modal, wrapper } = buildModal(`
        <div class="modal fade" tabindex="-1">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">${title}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
              </div>
              <div class="modal-body">${message}</div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="__cancelBtn">${cancelText}</button>
                <button type="button" class="btn btn-danger" id="__confirmBtn">${confirmText}</button>
              </div>
            </div>
          </div>
        </div>
      `);

      wrapper.querySelector('#__confirmBtn').addEventListener('click', function(){
        modal.hide();
        resolve(true);
      });

      wrapper.querySelector('#__cancelBtn').addEventListener('click', function(){
        modal.hide();
        resolve(false);
      });

      wrapper.querySelector('.modal').addEventListener('hidden.bs.modal', function(){
        resolve(false);
      });
    });
  };

  // Loading helpers forwarders
  window.actionModals.showLoadingModal = function(message){ return window.showLoadingModal(message); };
  window.actionModals.hideLoadingModal = function(){ if (window.closeModal) window.closeModal(); };
})();
