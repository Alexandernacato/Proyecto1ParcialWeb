"""
🏠 Main Window - Ventana principal refactorizada
"""

import customtkinter as ctk
import threading
from pathlib import Path
import sys
import os

# Add parent directories to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.dirname(current_dir)
sys.path.insert(0, client_dir)

from .components.header import HeaderComponent
from .components.sidebar import SidebarComponent
from .components.footer import FooterComponent
from .components.content_area import ContentAreaComponent
from .managers.species_manager import SpeciesManager
from .managers.zones_manager import ZonesManager
from utils.theme_manager import ThemeManager
from utils.logger import Logger


class MainWindow:
    """Ventana principal de la aplicación - Arquitectura modular"""
    
    def __init__(self, soap_client, data_manager):
        """Inicializar ventana principal"""
        self.soap_client = soap_client
        self.data_manager = data_manager
        
        # Componentes base
        self.theme_manager = ThemeManager()
        self.logger = Logger()
          # UI Components
        self.header = None
        self.sidebar = None
        self.footer = None
        self.content_area = None
        
        # Gestores funcionales
        self.species_manager = None
        self.zones_manager = None
        
        # Configurar ventana
        self._configurar_ventana()
        
        # Configurar componentes
        self._configurar_componentes()
        
        # Configurar gestores
        self._configurar_gestores()
        
        # Configurar logging
        self._configurar_logging()
        
        # Mensaje de bienvenida
        self.logger.success("🎉 Welcome to Modern Forest Management System")
    
    def _configurar_ventana(self):
        """Configurar ventana principal"""
        self.root = ctk.CTk()
        self.root.title("🌳 Modern Forest Species Management")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
          # Aplicar tema
        self.theme_manager.aplicar_tema()
    
    def _configurar_componentes(self):
        """Configurar componentes de UI"""
        # Header
        self.header = HeaderComponent(self.root, self.theme_manager)
        
        # Container principal
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Sidebar
        self.sidebar = SidebarComponent(
            main_container,
            self.theme_manager,
            self._obtener_callbacks_sidebar()
        )
        
        # Área de contenido
        self.content_area = ContentAreaComponent(
            main_container,
            self.theme_manager,
            self.logger
        )
        
        # Footer
        self.footer = FooterComponent(self.root, self.theme_manager)
    
    def _configurar_gestores(self):
        """Configurar gestores de funcionalidad"""
        # Gestor de especies
        self.species_manager = SpeciesManager(
            data_manager=self.data_manager,
            content_area=self.content_area,
            theme_manager=self.theme_manager,
            logger=self.logger
        )
        
        # Gestor de zonas
        self.zones_manager = ZonesManager(
            data_manager=self.data_manager,
            content_area=self.content_area,
            theme_manager=self.theme_manager,
            logger=self.logger
        )
    
    def _configurar_logging(self):
        """Configurar sistema de logging"""
        # Configurar tab de log
        log_tab = self.content_area.obtener_tab("log")
        if log_tab:
            self._configurar_tab_log(log_tab)
        
        # Configurar tab de estadísticas
        stats_tab = self.content_area.obtener_tab("stats")
        if stats_tab:
            self._configurar_tab_stats(stats_tab)
    
    def _configurar_tab_log(self, log_frame):
        """Configurar pestaña de log"""
        # Header del log
        header_frame = ctk.CTkFrame(log_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📋 Activity Log",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.theme_manager.obtener_color('primary')
        )
        title_label.pack(side="left")
        
        # Botón para limpiar log
        estilo_error = self.theme_manager.obtener_estilo_boton("error")
        clear_button = ctk.CTkButton(
            header_frame,
            text="🗑️ Clear Log",
            command=self.logger.limpiar,
            width=100,
            **estilo_error
        )
        clear_button.pack(side="right")
        
        # Área de texto para el log
        log_text = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        log_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Conectar logger con el widget
        self.logger.agregar_widget(log_text)
    
    def _configurar_tab_stats(self, stats_frame):
        """Configurar pestaña de estadísticas"""
        # Header
        header_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 System Statistics",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.theme_manager.obtener_color('primary')
        )
        title_label.pack(side="left")
        
        # Botón de actualizar estadísticas
        estilo_info = self.theme_manager.obtener_estilo_boton("info")
        refresh_button = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            command=self._actualizar_stats,
            width=100,
            **estilo_info
        )
        refresh_button.pack(side="right")
        
        # Grid de estadísticas
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="both", expand=True, padx=20, pady=10)
        
        self._crear_tarjetas_stats(stats_grid)
    
    def _crear_tarjetas_stats(self, parent):
        """Crear tarjetas de estadísticas"""
        stats_data = [
            ("🌳", "Total Species", "0", self.theme_manager.obtener_color("success")),
            ("🌍", "Total Zones", "0", self.theme_manager.obtener_color("info")),
            ("🛡️", "Conservation States", "0", self.theme_manager.obtener_color("warning")),
            ("🔄", "Operations Today", "0", self.theme_manager.obtener_color("primary"))
        ]
        
        self.stats_cards = {}
        
        for i, (icon, title, value, color) in enumerate(stats_data):
            card = ctk.CTkFrame(parent, fg_color=color, corner_radius=15)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
            parent.grid_columnconfigure(i%2, weight=1)
            
            # Icono
            icon_label = ctk.CTkLabel(
                card,
                text=icon,
                font=ctk.CTkFont(size=32),
                text_color="white"
            )
            icon_label.pack(pady=(20, 5))
            
            # Título
            title_label = ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="white"
            )
            title_label.pack()
            
            # Valor
            value_label = ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="white"
            )
            value_label.pack(pady=(5, 20))
            
            self.stats_cards[title] = value_label
    
    def _actualizar_stats(self):
        """Actualizar estadísticas del sistema"""
        def _actualizar_thread():
            try:
                # Obtener estadísticas
                species_count = len(self.data_manager.get_all_species())
                zones_count = len(self.data_manager.get_all_zones())
                conservation_count = len(self.data_manager.get_all_conservation_states())
                
                # Actualizar UI en hilo principal
                self.root.after(0, self._aplicar_stats, species_count, zones_count, conservation_count)
                
            except Exception as e:
                self.root.after(0, self.logger.error, f"Error updating statistics: {e}")
        
        threading.Thread(target=_actualizar_thread, daemon=True).start()
    
    def _aplicar_stats(self, species_count, zones_count, conservation_count):
        """Aplicar estadísticas a las tarjetas"""
        try:
            if "Total Species" in self.stats_cards:
                self.stats_cards["Total Species"].configure(text=str(species_count))
                # Actualizar header también
                if self.header:
                    self.header.actualizar_contador_especies(species_count)
            
            if "Total Zones" in self.stats_cards:
                self.stats_cards["Total Zones"].configure(text=str(zones_count))
            
            if "Conservation States" in self.stats_cards:
                self.stats_cards["Conservation States"].configure(text=str(conservation_count))
            
            self.logger.success("📊 Statistics updated successfully")
        except Exception as e:
            self.logger.error(f"Error applying statistics: {e}")
    
    def conectar_servicios(self):
        """Conectar a servicios SOAP"""
        def _conectar_thread():
            try:
                self.logger.info("🔌 Connecting to SOAP services...")
                success = self.soap_client.connect()
                
                if success:
                    self.root.after(0, self._al_conectar_exitoso)
                else:
                    self.root.after(0, self._al_fallar_conexion)
                    
            except Exception as e:
                self.root.after(0, self._al_error_conexion, str(e))
        
        threading.Thread(target=_conectar_thread, daemon=True).start()
    
    def _al_conectar_exitoso(self):
        """Callback para conexión exitosa"""
        self.logger.success("✅ Connected to SOAP services successfully")
        if self.header:
            self.header.actualizar_conexion(True)
        
        # Cargar datos iniciales
        self._cargar_datos_iniciales()
    
    def _al_fallar_conexion(self):
        """Callback para fallo en conexión"""
        self.logger.error("❌ Failed to connect to SOAP services")
        if self.header:
            self.header.actualizar_conexion(False)
    
    def _al_error_conexion(self, error):
        """Callback para error en conexión"""
        self.logger.error(f"💥 Connection error: {error}")
        if self.header:
            self.header.actualizar_conexion(False)
    
    def _cargar_datos_iniciales(self):
        """Cargar datos iniciales tras conexión"""
        def _cargar_thread():
            try:
                # Cargar datos de referencia
                zones = self.data_manager.get_all_zones()
                states = self.data_manager.get_all_conservation_states()
                self.root.after(0, self.logger.info, f"📍 Loaded {len(zones)} zones and {len(states)} conservation states")
                
                # Actualizar estadísticas
                self.root.after(0, self._actualizar_stats)
                
            except Exception as e:
                self.root.after(0, self.logger.error, f"Error loading initial data: {e}")
        
        threading.Thread(target=_cargar_thread, daemon=True).start()
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        try:
            # Programar conexión inicial
            self.root.after(1000, self.conectar_servicios)
            
            # Iniciar bucle principal
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Error running application: {e}")
            raise
    
    def _obtener_callbacks_sidebar(self):
        """Obtener callbacks para acciones de sidebar"""
        return {
            # Conexión
            'connect_soap': self.conectar_servicios,
            'test_connection': self._probar_conexion,
            
            # Especies
            'view_all_species': lambda: self._cambiar_tab_y_ejecutar("species", "ver_todas"),
            
            # Zonas
            'view_zones': lambda: self._cambiar_tab_y_ejecutar("zones", "ver_todas"),
            
            # Utilidades
            'refresh_data': self._refrescar_datos,
            'clear_log': self.logger.limpiar,
            'update_stats': self._actualizar_stats
        }
    
    def _cambiar_tab_y_ejecutar(self, tab_name: str, metodo: str):
        """Cambiar a una pestaña y ejecutar método del gestor correspondiente"""
        # Cambiar a la pestaña
        self.content_area.cambiar_tab(tab_name)
          # Ejecutar método
        if tab_name == "species" and hasattr(self.species_manager, metodo):
            getattr(self.species_manager, metodo)()
        elif tab_name == "zones" and hasattr(self.zones_manager, metodo):
            getattr(self.zones_manager, metodo)()
    
    def _probar_conexion(self):
        """Probar conexión SOAP"""
        if self.soap_client.is_connected():
            self.logger.success("✅ SOAP connection is active")
        else:
            self.logger.warning("⚠️ SOAP connection is not active")
    
    def _buscar_por_id(self):
        """Buscar especie por ID"""
        # This method might be deprecated or refactored if search is centralized
        self.content_area.cambiar_tab("species")
        self.logger.info("🔍 Activating Search by ID functionality")
        
        if self.species_manager:
            # This now directly calls the species_manager's unified search
            # It assumes the species_manager's search UI is already visible
            # and the user will input the ID there.
            # For a direct dialog, that logic would be here or in species_manager
            pass # Functionality moved to species_manager search bar

    def _buscar_por_nombre(self):
        """Buscar especie por nombre"""
        # This method might be deprecated or refactored if search is centralized
        self.content_area.cambiar_tab("species")
        self.logger.info("🔍 Activating Search by Name functionality")

        if self.species_manager:
            # Similar to _buscar_por_id, functionality moved to species_manager search bar
            pass # Functionality moved to species_manager search bar

    def _refrescar_datos(self):
        """Refrescar todos los datos"""
        self.logger.info("🔄 Refreshing all data...")
        
        # Refrescar especies
        if self.species_manager:
            self.species_manager.ver_todas()
        
        # Refrescar zonas
        if self.zones_manager:
            self.zones_manager.ver_todas()
        
        # Refrescar estadísticas
        self._actualizar_stats()
        
        self.logger.success("✅ Data refreshed successfully")
