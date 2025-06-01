"""
🌍 Zones Manager - Gestor de operaciones de zonas
"""

import customtkinter as ctk
import threading
from typing import List, Optional
import sys
import os

# Add parent directories to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, client_dir)

from utils.theme_manager import ThemeManager
from utils.logger import Logger


class ZonesManager:
    """Gestor de operaciones CRUD para zonas"""
    
    def __init__(self, data_manager, content_area, theme_manager: ThemeManager, logger: Logger):
        """Inicializar gestor de zonas"""
        self.data_manager = data_manager
        self.content_area = content_area
        self.theme_manager = theme_manager
        self.logger = logger
        
        # Estado del gestor
        self.zonas_actuales = []
        self.zones_content = None
        
        # Configurar pestaña de zonas
        self._configurar_tab_zonas()
    
    def _configurar_tab_zonas(self):
        """Configurar pestaña de zonas"""
        zones_frame = self.content_area.obtener_tab("zones")
        if not zones_frame:
            self.logger.error("Zones tab not found")
            return
        
        # Header de la pestaña
        self._crear_header_zonas(zones_frame)
        
        # Área de contenido para zonas
        self._crear_area_contenido(zones_frame)
        
        # Mensaje inicial
        self._mostrar_mensaje_inicial()
    
    def _crear_header_zonas(self, parent):
        """Crear header de la pestaña de zonas"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="🌍 Zones Management",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.theme_manager.obtener_color('primary')
        )
        title_label.pack(side="left")
        
        # Botones CRUD para zonas
        self._crear_botones_zonas(header_frame)
    
    def _crear_botones_zonas(self, parent):
        """Crear botones CRUD para zonas"""
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        botones = [
            ("➕ Add Zone", self.crear, "success"),
            ("🗑️ Delete Zone", self.eliminar, "error"),
            ("👁️ View Zones", self.ver_todas, "info")
        ]
        
        for texto, comando, tipo in botones:
            estilo = self.theme_manager.obtener_estilo_boton(tipo)
            ctk.CTkButton(
                buttons_frame,
                text=texto,
                command=comando,
                width=120,
                **estilo
            ).pack(side="left", padx=5)
    
    def _crear_area_contenido(self, parent):
        """Crear área de contenido para zonas"""
        self.zones_content = ctk.CTkScrollableFrame(
            parent,
            fg_color=self.theme_manager.obtener_color('background'),
            corner_radius=10
        )
        self.zones_content.pack(fill="both", expand=True, padx=20, pady=10)
    
    def _mostrar_mensaje_inicial(self):
        """Mostrar mensaje inicial en el área de zonas"""
        if self.zones_content:
            initial_label = ctk.CTkLabel(
                self.zones_content,
                text="🌍 Use the buttons above to manage zones",
                font=ctk.CTkFont(size=16),
                text_color=self.theme_manager.obtener_color('text_secondary')
            )
            initial_label.pack(pady=50)
    
    def ver_todas(self):
        """Ver todas las zonas"""
        self.logger.info("🔍 Loading all zones...")
        threading.Thread(target=self._cargar_zonas_thread, daemon=True).start()
    
    def _cargar_zonas_thread(self):
        """Hilo para cargar todas las zonas"""
        try:
            zonas_lista = self.data_manager.get_all_zones()
            self.zonas_actuales = zonas_lista
            
            # Actualizar UI en el hilo principal
            if hasattr(self.content_area, 'parent'):
                self.content_area.parent.after(0, self._mostrar_zonas, zonas_lista)
        except Exception as e:
            if hasattr(self.content_area, 'parent'):
                self.content_area.parent.after(0, self.logger.error, f"Error loading zones: {e}")
    
    def _mostrar_zonas(self, zonas_lista):
        """Mostrar lista de zonas en la interfaz"""
        try:
            if not self.zones_content:
                self.logger.warning("Zones display frame not ready")
                return
            
            # Limpiar display actual
            for widget in self.zones_content.winfo_children():
                widget.destroy()
            
            if not zonas_lista:
                self._mostrar_sin_zonas()
                return
            
            # Mostrar zonas en diseño de tarjetas
            for zona in zonas_lista:
                self._crear_tarjeta_zona(zona)
            
            self.logger.success(f"✅ Displayed {len(zonas_lista)} zones")
            
        except Exception as e:
            self.logger.error(f"Error displaying zones list: {e}")
    
    def _crear_tarjeta_zona(self, zona):
        """Crear tarjeta individual para una zona"""
        # Tarjeta de zona
        tarjeta = ctk.CTkFrame(self.zones_content)
        tarjeta.pack(fill="x", padx=5, pady=5)
        
        # Header de la tarjeta
        header_frame = ctk.CTkFrame(tarjeta)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # ID y nombre de la zona
        id_label = ctk.CTkLabel(
            header_frame,
            text=f"ID: {zona.id}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3B82F6"
        )
        id_label.pack(side="left", padx=(10, 5))
        
        nombre_label = ctk.CTkLabel(
            header_frame,
            text=f"🌍 {zona.nombre}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        nombre_label.pack(side="left", padx=5)
        
        # Botones de acción
        self._crear_botones_zona(tarjeta, zona)
    
    def _crear_botones_zona(self, parent, zona):
        """Crear botones de acción para la zona"""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Botón eliminar
        ctk.CTkButton(
            button_frame,
            text="🗑️ Delete",
            width=80,
            height=30,
            command=lambda: self._eliminar_zona(zona),
            **self.theme_manager.obtener_estilo_boton("error")
        ).pack(side="left", padx=(10, 5), pady=5)
    
    def _mostrar_sin_zonas(self):
        """Mostrar mensaje cuando no hay zonas"""
        no_data_label = ctk.CTkLabel(
            self.zones_content,
            text="📋 No zones data to display",
            font=ctk.CTkFont(size=14)
        )
        no_data_label.pack(pady=20)
    
    def crear(self):
        """Crear nueva zona"""
        self.logger.info("🆕 Opening create zone dialog...")
        # TODO: Implementar diálogo de creación de zona
        pass
    
    def eliminar(self):
        """Eliminar zona seleccionada"""
        self.logger.info("🗑️ Select zone to delete...")
        # TODO: Implementar diálogo de selección y eliminación
        pass
    
    def _eliminar_zona(self, zona):
        """Eliminar zona específica"""
        self.logger.info(f"🗑️ Deleting zone: {zona.nombre}")
        # TODO: Implementar eliminación de zona
        pass
