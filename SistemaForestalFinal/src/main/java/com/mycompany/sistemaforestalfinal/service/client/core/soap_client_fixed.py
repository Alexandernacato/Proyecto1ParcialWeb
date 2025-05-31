"""
🌳 SOAP Client Manager
Gestiona la comunicación con los servicios SOAP del sistema forestal
"""

import logging
from typing import List, Optional, Any
from zeep import Client
from zeep.exceptions import Fault, TransportError
import requests.exceptions
from dataclasses import dataclass

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ZoneData:
    """Estructura de datos para zonas"""
    id: int
    nombre: str
    tipoBosque: str = ""
    areaHa: float = 0.0
    activo: bool = True


@dataclass 
class TreeSpeciesData:
    """Estructura de datos para especies"""
    id: int
    nombreComun: str
    nombreCientifico: str = ""
    estadoConservacionId: int = 0
    estadoConservacionNombre: str = ""
    zonaId: int = 0
    zonaNombre: str = ""
    activo: bool = True


@dataclass
class ConservationStateData:
    """Estructura de datos para estados de conservación"""
    id: int
    nombre: str
    descripcion: str = ""


class SOAPClientManager:
    """
    Gestor de cliente SOAP para comunicación con servicios forestales.
    Maneja conexiones a los servicios de zonas y especies.
    """
    
    def __init__(self,
                 zones_service_url: str = "http://localhost:8081/SistemaForestalFinal/ZoneCrudService?wsdl",
                 species_service_url: str = "http://localhost:8282/TreeSpeciesCrudService?wsdl"):
        """
        Inicializar el gestor de clientes SOAP
        
        Args:
            zones_service_url: URL del servicio SOAP de zonas
            species_service_url: URL del servicio SOAP de especies
        """
        self.zones_service_url = zones_service_url
        self.species_service_url = species_service_url
        self._zones_client = None
        self._species_client = None
        self._is_connected = False
        
        logger.info("SOAPClientManager initialized")

    def connect(self) -> bool:
        """
        Establecer conexión con los servicios SOAP
        
        Returns:
            bool: True si al menos un servicio está disponible
        """
        try:
            logger.info("Connecting to SOAP services...")
            
            zones_connected = False
            species_connected = False
            
            # Intentar conectar al servicio de zonas
            try:
                logger.info(f"Connecting to zones service: {self.zones_service_url}")
                self._zones_client = Client(self.zones_service_url)
                zones_connected = True
                logger.info("✅ Zones service connected")
            except (TransportError, requests.exceptions.ConnectionError) as e:
                logger.warning(f"⚠️ Zones service not available: {e}")
                self._zones_client = None
            
            # Intentar conectar al servicio de especies
            try:
                logger.info(f"Connecting to species service: {self.species_service_url}")
                self._species_client = Client(self.species_service_url)
                species_connected = True
                logger.info("✅ Species service connected")
            except (TransportError, requests.exceptions.ConnectionError) as e:
                logger.error(f"❌ Species service connection error: {e}")
                self._species_client = None
            
            # Considerar conexión exitosa si al menos especies está disponible
            self._is_connected = species_connected
            
            if self._is_connected:
                if zones_connected and species_connected:
                    logger.info("✅ Successfully connected to all SOAP services")
                elif species_connected:
                    logger.info("✅ Connected to species service (zones service unavailable)")
                return True
            else:
                logger.error("❌ Failed to connect to any SOAP services")
                return False
                
        except Exception as e:
            logger.error(f"❌ Unexpected error during connection: {e}")
            self._is_connected = False
            return False

    def _test_connections(self):
        """Probar las conexiones con consultas simples"""
        try:
            # Probar servicio de zonas
            if self._zones_client:
                self._zones_client.service.getAllZones()
            
            # Probar servicio de especies  
            if self._species_client:
                self._species_client.service.getAllTreeSpecies()
                
        except Exception as e:
            logger.warning(f"Connection test warning: {e}")
            # No lanzar error aquí, solo advertir

    def is_connected(self) -> bool:
        """
        Verificar si está conectado a los servicios SOAP
        
        Returns:
            bool: True si está conectado al menos al servicio de especies
        """
        return self._is_connected and self._species_client is not None

    def disconnect(self):
        """Desconectar de los servicios SOAP"""
        self._zones_client = None
        self._species_client = None
        self._is_connected = False
        logger.info("Disconnected from SOAP services")

    # ==================== MÉTODOS PARA ZONAS ====================
    
    def get_all_zones(self) -> List[ZoneData]:
        """
        Obtener todas las zonas
        
        Returns:
            List[ZoneData]: Lista de zonas disponibles
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        if not self._zones_client:
            logger.warning("Zones service not available, trying species service")
            return self.get_zones_from_species_service()
        
        try:
            logger.info("Fetching all zones from SOAP service")
            response = self._zones_client.service.getAllZones()
            
            zones = []
            if response:
                for zone_obj in response:
                    zone_data = ZoneData(
                        id=getattr(zone_obj, 'id', 0),
                        nombre=getattr(zone_obj, 'nombre', ''),
                        tipoBosque=getattr(zone_obj, 'tipoBosque', ''),
                        areaHa=float(getattr(zone_obj, 'areaHa', 0.0)) if getattr(zone_obj, 'areaHa', None) else 0.0,
                        activo=getattr(zone_obj, 'activo', True)
                    )
                    zones.append(zone_data)
            
            logger.info(f"Retrieved {len(zones)} zones")
            return zones
            
        except Fault as e:
            logger.error(f"SOAP fault getting zones: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error getting zones: {e}")
            raise Exception(f"Failed to get zones: {e}")

    def get_zone_by_id(self, zone_id: int) -> Optional[ZoneData]:
        """
        Obtener zona por ID
        
        Args:
            zone_id: ID de la zona
        
        Returns:
            Optional[ZoneData]: Datos de la zona o None si no existe
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        if not self._zones_client:
            logger.warning("Zones service not available")
            return None
        
        try:
            logger.info(f"Fetching zone with ID {zone_id}")
            response = self._zones_client.service.getZoneById(zone_id)
            
            if response:
                zone_data = ZoneData(
                    id=getattr(response, 'id', 0),
                    nombre=getattr(response, 'nombre', ''),
                    tipoBosque=getattr(response, 'tipoBosque', ''),
                    areaHa=float(getattr(response, 'areaHa', 0.0)) if getattr(response, 'areaHa', None) else 0.0,
                    activo=getattr(response, 'activo', True)
                )
                return zone_data
            return None
            
        except Fault as e:
            logger.error(f"SOAP fault getting zone {zone_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting zone {zone_id}: {e}")
            return None

    def create_zone(self, nombre: str, tipoBosque: str, areaHa: float, activo: bool = True) -> bool:
        """
        Crear nueva zona
        
        Args:
            nombre: Nombre de la zona
            tipoBosque: Tipo de bosque
            areaHa: Área en hectáreas
            activo: Estado activo de la zona
        
        Returns:
            bool: True si la creación fue exitosa
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        if not self._zones_client:
            logger.error("Zones service not available for zone creation")
            return False
        
        try:
            logger.info(f"Creating zone: {nombre}")
            response = self._zones_client.service.createZone(
                nombre=nombre,
                tipoBosque=tipoBosque,
                areaHa=areaHa,
                activo=activo
            )
            return bool(response)
            
        except Fault as e:
            logger.error(f"SOAP fault creating zone: {e}")
            return False
        except Exception as e:
            logger.error(f"Error creating zone: {e}")
            return False

    def update_zone(self, zone_id: int, nombre: str, tipoBosque: str, areaHa: float, activo: bool = True) -> bool:
        """
        Actualizar zona existente
        
        Args:
            zone_id: ID de la zona a actualizar
            nombre: Nuevo nombre de la zona
            tipoBosque: Nuevo tipo de bosque
            areaHa: Nueva área en hectáreas
            activo: Estado activo de la zona
        
        Returns:
            bool: True si la actualización fue exitosa
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        if not self._zones_client:
            logger.error("Zones service not available for zone update")
            return False
        
        try:
            logger.info(f"Updating zone {zone_id}")
            response = self._zones_client.service.updateZone(
                id=zone_id,
                nombre=nombre,
                tipoBosque=tipoBosque,
                areaHa=areaHa,
                activo=activo
            )
            return bool(response)
            
        except Fault as e:
            logger.error(f"SOAP fault updating zone: {e}")
            return False
        except Exception as e:
            logger.error(f"Error updating zone: {e}")
            return False

    def delete_zone(self, zone_id: int) -> bool:
        """
        Eliminar zona (borrado lógico)
        
        Args:
            zone_id: ID de la zona a eliminar
        
        Returns:
            bool: True si la eliminación fue exitosa
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        if not self._zones_client:
            logger.error("Zones service not available for zone deletion")
            return False
        
        try:
            logger.info(f"Deleting zone {zone_id}")
            response = self._zones_client.service.deleteZone(zone_id)
            return bool(response)
            
        except Fault as e:
            logger.error(f"SOAP fault deleting zone: {e}")
            return False
        except Exception as e:
            logger.error(f"Error deleting zone: {e}")
            return False

    # ==================== MÉTODOS PARA ESPECIES ====================
    
    def get_all_species(self) -> List[TreeSpeciesData]:
        """
        Obtener todas las especies de árboles
        
        Returns:
            List[TreeSpeciesData]: Lista de especies disponibles
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        try:
            logger.info("Fetching all tree species from SOAP service")
            response = self._species_client.service.getAllTreeSpecies()
            
            species = []
            if response:
                for species_obj in response:
                    species_data = TreeSpeciesData(
                        id=getattr(species_obj, 'id', 0),
                        nombreComun=getattr(species_obj, 'nombreComun', ''),
                        nombreCientifico=getattr(species_obj, 'nombreCientifico', ''),
                        estadoConservacionId=getattr(species_obj, 'estadoConservacionId', 0),
                        estadoConservacionNombre=getattr(species_obj, 'estadoConservacionNombre', ''),
                        zonaId=getattr(species_obj, 'zonaId', 0),
                        zonaNombre=getattr(species_obj, 'zonaNombre', ''),
                        activo=getattr(species_obj, 'activo', True)
                    )
                    species.append(species_data)
            
            logger.info(f"Retrieved {len(species)} species")
            return species
            
        except Fault as e:
            logger.error(f"SOAP fault getting species: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error getting species: {e}")
            raise Exception(f"Failed to get species: {e}")

    def get_species_by_id(self, species_id: int) -> Optional[TreeSpeciesData]:
        """
        Obtener especie por ID
        
        Args:
            species_id: ID de la especie
        
        Returns:
            Optional[TreeSpeciesData]: Datos de la especie o None si no existe
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        try:
            logger.info(f"Fetching species with ID {species_id}")
            response = self._species_client.service.getTreeSpeciesById(species_id)
            
            if response:
                species_data = TreeSpeciesData(
                    id=getattr(response, 'id', 0),
                    nombreComun=getattr(response, 'nombreComun', ''),
                    nombreCientifico=getattr(response, 'nombreCientifico', ''),
                    estadoConservacionId=getattr(response, 'estadoConservacionId', 0),
                    estadoConservacionNombre=getattr(response, 'estadoConservacionNombre', ''),
                    zonaId=getattr(response, 'zonaId', 0),
                    zonaNombre=getattr(response, 'zonaNombre', ''),
                    activo=getattr(response, 'activo', True)
                )
                return species_data
            return None
            
        except Fault as e:
            logger.error(f"SOAP fault getting species {species_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting species {species_id}: {e}")
            return None

    def search_species_by_name(self, name: str) -> List[TreeSpeciesData]:
        """
        Buscar especies por nombre (simulado con filtrado local)
        
        Args:
            name: Nombre a buscar
        
        Returns:
            List[TreeSpeciesData]: Lista de especies que coinciden
        """
        try:
            all_species = self.get_all_species()
            filtered_species = [
                species for species in all_species
                if name.lower() in species.nombreComun.lower() or 
                   name.lower() in species.nombreCientifico.lower()
            ]
            return filtered_species
        except Exception as e:
            logger.error(f"Error searching species: {e}")
            return []

    def create_species(self, common_name: str, scientific_name: str, 
                      conservation_state_id: int, zone_id: int, active: bool = True) -> bool:
        """
        Crear nueva especie de árbol
        
        Args:
            common_name: Nombre común de la especie
            scientific_name: Nombre científico
            conservation_state_id: ID del estado de conservación
            zone_id: ID de la zona
            active: Estado activo de la especie
        
        Returns:
            bool: True si la creación fue exitosa
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        try:
            logger.info(f"Creating species: {common_name}")
            response = self._species_client.service.createTreeSpecies(
                nombreComun=common_name,
                nombreCientifico=scientific_name,
                estadoConservacionId=conservation_state_id,
                zonaId=zone_id,
                activo=active
            )
            return bool(response)
            
        except Fault as e:
            logger.error(f"SOAP fault creating species: {e}")
            return False
        except Exception as e:
            logger.error(f"Error creating species: {e}")
            return False

    def update_species(self, species_id: int, common_name: str, scientific_name: str,
                      conservation_state_id: int, zone_id: int, active: bool = True) -> bool:
        """
        Actualizar especie de árbol existente
        
        Args:
            species_id: ID de la especie a actualizar
            common_name: Nuevo nombre común
            scientific_name: Nuevo nombre científico
            conservation_state_id: Nuevo ID del estado de conservación
            zone_id: Nuevo ID de la zona
            active: Estado activo de la especie
        
        Returns:
            bool: True si la actualización fue exitosa
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        try:
            logger.info(f"Updating species {species_id}")
            response = self._species_client.service.updateTreeSpecies(
                id=species_id,
                nombreComun=common_name,
                nombreCientifico=scientific_name,
                estadoConservacionId=conservation_state_id,
                zonaId=zone_id,
                activo=active
            )
            return bool(response)
            
        except Fault as e:
            logger.error(f"SOAP fault updating species: {e}")
            return False
        except Exception as e:
            logger.error(f"Error updating species: {e}")
            return False

    def delete_species(self, species_id: int) -> bool:
        """
        Eliminar especie de árbol (borrado lógico)
        
        Args:
            species_id: ID de la especie a eliminar
        
        Returns:
            bool: True si la eliminación fue exitosa
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        try:
            logger.info(f"Deleting species {species_id}")
            response = self._species_client.service.deleteTreeSpecies(species_id)
            return bool(response)
            
        except Fault as e:
            logger.error(f"SOAP fault deleting species: {e}")
            return False
        except Exception as e:
            logger.error(f"Error deleting species: {e}")
            return False

    # ==================== MÉTODOS AUXILIARES ====================
    
    def get_conservation_states(self) -> List[ConservationStateData]:
        """
        Obtener todos los estados de conservación
        
        Returns:
            List[ConservationStateData]: Lista de estados de conservación
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        try:
            logger.info("Fetching conservation states")
            response = self._species_client.service.getAllConservationStates()
            
            states = []
            if response:
                for state_obj in response:
                    state_data = ConservationStateData(
                        id=getattr(state_obj, 'id', 0),
                        nombre=getattr(state_obj, 'nombre', ''),
                        descripcion=getattr(state_obj, 'descripcion', '')
                    )
                    states.append(state_data)
            
            return states
            
        except Fault as e:
            logger.error(f"SOAP fault getting conservation states: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting conservation states: {e}")
            return []

    def get_zones_from_species_service(self) -> List[ZoneData]:
        """
        Obtener zonas desde el servicio de especies (método auxiliar)
        
        Returns:
            List[ZoneData]: Lista de zonas desde el servicio de especies
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        try:
            logger.info("Fetching zones from species service")
            response = self._species_client.service.getAllZones()
            
            zones = []
            if response:
                for zone_obj in response:
                    zone_data = ZoneData(
                        id=getattr(zone_obj, 'id', 0),
                        nombre=getattr(zone_obj, 'nombre', ''),
                        tipoBosque=getattr(zone_obj, 'tipoBosque', ''),
                        areaHa=float(getattr(zone_obj, 'areaHa', 0.0)) if getattr(zone_obj, 'areaHa', None) else 0.0,
                        activo=getattr(zone_obj, 'activo', True)
                    )
                    zones.append(zone_data)
            
            return zones
            
        except Fault as e:
            logger.error(f"SOAP fault getting zones from species service: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting zones from species service: {e}")
            return []

    def get_service_info(self) -> dict:
        """
        Obtener información de los servicios SOAP conectados
        
        Returns:
            dict: Información de los servicios
        """
        return {
            'zones_service_url': self.zones_service_url,
            'species_service_url': self.species_service_url,
            'zones_connected': self._zones_client is not None,
            'species_connected': self._species_client is not None,
            'is_connected': self._is_connected
        }


# ==================== FUNCIÓN DE UTILIDAD ====================

def create_default_soap_client(zones_port: int = 8081, species_port: int = 8282) -> SOAPClientManager:
    """
    Crear una instancia de SOAPClientManager con configuración por defecto
    
    Args:
        zones_port: Puerto del servicio de zonas
        species_port: Puerto del servicio de especies
    
    Returns:
        SOAPClientManager: Instancia configurada del cliente SOAP
    """
    zones_url = f"http://localhost:{zones_port}/SistemaForestalFinal/ZoneCrudService?wsdl"
    species_url = f"http://localhost:{species_port}/TreeSpeciesCrudService?wsdl"
    
    return SOAPClientManager(zones_url, species_url)
