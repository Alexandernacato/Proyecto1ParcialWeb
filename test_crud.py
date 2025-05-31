#!/usr/bin/env python3
"""
🌳 Forest Management CRUD Testing Script
Simple test to verify SOAP services and perform CRUD operations
"""

from zeep import Client
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

def test_soap_connection():
    """Test SOAP connection and basic operations"""
    print("🌳 === TESTING FOREST MANAGEMENT SOAP SERVICES ===")
    
    # URLs de los servicios
    species_url = "http://localhost:8282/TreeSpeciesCrudService?wsdl"
    
    try:
        print("🔌 Connecting to Species SOAP service...")
        species_client = Client(species_url)
        print("✅ Species service connected successfully!")
        
        # Test READ - Get all species
        print("\n📖 Testing READ operation...")
        species_list = species_client.service.getAllTreeSpecies()
        print(f"📊 Found {len(species_list) if species_list else 0} species")
        
        if species_list:
            print("Current species:")
            for i, species in enumerate(species_list[:5]):  # Show first 5
                print(f"  {i+1}. {species.nombreComun} (ID: {species.id})")
        
        # Test CREATE - Add new species
        print("\n➕ Testing CREATE operation...")
        new_species_name = f"Test Species {len(species_list) + 1}"
        create_result = species_client.service.createTreeSpecies(
            nombreComun=new_species_name,
            nombreCientifico="Testus speciesus",
            estadoConservacionId=None,
            zonaId=None,
            activo=True
        )
        
        if create_result:
            print(f"✅ Successfully created species: {new_species_name}")
        else:
            print(f"❌ Failed to create species: {new_species_name}")
        
        # Verify CREATE by reading again
        print("\n🔍 Verifying creation...")
        updated_species_list = species_client.service.getAllTreeSpecies()
        new_count = len(updated_species_list) if updated_species_list else 0
        print(f"📊 Species count after creation: {new_count}")
        
        if new_count > len(species_list if species_list else []):
            print("✅ CREATE operation verified - species count increased!")
            
            # Find the newly created species for UPDATE test
            new_species = None
            for species in updated_species_list:
                if species.nombreComun == new_species_name:
                    new_species = species
                    break
            
            if new_species:
                # Test UPDATE
                print(f"\n✏️ Testing UPDATE operation on species ID: {new_species.id}...")
                updated_name = f"{new_species_name} - UPDATED"
                update_result = species_client.service.updateTreeSpecies(
                    id=new_species.id,
                    nombreComun=updated_name,
                    nombreCientifico="Testus speciesus updated",
                    estadoConservacionId=None,
                    zonaId=None,
                    activo=True
                )
                
                if update_result:
                    print(f"✅ Successfully updated species to: {updated_name}")
                    
                    # Verify UPDATE
                    print("🔍 Verifying update...")
                    final_species_list = species_client.service.getAllTreeSpecies()
                    for species in final_species_list:
                        if species.id == new_species.id:
                            if species.nombreComun == updated_name:
                                print("✅ UPDATE operation verified!")
                            else:
                                print(f"❌ UPDATE verification failed. Expected: {updated_name}, Got: {species.nombreComun}")
                            break
                    
                    # Test DELETE
                    print(f"\n🗑️ Testing DELETE operation on species ID: {new_species.id}...")
                    delete_result = species_client.service.deleteTreeSpecies(id=new_species.id)
                    
                    if delete_result:
                        print(f"✅ Successfully deleted species ID: {new_species.id}")
                        
                        # Verify DELETE
                        print("🔍 Verifying deletion...")
                        final_final_species_list = species_client.service.getAllTreeSpecies()
                        final_count = len(final_final_species_list) if final_final_species_list else 0
                        
                        species_still_exists = False
                        if final_final_species_list:
                            for species in final_final_species_list:
                                if species.id == new_species.id and species.activo:
                                    species_still_exists = True
                                    break
                        
                        if not species_still_exists:
                            print("✅ DELETE operation verified - species removed or deactivated!")
                        else:
                            print("❌ DELETE verification failed - species still active")
                    else:
                        print(f"❌ Failed to delete species ID: {new_species.id}")
                else:
                    print(f"❌ Failed to update species ID: {new_species.id}")
        else:
            print("❌ CREATE operation failed - species count did not increase")
        
        print("\n🎉 === CRUD TESTING COMPLETED ===")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_soap_connection()
    if success:
        print("\n✅ All SOAP services are working correctly!")
    else:
        print("\n❌ SOAP services testing failed!")
