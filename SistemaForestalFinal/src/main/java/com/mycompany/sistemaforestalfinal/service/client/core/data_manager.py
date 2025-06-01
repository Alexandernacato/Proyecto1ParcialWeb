"""
🌳 Data Manager
Gestor de datos para el sistema forestal con operaciones CRUD completas
"""

import time
from typing import List, Optional, Dict, Any, Callable
from datetime import datetime

# Simulamos el cliente SOAP para desarrollo
try:
    from zeep import Client
    from zeep.exceptions import Fault
    SOAP_AVAILABLE = True
except ImportError:
    SOAP_AVAILABLE = False
    Client = None
    Fault = Exception

from .models import TreeSpecies, Zone, ConservationState, SearchFilter, TipoBosque, ZoneData


class DataManager:
    """Gestor de datos con comunicación SOAP y cache local"""
    
    def __init__(self, base_url: str = "http://localhost:8282"):
        self.base_url = base_url
        self.client = None
        self.species_cache = {}
        self.zones_cache = {}
        self.conservation_states_cache = {}
        self.cache_timestamp = {}
        self.cache_ttl = 300  # 5 minutos
        
        # URLs de los servicios SOAP actualizadas para coincidir con los servicios ejecutándose
        self.species_service_url = "http://localhost:8282/TreeSpeciesCrudService?wsdl"
        self.zone_service_url = "http://localhost:8081/SistemaForestalFinal/ZoneCrudService?wsdl" 
        self.conservation_service_url = "http://localhost:8282/TreeSpeciesCrudService?wsdl"  # Conservation states from species service
        
        self._init_soap_clients()
    
    def _init_soap_clients(self):
        """Inicializa los clientes SOAP"""
        if not SOAP_AVAILABLE:
            print("⚠️  SOAP no disponible - modo simulación")
            return
        
        try:
            self.species_client = Client(self.species_service_url)
            self.zone_client = Client(self.zone_service_url)
            self.conservation_client = Client(self.conservation_service_url)
            print("✅ Clientes SOAP inicializados")
        except Exception as e:
            print(f"⚠️  Error al conectar con SOAP: {e}")
            self.species_client = None
            self.zone_client = None
            self.conservation_client = None
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Verifica si el cache está válido"""
        if cache_key not in self.cache_timestamp:
            return False
        return (time.time() - self.cache_timestamp[cache_key]) < self.cache_ttl
    
    def _invalidate_cache(self, cache_key: str):
        """Invalida el cache específico"""
        if cache_key in self.cache_timestamp:
            del self.cache_timestamp[cache_key]
        
        if cache_key == 'species' and 'species' in self.species_cache:
            del self.species_cache['species']
        elif cache_key == 'zones' and 'zones' in self.zones_cache:
            del self.zones_cache['zones']
        elif cache_key == 'conservation_states' and 'conservation_states' in self.conservation_states_cache:
            del self.conservation_states_cache['conservation_states']
    
    # ===========================================
    # OPERACIONES DE ESPECIES
    # ===========================================
    
    def get_species(self, force_refresh: bool = False) -> List[TreeSpecies]:
        """Obtiene todas las especies de árboles"""
        cache_key = 'species'
        
        if not force_refresh and self._is_cache_valid(cache_key) and cache_key in self.species_cache:
            return self.species_cache[cache_key]
        
        try:
            if self.species_client:
                response = self.species_client.service.getAllTreeSpecies()
                species_list = self._convert_soap_response_to_species(response)
            else:
                print("⚠️  SOAP client not available - cannot load species")
                species_list = []
            
            self.species_cache[cache_key] = species_list
            self.cache_timestamp[cache_key] = time.time()
            return species_list
            
        except Exception as e:
            print(f"❌ Error al obtener especies: {e}")
            return []
    
    def create_species(self, species: TreeSpecies, callback: Callable = None) -> bool:
        """Crea una nueva especie"""
        try:
            if self.species_client:
                response = self.species_client.service.createTreeSpecies(
                    nombreComun=species.nombreComun,
                    nombreCientifico=species.nombreCientifico or "",
                    estadoConservacionId=species.estadoConservacionId,
                    zonaId=species.zonaId
                )
                success = bool(response)  # SOAP returns boolean directly
            else:
                # Simulación
                success = True
                print(f"✅ Especie simulada creada: {species.nombreComun}")
            
            if success:
                self._invalidate_cache('species')
            
            if callback:
                message = f"Species '{species.nombreComun}' created successfully!" if success else "Failed to create species"
                callback(success, message)
            
            return success
            
        except Exception as e:
            print(f"❌ Error al crear especie: {e}")
            if callback:
                callback(False, f"Error creating species: {e}")
            return False
    
    def update_species(self, species: TreeSpecies, callback: Callable = None) -> bool:
        """Actualiza una especie existente"""
        try:
            if self.species_client and species.id:
                response = self.species_client.service.updateTreeSpecies(
                    id=species.id,
                    nombreComun=species.nombreComun,
                    nombreCientifico=species.nombreCientifico or "",
                    estadoConservacionId=species.estadoConservacionId,
                    zonaId=species.zonaId,
                    activo=species.activo
                )
                success = bool(response)  # SOAP returns boolean directly
            else:
                # Simulación
                success = True
                print(f"✅ Especie simulada actualizada: {species.nombreComun}")
            
            if success:
                self._invalidate_cache('species')
            
            if callback:
                message = f"Species '{species.nombreComun}' updated successfully!" if success else "Failed to update species"
                callback(success, message)
            
            return success
            
        except Exception as e:
            print(f"❌ Error al actualizar especie: {e}")
            if callback:
                callback(False, f"Error updating species: {e}")
            return False
    
    def delete_species(self, species_id: int, callback: Callable = None) -> bool:
        """Elimina una especie (soft delete)"""
        try:
            if self.species_client:
                response = self.species_client.service.deleteTreeSpecies(id=species_id)
                success = bool(response)  # SOAP returns boolean directly
            else:
                # Simulación
                success = True
                print(f"✅ Especie simulada eliminada: ID {species_id}")
            
            if success:
                self._invalidate_cache('species')
            
            if callback:
                message = f"Species deleted successfully!" if success else "Failed to delete species"
                callback(success, message)
            
            return success
            
        except Exception as e:
            print(f"❌ Error al eliminar especie: {e}")
            if callback:
                callback(False, f"Error deleting species: {e}")
            return False
    
    def search_species(self, filter: SearchFilter) -> List[TreeSpecies]:
        """Busca especies con filtros"""
        try:
            if self.species_client:
                response = self.species_client.service.searchSpecies(
                    nameQuery=filter.name_query or "",
                    zoneId=filter.zone_id or 0,
                    conservationStateId=filter.conservation_state_id or 0,
                    activeOnly=filter.active_only if filter.active_only is not None else True
                )
                return self._convert_soap_response_to_species(response)
            else:
                # Simulación con filtrado local
                all_species = self.get_species()
                return self._filter_species_locally(all_species, filter)
                
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return []
    
    # ===========================================
    # OPERACIONES DE ZONAS (CORREGIDAS PARA USAR TipoBosque ENUM)
    # ===========================================
    
    def get_zones(self, force_refresh: bool = False) -> List[Zone]:
        """Obtiene todas las zonas"""
        cache_key = 'zones'
        
        if not force_refresh and self._is_cache_valid(cache_key) and cache_key in self.zones_cache:
            return self.zones_cache[cache_key]
        
        try:
            if self.zone_client:
                response = self.zone_client.service.getAllZones()
                zones_list = self._convert_soap_response_to_zones(response)
            else:
                print("⚠️  SOAP client not available - cannot load zones")
                zones_list = []
            
            self.zones_cache[cache_key] = zones_list
            self.cache_timestamp[cache_key] = time.time()
            return zones_list
            
        except Exception as e:
            print(f"❌ Error al obtener zonas: {e}")
            return []
    
    def create_zone(self, zone_data: Zone, callback: Callable = None) -> bool:
        """Crea una nueva zona usando el enum TipoBosque"""
        try:
            # Convertir el enum TipoBosque a string para el SOAP
            tipo_bosque_str = zone_data.tipo_bosque.value if zone_data.tipo_bosque else TipoBosque.OTRO.value
            
            if self.zone_client:
                response = self.zone_client.service.createZone(
                    nombre=zone_data.nombre,
                    tipoBosque=tipo_bosque_str,
                    areaHa=zone_data.area_ha,
                    activo=True  # Default to active
                )
                success = bool(response)  # SOAP returns boolean directly
            else:
                print("⚠️  SOAP client not available - cannot create zone")
                success = False
            
            if success:
                self._invalidate_cache('zones')
            
            if callback:
                message = f"Zone '{zone_data.nombre}' created successfully!" if success else "Failed to create zone"
                callback(success, message)
            
            return success
            
        except Exception as e:
            print(f"❌ Error al crear zona: {e}")
            if callback:
                callback(False, f"Error creating zone: {e}")
            return False
            return False
    
    def update_zone(self, zone_data: Zone, callback: Callable = None) -> bool:
        """Actualiza una zona existente usando el enum TipoBosque"""
        try:
            # Convertir el enum TipoBosque a string para el SOAP
            tipo_bosque_str = zone_data.tipo_bosque.value if zone_data.tipo_bosque else TipoBosque.OTRO.value
            
            if self.zone_client and zone_data.id:
                response = self.zone_client.service.updateZone(
                    id=zone_data.id,
                    nombre=zone_data.nombre,
                    tipoBosque=tipo_bosque_str,
                    areaHa=zone_data.area_ha,
                    activo=zone_data.activo
                )
                success = bool(response)  # SOAP returns boolean directly
            else:
                print("⚠️  SOAP client not available or zone ID missing - cannot update zone")
                success = False
            
            if success:
                self._invalidate_cache('zones')
            
            if callback:
                message = f"Zone '{zone_data.nombre}' updated successfully!" if success else "Failed to update zone"
                callback(success, message)
            
            return success
            
        except Exception as e:
            print(f"❌ Error al actualizar zona: {e}")
            if callback:
                callback(False, f"Error updating zone: {e}")
            return False
    
    def delete_zone(self, zone_id: int, callback: Callable = None) -> bool:
        """Elimina una zona (soft delete)"""
        try:
            if self.zone_client:
                response = self.zone_client.service.deleteZone(id=zone_id)
                success = bool(response)  # SOAP returns boolean directly
            else:
                print("⚠️  SOAP client not available - cannot delete zone")
                success = False
            
            if success:
                self._invalidate_cache('zones')
            
            if callback:
                message = f"Zone deleted successfully!" if success else "Failed to delete zone"
                callback(success, message)
            
            return success
            
        except Exception as e:
            print(f"❌ Error al eliminar zona: {e}")
            if callback:
                callback(False, f"Error deleting zone: {e}")
            return False
    
    def get_tipos_bosque(self) -> List[TipoBosque]:
        """Obtiene todos los tipos de bosque disponibles"""
        return list(TipoBosque)
    
    # ===========================================
    # OPERACIONES DE ESTADOS DE CONSERVACIÓN
    # ===========================================
    
    def get_conservation_states(self, force_refresh: bool = False) -> List[ConservationState]:
        """Obtiene todos los estados de conservación"""
        cache_key = 'conservation_states'
        
        if not force_refresh and self._is_cache_valid(cache_key) and cache_key in self.conservation_states_cache:
            return self.conservation_states_cache[cache_key]
        
        try:
            if self.conservation_client:
                response = self.conservation_client.service.getAllConservationStates()
                states_list = self._convert_soap_response_to_conservation_states(response)
            else:
                print("⚠️  SOAP client not available - cannot load conservation states")
                states_list = []
            
            self.conservation_states_cache[cache_key] = states_list
            self.cache_timestamp[cache_key] = time.time()
            return states_list
            
        except Exception as e:
            print(f"❌ Error al obtener estados de conservación: {e}")
            return []
    
    # ===========================================
    # MÉTODOS DE CONVERSIÓN Y UTILIDADES
    # ===========================================
    
    def _convert_soap_response_to_species(self, response) -> List[TreeSpecies]:
        """Convierte respuesta SOAP a lista de especies"""
        species_list = []
        
        # The SOAP service returns a list directly, not wrapped in an object
        if response and hasattr(response, '__iter__'):
            for species_data in response:
                species = TreeSpecies(
                    id=getattr(species_data, 'id', None),
                    nombreComun=getattr(species_data, 'nombreComun', ''),
                    nombreCientifico=getattr(species_data, 'nombreCientifico', None),
                    estadoConservacionId=getattr(species_data, 'estadoConservacionId', 0),
                    estadoConservacionNombre=getattr(species_data, 'estadoConservacionNombre', ''),
                    zonaId=getattr(species_data, 'zonaId', 0),
                    zonaNombre=getattr(species_data, 'zonaNombre', ''),
                    activo=getattr(species_data, 'activo', True),
                    fechaCreacion=self._parse_datetime(getattr(species_data, 'fechaCreacion', None)),
                    fechaModificacion=self._parse_datetime(getattr(species_data, 'fechaModificacion', None))
                )
                species_list.append(species)
        
        return species_list
    
    def _convert_soap_response_to_zones(self, response) -> List[Zone]:
        """Convierte respuesta SOAP a lista de zonas usando TipoBosque enum"""
        zones_list = []
        
        # The SOAP service returns a list directly, not wrapped in an object
        if response and hasattr(response, '__iter__'):
            for zone_data in response:
                # Convertir string a enum TipoBosque
                tipo_bosque_str = getattr(zone_data, 'tipoBosque', '')
                tipo_bosque = TipoBosque.from_string(tipo_bosque_str) if tipo_bosque_str else None
                
                zone = Zone(
                    id=getattr(zone_data, 'id', 0),
                    nombre=getattr(zone_data, 'nombre', ''),
                    descripcion=getattr(zone_data, 'descripcion', None),
                    tipo_bosque=tipo_bosque,
                    area_ha=getattr(zone_data, 'areaHa', 0.0),
                    activo=getattr(zone_data, 'activo', True),
                    fecha_creacion=self._parse_datetime(getattr(zone_data, 'fechaCreacion', None)),
                    fecha_modificacion=self._parse_datetime(getattr(zone_data, 'fechaModificacion', None))
                )
                zones_list.append(zone)
        
        return zones_list
    
    def _convert_soap_response_to_conservation_states(self, response) -> List[ConservationState]:
        """Convierte respuesta SOAP a lista de estados de conservación"""
        states_list = []
        
        # The SOAP service returns a list directly, not wrapped in an object
        if response and hasattr(response, '__iter__'):
            for state_data in response:
                state = ConservationState(
                    id=getattr(state_data, 'id', 0),
                    nombre=getattr(state_data, 'nombre', ''),
                    descripcion=getattr(state_data, 'descripcion', None),
                    nivel_riesgo=getattr(state_data, 'nivelRiesgo', None)
                )
                states_list.append(state)
        
        return states_list
    
    def _parse_datetime(self, date_str) -> Optional[datetime]:
        """Convierte string de fecha a datetime"""
        if not date_str:
            return None
        
        try:
            # Intenta varios formatos de fecha
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d',
                '%d/%m/%Y %H:%M:%S',
                '%d/%m/%Y'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(str(date_str), fmt)
                except ValueError:
                    continue
            
            return None
        except Exception:
            return None
    
    def _filter_species_locally(self, species_list: List[TreeSpecies], filter: SearchFilter) -> List[TreeSpecies]:
        """Filtra especies localmente"""
        filtered = species_list
        
        if filter.name_query:
            query = filter.name_query.lower()
            filtered = [s for s in filtered if 
                       query in s.nombreComun.lower() or 
                       (s.nombreCientifico and query in s.nombreCientifico.lower())]
        
        if filter.zone_id:
            filtered = [s for s in filtered if s.zonaId == filter.zone_id]
        
        if filter.conservation_state_id:
            filtered = [s for s in filtered if s.estadoConservacionId == filter.conservation_state_id]
        
        if filter.active_only is not None:
            filtered = [s for s in filtered if s.activo == filter.active_only]
        
        return filtered
    
    # ===========================================
    # MÉTODOS DE UTILIDAD
    # ===========================================
    
    def clear_cache(self):
        """Limpia todo el cache"""
        self.species_cache.clear()
        self.zones_cache.clear()
        self.conservation_states_cache.clear()
        self.cache_timestamp.clear()
        print("🧹 Cache limpiado")
    
    def get_cache_status(self) -> Dict[str, Any]:
        """Obtiene el estado del cache"""
        current_time = time.time()
        status = {}
        
        for cache_key, timestamp in self.cache_timestamp.items():
            age = current_time - timestamp
            status[cache_key] = {
                'age_seconds': age,
                'is_valid': age < self.cache_ttl,
                'expires_in': max(0, self.cache_ttl - age)
            }
        
        return status
    
    def test_connection(self) -> Dict[str, bool]:
        """Prueba la conexión con los servicios"""
        status = {
            'species_service': False,
            'zone_service': False,
            'conservation_service': False
        }
        
        try:
            if self.species_client:
                # Intenta una operación simple
                self.species_client.service.getAllSpecies()
                status['species_service'] = True
        except Exception:
            pass
        
        try:
            if self.zone_client:
                self.zone_client.service.getAllZones()
                status['zone_service'] = True
        except Exception:
            pass
        
        try:
            if self.conservation_client:
                self.conservation_client.service.getAllConservationStates()
                status['conservation_service'] = True
        except Exception:
            pass
        
        return status
    
    # ===========================================
    # MÉTODOS ALIAS PARA COMPATIBILIDAD CON UI
    # ===========================================
    
    def get_all_species(self, force_refresh: bool = False) -> List[TreeSpecies]:
        """Alias para get_species() - compatibilidad con UI"""
        return self.get_species(force_refresh)
    
    def get_all_zones(self, force_refresh: bool = False) -> List[Zone]:
        """Alias para get_zones() - compatibilidad con UI"""
        return self.get_zones(force_refresh)
    
    def get_all_conservation_states(self, force_refresh: bool = False) -> List[ConservationState]:
        """Alias para get_conservation_states() - compatibilidad con UI"""
        return self.get_conservation_states(force_refresh)