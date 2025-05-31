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
        Inicializar el cliente SOAP
        
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
            bool: True si la conexión es exitosa, False en caso contrario
        """
        try:
            logger.info("Connecting to SOAP services...")
            
            # Conectar al servicio de zonas
            logger.info(f"Connecting to zones service: {self.zones_service_url}")
            self._zones_client = Client(self.zones_service_url)
            
            # Conectar al servicio de especies
            logger.info(f"Connecting to species service: {self.species_service_url}")
            self._species_client = Client(self.species_service_url)
            
            # Verificar conexiones con una consulta simple
            self._test_connections()
            
            self._is_connected = True
            logger.info("✅ Successfully connected to all SOAP services")
            return True
            
        except (TransportError, requests.exceptions.ConnectionError) as e:
            logger.error(f"❌ Connection error: {e}")
            self._is_connected = False
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
            bool: True si está conectado, False en caso contrario
        """
        return self._is_connected and self._zones_client is not None and self._species_client is not None

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
        
        try:
            logger.info(f"Fetching zone with ID: {zone_id}")
            response = self._zones_client.service.getZoneById(id=zone_id)
            
            if response:
                zone_data = ZoneData(
                    id=getattr(response, 'id', 0),
                    nombre=getattr(response, 'nombre', ''),
                    tipoBosque=getattr(response, 'tipoBosque', ''),
                    areaHa=float(getattr(response, 'areaHa', 0.0)) if getattr(response, 'areaHa', None) else 0.0,
                    activo=getattr(response, 'activo', True)
                )
                logger.info(f"Retrieved zone: {zone_data.nombre}")
                return zone_data
            
            logger.warning(f"Zone with ID {zone_id} not found")
            return None
            
        except Fault as e:
            logger.error(f"SOAP fault getting zone by ID: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error getting zone by ID: {e}")
            raise Exception(f"Failed to get zone: {e}")

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
        
        try:
            logger.info(f"Creating new zone: {nombre}")
            
            # Convertir areaHa a Decimal para el servicio Java
            from decimal import Decimal
            area_decimal = Decimal(str(areaHa))
            
            success = self._zones_client.service.createZone(
                nombre=nombre,
                tipoBosque=tipoBosque,
                areaHa=area_decimal,
                activo=activo
            )
            
            if success:
                logger.info(f"✅ Zone '{nombre}' created successfully")
            else:
                logger.warning(f"❌ Failed to create zone '{nombre}'")
                
            return success
            
        except Fault as e:
            logger.error(f"SOAP fault creating zone: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error creating zone: {e}")
            raise Exception(f"Failed to create zone: {e}")

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
        
        try:
            logger.info(f"Updating zone ID {zone_id}: {nombre}")
            
            # Convertir areaHa a Decimal para el servicio Java
            from decimal import Decimal
            area_decimal = Decimal(str(areaHa))
            
            success = self._zones_client.service.updateZone(
                id=zone_id,
                nombre=nombre,
                tipoBosque=tipoBosque,
                areaHa=area_decimal,
                activo=activo
            )
            
            if success:
                logger.info(f"✅ Zone ID {zone_id} updated successfully")
            else:
                logger.warning(f"❌ Failed to update zone ID {zone_id}")
                
            return success
            
        except Fault as e:
            logger.error(f"SOAP fault updating zone: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error updating zone: {e}")
            raise Exception(f"Failed to update zone: {e}")

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
        
        try:
            logger.info(f"Deleting zone ID: {zone_id}")
            success = self._zones_client.service.deleteZone(id=zone_id)
            
            if success:
                logger.info(f"✅ Zone ID {zone_id} deleted successfully")
            else:
                logger.warning(f"❌ Failed to delete zone ID {zone_id}")
                
            return success
            
        except Fault as e:
            logger.error(f"SOAP fault deleting zone: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error deleting zone: {e}")
            raise Exception(f"Failed to delete zone: {e}")

    # ==================== MÉTODOS PARA ESPECIES ====================

    def get_all_tree_species(self) -> List[TreeSpeciesData]:
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
            
            species_list = []
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
                    species_list.append(species_data)
            
            logger.info(f"Retrieved {len(species_list)} tree species")
            return species_list
            
        except Fault as e:
            logger.error(f"SOAP fault getting tree species: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error getting tree species: {e}")
            raise Exception(f"Failed to get tree species: {e}")

    def get_tree_species_by_id(self, species_id: int) -> Optional[TreeSpeciesData]:
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
            logger.info(f"Fetching tree species with ID: {species_id}")
            response = self._species_client.service.getTreeSpeciesById(id=species_id)
            
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
                logger.info(f"Retrieved species: {species_data.nombreComun}")
                return species_data
            
            logger.warning(f"Tree species with ID {species_id} not found")
            return None
            
        except Fault as e:
            logger.error(f"SOAP fault getting tree species by ID: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error getting tree species by ID: {e}")
            raise Exception(f"Failed to get tree species: {e}")

    def search_tree_species_by_name(self, name: str) -> List[TreeSpeciesData]:
        """
        Buscar especies por nombre (simulado con filtrado local)
        
        Args:
            name: Nombre a buscar
            
        Returns:
            List[TreeSpeciesData]: Lista de especies que coinciden
        """
        # Como el servicio no tiene un método específico de búsqueda, 
        # obtenemos todas y filtramos localmente
        all_species = self.get_all_tree_species()
        name_lower = name.lower()
        
        filtered_species = [
            species for species in all_species
            if name_lower in species.nombreComun.lower() or 
               name_lower in species.nombreCientifico.lower()
        ]
        
        logger.info(f"Found {len(filtered_species)} species matching '{name}'")
        return filtered_species

    def create_tree_species(self, common_name: str, scientific_name: str = "", 
                          conservation_state_id: int = 0, zone_id: int = 0, 
                          active: bool = True) -> bool:
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
            logger.info(f"Creating new tree species: {common_name}")
            success = self._species_client.service.createTreeSpecies(
                nombreComun=common_name,
                nombreCientifico=scientific_name,
                estadoConservacionId=conservation_state_id if conservation_state_id > 0 else None,
                zonaId=zone_id if zone_id > 0 else None,
                activo=active
            )
            
            if success:
                logger.info(f"✅ Tree species '{common_name}' created successfully")
            else:
                logger.warning(f"❌ Failed to create tree species '{common_name}'")
                
            return success
            
        except Fault as e:
            logger.error(f"SOAP fault creating tree species: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error creating tree species: {e}")
            raise Exception(f"Failed to create tree species: {e}")

    def update_tree_species(self, species_id: int, common_name: str, scientific_name: str = "", 
                          conservation_state_id: int = 0, zone_id: int = 0, 
                          active: bool = True) -> bool:
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
            logger.info(f"Updating tree species ID {species_id}: {common_name}")
            success = self._species_client.service.updateTreeSpecies(
                id=species_id,
                nombreComun=common_name,
                nombreCientifico=scientific_name,
                estadoConservacionId=conservation_state_id if conservation_state_id > 0 else None,
                zonaId=zone_id if zone_id > 0 else None,
                activo=active
            )
            
            if success:
                logger.info(f"✅ Tree species ID {species_id} updated successfully")
            else:
                logger.warning(f"❌ Failed to update tree species ID {species_id}")
                
            return success
            
        except Fault as e:
            logger.error(f"SOAP fault updating tree species: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error updating tree species: {e}")
            raise Exception(f"Failed to update tree species: {e}")

    def delete_tree_species(self, species_id: int) -> bool:
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
            logger.info(f"Deleting tree species ID: {species_id}")
            success = self._species_client.service.deleteTreeSpecies(id=species_id)
            
            if success:
                logger.info(f"✅ Tree species ID {species_id} deleted successfully")
            else:
                logger.warning(f"❌ Failed to delete tree species ID {species_id}")
                
            return success
            
        except Fault as e:
            logger.error(f"SOAP fault deleting tree species: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error deleting tree species: {e}")
            raise Exception(f"Failed to delete tree species: {e}")

    # ==================== MÉTODOS AUXILIARES ====================

    def get_all_conservation_states(self) -> List[ConservationStateData]:
        """
        Obtener todos los estados de conservación
        
        Returns:
            List[ConservationStateData]: Lista de estados de conservación
        """
        if not self.is_connected():
            raise Exception("Not connected to SOAP services")
        
        try:
            logger.info("Fetching all conservation states from SOAP service")
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
            
            logger.info(f"Retrieved {len(states)} conservation states")
            return states
            
        except Fault as e:
            logger.error(f"SOAP fault getting conservation states: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error getting conservation states: {e}")
            raise Exception(f"Failed to get conservation states: {e}")

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
                        areaHa=float(getattr(zone_obj, 'areaHa', 0.0)),
                        activo=True  # Asumimos activo desde el servicio de especies
                    )
                    zones.append(zone_data)
            
            logger.info(f"Retrieved {len(zones)} zones from species service")
            return zones
            
        except Fault as e:
            logger.error(f"SOAP fault getting zones from species service: {e}")
            raise Exception(f"SOAP service error: {e}")
        except Exception as e:
            logger.error(f"Error getting zones from species service: {e}")
            raise Exception(f"Failed to get zones from species service: {e}")

    # ==================== MÉTODOS DE DIAGNÓSTICO ====================

    def get_service_info(self) -> dict:
        """
        Obtener información de los servicios SOAP conectados
        
        Returns:
            dict: Información de los servicios
        """
        info = {
            "connected": self.is_connected(),
            "zones_service_url": self.zones_service_url,
            "species_service_url": self.species_service_url,
            "zones_client": self._zones_client is not None,
            "species_client": self._species_client is not None
        }
        
        if self.is_connected():
            try:
                # Obtener estadísticas básicas
                zones_count = len(self.get_all_zones())
                species_count = len(self.get_all_tree_species())
                states_count = len(self.get_all_conservation_states())
                
                info.update({
                    "zones_count": zones_count,
                    "species_count": species_count,
                    "conservation_states_count": states_count
                })
            except Exception as e:
                info["stats_error"] = str(e)
        
        return info


# Función de utilidad para crear una instancia configurada
def create_soap_client(zones_port: int = 8081, species_port: int = 8282) -> SOAPClientManager:
    """
    Crear una instancia de SOAPClientManager con configuración por defecto
    
    Args:
        zones_port: Puerto del servicio de zonas
        species_port: Puerto del servicio de especies
        
    Returns:
        SOAPClientManager: Instancia configurada del cliente SOAP
    """
    zones_url = f"http://localhost:{zones_port}/SistemaForestalFinal/ZoneCrudService?wsdl"
    species_url = f"http://localhost:{species_port}/SistemaForestalFinal/TreeSpeciesCrudService?wsdl"
    
    return SOAPClientManager(zones_url, species_url)


if __name__ == "__main__":
    # Prueba básica del cliente SOAP
    print("🌳 Testing SOAP Client Manager...")
    
    client = create_soap_client()
    
    if client.connect():
        print("✅ Connection successful!")
        
        # Mostrar información del servicio
        info = client.get_service_info()
        print(f"📊 Service info: {info}")
        
        # Prueba básica: obtener zonas
        try:
            zones = client.get_all_zones()
            print(f"🗺️ Found {len(zones)} zones")
            for zone in zones[:3]:  # Mostrar primeras 3
                print(f"  - {zone.nombre} ({zone.tipoBosque})")
        except Exception as e:
            print(f"❌ Error getting zones: {e}")
        
        # Prueba básica: obtener especies
        try:
            species = client.get_all_tree_species()
            print(f"🌲 Found {len(species)} tree species")
            for specie in species[:3]:  # Mostrar primeras 3
                print(f"  - {specie.nombreComun}")
        except Exception as e:
            print(f"❌ Error getting species: {e}")
        
        client.disconnect()
    else:
        print("❌ Connection failed!")