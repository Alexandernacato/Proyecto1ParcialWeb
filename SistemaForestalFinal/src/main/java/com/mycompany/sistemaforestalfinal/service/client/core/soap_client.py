"""
🌳 SOAP Client Manager
Maneja las conexiones y operaciones SOAP del sistema forestal
"""

from zeep import Client
from zeep.transports import Transport
import threading
from typing import List, Optional, Dict, Any
from datetime import datetime


class SOAPClientManager:
    """Gestor de cliente SOAP para operaciones forestales"""
    
    def __init__(self, service_url: str = "http://localhost:8282/TreeSpeciesCrudService?wsdl"):
        self.service_url = service_url
        self.client = None
        self.connected = False
        self._connection_callbacks = []
        
    def add_connection_callback(self, callback):
        """Añadir callback para cambios de estado de conexión"""
        self._connection_callbacks.append(callback)
        
    def _notify_connection_change(self, connected: bool):
        """Notificar cambios de estado de conexión a los callbacks"""
        for callback in self._connection_callbacks:
            try:
                callback(connected)
            except Exception:
                pass  # Ignorar errores en callbacks
                
    def connect(self) -> bool:
        """Conectar al servicio SOAP"""
        try:
            transport = Transport(timeout=10)
            self.client = Client(self.service_url, transport=transport)
            self.connected = True
            self._notify_connection_change(True)
            return True
        except Exception as e:
            self.connected = False
            self._notify_connection_change(False)
            raise e
            
    def disconnect(self):
        """Desconectar del servicio SOAP"""
        self.client = None
        self.connected = False
        self._notify_connection_change(False)
        
    def is_connected(self) -> bool:
        """Verificar si está conectado"""
        return self.connected and self.client is not None
        
    # Operaciones CRUD para especies
    def get_all_tree_species(self) -> List[Any]:
        """Obtener todas las especies de árboles"""
        if not self.is_connected():
            raise Exception("Not connected to SOAP service")
        result = self.client.service.getAllTreeSpecies()
        return list(result) if result else []
        
    def get_tree_species_by_id(self, species_id: int) -> Optional[Any]:
        """Obtener especie por ID"""
        if not self.is_connected():
            raise Exception("Not connected to SOAP service")
        return self.client.service.getTreeSpeciesById(species_id)
        
    def create_tree_species(self, common_name: str, scientific_name: Optional[str], 
                           conservation_state_id: int, zone_id: int, active: bool = True) -> Optional[int]:
        """Crear nueva especie"""
        if not self.is_connected():
            raise Exception("Not connected to SOAP service")
        return self.client.service.createTreeSpecies(
            nombreComun=common_name,
            nombreCientifico=scientific_name,
            estadoConservacionId=conservation_state_id,
            zonaId=zone_id,
            activo=active
        )
        
    def update_tree_species(self, species_id: int, common_name: str, 
                           scientific_name: Optional[str], conservation_state_id: int, 
                           zone_id: int, active: bool = True) -> bool:
        """Actualizar especie existente"""
        if not self.is_connected():
            raise Exception("Not connected to SOAP service")
        return self.client.service.updateTreeSpecies(
            id=species_id,
            nombreComun=common_name,
            nombreCientifico=scientific_name,
            estadoConservacionId=conservation_state_id,
            zonaId=zone_id,
            activo=active
        )
        
    def delete_tree_species(self, species_id: int) -> bool:
        """Eliminar especie"""
        if not self.is_connected():
            raise Exception("Not connected to SOAP service")
        return self.client.service.deleteTreeSpecies(species_id)
        
    def search_tree_species_by_name(self, name: str) -> List[Any]:
        """Buscar especies por nombre (común o científico)"""
        if not self.is_connected():
            raise Exception("Not connected to SOAP service")
        result = self.client.service.searchTreeSpeciesByName(name)
        return list(result) if result else []
        
    # Operaciones para datos de referencia
    def get_all_zones(self) -> List[Any]:
        """Obtener todas las zonas"""
        if not self.is_connected():
            raise Exception("Not connected to SOAP service")
        result = self.client.service.getAllZones()
        return list(result) if result else []
        
    def get_all_conservation_states(self) -> List[Any]:
        """Obtener todos los estados de conservación"""
        if not self.is_connected():
            raise Exception("Not connected to SOAP service")
        result = self.client.service.getAllConservationStates()
        return list(result) if result else []
