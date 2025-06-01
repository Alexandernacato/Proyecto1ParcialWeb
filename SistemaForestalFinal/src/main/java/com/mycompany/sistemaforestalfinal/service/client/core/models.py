"""
🌳 Data Models
Modelos de datos para el sistema forestal
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TipoBosque(Enum):
    SECO = "Seco"
    HUMEDO_TROPICAL = "Húmedo Tropical"
    MONTANO = "Montano"
    MANGLAR = "Manglar"
    OTRO = "Otro"

    def get_display_name(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, text: str) -> 'TipoBosque':
        if text:
            for member in cls:
                if text.lower() == member.value.lower():
                    return member
        return cls.OTRO


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
    tipo_bosque: Optional[TipoBosque] = None  # Updated to use TipoBosque enum
    area_ha: float = 0.0
    activo: bool = True
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None


@dataclass
class ConservationState:
    """Modelo de datos para estados de conservación"""
    id: int
    nombre: str
    descripcion: Optional[str] = None
    nivel_riesgo: Optional[str] = None


@dataclass
class ZoneData:
    """Estructura de datos para zonas (compatibilidad con SOAP)"""
    id: int
    nombre: str
    tipo_bosque: str = ""
    area_ha: float = 0.0
    activo: bool = True


@dataclass
class SearchFilter:
    """Filtros para búsqueda de especies"""
    name_query: Optional[str] = None
    zone_id: Optional[int] = None
    conservation_state_id: Optional[int] = None
    active_only: Optional[bool] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
