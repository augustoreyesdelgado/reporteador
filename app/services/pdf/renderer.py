import io, base64
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

env = Environment(
    loader=FileSystemLoader("app/templates"),
    autoescape=select_autoescape(["html", "xml"])
)

def _fig_to_data_uri(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=160)
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")

def chart_estatus_aprob_tramite(rows: List[Dict[str, Any]]) -> Optional[str]:
    # Sumamos 'aprobadas' y 'en_tramite' si existen; si no, regresamos None
    total_aprob = 5
    total_tram = 5
    have_data = False
    for r in rows:
        if "aprobadas" in r or "en_tramite" in r:
            have_data = True
        total_aprob += int(r.get("aprobadas", 0) or 0)
        total_tram  += int(r.get("en_tramite", 0) or 0)
    if not have_data:
        return None
    fig = plt.figure()
    ax = fig.gca()
    ax.bar(["Aprobadas","En trámite"], [total_aprob, total_tram])
    ax.set_ylabel("Total")
    ax.set_title("Estatus")
    return _fig_to_data_uri(fig)

def chart_tiempo_promedio(promedios_meses: Optional[Dict[str, float]]) -> str:
    # Si no mandan datos aún, usamos placeholders 0 que luego podrás cambiar
    pm = promedios_meses or {"Patentes": 8, "MU": 6.5, "DI": 3, "DA": 6}
    labels = ["Patentes","MU","DI","DA"]
    vals = [pm.get("Patentes",0), pm.get("MU",0), pm.get("DI",0), pm.get("DA",0)]
    fig = plt.figure()
    ax = fig.gca()
    ax.bar(labels, vals)
    ax.set_ylabel("Meses")
    ax.set_title("Tiempo promedio de aprobación")
    return _fig_to_data_uri(fig)

def chart_pie_por_tipo_tecnologico(rows: List[Dict[str, Any]]) -> Optional[str]:
    # Cuenta 'tipo' → Federal / Descentralizado
    counts = {"Federal": 0, "Descentralizado": 0}
    have_data = False
    for r in rows:
        tipo = str(r.get("tipo","")).strip()
        if tipo:
            have_data = True
            if tipo not in counts:
                counts[tipo] = 0
            counts[tipo] += 1
    if not have_data:
        return None
    labels = list(counts.keys())
    vals = list(counts.values())
    fig = plt.figure()
    ax = fig.gca()
    ax.pie(vals, labels=labels, autopct="%1.0f%%")
    ax.set_title("Federal vs Descentralizado")
    return _fig_to_data_uri(fig)

def chart_bar_por_tipo_pi(rows: List[Dict[str, Any]]) -> Optional[str]:
    # Suma totales por DA/MU/DI/MC
    keys = ["da","mu","di","mc"]
    totals = {k: 0 for k in keys}
    have_any = False
    for r in rows:
        for k in keys:
            if k in r:
                have_any = True
            try:
                totals[k] += int(r.get(k, 0) or 0)
            except (TypeError, ValueError):
                pass
    if not have_any:
        return None
    labels = ["DA","MU","DI","MC"]
    vals = [totals["da"], totals["mu"], totals["di"], totals["mc"]]
    fig = plt.figure()
    ax = fig.gca()
    ax.bar(labels, vals)
    ax.set_ylabel("Total")
    ax.set_title("Distribución por tipo de PI")
    return _fig_to_data_uri(fig)

def render_pdf_template(template_name: str, context: dict) -> bytes:
    template = env.get_template(template_name)
    html_str = template.render(**context)
    return HTML(string=html_str, base_url=".").write_pdf()
