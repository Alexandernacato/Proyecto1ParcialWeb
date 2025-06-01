"""
🧭 Sidebar Component - Panel de navegación lateral
"""

import customtkinter as ctk
from typing import Dict, Callable
import sys
import os

# Add parent directories to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, client_dir)

from utils.theme_manager import ThemeManager


class SidebarComponent:
    """Componente de barra lateral con botones de navegación"""
    
    def __init__(self, parent, theme_manager: ThemeManager, callbacks: Dict[str, Callable] = None):
        """Inicializar componente de sidebar"""
        self.parent = parent
        self.theme_manager = theme_manager
        self.callbacks = callbacks or {}
        self._crear_sidebar()
    
    def _crear_sidebar(self):
        """Crear sidebar moderno con botones estilo Material Design"""
        self.sidebar_frame = ctk.CTkScrollableFrame(
            self.parent,
            width=280,
            fg_color=self.theme_manager.obtener_color('surface'),
            corner_radius=12
        )
        self.sidebar_frame.pack(side="left", fill="y", padx=(0, 10))
        
        # Título de la sidebar
        self._crear_titulo()
        
        # Crear grupos de botones
        self._crear_grupos_botones()
    
    def _crear_titulo(self):
        """Crear título de la sidebar"""
        sidebar_title = ctk.CTkLabel(
            self.sidebar_frame,
            text="🔧 Operations Panel",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.theme_manager.obtener_color('secondary')
        )
        sidebar_title.pack(pady=(10, 20))
    
    def _crear_grupos_botones(self):
        """Crear grupos de botones organizados por funcionalidad"""
        # Grupo de conexión
        self._crear_grupo_conexion()
        
        # Grupo de especies
        self._crear_grupo_especies()
        
        # Grupo de zonas
        self._crear_grupo_zonas()
        
        # Grupo de utilidades
        self._crear_grupo_utilidades()
    
    def _crear_grupo_conexion(self):
        """Crear grupo de botones de conexión"""
        self._crear_separador("🔌 Connection")
        
        botones_conexion = [
            ("🔗 Connect SOAP", "connect_soap", "primary"),
            ("📊 Test Connection", "test_connection", "info")
        ]
        
        for texto, comando, tipo in botones_conexion:
            self._crear_boton(texto, comando, tipo)
    
    def _crear_grupo_especies(self):
        """Crear grupo de botones de especies"""
        self._crear_separador("🌳 Species Operations")
        
        botones_especies = [
            ("👁️ View All Species", "view_all_species", "info"),
            ("➕ Create Species", "create_species", "success"),
            ("✏️ Edit Species", "edit_species", "warning"),
            ("🗑️ Delete Species", "delete_species", "error"),
            ("🔍 Search by ID", "search_by_id", "info"),
            ("🔍 Search by Name", "search_by_name", "info")
        ]
        
        for texto, comando, tipo in botones_especies:
            self._crear_boton(texto, comando, tipo)
    
    def _crear_grupo_zonas(self):
        """Crear grupo de botones de zonas"""
        self._crear_separador("🌍 Zones Operations")
        
        botones_zonas = [
            ("👁️ View Zones", "view_zones", "info"),
            ("➕ Create Zone", "create_zone", "success"),
            ("🗑️ Delete Zone", "delete_zone", "error")
        ]
        
        for texto, comando, tipo in botones_zonas:
            self._crear_boton(texto, comando, tipo)
    
    def _crear_grupo_utilidades(self):
        """Crear grupo de botones de utilidades"""
        self._crear_separador("🛠️ Utilities")
        
        botones_utilidades = [
            ("🔄 Refresh Data", "refresh_data", "info"),
            ("📋 Clear Log", "clear_log", "warning"),
            ("📊 Update Stats", "update_stats", "primary")
        ]
        
        for texto, comando, tipo in botones_utilidades:
            self._crear_boton(texto, comando, tipo)
    
    def _crear_separador(self, titulo: str):
        """Crear separador visual con título"""
        # Espacio
        ctk.CTkLabel(self.sidebar_frame, text="", height=10).pack()
        
        # Título del grupo
        titulo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text=titulo,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.theme_manager.obtener_color('accent')
        )
        titulo_label.pack(pady=(10, 5))
        
        # Línea separadora visual
        separator = ctk.CTkFrame(
            self.sidebar_frame,
            height=2,
            fg_color=self.theme_manager.obtener_color('accent')
        )
        separator.pack(fill="x", padx=20, pady=(0, 10))
    
    def _crear_boton(self, texto: str, comando: str, tipo: str):
        """Crear botón individual con estilo"""
        estilo = self.theme_manager.obtener_estilo_boton(tipo)
        
        def ejecutar_comando():
            if comando in self.callbacks:
                try:
                    self.callbacks[comando]()
                except Exception as e:
                    print(f"Error executing {comando}: {e}")
            else:
                print(f"Callback not found for: {comando}")
        
        boton = ctk.CTkButton(
            self.sidebar_frame,
            text=texto,
            command=ejecutar_comando,
            width=240,
            height=35,
            **estilo
        )
        boton.pack(pady=2, padx=10)
    
    def agregar_callback(self, comando: str, callback: Callable):
        """Agregar callback para un comando"""
        self.callbacks[comando] = callback
    
    def actualizar_callbacks(self, nuevos_callbacks: Dict[str, Callable]):
        """Actualizar todos los callbacks"""
        self.callbacks.update(nuevos_callbacks)
