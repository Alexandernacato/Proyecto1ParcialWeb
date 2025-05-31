"""
🎨 Theme Manager - Gestión de temas y colores modernos
"""

import customtkinter as ctk


class ThemeManager:
    """Gestor de temas modernos estilo React/Material Design"""
    
    def __init__(self):
        """Inicializar gestor de temas"""
        self.is_dark_mode = True
        self._configurar_colores()
    
    def _configurar_colores(self):
        """Configurar paleta de colores moderna"""
        self.colores_modernos = {
            'primary': "#2E7D32",      # Verde principal
            'secondary': "#4CAF50",    # Verde secundario
            'accent': "#81C784",       # Verde claro
            'warning': "#FF9800",      # Naranja
            'error': "#F44336",        # Rojo
            'success': "#4CAF50",      # Verde
            'info': "#2196F3",         # Azul
            'background': "#1a1a1a",   # Fondo oscuro
            'surface': "#2d2d2d",      # Superficie
            'text_primary': "#ffffff", # Texto principal
            'text_secondary': "#b0b0b0" # Texto secundario
        }
    
    def obtener_color(self, nombre_color: str) -> str:
        """Obtener color por nombre"""
        return self.colores_modernos.get(nombre_color, "#ffffff")
    
    def aplicar_tema(self):
        """Aplicar tema actual a la aplicación"""
        ctk.set_appearance_mode("dark" if self.is_dark_mode else "light")
        ctk.set_default_color_theme("green")
    
    def cambiar_modo(self):
        """Cambiar entre modo oscuro y claro"""
        self.is_dark_mode = not self.is_dark_mode
        self.aplicar_tema()
    
    def obtener_estilo_boton(self, tipo: str = "primary") -> dict:
        """Obtener configuración de estilo para botones"""
        estilos = {
            "primary": {
                "fg_color": self.obtener_color("primary"),
                "hover_color": "#1B5E20",
                "text_color": "white"
            },
            "secondary": {
                "fg_color": self.obtener_color("secondary"),
                "hover_color": "#388E3C",
                "text_color": "white"
            },
            "success": {
                "fg_color": self.obtener_color("success"),
                "hover_color": "#45a049",
                "text_color": "white"
            },
            "warning": {
                "fg_color": self.obtener_color("warning"),
                "hover_color": "#e68900",
                "text_color": "white"
            },
            "error": {
                "fg_color": self.obtener_color("error"),
                "hover_color": "#c82333",
                "text_color": "white"
            },
            "info": {
                "fg_color": self.obtener_color("info"),
                "hover_color": "#117a8b",
                "text_color": "white"
            }
        }
        return estilos.get(tipo, estilos["primary"])
