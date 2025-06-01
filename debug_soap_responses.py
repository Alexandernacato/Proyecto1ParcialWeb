#!/usr/bin/env python3
"""
🌳 Debug SOAP Response Structure
Debug script to examine the actual SOAP response format
"""

import sys
from pathlib import Path

# Add paths for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / "SistemaForestalFinal" / "src" / "main" / "java" / "com" / "mycompany" / "sistemaforestalfinal" / "service" / "client"))

try:
    from core.data_manager import DataManager
    print("✅ Successfully imported SOAP modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def debug_soap_responses():
    """Debug SOAP response structures"""
    print("\n🔍 === DEBUGGING SOAP RESPONSES ===")
    
    try:
        data_manager = DataManager()
        print("✅ DataManager initialized")
        
        # Debug species response
        print("\n🌱 Debugging Species SOAP Response...")
        if data_manager.species_client:
            response = data_manager.species_client.service.getAllTreeSpecies()
            print(f"📋 Response type: {type(response)}")
            print(f"📋 Response: {response}")
            
            if hasattr(response, '__dict__'):
                print(f"📋 Response attributes: {list(response.__dict__.keys())}")
            
            if hasattr(response, '_raw_elements'):
                print(f"📋 Raw elements: {response._raw_elements}")
                
            # Try to iterate if it's a list
            if hasattr(response, '__iter__') and not isinstance(response, str):
                print(f"📋 Response is iterable, length: {len(list(response))}")
                for i, item in enumerate(response):
                    if i < 3:  # Show first 3 items
                        print(f"   Item {i}: {type(item)} - {item}")
                        if hasattr(item, '__dict__'):
                            print(f"   Item {i} attributes: {list(item.__dict__.keys())}")
        
        # Debug zones response  
        print("\n🗺️ Debugging Zones SOAP Response...")
        if data_manager.zone_client:
            response = data_manager.zone_client.service.getAllZones()
            print(f"📋 Response type: {type(response)}")
            print(f"📋 Response: {response}")
            
            if hasattr(response, '__dict__'):
                print(f"📋 Response attributes: {list(response.__dict__.keys())}")
                
            # Try to iterate if it's a list
            if hasattr(response, '__iter__') and not isinstance(response, str):
                print(f"📋 Response is iterable, length: {len(list(response))}")
                for i, item in enumerate(response):
                    if i < 3:  # Show first 3 items
                        print(f"   Item {i}: {type(item)} - {item}")
                        if hasattr(item, '__dict__'):
                            print(f"   Item {i} attributes: {list(item.__dict__.keys())}")
            
        # Debug conservation states response
        print("\n🛡️ Debugging Conservation States SOAP Response...")
        if data_manager.conservation_client:
            response = data_manager.conservation_client.service.getAllConservationStates()
            print(f"📋 Response type: {type(response)}")
            print(f"📋 Response: {response}")
            
            if hasattr(response, '__dict__'):
                print(f"📋 Response attributes: {list(response.__dict__.keys())}")
                
            # Try to iterate if it's a list
            if hasattr(response, '__iter__') and not isinstance(response, str):
                print(f"📋 Response is iterable, length: {len(list(response))}")
                for i, item in enumerate(response):
                    if i < 3:  # Show first 3 items
                        print(f"   Item {i}: {type(item)} - {item}")
                        if hasattr(item, '__dict__'):
                            print(f"   Item {i} attributes: {list(item.__dict__.keys())}")
        
    except Exception as e:
        print(f"❌ Debug error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Starting SOAP Response Debug...")
    debug_soap_responses()
    print("\n🎉 Debug completed!")
