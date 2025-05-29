#!/usr/bin/env python3
"""
Cliente Python para consumir el servicio SOAP de Especies en Conservación
Requiere: pip install zeep requests
"""

import requests
from zeep import Client
from zeep.transports import Transport
import sys

class ConservationSpeciesClient:
    def __init__(self, service_url="http://localhost:8282/ConservationSpeciesService?wsdl"):
        """
        Inicializa el cliente SOAP
        Args:
            service_url (str): URL del WSDL del servicio SOAP
        """
        self.service_url = service_url
        self.client = None
        self.connected = self._connect()
    
    def _connect(self):
        """Establece la conexión con el servicio SOAP"""
        try:
            # Configurar transporte con timeout
            transport = Transport(timeout=10)
            
            # Crear cliente SOAP
            self.client = Client(self.service_url, transport=transport)
            print(f"✅ Conexión exitosa al servicio SOAP: {self.service_url}")
            return True
            
        except Exception as e:
            print(f"❌ Error al conectar con el servicio SOAP: {e}")
            print("⚠️  No se pudo conectar inicialmente, pero puedes intentar en el menú")
            return False
    
    def retry_connection(self):
        """Reintenta la conexión con el servicio SOAP"""
        print("🔄 Intentando reconectar...")
        self.connected = self._connect()
        return self.connected
    
    def get_all_species_in_conservation(self):
        """
        Obtiene todas las especies que están en conservación
        Returns:
            list: Lista de especies en conservación
        """
        if not self.connected and not self.retry_connection():
            print("❌ No se puede conectar al servicio")
            return []
            
        try:
            print("🔍 Obteniendo todas las especies en conservación...")
            result = self.client.service.getSpeciesInConservation()
            
            if result:
                print(f"✅ Se encontraron {len(result)} especies en conservación")
                return result
            else:
                print("ℹ️  No se encontraron especies en conservación")
                return []
                
        except Exception as e:
            print(f"❌ Error al obtener especies en conservación: {e}")
            return []
    
    def get_species_by_conservation_state(self, estado_id):
        """
        Obtiene especies filtradas por estado de conservación específico
        Args:
            estado_id (int): ID del estado de conservación
        Returns:
            list: Lista de especies con el estado especificado
        """
        if not self.connected and not self.retry_connection():
            print("❌ No se puede conectar al servicio")
            return []
            
        try:
            print(f"🔍 Obteniendo especies con estado de conservación ID: {estado_id}")
            result = self.client.service.getSpeciesByConservationState(estado_id)
            
            if result:
                print(f"✅ Se encontraron {len(result)} especies con estado ID {estado_id}")
                return result
            else:
                print(f"ℹ️  No se encontraron especies con estado de conservación ID {estado_id}")
                return []
                
        except Exception as e:
            print(f"❌ Error al obtener especies por estado: {e}")
            return []
    
    def get_conservation_statistics(self):
        """
        Obtiene estadísticas generales de conservación
        Returns:
            object: Estadísticas de conservación
        """
        if not self.connected and not self.retry_connection():
            print("❌ No se puede conectar al servicio")
            return None
            
        try:
            print("📊 Obteniendo estadísticas de conservación...")
            result = self.client.service.getConservationStatistics()
            
            if result:
                print("✅ Estadísticas obtenidas correctamente")
                return result
            else:
                print("ℹ️  No se pudieron obtener las estadísticas")
                return None
                
        except Exception as e:
            print(f"❌ Error al obtener estadísticas: {e}")
            return None
    
    def print_species_info(self, species_list):
        """
        Imprime información detallada de las especies
        Args:
            species_list (list): Lista de especies a mostrar
        """
        if not species_list:
            print("📋 No hay especies para mostrar")
            return
        
        print("\n" + "="*80)
        print("🌳 ESPECIES EN CONSERVACIÓN")
        print("="*80)
        
        for i, species in enumerate(species_list, 1):
            print(f"\n{i}. {species.nombreComun}")
            print(f"   ID: {species.id}")
            print(f"   Nombre Científico: {species.nombreCientifico or 'No especificado'}")
            print(f"   Estado de Conservación: {species.estadoConservacion} (ID: {species.estadoConservacionId})")
            print(f"   Zona ID: {species.zonaId or 'No asignada'}")
        
        print("\n" + "="*80)
    
    def print_conservation_statistics(self, stats):
        """
        Imprime estadísticas de conservación de manera organizada
        Args:
            stats: Objeto con estadísticas de conservación
        """
        if not stats:
            print("📊 No hay estadísticas disponibles")
            return
        
        print("\n" + "="*80)
        print("📊 ESTADÍSTICAS DE CONSERVACIÓN")
        print("="*80)
        print(f"🌳 Total de especies activas: {stats.totalActiveSpecies}")
        print(f"🔒 Especies en conservación: {stats.speciesInConservation}")
        print(f"❓ Especies sin estado de conservación: {stats.speciesWithoutConservationStatus}")
        print(f"📋 Total de estados de conservación: {stats.totalConservationStates}")
        
        # Calcular porcentajes
        if stats.totalActiveSpecies > 0:
            conservation_percentage = (stats.speciesInConservation / stats.totalActiveSpecies) * 100
            print(f"📈 Porcentaje en conservación: {conservation_percentage:.1f}%")
        
        print("="*80)
    
    def check_service_status(self):
        """Verifica si el servicio está disponible"""
        try:
            response = requests.get(self.service_url.replace("?wsdl", ""), timeout=5)
            if response.status_code == 200:
                print("✅ Servicio SOAP disponible")
                return True
            else:
                print(f"⚠️  Servicio responde con código: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Servicio no disponible: {e}")
            return False


def main():
    """Función principal del cliente"""
    print("🚀 Cliente Python para Especies en Conservación")
    print("================================================")
    
    # Crear cliente
    client = ConservationSpeciesClient()
    
    while True:
        print("\n📋 MENÚ DE OPCIONES:")
        print("1. Obtener todas las especies en conservación")
        print("2. Obtener especies por estado de conservación específico")
        print("3. Obtener estadísticas de conservación")
        print("4. Verificar estado del servicio")
        print("5. Reconectar al servicio")
        print("6. Salir")
        
        try:
            opcion = input("\nSelecciona una opción (1-6): ").strip()
            
            if opcion == "1":
                species = client.get_all_species_in_conservation()
                client.print_species_info(species)
                
            elif opcion == "2":
                try:
                    estado_id = int(input("Ingresa el ID del estado de conservación: "))
                    species = client.get_species_by_conservation_state(estado_id)
                    client.print_species_info(species)
                except ValueError:
                    print("❌ Por favor ingresa un número válido")
                    
            elif opcion == "3":
                stats = client.get_conservation_statistics()
                client.print_conservation_statistics(stats)
                    
            elif opcion == "4":
                client.check_service_status()
                
            elif opcion == "5":
                client.retry_connection()
                
            elif opcion == "6":
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción no válida. Selecciona 1, 2, 3, 4, 5 o 6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Cliente interrumpido por el usuario. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
