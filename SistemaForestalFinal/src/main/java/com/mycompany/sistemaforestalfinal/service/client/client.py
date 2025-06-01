#!/usr/bin/env python3
"""
🌳 Forest Species Management Client - Refactorizado Modular
Arquitectura modular siguiendo lineamientos PLANNING.md (<500 líneas por archivo)
"""

import customtkinter as ctk
import sys
from pathlib import Path

# Configurar imports relativos
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir.parent))

# Imports de módulos core existentes
from core.soap_client import SOAPClientManager
from core.data_manager import DataManager

# Imports de UI modular refactorizada
from ui.main_window import MainWindow

# Configuración del tema moderno
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ForestManagementClient:
    """Cliente forestal principal - Orquestrador de componentes (<500 líneas)"""
    
    def __init__(self):
        """Inicializar cliente con arquitectura modular"""
        # Inicializar componentes core
        self.soap_client = SOAPClientManager()
        self.data_manager = DataManager()  # DataManager uses its own SOAP client with zeep
        
        # Configurar ventana principal con arquitectura modular
        self.main_window = MainWindow(
            soap_client=self.soap_client,
            data_manager=self.data_manager
        )
        
        # Mostrar mensaje de inicio
        self.main_window.logger.success("🌟 Forest Management System Ready!")
        self.main_window.logger.info("✨ Modular architecture loaded successfully")
    
    def ejecutar(self):
        """Ejecutar la aplicación principal"""
        try:
            self.main_window.ejecutar()
        except Exception as e:
            print(f"❌ Error running application: {e}")
            raise


def main():
    """Función principal del sistema"""
    try:
        print("🌳 Starting Modern Forest Species Management System...")
        print("📦 Loading modular architecture...")
        
        # Crear y ejecutar aplicación
        app = ForestManagementClient()
        app.ejecutar()
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
