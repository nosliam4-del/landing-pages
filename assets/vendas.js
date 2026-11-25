/* Páginas de venda: entrada ao rolar, números que contam, preço com
   dígitos rolando, barra de progresso e barra fixa de compra no celular. */
(function () {
  var d = document;
  var reduz = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // preço com dígitos rolando
  var rolls = [].slice.call(d.querySelectorAll('.roll'));
  if (!reduz) rolls.forEach(function (el) {
    var v = el.textContent.trim();
    el.setAttribute('aria-label', v);
    el.textContent = '';
    v.split('').forEach(function (ch, k) {
      var s = d.createElement('span');
      s.setAttribute('aria-hidden', 'true');
      if (/\d/.test(ch)) {
        s.className = 'col';
        var st = d.createElement('span');
        st.className = 'strip';
        st.setAttribute('data-d', ch);
        st.style.transitionDelay = (k * 0.12) + 's';
        st.innerHTML = '<i>0</i><i>1</i><i>2</i><i>3</i><i>4</i><i>5</i><i>6</i><i>7</i><i>8</i><i>9</i>';
        s.appendChild(st);
      } else {
        s.textContent = ch;
      }
      el.appendChild(s);
    });
  });
  function rolar(el) {
    el.querySelectorAll('.strip').forEach(function (st) {
      st.style.transform = 'translateY(-' + (+st.getAttribute('data-d')) + 'em)';
    });
  }

  // números da faixa contando
  function contar(b) {
    var m = b.textContent.match(/^(\d+)(.*)$/);
    if (!m || reduz) return;
    var alvo = +m[1], resto = m[2], t0 = null;
    function passo(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / 1100);
      b.textContent = Math.round(alvo * (1 - Math.pow(1 - p, 3))) + resto;
      if (p < 1) requestAnimationFrame(passo);
    }
    requestAnimationFrame(passo);
  }

  // barra de progresso
  var pr = d.querySelector('.progress');
  if (pr) {
    var upd = function () {
      var h = d.documentElement.scrollHeight - window.innerHeight;
      pr.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, window.scrollY / h) : 0) + ')';
    };
    window.addEventListener('scroll', upd, { passive: true });
    upd();
  }

  if (!('IntersectionObserver' in window)) {
    rolls.forEach(rolar);
    return;
  }

  // barra fixa: aparece quando o botão do topo sai da tela
  var barra = d.getElementById('bar');
  var principal = d.querySelector('.cta.main');
  if (barra && principal) {
    new IntersectionObserver(function (e) {
      barra.classList.toggle('on', !e[0].isIntersecting && e[0].boundingClientRect.top < 0);
    }).observe(principal);
  }

  d.documentElement.classList.add('js');
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target;
      el.classList.add('in');
      if (el.classList.contains('stat')) contar(el.querySelector('b'));
      if (el.classList.contains('price-card')) rolls.forEach(function (r) { if (el.contains(r)) setTimeout(function () { rolar(r); }, 250); });
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -40px 0px' });
  d.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });
})();
