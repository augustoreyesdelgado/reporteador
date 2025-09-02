from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.schemas.reports import ReportIn
from app.services.pdf.renderer import (
    render_pdf_template,
    chart_estatus_aprob_tramite,
    chart_tiempo_promedio,
    chart_pie_por_tipo_tecnologico,
    chart_bar_por_tipo_pi,
)

router = APIRouter(prefix="/v1/reports", tags=["reports"])

@router.post("", response_class=Response, responses={200: {"content": {"application/pdf": {}}}})
def create_report(payload: ReportIn):
    if payload.kind != "reporte_entidad_federativa":
        raise HTTPException(400, f"kind no soportado: {payload.kind}")

    required = {"institucion", "tipo", "patentes", "da", "mu", "di", "mc"}
    rows_models = payload.data
    for i, row in enumerate(rows_models):
        missing = required - set(row.model_dump().keys())
        if missing:
            raise HTTPException(422, f"Fila {i} incompleta: faltan {sorted(list(missing))}")

    rows = [r.model_dump() for r in rows_models]

    charts = {
        "estatus": chart_estatus_aprob_tramite(rows),                     # Aprobadas vs En trámite
        "tiempo_promedio": chart_tiempo_promedio(getattr(payload, "promedios_meses", None)),  # Meses (placeholder si no viene)
        "por_tipo_tec": chart_pie_por_tipo_tecnologico(rows),             # Federal vs Descentralizado
        "por_tipo_pi": chart_bar_por_tipo_pi(rows),                       # DA/MU/DI/MC
    }

    context = {
        "fecha": str(payload.fecha),
        "data": rows,
        "charts": charts,
    }
    pdf = render_pdf_template("reporte_entidad_federativa.html", context)
    return Response(pdf, media_type="application/pdf",
                    headers={"Content-Disposition": 'inline; filename="reporte_entidad_federativa.pdf"'})

# NUEVO endpoint (descarga directa)
@router.post("/download", response_class=Response)
def download_report(payload: ReportIn):
    if payload.kind != "reporte_entidad_federativa":
        raise HTTPException(400, f"kind no soportado: {payload.kind}")

    rows = [r.model_dump() for r in payload.data]

    charts = {
        "estatus": chart_estatus_aprob_tramite(rows),
        "tiempo_promedio": chart_tiempo_promedio(getattr(payload, "promedios_meses", None)),
        "por_tipo_tec": chart_pie_por_tipo_tecnologico(rows),
        "por_tipo_pi": chart_bar_por_tipo_pi(rows),
    }

    context = {"fecha": str(payload.fecha), "data": rows, "charts": charts}
    pdf = render_pdf_template("reporte_entidad_federativa.html", context)

    return Response(pdf, media_type="application/pdf",
                    headers={"Content-Disposition": 'attachment; filename="reporte_entidad_federativa.pdf"'})