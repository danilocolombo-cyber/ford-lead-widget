#!/usr/bin/env python3
"""Rigenera i file pubblicabili a partire da src/ford-lead-widget.js.

  python3 build.py

Produce:
  index.html                              pagina ospitata (GitHub Pages) da usare in un iframe con src
  dist/ford-lead-srcdoc-auto-qualify.html iframe "tutto dentro" per le landing auto
  dist/ford-lead-srcdoc-pro-qualify.html  iframe "tutto dentro" per le landing veicoli commerciali

Nessuna dipendenza: solo Python 3.
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).parent

# --- Impostazioni da modificare se cambiano ---------------------------------
FORM_ID = "umbraco_form_be2f4f1afda648c4bd1c14cc52ca592f"  # id del form Umbraco sulla stessa pagina
IFRAME_HEIGHT = 620                                          # altezza iniziale dell'iframe (px)
# -----------------------------------------------------------------------------

widget_js = (ROOT / "src" / "ford-lead-widget.js").read_text(encoding="utf-8")
widget_js = widget_js.replace("</script", "<\\/script")  # sicuro dentro un tag <script>

BOOT = """<script>
(function(){
  var d=document.createElement("div"); d.setAttribute("data-ford-lead-widget","");
  var P=new URLSearchParams(location.search), cfg={product:%(product)s,mode:%(mode)s,endpoint:"",privacy:"",phone:"",form:%(form)s,anchor:%(anchor)s};
  %(params)s
  d.setAttribute("data-product",cfg.product); d.setAttribute("data-mode",cfg.mode);
  ["endpoint","privacy","phone"].forEach(function(k){if(cfg[k])d.setAttribute("data-"+k,cfg[k]);});
  if(cfg.form) d.setAttribute("data-form-url",cfg.form);
  if(cfg.anchor) d.setAttribute("data-form-anchor",cfg.anchor);
  document.body.appendChild(d);
  d.addEventListener("ford-lead:complete",function(e){var x=e.detail;
    parent.postMessage({fordLead:"complete",segment:x.segment,score:x.score,product:x.product,tags:x.tags,summary:x.summary},"*");});
  function h(){parent.postMessage({fordLeadHeight:document.documentElement.scrollHeight},"*");}
  if(window.ResizeObserver) new ResizeObserver(h).observe(document.body); window.addEventListener("load",h);
})();
</script>"""


def page(product=None, mode=None, form="", anchor="", from_url=False):
    if from_url:
        values = dict(
            product='P.get("product")==="pro"?"pro":"auto"',
            mode='P.get("mode")==="qualify"?"qualify":"full"',
            form='""',
            anchor='""',
            params='["endpoint","privacy","phone","form","anchor"].forEach(function(k){if(P.get(k))cfg[k]=P.get(k);});',
        )
    else:
        values = dict(product='"%s"' % product, mode='"%s"' % mode,
                      form='"%s"' % form, anchor='"%s"' % anchor, params="")
    return (
        '<!DOCTYPE html>\n<html lang="it"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        "<title>Ford Interauto – richiedi informazioni</title>"
        "<style>html,body{margin:0;padding:4px;background:transparent}</style></head><body>\n"
        + BOOT % values
        + "\n<script>\n" + widget_js + "\n</script>\n</body></html>\n"
    )


# 1) Pagina ospitata: configurata dall'URL (?product=auto|pro&mode=qualify&form=...&anchor=...)
(ROOT / "index.html").write_text(page(from_url=True), encoding="utf-8")

# 2) Snippet "tutto dentro" (srcdoc), uno per versione
(ROOT / "dist").mkdir(exist_ok=True)
for product, title in (("auto", "Qualificazione auto Ford"), ("pro", "Qualificazione veicoli commerciali Ford")):
    src = html.escape(page(product, "qualify", "same", FORM_ID), quote=True)
    out = (
        "<!-- Ford Interauto: domande di qualificazione, poi il form Umbraco sulla stessa pagina.\n"
        "     Id del form: %s -->\n"
        '<iframe title="%s" style="width:100%%;border:0;height:%dpx" scrolling="auto" srcdoc="%s"></iframe>\n'
        % (FORM_ID, title, IFRAME_HEIGHT, src)
    )
    (ROOT / "dist" / ("ford-lead-srcdoc-%s-qualify.html" % product)).write_text(out, encoding="utf-8")

print("OK: index.html e dist/ rigenerati")
