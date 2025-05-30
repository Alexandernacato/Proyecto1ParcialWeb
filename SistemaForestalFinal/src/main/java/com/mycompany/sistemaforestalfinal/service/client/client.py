#!/usr/bin/env python3
"""
🌳 Forest Species Management Client - Refactored Version
Arquitectura modular siguiendo PLANNING.md (archivo < 500 líneas)
"""

import customtkinter as ctk
from tkinter import messagebox
import threading
import sys
from pathlib import Path
from datetime import datetime

# Configurar imports relativos
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Imports de módulos existentes
from core.soap_client import SOAPClientManager
from core.data_manager import DataManager
from gui.main_interface import HeaderComponent, SidebarComponent, TabbedContentArea, FooterComponent
from gui.species_dialogs import SpeciesCreateDialog, SpeciesEditDialog, SpeciesDeleteDialog

# Configuración del tema moderno
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ModernForestClient:
    """Cliente forestal moderno refactorizado (< 500 líneas)"""
    
    def __init__(self):
        """Inicializar cliente con arquitectura modular"""
        # Configurar ventana principal
        self.root = ctk.CTk()
        self.root.title("🌳 Forest Species Management System")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        
        # Inicializar componentes core
        self.soap_client = SOAPClientManager()
        self.data_manager = DataManager(self.soap_client)
        
        # Estado de la aplicación
        self.current_species_list = []
        self.is_dark_mode = True
        
        # Configurar interfaz
        self._setup_interface()
        self._setup_callbacks()
        
        # Conectar al servicio
        self._initial_connection()
    
    def _setup_interface(self):
        """Configurar interfaz usando componentes modulares"""
        # Header
        self.header = HeaderComponent(self.root)
        
        # Contenedor principal
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Configurar grid
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = SidebarComponent(main_container)
        sidebar_callbacks = {
            'connect': self._connect_service,
            'disconnect': self._disconnect_service,
            'view_all_species': self.view_all_species,
            'search_by_id': self.search_by_id,
            'view_zones': self.view_zones,
            'view_conservation_states': self.view_conservation_states,
            'create_species': self.create_species,
            'edit_species': self.edit_species,
            'delete_species': self.delete_species,
            'clear_results': self.clear_results,
            'clear_logs': self.clear_logs,
            'refresh_all_data': self.refresh_all_data,
            'toggle_theme': self.toggle_theme
        }
        for action, callback in sidebar_callbacks.items():
            self.sidebar.set_callback(action, callback)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        
        # Área de contenido con pestañas
        self.content_area = TabbedContentArea(
            main_container,
            callbacks={
                'log_message': self.log_message,
                'clear_logs': self.clear_logs
            }
        )
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=(2, 0))
        
        # Footer
        self.footer = FooterComponent(self.root)
        
        # Mensajes de bienvenida
        self.log_message("🌟 Welcome to Forest Species Management System!")
        self.log_message("Modular architecture following PLANNING.md guidelines.")
        self.log_message("=" * 70)
    
    def _setup_callbacks(self):
        """Configurar callbacks entre componentes"""
        # Callback para cambios de conexión
        self.soap_client.add_connection_callback(self._on_connection_change)
        
        # Callback para cambios de datos
        self.data_manager.add_data_change_callback(self._on_data_change)
    
    def _initial_connection(self):
        """Intentar conexión inicial"""
        self.log_message("🔄 Attempting initial connection...")
        threading.Thread(target=self._connect_service, daemon=True).start()
    
    def _connect_service(self):
        """Conectar al servicio SOAP"""
        try:
            self.soap_client.connect()
            self.root.after(0, self.log_message, "✅ Connected to SOAP service successfully")
            self._load_reference_data()
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Connection failed: {e}")
    
    def _disconnect_service(self):
        """Desconectar del servicio"""
        self.soap_client.disconnect()
        self.log_message("🔌 Disconnected from service")
    
    def _on_connection_change(self, connected: bool):
        """Callback para cambios de estado de conexión"""
        self.root.after(0, self.header.update_connection_status, connected)
    
    def _on_data_change(self, change_type: str, data: any):
        """Callback para cambios de datos"""
        if change_type in ['species_created', 'species_updated', 'species_deleted']:
            self.root.after(0, self.log_message, f"🔄 Data updated: {change_type}")
    
    def _load_reference_data(self):
        """Cargar datos de referencia en hilo separado"""
        def _load_thread():
            try:
                zones = self.data_manager.get_all_zones()
                states = self.data_manager.get_all_conservation_states()
                self.root.after(0, self.log_message, f"📍 Loaded {len(zones)} zones and {len(states)} conservation states")
            except Exception as e:
                self.root.after(0, self.log_message, f"❌ Error loading reference data: {e}")
        
        threading.Thread(target=_load_thread, daemon=True).start()
    
    # === Métodos de operaciones CRUD ===
    
    def view_all_species(self):
        """Ver todas las especies"""
        if not self._check_connection():
            return
        
        self.log_message("🔍 Loading all species...")
        threading.Thread(target=self._load_all_species_thread, daemon=True).start()
    
    def _load_all_species_thread(self):
        """Hilo para cargar todas las especies"""
        try:
            species_list = self.data_manager.get_all_species()
            self.current_species_list = species_list
            self.root.after(0, self._display_species_list, species_list, "All Species")
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Error loading species: {e}")
    
    def search_by_id(self):
        """Buscar especie por ID"""
        if not self._check_connection():
            return
        
        dialog = ctk.CTkInputDialog(text="Enter Species ID:", title="🔍 Search by ID")
        species_id_str = dialog.get_input()
        
        if species_id_str:
            try:
                species_id = int(species_id_str)
                threading.Thread(target=self._search_by_id_thread, args=(species_id,), daemon=True).start()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric ID")
    
    def _search_by_id_thread(self, species_id: int):
        """Hilo para buscar por ID"""
        try:
            species = self.data_manager.get_species_by_id(species_id)
            if species:
                self.root.after(0, self._display_species_list, [species], f"Species ID: {species_id}")
            else:
                self.root.after(0, self.log_message, f"❌ Species with ID {species_id} not found")
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Search error: {e}")
    
    def create_species(self):
        """Crear nueva especie"""
        if not self._check_connection():
            return
        
        try:
            zones = self.data_manager.get_all_zones()
            conservation_states = self.data_manager.get_all_conservation_states()
            
            if not zones or not conservation_states:
                self.log_message("⚠️ Loading reference data first...")
                self._load_reference_data()
                return
            
            dialog = SpeciesCreateDialog(
                self.root,
                zones=zones,
                conservation_states=conservation_states,
                on_submit=self._on_species_created
            )
            dialog.show()
        except Exception as e:
            self.log_message(f"❌ Error opening create dialog: {e}")
    
    def edit_species(self):
        """Editar especie existente"""
        if not self._check_connection():
            return
        
        if not self.current_species_list:
            self.log_message("ℹ️ Load species data first to edit")
            return
        
        dialog = ctk.CTkInputDialog(text="Enter Species ID to edit:", title="📝 Edit Species")
        species_id_str = dialog.get_input()
        
        if species_id_str:
            try:
                species_id = int(species_id_str)
                species = next((s for s in self.current_species_list if s.id == species_id), None)
                
                if species:
                    zones = self.data_manager.get_all_zones()
                    conservation_states = self.data_manager.get_all_conservation_states()
                    
                    edit_dialog = SpeciesEditDialog(
                        self.root,
                        species=species,
                        zones=zones,
                        conservation_states=conservation_states,
                        on_submit=self._on_species_updated
                    )
                    edit_dialog.show()
                else:
                    messagebox.showerror("Error", f"Species with ID {species_id} not found in current list")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric ID")
    
    def delete_species(self):
        """Eliminar especie"""
        if not self._check_connection():
            return
        
        if not self.current_species_list:
            self.log_message("ℹ️ Load species data first to delete")
            return
        
        dialog = ctk.CTkInputDialog(text="Enter Species ID to delete:", title="🗑️ Delete Species")
        species_id_str = dialog.get_input()
        
        if species_id_str:
            try:
                species_id = int(species_id_str)
                species = next((s for s in self.current_species_list if s.id == species_id), None)
                
                if species:
                    delete_dialog = SpeciesDeleteDialog(
                        self.root,
                        species=species,
                        on_confirm=self._on_species_deleted
                    )
                    delete_dialog.show()
                else:
                    messagebox.showerror("Error", f"Species with ID {species_id} not found in current list")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric ID")
    
    # === Callbacks para operaciones CRUD ===
    
    def _on_species_created(self, species, success: bool, message: str):
        """Callback para especie creada"""
        if success:
            self.log_message(f"✅ Species created: {message}")
            self._refresh_current_view()
        else:
            self.log_message(f"❌ Create failed: {message}")
            messagebox.showerror("Error", message)
    
    def _on_species_updated(self, species, success: bool, message: str):
        """Callback para especie actualizada"""
        if success:
            self.log_message(f"✅ Species updated: {message}")
            self._refresh_current_view()
        else:
            self.log_message(f"❌ Update failed: {message}")
            messagebox.showerror("Error", message)
    
    def _on_species_deleted(self, species_id: int, success: bool, message: str):
        """Callback para especie eliminada"""
        if success:
            self.log_message(f"✅ Species deleted: {message}")
            self._refresh_current_view()
        else:
            self.log_message(f"❌ Delete failed: {message}")
            messagebox.showerror("Error", message)
    
    # === Métodos de visualización ===
    
    def view_zones(self):
        """Ver zonas disponibles"""
        try:
            zones = self.data_manager.get_all_zones()
            if zones:
                self.log_message("🌍 Available zones:")
                self.log_message("=" * 40)
                for zone in zones:
                    self.log_message(f"📍 ID: {zone.id} - {zone.nombre}")
                self.log_message("=" * 40)
            else:
                self.log_message("ℹ️ No zones found")
        except Exception as e:
            self.log_message(f"❌ Error loading zones: {e}")
    
    def view_conservation_states(self):
        """Ver estados de conservación"""
        try:
            states = self.data_manager.get_all_conservation_states()
            if states:
                self.log_message("🛡️ Conservation states:")
                self.log_message("=" * 50)
                for state in states:
                    self.log_message(f"🛡️ ID: {state.id} - {state.nombre}")
                self.log_message("=" * 50)
            else:
                self.log_message("ℹ️ No conservation states found")
        except Exception as e:
            self.log_message(f"❌ Error loading conservation states: {e}")
    
    def _display_species_list(self, species_list, title: str):
        """Mostrar lista de especies"""
        self.log_message(f"✅ {title} - Found {len(species_list)} species:")
        self.log_message("=" * 80)
        
        if species_list:
            for i, species in enumerate(species_list, 1):
                self.log_message(f"🌿 {i}. {species.nombreComun}")
                self.log_message(f"   📋 ID: {species.id}")
                self.log_message(f"   🧬 Scientific: {species.nombreCientifico or 'Not specified'}")
                self.log_message(f"   🛡️ Status: {getattr(species, 'estadoConservacionNombre', 'Unknown')}")
                self.log_message(f"   🌍 Zone: {getattr(species, 'zonaNombre', 'Unknown')}")
                self.log_message(f"   ✅ Active: {'Yes' if species.activo else 'No'}")
                self.log_message("")
        else:
            self.log_message("ℹ️ No species found")
        
        self.log_message("=" * 80)
        
        # Actualizar lista en content area
        self.content_area.update_species_list(species_list)
    
    # === Métodos utilitarios ===
    
    def _check_connection(self) -> bool:
        """Verificar conexión"""
        if not self.soap_client.is_connected():
            messagebox.showerror("Connection Error", "No connection to service. Please reconnect.")
            return False
        return True
    
    def _refresh_current_view(self):
        """Refrescar vista actual"""
        if self.current_species_list:
            threading.Thread(target=self._load_all_species_thread, daemon=True).start()
    
    def log_message(self, message: str):
        """Registrar mensaje en logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.content_area.log_message(formatted_message)
    
    def clear_results(self):
        """Limpiar resultados"""
        self.content_area.clear_results()
        self.current_species_list = []
        self.log_message("🧹 Results cleared")
    
    def clear_logs(self):
        """Limpiar logs"""
        self.content_area.clear_logs()
    
    def refresh_all_data(self):
        """Refrescar todos los datos"""
        if not self._check_connection():
            return
        
        self.log_message("🔄 Refreshing all data...")
        self._load_reference_data()
        self._refresh_current_view()
    
    def toggle_theme(self):
        """Cambiar tema"""
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            ctk.set_appearance_mode("dark")
            self.log_message("🌙 Switched to dark mode")
        else:
            ctk.set_appearance_mode("light")
            self.log_message("☀️ Switched to light mode")
    
    def run(self):
        """Ejecutar aplicación"""
        self.root.mainloop()


def main():
    """Función principal"""
    try:
        app = ModernForestClient()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
