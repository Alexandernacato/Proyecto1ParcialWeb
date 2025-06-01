"""
Simple SOAP Client for Species Testing
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

class SimpleSOAPClient:
    """Cliente SOAP simplificado solo para especies"""
    
    def __init__(self, species_service_url: str = "http://localhost:8282/TreeSpeciesCrudService?wsdl"):
        self.species_service_url = species_service_url
        self._species_client = None
        self._is_connected = False
        logger.info("SimpleSOAPClient initialized")

    def connect(self) -> bool:
        """Conectar al servicio de especies"""
        try:
            logger.info(f"Connecting to species service: {self.species_service_url}")
            self._species_client = Client(self.species_service_url)
            self._is_connected = True
            logger.info("✅ Species service connected")
            return True
        except (TransportError, requests.exceptions.ConnectionError) as e:
            logger.error(f"❌ Species service connection error: {e}")
            self._species_client = None
            self._is_connected = False
            return False

    def is_connected(self) -> bool:
        return self._is_connected and self._species_client is not None

    def get_all_tree_species(self) -> List[TreeSpeciesData]:
        """Obtener todas las especies"""
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
            
        except Exception as e:
            logger.error(f"Error getting tree species: {e}")
            raise Exception(f"Failed to get tree species: {e}")

    def create_tree_species(self, common_name: str, scientific_name: str = "", 
                          conservation_state_id: int = 0, zone_id: int = 0, 
                          active: bool = True) -> bool:
        """Crear nueva especie"""
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
            
        except Exception as e:
            logger.error(f"Error creating tree species: {e}")
            raise Exception(f"Failed to create tree species: {e}")

    def update_tree_species(self, species_id: int, common_name: str, scientific_name: str = "", 
                          conservation_state_id: int = 0, zone_id: int = 0, 
                          active: bool = True) -> bool:
        """Actualizar especie existente"""
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
            
        except Exception as e:
            logger.error(f"Error updating tree species: {e}")
            raise Exception(f"Failed to update tree species: {e}")

    def delete_tree_species(self, species_id: int) -> bool:
        """Eliminar especie"""
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
            
        except Exception as e:
            logger.error(f"Error deleting tree species: {e}")
            raise Exception(f"Failed to delete tree species: {e}")

if __name__ == "__main__":
    # Test básico
    print("🌳 Testing Simple SOAP Client...")
    
    client = SimpleSOAPClient()
    
    if client.connect():
        print("✅ Connection successful!")
        
        # Obtener especies
        try:
            species = client.get_all_tree_species()
            print(f"🌲 Found {len(species)} tree species")
            for specie in species[:3]:  # Mostrar primeras 3
                print(f"  - {specie.nombreComun}")
        except Exception as e:
            print(f"❌ Error getting species: {e}")
    else:
        print("❌ Connection failed!")
