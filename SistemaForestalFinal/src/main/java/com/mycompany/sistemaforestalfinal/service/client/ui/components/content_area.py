"""
📱 Content Area - Área de contenido principal con pestañas
"""

import customtkinter as ctk
import sys
import os

# Add parent directories to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, client_dir)

from utils.theme_manager import ThemeManager
from utils.logger import Logger


class ContentAreaComponent:
    """Área de contenido principal con sistema de pestañas"""
    
    def __init__(self, parent, theme_manager: ThemeManager, logger: Logger = None):
        """Inicializar área de contenido"""
        self.parent = parent
        self.theme_manager = theme_manager
        self.logger = logger or Logger()
        self.tabview = None
        self.tabs = {}
        self._crear_area_contenido()
    
    def _crear_area_contenido(self):
        """Crear área de contenido con diseño de tarjetas"""
        self.content_frame = ctk.CTkFrame(
            self.parent,
            fg_color=self.theme_manager.obtener_color('background'),
            corner_radius=12
        )
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Configurar notebook moderno
        self._crear_tabview()
        
        # Crear pestañas
        self._crear_pestanas()
    
    def _crear_tabview(self):
        """Crear componente de pestañas moderno"""
        self.tabview = ctk.CTkTabview(
            self.content_frame,
            height=400,
            fg_color=self.theme_manager.obtener_color('surface'),
            segmented_button_fg_color=self.theme_manager.obtener_color('primary'),
            segmented_button_selected_color=self.theme_manager.obtener_color('secondary')
        )
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)
    
    def _crear_pestanas(self):
        """Crear pestañas principales"""
        # Pestañas del sistema
        pestanas = [
            ("🗂️ Species Data", "species"),
            ("🌍 Zones Management", "zones"), 
            ("📋 Activity Log", "log"),
            ("📊 Statistics", "stats")
        ]
        
        for titulo, nombre in pestanas:
            self.tabview.add(titulo)
            self.tabs[nombre] = self.tabview.tab(titulo)
    
    def obtener_tab(self, nombre: str):
        """Obtener pestaña por nombre"""
        return self.tabs.get(nombre)
    
    def cambiar_tab(self, nombre: str):
        """Cambiar a una pestaña específica"""
        if nombre in self.tabs:
            # Cambiar a la pestaña correspondiente
            for tab_name, tab_frame in self.tabs.items():
                if tab_name == nombre:
                    # Encontrar el título de la pestaña
                    for i, (titulo, tab_id) in enumerate([
                        ("🗂️ Species Data", "species"),
                        ("🌍 Zones Management", "zones"),
                        ("📋 Activity Log", "log"),
                        ("📊 Statistics", "stats")
                    ]):
                        if tab_id == nombre:
                            self.tabview.set(titulo)
                            break
    
    def limpiar_tab(self, nombre: str):
        """Limpiar contenido de una pestaña"""
        tab = self.obtener_tab(nombre)
        if tab:
            for widget in tab.winfo_children():
                widget.destroy()
    
    def agregar_widget_a_tab(self, nombre: str, widget):
        """Agregar widget a una pestaña específica"""
        tab = self.obtener_tab(nombre)
        if tab:
            widget.pack(in_=tab, fill="both", expand=True)
        else:
            self.logger.error(f"Tab '{nombre}' not found")
    
    def obtener_frame_contenido(self):
        """Obtener frame principal de contenido"""
        return self.content_frame
