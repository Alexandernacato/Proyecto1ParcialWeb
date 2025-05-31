#!/usr/bin/env python3
"""
Test script to verify Species CRUD functionality
"""

import sys
import os

# Add the paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.join(current_dir, "SistemaForestalFinal", "src", "main", "java", "com", "mycompany", "sistemaforestalfinal", "service", "client")
sys.path.insert(0, client_dir)

from core.soap_client import SOAPClientManager
from core.data_manager import DataManager
from core.models import TreeSpecies

def test_species_crud():
    """Test Species CRUD operations"""
    print("🌳 Testing Species CRUD Operations")
    print("=" * 50)
    
    try:
        # Initialize SOAP client and data manager
        print("📡 Initializing SOAP client...")
        soap_client = SOAPClientManager()
        data_manager = DataManager(soap_client)
        
        print("✅ SOAP client initialized successfully")
        
        # Test 1: Get all species
        print("\n📋 Test 1: Getting all species...")
        species_list = data_manager.get_all_species()
        print(f"✅ Found {len(species_list)} species")
        
        if species_list:
            print("First few species:")
            for i, species in enumerate(species_list[:3]):
                print(f"  {i+1}. ID: {species.id}, Name: {species.nombreComun}")
        
        # Test 2: Get zones and conservation states for creating new species
        print("\n🗺️ Test 2: Getting zones and conservation states...")
        zones = data_manager.get_all_zones()
        states = data_manager.get_all_conservation_states()
        print(f"✅ Found {len(zones)} zones and {len(states)} conservation states")
        
        if zones and states:
            # Test 3: Create new species
            print("\n➕ Test 3: Creating new test species...")
            test_species = TreeSpecies(
                nombreComun="Test Species",
                nombreCientifico="Testicus speciesus",
                estadoConservacionId=states[0].id,
                zonaId=zones[0].id,
                activo=True
            )
            
            # Create species synchronously (for testing)
            def create_callback(success, message, species_id=None):
                if success:
                    print(f"✅ Species created successfully! ID: {species_id}")
                    
                    # Test 4: Update the species
                    print(f"\n✏️ Test 4: Updating species with ID {species_id}...")
                    updated_species = TreeSpecies(
                        id=species_id,
                        nombreComun="Updated Test Species",
                        nombreCientifico="Testicus speciesus updatus",
                        estadoConservacionId=states[0].id,
                        zonaId=zones[0].id,
                        activo=True
                    )
                    
                    def update_callback(success, message):
                        if success:
                            print("✅ Species updated successfully!")
                            
                            # Test 5: Get species by ID
                            print(f"\n🔍 Test 5: Getting species by ID {species_id}...")
                            retrieved_species = data_manager.get_species_by_id(species_id)
                            if retrieved_species:
                                print(f"✅ Species retrieved: {retrieved_species.nombreComun}")
                                
                                # Test 6: Delete the species
                                print(f"\n🗑️ Test 6: Deleting species with ID {species_id}...")
                                def delete_callback(success, message):
                                    if success:
                                        print("✅ Species deleted successfully!")
                                        print("\n🎉 All CRUD tests completed successfully!")
                                    else:
                                        print(f"❌ Failed to delete species: {message}")
                                
                                data_manager.delete_species(species_id, delete_callback)
                            else:
                                print("❌ Failed to retrieve species")
                        else:
                            print(f"❌ Failed to update species: {message}")
                    
                    data_manager.update_species(updated_species, update_callback)
                else:
                    print(f"❌ Failed to create species: {message}")
            
            data_manager.create_species(test_species, create_callback)
            
        else:
            print("❌ Cannot test CRUD operations - no zones or conservation states found")
            
    except Exception as e:
        print(f"❌ Error during CRUD testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_species_crud()
    
    # Keep the script running for a bit to allow async operations to complete
    import time
    print("\n⏳ Waiting for operations to complete...")
    time.sleep(5)
    print("✅ Test completed!")
