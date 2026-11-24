#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera as paginas de afiliado a partir do conteudo verificado de cada produto.

Regra do projeto: so entra aqui o que foi conferido na pagina de pagamento ou
na pagina de vendas do produtor. Nada de afirmacao inventada.
"""

import io
import os

GTAG_ID = "AW-861487809"
GTAG_LABEL = "AW-861487809/cj40CJzvyL0dEMGF5ZoD"

TPL = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="icon" href="data:image/svg+xml,<svg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2032%2032'><rect%20width='32'%20height='32'%20rx='6'%20fill='{accent_enc}'/></svg>">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap">
<link rel="stylesheet" href="assets/pagina.css">
<style>:root{{--accent:{accent};}}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id={gtag_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{gtag_id}');

  function gtag_report_conversion(url) {{
    var callback = function () {{
      if (typeof(url) != 'undefined') {{
        window.location = url;
      }}
    }};
    gtag('event', 'conversion', {{
        'send_to': '{gtag_label}',
        'value': 1.0,
        'currency': 'BRL',
        'event_callback': callback
    }});
    return false;
  }}
</script>
</head>
<body>
<div class="sheet">
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>

  <a class="go" href="{link}" rel="nofollow sponsored" onclick="return gtag_report_conversion(this.href);">{cta}</a>
  <p class="under-go">{undergo}</p>

  <dl class="spec">
{spec}
  </dl>
{flag}{sections}
  <section>
    <h2>Perguntas frequentes</h2>
{faq}
  </section>

  <div class="close">
    <a class="go" href="{link}" rel="nofollow sponsored" onclick="return gtag_report_conversion(this.href);">{cta}</a>
    <p class="under-go">{closing}</p>
  </div>

  <footer>
    Esta página contém link de afiliado. Ao comprar por aqui, você paga o mesmo valor
    e podemos receber uma comissão pela indicação. Pagamento processado com segurança
    pela Kiwify.<br>
    <a href="privacidade.html">Política de Privacidade</a>
  </footer>
</div>

<div class="bar" id="bar">
  <a class="go" href="{link}" rel="nofollow sponsored" onclick="return gtag_report_conversion(this.href);">{cta}</a>
</div>

<script>
  // A barra fixa so aparece depois que o botao do topo sai da tela.
  (function () {{
    var alvo = document.querySelector('.sheet > .go');
    var barra = document.getElementById('bar');
    if (!alvo || !barra || !('IntersectionObserver' in window)) return;
    new IntersectionObserver(function (e) {{
      barra.classList.toggle('on', !e[0].isIntersecting);
    }}).observe(alvo);
  }})();
</script>
</body>
</html>
"""


def esc_attr(s):
    return s.replace('"', "&quot;")


def render(slug, p):
    spec = "\n".join(
        '    <div><dt>{}</dt><dd>{}</dd></div>'.format(k, v) for k, v in p["spec"]
    )

    sections = ""
    for head, items in p["sections"]:
        lis = "\n".join("      <li>{}</li>".format(i) for i in items)
        sections += (
            "\n  <section>\n    <h2>{}</h2>\n    <ul>\n{}\n    </ul>\n  </section>\n"
        ).format(head, lis)

    faq = "\n".join(
        "    <details><summary>{}</summary><p>{}</p></details>".format(q, a)
        for q, a in p["faq"]
    )

    flag = ""
    if p.get("flag"):
        t, b = p["flag"]
        flag = '\n  <div class="flag"><strong>{}</strong>{}</div>\n'.format(t, b)

    html = TPL.format(
        title=esc_attr(p["title"]),
        desc=esc_attr(p["desc"]),
        accent=p["accent"],
        accent_enc=p["accent"].replace("#", "%23"),
        gtag_id=GTAG_ID,
        gtag_label=GTAG_LABEL,
        h1=p["h1"],
        lead=p["lead"],
        link=p["link"],
        cta=p["cta"],
        undergo=p["undergo"],
        spec=spec,
        flag=flag,
        sections=sections,
        faq=faq,
        closing=p["closing"],
    )
    io.open(slug + ".html", "w", encoding="utf-8").write(html)
    return len(html)


if __name__ == "__main__":
    from conteudo import PAGINAS

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    total = 0
    for slug, p in PAGINAS.items():
        n = render(slug, p)
        total += 1
        print("  {:<24} {:>6} bytes".format(slug + ".html", n))
    print("\n{} paginas geradas.".format(total))
