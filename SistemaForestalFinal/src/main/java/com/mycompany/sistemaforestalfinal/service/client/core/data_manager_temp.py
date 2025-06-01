"""
🌳 Data Manager
Gestiona operaciones de datos y filtrado para el sistema forestal
"""

from typing import List, Optional, Callable, Any
import threading
from .soap_client import SOAPClientManager
from .models import TreeSpecies, Zone, ConservationState, SearchFilter, TipoBosque


class DataManager:
    """Gestor de datos para operaciones forestales"""
    
    def __init__(self, soap_client: SOAPClientManager):
        self.soap_client = soap_client
        self.zones: List[Zone] = []
        self.conservation_states: List[ConservationState] = []
        self.current_species_list: List[TreeSpecies] = []
        self._data_callbacks = []
        
    def add_data_callback(self, callback: Callable[[str, Any], None]):
        """Añadir callback para notificaciones de datos"""
        self._data_callbacks.append(callback)
    
    def add_data_change_callback(self, callback: Callable[[str, Any], None]):
        """Alias para add_data_callback para compatibilidad"""
        self.add_data_callback(callback)
    
    def get_all_zones(self) -> List[Zone]:
        """Obtener todas las zonas sincronamente"""
        try:
            if not self.zones:
                zones_raw = self.soap_client.get_all_zones()
                self.zones = [self._convert_to_zone(z) for z in zones_raw]
            return self.zones
        except Exception as e:
            print(f"Error getting zones: {e}")
            return []
    
    def get_all_conservation_states(self) -> List[ConservationState]:
        """Obtener todos los estados de conservación sincronamente"""
        try:
            if not self.conservation_states:
                states_raw = self.soap_client.get_all_conservation_states()
                self.conservation_states = [self._convert_to_conservation_state(s) for s in states_raw]
            return self.conservation_states
        except Exception as e:
            print(f"Error getting conservation states: {e}")
            return []
    
    def get_all_species(self) -> List[TreeSpecies]:
        """Obtener todas las especies sincronamente"""
        try:
            species_raw = self.soap_client.get_all_tree_species()
            self.current_species_list = [self._convert_to_tree_species(s) for s in species_raw]
            return self.current_species_list
        except Exception as e:
            print(f"Error getting species: {e}")
            return []
    
    def get_species_by_id(self, species_id: int) -> Optional[TreeSpecies]:
        """Obtener especie por ID sincronamente"""
        try:
            species_raw = self.soap_client.get_tree_species_by_id(species_id)
            if species_raw:
                return self._convert_to_tree_species(species_raw)
            return None
        except Exception as e:
            print(f"Error getting species by ID: {e}")
            return None

    def _convert_to_zone(self, zone_raw) -> Zone:
        """Convertir zona raw a modelo Zone"""
        return Zone(
            id=getattr(zone_raw, 'id', 0),
            nombre=getattr(zone_raw, 'nombre', ''),
            descripcion=getattr(zone_raw, 'descripcion', None),
            tipo_bosque=TipoBosque.from_string(getattr(zone_raw, 'tipoBosque', '')) if getattr(zone_raw, 'tipoBosque', None) else None,
            area_ha=float(getattr(zone_raw, 'areaHa', 0.0)) if getattr(zone_raw, 'areaHa', None) else 0.0,
            activo=getattr(zone_raw, 'activo', True),
            fecha_creacion=getattr(zone_raw, 'fechaCreacion', None),
            fecha_modificacion=getattr(zone_raw, 'fechaModificacion', None)
        )

    def _convert_to_conservation_state(self, state_raw) -> ConservationState:
        """Convertir estado raw a modelo ConservationState"""
        return ConservationState(
            id=state_raw.id,
            nombre=state_raw.nombre,
            descripcion=getattr(state_raw, 'descripcion', '')
        )

    def _convert_to_tree_species(self, species_raw) -> TreeSpecies:
        """Convertir especie raw a modelo TreeSpecies"""
        return TreeSpecies(
            id=species_raw.id,
            nombreComun=species_raw.nombreComun,
            nombreCientifico=getattr(species_raw, 'nombreCientifico', ''),
            estadoConservacionId=species_raw.estadoConservacionId,
            zonaId=species_raw.zonaId,
            activo=getattr(species_raw, 'activo', True),
            estadoConservacionNombre=getattr(species_raw, 'estadoConservacionNombre', ''),
            zonaNombre=getattr(species_raw, 'zonaNombre', '')
        )

    def filter_species(self, search_filter: SearchFilter) -> List[TreeSpecies]:
        """Filtrar especies localmente según criterios"""
        filtered = self.current_species_list.copy()
        
        if search_filter.name_query:
            query = search_filter.name_query.lower()
            filtered = [s for s in filtered if 
                       query in s.nombreComun.lower() or 
                       (s.nombreCientifico and query in s.nombreCientifico.lower())]
        
        if search_filter.zone_id is not None:
            filtered = [s for s in filtered if s.zonaId == search_filter.zone_id]
            
        if search_filter.conservation_state_id is not None:
            filtered = [s for s in filtered if s.estadoConservacionId == search_filter.conservation_state_id]
            
        if search_filter.active_only is not None:
            filtered = [s for s in filtered if s.activo == search_filter.active_only]
            
        return filtered

    def create_species(self, species: TreeSpecies, callback: Optional[Callable[[bool, str, Optional[int]], None]] = None):
        """Crear nueva especie"""
        def _create_thread():
            try:
                result_id = self.soap_client.create_tree_species(
                    common_name=species.nombreComun,
                    scientific_name=species.nombreCientifico,
                    conservation_state_id=species.estadoConservacionId,
                    zone_id=species.zonaId,
                    active=species.activo
                )
                
                if result_id:
                    self._notify_data_change("species_created", result_id)
                    if callback:
                        callback(True, f"Species '{species.nombreComun}' created successfully", result_id)
                else:
                    if callback:
                        callback(False, f"Failed to create species '{species.nombreComun}'", None)
                        
            except Exception as e:
                if callback:
                    callback(False, f"Error creating species: {e}", None)
                    
        threading.Thread(target=_create_thread, daemon=True).start()

    def update_species(self, species: TreeSpecies, callback: Optional[Callable[[bool, str], None]] = None):
        """Actualizar especie existente"""
        def _update_thread():
            try:
                success = self.soap_client.update_tree_species(
                    species_id=species.id,
                    common_name=species.nombreComun,
                    scientific_name=species.nombreCientifico,
                    conservation_state_id=species.estadoConservacionId,
                    zone_id=species.zonaId,
                    active=species.activo
                )
                
                if success:
                    self._notify_data_change("species_updated", species.id)
                    if callback:
                        callback(True, f"Species '{species.nombreComun}' updated successfully")
                else:
                    if callback:
                        callback(False, f"Failed to update species '{species.nombreComun}'")
                        
            except Exception as e:
                if callback:
                    callback(False, f"Error updating species: {e}")
                    
        threading.Thread(target=_update_thread, daemon=True).start()
        
    def delete_species(self, species_id: int, callback: Optional[Callable[[bool, str], None]] = None):
        """Eliminar especie"""
        def _delete_thread():
            try:
                success = self.soap_client.delete_tree_species(species_id)
                
                if success:
                    self._notify_data_change("species_deleted", species_id)
                    if callback:
                        callback(True, f"Species with ID {species_id} deleted successfully")
                else:
                    if callback:
                        callback(False, f"Failed to delete species with ID {species_id}")
                        
            except Exception as e:
                if callback:
                    callback(False, f"Error deleting species: {e}")
                    
        threading.Thread(target=_delete_thread, daemon=True).start()
    
    # ======== ZONE CRUD OPERATIONS ========
    
    def create_zone(self, zone_data: Zone) -> bool:
        """Crear nueva zona sincrónicamente"""
        try:
            # Use the SOAP client to create zone
            success = self.soap_client.create_zone(
                nombre=zone_data.nombre,
                tipo_bosque=zone_data.tipo_bosque.value if zone_data.tipo_bosque else TipoBosque.OTRO.value,
                area_ha=zone_data.area_ha,
                activo=zone_data.activo
            )
            
            if success:
                # Refresh zones cache
                self.zones = None  # Force reload on next access
                self._notify_data_change("zone_created", zone_data)
                
            return success
            
        except Exception as e:
            print(f"Error creating zone: {e}")
            return False
    
    def update_zone(self, zone_data: Zone) -> bool:
        """Actualizar zona existente sincrónicamente"""
        try:
            # Use the SOAP client to update zone
            success = self.soap_client.update_zone(
                id=zone_data.id,
                nombre=zone_data.nombre,
                tipo_bosque=zone_data.tipo_bosque.value if zone_data.tipo_bosque else TipoBosque.OTRO.value,
                area_ha=zone_data.area_ha,
                activo=zone_data.activo
            )
            
            if success:
                # Refresh zones cache
                self.zones = None  # Force reload on next access
                self._notify_data_change("zone_updated", zone_data)
                
            return success
            
        except Exception as e:
            print(f"Error updating zone: {e}")
            return False
    
    def delete_zone(self, zone_id: int) -> bool:
        """Eliminar zona por ID sincrónicamente"""
        try:
            # Use the SOAP client to delete zone
            success = self.soap_client.delete_zone(zone_id)
            
            if success:
                # Refresh zones cache
                self.zones = None  # Force reload on next access
                self._notify_data_change("zone_deleted", zone_id)
                
            return success
            
        except Exception as e:
            print(f"Error deleting zone: {e}")
            return False
    
    def get_zone_by_id(self, zone_id: int):
        """Obtener zona por ID sincrónicamente"""
        try:
            return self.soap_client.get_zone_by_id(zone_id)
        except Exception as e:
            print(f"Error getting zone by ID: {e}")
            return None
    
    # ======== END ZONE CRUD OPERATIONS ========
    
    def _notify_data_change(self, event_type: str, data: Any = None):
        """Notificar cambios de datos a todos los callbacks registrados"""
        for callback in self._data_callbacks:
            try:
                callback(event_type, data)
            except Exception as e:
                print(f"Error in data change callback: {e}")
