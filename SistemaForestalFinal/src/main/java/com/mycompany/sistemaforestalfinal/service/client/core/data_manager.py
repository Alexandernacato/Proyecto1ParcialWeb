"""
🌳 Data Manager
Gestiona operaciones de datos y filtrado para el sistema forestal
"""

from typing import List, Optional, Callable, Any
import threading
from .soap_client import SOAPClientManager
from .models import TreeSpecies, Zone, ConservationState, SearchFilter


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
            tipoBosque=getattr(zone_raw, 'tipoBosque', None),
            areaHa=float(getattr(zone_raw, 'areaHa', 0.0)) if getattr(zone_raw, 'areaHa', None) else 0.0,
            activo=getattr(zone_raw, 'activo', True),
            fechaCreacion=getattr(zone_raw, 'fechaCreacion', None),
            fechaModificacion=getattr(zone_raw, 'fechaModificacion', None)
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

    def load_reference_data(self, callback: Optional[Callable[[bool, str], None]] = None):
        """Cargar datos de referencia (zonas y estados de conservación)"""
        def _load_thread():
            try:
                # Cargar zonas
                zones_result = self.soap_client.get_all_zones()
                self.zones = [Zone(id=z.id, nombre=z.nombre) for z in zones_result]
                
                # Cargar estados de conservación
                states_result = self.soap_client.get_all_conservation_states()
                self.conservation_states = [
                    ConservationState(id=s.id, nombre=s.nombre) 
                    for s in states_result
                ]
                
                self._notify_data_change("reference_data_loaded", {
                    "zones": self.zones,
                    "conservation_states": self.conservation_states
                })
                
                if callback:
                    callback(True, f"Loaded {len(self.zones)} zones and {len(self.conservation_states)} conservation states")
                    
            except Exception as e:
                if callback:
                    callback(False, f"Error loading reference data: {e}")
                    
        threading.Thread(target=_load_thread, daemon=True).start()
        
    def load_all_species(self, callback: Optional[Callable[[bool, str, List[TreeSpecies]], None]] = None):
        """Cargar todas las especies"""
        def _load_thread():
            try:
                species_result = self.soap_client.get_all_tree_species()
                self.current_species_list = [
                    TreeSpecies(
                        id=s.id,
                        nombreComun=s.nombreComun,
                        nombreCientifico=getattr(s, 'nombreCientifico', None),
                        estadoConservacionId=s.estadoConservacionId,
                        estadoConservacionNombre=getattr(s, 'estadoConservacionNombre', ''),
                        zonaId=s.zonaId,
                        zonaNombre=getattr(s, 'zonaNombre', ''),
                        activo=getattr(s, 'activo', True)
                    )
                    for s in species_result
                ]
                
                self._notify_data_change("species_loaded", self.current_species_list)
                
                if callback:
                    callback(True, f"Loaded {len(self.current_species_list)} species", self.current_species_list)
                    
            except Exception as e:
                if callback:
                    callback(False, f"Error loading species: {e}", [])
                    
        threading.Thread(target=_load_thread, daemon=True).start()
        
    def search_species_by_id(self, species_id: int, callback: Optional[Callable[[bool, str, Optional[TreeSpecies]], None]] = None):
        """Buscar especie por ID"""
        def _search_thread():
            try:
                result = self.soap_client.get_tree_species_by_id(species_id)
                if result:
                    species = TreeSpecies(
                        id=result.id,
                        nombreComun=result.nombreComun,
                        nombreCientifico=getattr(result, 'nombreCientifico', None),
                        estadoConservacionId=result.estadoConservacionId,
                        estadoConservacionNombre=getattr(result, 'estadoConservacionNombre', ''),
                        zonaId=result.zonaId,
                        zonaNombre=getattr(result, 'zonaNombre', ''),
                        activo=getattr(result, 'activo', True)
                    )
                    if callback:
                        callback(True, "Species found", species)
                else:
                    if callback:
                        callback(False, f"Species with ID {species_id} not found", None)
                        
            except Exception as e:
                if callback:
                    callback(False, f"Error searching species: {e}", None)
                    
        threading.Thread(target=_search_thread, daemon=True).start()
        
    def search_species_by_name(self, name: str, callback: Optional[Callable[[bool, str, List[TreeSpecies]], None]] = None):
        """Buscar especies por nombre"""
        def _search_thread():
            try:
                species_result = self.soap_client.search_tree_species_by_name(name)
                species_list = [
                    TreeSpecies(
                        id=s.id,
                        nombreComun=s.nombreComun,
                        nombreCientifico=getattr(s, 'nombreCientifico', None),
                        estadoConservacionId=s.estadoConservacionId,
                        estadoConservacionNombre=getattr(s, 'estadoConservacionNombre', ''),
                        zonaId=s.zonaId,
                        zonaNombre=getattr(s, 'zonaNombre', ''),
                        activo=getattr(s, 'activo', True)
                    )
                    for s in species_result
                ]
                
                if callback:
                    callback(True, f"Found {len(species_list)} species matching '{name}'", species_list)
                    
            except Exception as e:
                if callback:
                    callback(False, f"Error searching species by name: {e}", [])
                    
        threading.Thread(target=_search_thread, daemon=True).start()
        
    def filter_species(self, search_filter: SearchFilter) -> List[TreeSpecies]:
        """Filtrar especies localmente según criterios"""
        filtered = self.current_species_list.copy()
        
        if search_filter.name_query:
            query = search_filter.name_query.lower()
            filtered = [
                s for s in filtered
                if query in s.nombreComun.lower() or 
                   (s.nombreCientifico and query in s.nombreCientifico.lower())
            ]
            
        if search_filter.zone_id:
            filtered = [s for s in filtered if s.zonaId == search_filter.zone_id]
            
        if search_filter.conservation_state_id:
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
    
    def _notify_data_change(self, event_type: str, data: Any = None):
        """Notificar cambios de datos a todos los callbacks registrados"""
        for callback in self._data_callbacks:
            try:
                callback(event_type, data)
            except Exception as e:
                print(f"Error in data change callback: {e}")
