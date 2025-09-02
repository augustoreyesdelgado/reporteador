from typing import Literal, List, Optional, Dict
from datetime import date
from pydantic import BaseModel, Field

class ReportAdminRow(BaseModel):
    institucion: str = Field(..., description="Nombre de la institución")
    tipo: str = Field(..., description="Federal o Descentralizado")
    patentes: int = 0
    da: int = 0
    mu: int = 0
    di: int = 0
    mc: int = 0
    # opcionales para #1 (estatus)
    aprobadas: int = 0
    en_tramite: int = 0

class ReportAdminIn(BaseModel):
    kind: Literal["reporte_entidad_federativa"]
    fecha: date
    data: List[ReportAdminRow]
    # opcional para #2 (tiempo promedio en meses por tipo)
    # keys: "da","mu","di","mc"
    promedios_meses: Optional[Dict[str, float]] = None

ReportIn = ReportAdminIn
