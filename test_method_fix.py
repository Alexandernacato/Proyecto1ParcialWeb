#!/usr/bin/env python3
"""
🔧 Test Method Fix for Species CRUD
Testing if the get_all_tree_species method fix resolves the AttributeError
"""

import sys
import os

# Add the source path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'SistemaForestalFinal/src/main/java/com/mycompany/sistemaforestalfinal/service/client'))

from core.soap_client import SOAPClientManager
from core.data_manager import DataManager

def test_method_fix():
    """Test if the method name fix works"""
    print("🔧 Testing Method Fix for Species CRUD")
    print("=" * 60)
    
    try:
        # Create SOAP client
        print("📡 Creating SOAP client...")
        soap_client = SOAPClientManager()
        
        # Try to connect
        print("🔗 Attempting to connect...")
        if soap_client.connect():
            print("✅ SOAP client connected successfully")
            
            # Test if get_all_tree_species method exists
            print("🔍 Testing get_all_tree_species method...")
            if hasattr(soap_client, 'get_all_tree_species'):
                print("✅ get_all_tree_species method exists")
                
                # Test calling the method
                try:
                    species = soap_client.get_all_tree_species()
                    print(f"✅ Method call successful - Found {len(species)} species")
                except Exception as e:
                    print(f"❌ Method call failed: {e}")
            else:
                print("❌ get_all_tree_species method not found")
            
            # Test DataManager integration
            print("\n📋 Testing DataManager integration...")
            data_manager = DataManager(soap_client)
            
            try:
                species_list = data_manager.get_all_species()
                print(f"✅ DataManager.get_all_species() successful - Found {len(species_list)} species")
            except Exception as e:
                print(f"❌ DataManager.get_all_species() failed: {e}")
                
        else:
            print("❌ Failed to connect to SOAP services")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_method_fix()
