#!/usr/bin/env python3
"""
🧪 Test del fix para Species CRUD
Verifica que el método get_all_tree_species() funcione correctamente
"""

import sys
import os

# Agregar rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.join(current_dir, "SistemaForestalFinal", "src", "main", "java", "com", "mycompany", "sistemaforestalfinal", "service", "client")
sys.path.insert(0, client_dir)

try:
    from core.soap_client import SOAPClientManager, create_default_soap_client
    from core.data_manager import DataManager
    
    print("🌳 Testing Species CRUD Fix...")
    print("=" * 50)
    
    # 1. Crear cliente SOAP
    print("1️⃣ Creating SOAP client...")
    soap_client = create_default_soap_client()
    
    # 2. Intentar conectar
    print("2️⃣ Attempting to connect...")
    if soap_client.connect():
        print("✅ SOAP connection successful!")
        
        # 3. Verificar que el método existe
        print("3️⃣ Checking if get_all_tree_species method exists...")
        if hasattr(soap_client, 'get_all_tree_species'):
            print("✅ Method get_all_tree_species() found!")
            
            # 4. Probar DataManager
            print("4️⃣ Testing DataManager...")
            data_manager = DataManager(soap_client)
            
            try:
                especies = data_manager.get_all_species()
                print(f"✅ DataManager.get_all_species() works! Found {len(especies)} species")
                
                # Mostrar algunas especies
                if especies:
                    print("\n📋 Sample species:")
                    for i, especie in enumerate(especies[:3]):
                        print(f"   {i+1}. {especie.nombreComun} (ID: {especie.id})")
                
            except Exception as e:
                print(f"❌ DataManager test failed: {e}")
        else:
            print("❌ Method get_all_tree_species() NOT FOUND!")
    else:
        print("❌ SOAP connection failed!")
        print("💡 Make sure the server is running: .\\run_system.ps1")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Check if the file paths are correct")
except Exception as e:
    print(f"❌ Test error: {e}")
