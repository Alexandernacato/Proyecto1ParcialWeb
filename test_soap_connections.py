#!/usr/bin/env python3
"""
🌳 Test SOAP Connections - Quick verification
Tests the updated SOAP connections and data loading functionality
"""

import sys
from pathlib import Path

# Add paths for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / "SistemaForestalFinal" / "src" / "main" / "java" / "com" / "mycompany" / "sistemaforestalfinal" / "service" / "client"))

try:
    from core.data_manager import DataManager
    from core.soap_client import SOAPClientManager
    print("✅ Successfully imported SOAP modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_soap_connections():
    """Test SOAP service connections"""
    print("\n🌳 === TESTING SOAP CONNECTIONS ===")
    
    # Test DataManager
    print("\n1️⃣ Testing DataManager...")
    try:
        data_manager = DataManager()
        print("   ✅ DataManager initialized")
        
        # Test species loading
        print("   🔍 Testing species loading...")
        species_list = data_manager.get_species()
        print(f"   📊 Loaded {len(species_list)} species")
        
        # Test zones loading  
        print("   🔍 Testing zones loading...")
        zones_list = data_manager.get_zones()
        print(f"   🗺️ Loaded {len(zones_list)} zones")
        
        # Test conservation states
        print("   🔍 Testing conservation states loading...")
        conservation_states = data_manager.get_conservation_states()
        print(f"   🛡️ Loaded {len(conservation_states)} conservation states")
        
    except Exception as e:
        print(f"   ❌ DataManager error: {e}")
    
    # Test SOAPClientManager
    print("\n2️⃣ Testing SOAPClientManager...")
    try:
        soap_client = SOAPClientManager()
        print("   ✅ SOAPClientManager initialized")
        
        # Test connection
        print("   🔌 Testing SOAP connections...")
        soap_client.connect()
        print("   ✅ SOAP connections established")
        
    except Exception as e:
        print(f"   ❌ SOAPClientManager error: {e}")

def test_crud_operations():
    """Test basic CRUD operations"""
    print("\n🔧 === TESTING CRUD OPERATIONS ===")
    
    try:
        data_manager = DataManager()
          # Test zone creation
        print("\n🏞️ Testing zone creation...")
        from core.models import Zone, TipoBosque
        
        test_zone = Zone(
            id=0,
            nombre="Test Zone " + str(int(time.time())),
            tipo_bosque=TipoBosque.SECO,  # Use existing enum value
            area_ha=100.5,
            activo=True
        )
        
        success = data_manager.create_zone(test_zone)
        print(f"   Zone creation: {'✅ Success' if success else '❌ Failed'}")
        
    except Exception as e:
        print(f"   ❌ CRUD test error: {e}")

if __name__ == "__main__":
    print("🧪 Starting SOAP Connection Tests...")
    
    test_soap_connections()
    
    # Add time import for test
    import time
    test_crud_operations()
    
    print("\n🎉 Testing completed!")
