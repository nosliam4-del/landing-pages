/* v4 — acabamento das paginas de venda: abertura em duas colunas no
   computador, selo de produto digital, formas de pagamento, "Como funciona",
   chamada final e animacoes leves. Tudo gerado a partir do conteudo da pagina. */
(function () {
  var d = document;
  var sheet = d.querySelector('.sheet');
  if (!sheet) return;
  var h1 = sheet.querySelector(':scope > h1');
  var go = sheet.querySelector(':scope > .go');
  if (!h1 || !go) return;
  var img = sheet.querySelector(':scope > .hero');

  // formas de pagamento lidas da linha de preco
  var dd = sheet.querySelector('.spec dd');
  var t = (dd ? dd.textContent : '').toLowerCase();
  var pays = [];
  if (t.indexOf('pix') > -1) pays.push('Pix');
  if (t.indexOf('cartão') > -1 || t.indexOf('cartao') > -1) pays.push('Cartão');
  if (t.indexOf('boleto') > -1) pays.push('Boleto');

  // abertura: imagem + texto
  var intro = d.createElement('div');
  intro.className = 'intro';
  var text = d.createElement('div');
  text.className = 'intro-text';
  sheet.insertBefore(intro, h1);
  if (img) {
    var media = d.createElement('div');
    media.className = 'intro-media';
    media.appendChild(img);
    intro.appendChild(media);
  } else {
    intro.classList.add('no-media');
  }
  intro.appendChild(text);

  var kicker = d.createElement('span');
  kicker.className = 'kicker';
  kicker.textContent = 'Produto 100% digital';
  text.appendChild(kicker);

  var n = intro.nextElementSibling;
  while (n && !n.matches('.spec, section, .guarantee, .flag, .close, footer, .bar, script')) {
    var nx = n.nextElementSibling;
    text.appendChild(n);
    n = nx;
  }

  if (pays.length) {
    var pay = d.createElement('ul');
    pay.className = 'pay';
    pay.innerHTML = '<li class="pay-label">Aceita</li>' + pays.map(function (p) {
      return '<li>' + p + '</li>';
    }).join('');
    text.appendChild(pay);
  }

  // Como funciona
  var formas = pays.map(function (p) { return p === 'Pix' ? p : p.toLowerCase(); });
  var frase = formas.length > 1
    ? formas.slice(0, -1).join(', ') + ' ou ' + formas[formas.length - 1]
    : (formas[0] || 'a forma que preferir');
  var steps = d.createElement('section');
  steps.className = 'steps';
  steps.innerHTML =
    '<h2>Como funciona</h2><ol>' +
    '<li><b>1</b><strong>Clique no botão verde</strong><span>Você vai para o checkout seguro da Kiwify.</span></li>' +
    '<li><b>2</b><strong>Escolha como pagar</strong><span>Pague com ' + frase + '.</span></li>' +
    '<li><b>3</b><strong>Receba o acesso</strong><span>Os dados chegam no seu e-mail após a confirmação do pagamento.</span></li>' +
    '</ol>';
  var ref = sheet.querySelector(':scope > .guarantee') || sheet.querySelector(':scope > .close');
  if (ref) sheet.insertBefore(steps, ref);

  // chamada final
  var close = sheet.querySelector(':scope > .close');
  if (close) {
    var ct = d.createElement('p');
    ct.className = 'close-title';
    ct.textContent = 'Pronto para começar?';
    close.insertBefore(ct, close.firstChild);
    var trust = text.querySelector('.trust');
    if (trust) close.appendChild(trust.cloneNode(true));
  }

  if (!('IntersectionObserver' in window)) return;

  // barra fixa: aparece quando o botao principal sai da tela
  var barra = d.getElementById('bar');
  if (barra) {
    new IntersectionObserver(function (e) {
      barra.classList.toggle('on', !e[0].isIntersecting);
    }).observe(go);
  }

  // entrada suave dos blocos
  d.documentElement.classList.add('js');
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -40px 0px' });
  sheet.querySelectorAll(':scope > .spec, :scope > section, :scope > .guarantee, :scope > .flag, :scope > .close')
    .forEach(function (el) { el.classList.add('rv'); io.observe(el); });
})();

/* v5 — ilustracoes animadas: formas flutuando na faixa de cor, brilhos e
   halo na imagem, icones animados no "Como funciona", entrada em cascata
   e barra de progresso de leitura. */
(function () {
  var d = document;
  var sheet = d.querySelector('.sheet');
  if (!sheet) return;

  var deco = d.createElement('div');
  deco.className = 'deco';
  deco.setAttribute('aria-hidden', 'true');
  deco.innerHTML = '<i class="b b1"></i><i class="b b2"></i><i class="b b3"></i>' +
    '<i class="s s1">✦</i><i class="s s2">✦</i><i class="s s3">✦</i><i class="s s4">✦</i>';
  d.body.insertBefore(deco, d.body.firstChild);

  var media = sheet.querySelector('.intro-media');
  if (media) {
    var sp = d.createElement('span');
    sp.className = 'spark';
    sp.setAttribute('aria-hidden', 'true');
    sp.innerHTML = '<i>✦</i><i>✦</i><i>✦</i>';
    media.appendChild(sp);
  }

  var a = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"';
  var icons = [
    '<svg ' + a + '><circle class="r" cx="9" cy="9" r="4"/><path class="p" d="M9 9l5 12 1.8-5.2L21 14z"/></svg>',
    '<svg ' + a + '><g class="c"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/><path d="M6 15h4"/></g></svg>',
    '<svg ' + a + '><g class="m"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 6L2 7"/></g></svg>'
  ];
  sheet.querySelectorAll('.steps li').forEach(function (li, i) {
    var b = li.querySelector('b');
    if (!b || !icons[i]) return;
    var n = b.textContent;
    b.className = 'ico ico' + (i + 1);
    b.innerHTML = icons[i] + '<em>' + n + '</em>';
  });

  sheet.querySelectorAll('section ul, .steps ol, .spec').forEach(function (list) {
    Array.prototype.forEach.call(list.children, function (c, i) { c.style.setProperty('--i', i); });
  });

  var top = d.querySelector('.top');
  if (top) {
    var pr = d.createElement('div');
    pr.className = 'progress';
    top.appendChild(pr);
    var upd = function () {
      var h = d.documentElement.scrollHeight - window.innerHeight;
      pr.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, window.scrollY / h) : 0) + ')';
    };
    window.addEventListener('scroll', upd, { passive: true });
    upd();
  }
})();
