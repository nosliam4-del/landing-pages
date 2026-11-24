#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera as paginas de afiliado a partir do conteudo verificado de cada produto.

Regra do projeto: so entra aqui o que foi conferido na pagina de pagamento ou
na pagina de vendas do produtor. Nada de afirmacao inventada.
"""

import hashlib
import io
import os

GTAG_ID = "AW-861487809"
GTAG_LABEL = "AW-861487809/cj40CJzvyL0dEMGF5ZoD"

# Precos lidos em 23/11/2026 da mesma API que o checkout da Kiwify consulta
# (checkout-api.kiwify.com.br/link/<slug>), nao de pagina de vendas.
# Primeiro valor: a vista. Segundo: parcelado, com o acrescimo que a
# plataforma cobra, e o total que o parcelamento da. None = sem parcelamento
# que valha a pena informar. slim30 e assinatura: a cobranca ja esta na ficha.
CONFERIDO_EM = "23 de novembro de 2026"

PRECOS = {
    "acessorios": ("R$ 297,00 \u00e0 vista, no Pix ou no cart\u00e3o",
                   "at\u00e9 12x de R$ 30,72 no cart\u00e3o, com acr\u00e9scimo \u2014 R$ 368,64 no total"),
    "adestramento-canino": ("R$ 397,00 \u00e0 vista, no Pix ou no cart\u00e3o",
                            "at\u00e9 12x de R$ 41,06 no cart\u00e3o, com acr\u00e9scimo \u2014 R$ 492,72 no total"),
    "automaquiagem": ("R$ 147,00 \u00e0 vista, no Pix ou no cart\u00e3o",
                      "at\u00e9 12x de R$ 15,20 no cart\u00e3o, com acr\u00e9scimo \u2014 R$ 182,40 no total"),
    "caderno-trt": ("R$ 449,00 \u00e0 vista, no Pix, no boleto ou no cart\u00e3o",
                    "at\u00e9 12x de R$ 46,44 no cart\u00e3o, com acr\u00e9scimo \u2014 R$ 557,28 no total"),
    "casamento": ("R$ 19,90, no Pix ou no cart\u00e3o", None),
    "ebook-herois-biblia": ("R$ 19,90, no Pix, no boleto ou no cart\u00e3o", None),
    "financas": ("R$ 27,00, no Pix ou no cart\u00e3o", None),
    "geladinhos": ("R$ 47,00, no Pix, no boleto ou no cart\u00e3o", None),
    "ingles-fluencia": ("R$ 997,00 \u00e0 vista, no Pix ou no cart\u00e3o",
                        "at\u00e9 12x de R$ 103,11 no cart\u00e3o, com acr\u00e9scimo \u2014 R$ 1.237,32 no total"),
    "nails": ("R$ 29,90, no Pix, no boleto ou no cart\u00e3o", None),
    "organizacao-casa": ("R$ 29,90, no Pix ou no cart\u00e3o", None),
    "pintura-residencial": ("R$ 129,90 \u00e0 vista, no Pix ou no cart\u00e3o",
                            "at\u00e9 12x de R$ 13,44 no cart\u00e3o, com acr\u00e9scimo \u2014 R$ 161,28 no total"),
    "resumos-concursos": ("R$ 297,90 \u00e0 vista, no Pix, no boleto ou no cart\u00e3o",
                          "at\u00e9 12x de R$ 30,81 no cart\u00e3o, com acr\u00e9scimo \u2014 R$ 369,72 no total"),
    "slim30": None,
}

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
<link rel="stylesheet" href="assets/pagina.css?v={cssv}">
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
{specnote}
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


def css_version():
    """Hash do CSS, para o navegador nao servir uma versao em cache."""
    css = io.open("assets/pagina.css", "rb").read()
    return hashlib.md5(css).hexdigest()[:8]


CSSV = None


def render(slug, p):
    linhas = list(p["spec"])
    specnote = ""
    pr = PRECOS.get(slug)
    if slug in PRECOS:
        specnote = (
            '  <p class="spec-note">Valores conferidos no checkout em {}. '
            'O valor final aparece no checkout antes de voc\u00ea confirmar.</p>\n'
        ).format(CONFERIDO_EM)
    if pr:
        avista, parcelado = pr
        # a linha antiga de preco remetia ao checkout; agora o valor esta aqui
        linhas = [(k, v) for k, v in linhas if k != "Pre\u00e7o"]
        topo = [("Pre\u00e7o", avista)]
        if parcelado:
            topo.append(("Parcelado", parcelado))
        linhas = topo + linhas

    spec = "\n".join(
        '    <div><dt>{}</dt><dd>{}</dd></div>'.format(k, v) for k, v in linhas
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
        specnote=specnote,
        flag=flag,
        sections=sections,
        faq=faq,
        closing=p["closing"],
        cssv=CSSV,
    )
    io.open(slug + ".html", "w", encoding="utf-8").write(html)
    return len(html)



# --------------------------------------------------------------------------
# Paginas que nao sao ficha de produto: a politica e o indice interno.
# Sem tag do Google Ads e sem botao de compra, so o mesmo design system.
# --------------------------------------------------------------------------

ACENTO_DOC = "#3f4a56"

TPL_DOC = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="icon" href="data:image/svg+xml,<svg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2032%2032'><rect%20width='32'%20height='32'%20rx='6'%20fill='{accent_enc}'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap">
<link rel="stylesheet" href="assets/pagina.css?v={cssv}">
<style>:root{{--accent:{accent};}}</style>
</head>
<body>
<div class="sheet doc">
  <h1>{h1}</h1>
  <p class="updated">{updated}</p>
{body}
  <footer>
{foot}
  </footer>
</div>
</body>
</html>
"""


def render_privacidade(d):
    corpo = '  <p class="abertura">{}</p>\n'.format(d["abertura"])
    for head, blocos in d["secoes"]:
        corpo += '\n  <section>\n    <h2>{}</h2>\n'.format(head)
        for b in blocos:
            if isinstance(b, list):
                corpo += "    <ul>\n"
                corpo += "".join("      <li>{}</li>\n".format(i) for i in b)
                corpo += "    </ul>\n"
            else:
                corpo += "    <p>{}</p>\n".format(b)
        corpo += "  </section>\n"

    html = TPL_DOC.format(
        title=esc_attr(d["titulo"]),
        desc=esc_attr(d["desc"]),
        robots="index, follow",
        accent=ACENTO_DOC,
        accent_enc=ACENTO_DOC.replace("#", "%23"),
        h1=d["titulo"],
        updated=d["atualizado"],
        body=corpo,
        foot='    <a href="index.html">Todas as páginas</a>',
        cssv=CSSV,
    )
    io.open("privacidade.html", "w", encoding="utf-8").write(html)
    return len(html)


def preco_curto(slug):
    """Valor de capa para o indice. Vem do mesmo PRECOS, para nao divergir."""
    if slug == "slim30":
        return "R$ 49,00 por mês"
    pr = PRECOS.get(slug)
    if not pr:
        return "—"
    import re
    m = re.search(r"R\$\s?[\d.]+,\d{2}", pr[0])
    return m.group(0) if m else "—"


def render_index(paginas):
    """O indice sai do proprio conteudo: nao da mais para esquecer uma pagina."""
    itens = sorted(
        ((p["title"].split(" — ")[0].strip(), slug) for slug, p in paginas.items()),
        key=lambda t: t[0].lower(),
    )
    lista = '  <nav class="cat">\n'
    for nome, slug in itens:
        lista += '    <a href="{}.html"><b>{}</b><span>{}</span></a>\n'.format(
            slug, nome, preco_curto(slug)
        )
    lista += "  </nav>\n"

    html = TPL_DOC.format(
        title="Páginas de destino",
        desc="Índice interno das páginas usadas nas campanhas.",
        robots="noindex",
        accent=ACENTO_DOC,
        accent_enc=ACENTO_DOC.replace("#", "%23"),
        h1="Páginas de destino",
        updated="{} páginas · valores conferidos no checkout em {}".format(
            len(itens), CONFERIDO_EM
        ),
        body=lista,
        foot='    <a href="privacidade.html">Política de Privacidade</a>',
        cssv=CSSV,
    )
    io.open("index.html", "w", encoding="utf-8").write(html)
    return len(html)

if __name__ == "__main__":
    from conteudo import PAGINAS, PRIVACIDADE

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    globals()["CSSV"] = css_version()
    print("css v{}\n".format(CSSV))

    for slug, p in PAGINAS.items():
        print("  {:<24} {:>6} bytes".format(slug + ".html", render(slug, p)))

    print("")
    print("  {:<24} {:>6} bytes".format("privacidade.html", render_privacidade(PRIVACIDADE)))
    print("  {:<24} {:>6} bytes".format("index.html", render_index(PAGINAS)))
    print("\n{} paginas de produto + 2 paginas de apoio.".format(len(PAGINAS)))
