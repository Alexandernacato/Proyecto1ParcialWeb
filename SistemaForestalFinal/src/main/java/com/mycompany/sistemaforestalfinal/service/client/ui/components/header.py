"""
🏠 Header Component - Componente de cabecera moderna
"""

import customtkinter as ctk
import sys
import os

# Add parent directories to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, client_dir)

from utils.theme_manager import ThemeManager


class HeaderComponent:
    """Componente de cabecera moderna estilo React"""
    
    def __init__(self, parent, theme_manager: ThemeManager):
        """Inicializar componente de cabecera"""
        self.parent = parent
        self.theme_manager = theme_manager
        self.connection_indicator = None
        self.species_counter = None
        self._crear_header()
    
    def _crear_header(self):
        """Crear header moderno estilo React"""
        self.header_frame = ctk.CTkFrame(
            self.parent,
            height=80,
            fg_color=self.theme_manager.obtener_color('primary'),
            corner_radius=0
        )
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Contenedor del header
        header_content = ctk.CTkFrame(
            self.header_frame, 
            fg_color="transparent"
        )
        header_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Logo y título
        self._crear_titulo(header_content)
        
        # Indicadores de estado
        self._crear_indicadores(header_content)
    
    def _crear_titulo(self, parent):
        """Crear sección de título y logo"""
        title_frame = ctk.CTkFrame(parent, fg_color="transparent")
        title_frame.pack(side="left", fill="y")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🌳 Modern Forest Management",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", pady=10)
    
    def _crear_indicadores(self, parent):
        """Crear indicadores de estado"""
        status_frame = ctk.CTkFrame(parent, fg_color="transparent")
        status_frame.pack(side="right", fill="y")
        
        # Indicador de conexión
        self.connection_indicator = ctk.CTkLabel(
            status_frame,
            text="🔴 Disconnected",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.connection_indicator.pack(side="right", padx=(0, 20), pady=10)
        
        # Contador de especies
        self.species_counter = ctk.CTkLabel(
            status_frame,
            text="📊 Species: 0",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.species_counter.pack(side="right", padx=(0, 20), pady=10)
    
    def actualizar_conexion(self, conectado: bool):
        """Actualizar indicador de conexión"""
        if self.connection_indicator:
            texto = "🟢 Connected" if conectado else "🔴 Disconnected"
            self.connection_indicator.configure(text=texto)
    
    def actualizar_contador_especies(self, cantidad: int):
        """Actualizar contador de especies"""
        if self.species_counter:
            self.species_counter.configure(text=f"📊 Species: {cantidad}")
    
    def obtener_altura(self) -> int:
        """Obtener altura del header"""
        return 80
