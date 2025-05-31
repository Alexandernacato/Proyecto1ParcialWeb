"""
🌳 Data Models
Modelos de datos para el sistema forestal
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class TreeSpecies:
    """Modelo de datos para especies de árboles"""
    id: Optional[int] = None
    nombreComun: str = ""
    nombreCientifico: Optional[str] = None
    estadoConservacionId: int = 0
    estadoConservacionNombre: str = ""
    zonaId: int = 0
    zonaNombre: str = ""
    activo: bool = True
    fechaCreacion: Optional[datetime] = None
    fechaModificacion: Optional[datetime] = None


@dataclass
class Zone:
    """Modelo de datos para zonas"""
    id: int
    nombre: str
    descripcion: Optional[str] = None
    tipoBosque: Optional[str] = None
    areaHa: float = 0.0
    activo: bool = True
    fechaCreacion: Optional[datetime] = None
    fechaModificacion: Optional[datetime] = None


@dataclass
class ConservationState:
    """Modelo de datos para estados de conservación"""
    id: int
    nombre: str
    descripcion: Optional[str] = None
    nivel_riesgo: Optional[str] = None


@dataclass
class SearchFilter:
    """Filtros para búsqueda de especies"""
    name_query: Optional[str] = None
    zone_id: Optional[int] = None
    conservation_state_id: Optional[int] = None
    active_only: Optional[bool] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
