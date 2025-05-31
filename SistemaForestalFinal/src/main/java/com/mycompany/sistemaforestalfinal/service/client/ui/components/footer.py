"""
🦶 Footer Component - Componente de pie de página
"""

import customtkinter as ctk
import sys
import os

# Add parent directories to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, client_dir)

from utils.theme_manager import ThemeManager


class FooterComponent:
    """Componente de pie de página moderno"""
    
    def __init__(self, parent, theme_manager: ThemeManager):
        """Inicializar componente de pie de página"""
        self.parent = parent
        self.theme_manager = theme_manager
        self._crear_footer()
    
    def _crear_footer(self):
        """Crear footer moderno"""
        self.footer_frame = ctk.CTkFrame(
            self.parent,
            height=40,
            fg_color=self.theme_manager.obtener_color('surface'),
            corner_radius=0
        )
        self.footer_frame.pack(fill="x", side="bottom")
        self.footer_frame.pack_propagate(False)
        
        # Texto del footer
        footer_label = ctk.CTkLabel(
            self.footer_frame,
            text="Modern Forest Species Management System v2.0 | Ready for modern operations",
            font=ctk.CTkFont(size=12),
            text_color=self.theme_manager.obtener_color('text_secondary')
        )
        footer_label.pack(pady=10)
    
    def actualizar_texto(self, texto: str):
        """Actualizar texto del footer"""
        for widget in self.footer_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text=texto)
                break
    
    def obtener_altura(self) -> int:
        """Obtener altura del footer"""
        return 40
