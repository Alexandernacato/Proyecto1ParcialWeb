#!/usr/bin/env python3
"""
🔍 Test Search Functionality
Testing Search by ID and Search by Name features
"""

import sys
import os

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "SistemaForestalFinal", "src", "main", "java", "com", "mycompany", "sistemaforestalfinal", "service", "client"))

try:
    from core.data_manager import DataManager
    from core.models import TreeSpecies
    print("✅ Successfully imported modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_search_functionality():
    """Test both search by ID and search by name"""
    print("🔍 Testing Search Functionality...")
    
    # Initialize DataManager
    data_manager = DataManager()
    print("✅ DataManager initialized")
    
    # Test 1: Search by ID
    print("\n1️⃣ Testing Search by ID...")
    species_by_id = data_manager.get_species_by_id(1)
    if species_by_id:
        print(f"   ✅ Found species with ID 1: {species_by_id.nombreComun}")
        print(f"      Scientific name: {species_by_id.nombreCientifico or 'N/A'}")
        print(f"      Zone ID: {species_by_id.zonaId}")
        print(f"      Active: {species_by_id.activo}")
    else:
        print("   ❌ No species found with ID 1")
    
    # Test 2: Search by Name (partial match)
    print("\n2️⃣ Testing Search by Name (partial match)...")
    species_by_name = data_manager.search_species_by_name("Pino", exact_match=False)
    print(f"   Found {len(species_by_name)} species matching 'Pino':")
    for species in species_by_name:
        print(f"      - {species.nombreComun} (ID: {species.id})")
    
    # Test 3: Search by Name (exact match)
    print("\n3️⃣ Testing Search by Name (exact match)...")
    all_species = data_manager.get_species()
    if all_species:
        first_species_name = all_species[0].nombreComun
        exact_matches = data_manager.search_species_by_name(first_species_name, exact_match=True)
        print(f"   Searching for exact match: '{first_species_name}'")
        print(f"   Found {len(exact_matches)} exact matches:")
        for species in exact_matches:
            print(f"      - {species.nombreComun} (ID: {species.id})")
    
    # Test 4: Search with non-existing ID
    print("\n4️⃣ Testing Search with non-existing ID...")
    non_existing = data_manager.get_species_by_id(9999)
    if non_existing:
        print(f"   ❌ Unexpected: Found species with ID 9999: {non_existing.nombreComun}")
    else:
        print("   ✅ Correctly returned None for non-existing ID 9999")
    
    # Test 5: Search with non-existing name
    print("\n5️⃣ Testing Search with non-existing name...")
    non_existing_name = data_manager.search_species_by_name("NonExistentSpecies")
    print(f"   Found {len(non_existing_name)} species matching 'NonExistentSpecies'")
    if len(non_existing_name) == 0:
        print("   ✅ Correctly returned empty list for non-existing name")
    
    print("\n🎉 Search functionality tests completed!")

if __name__ == "__main__":
    test_search_functionality()
