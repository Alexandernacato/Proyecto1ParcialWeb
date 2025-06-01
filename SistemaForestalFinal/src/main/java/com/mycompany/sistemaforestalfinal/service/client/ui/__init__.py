"""
Configuración de importaciones para el módulo UI
"""
import sys
import os

# Add parent directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.dirname(current_dir)
sys.path.insert(0, client_dir)

# Importar todos los componentes principales
from .main_window import MainWindow
from .components.header import HeaderComponent
from .components.sidebar import SidebarComponent
from .components.footer import FooterComponent
from .components.content_area import ContentAreaComponent

# Importar gestores
from .managers.species_manager import SpeciesManager
from .managers.zones_manager import ZonesManager

# Importar utilidades
from utils.theme_manager import ThemeManager
from utils.logger import Logger

__all__ = [
    'MainWindow',
    'HeaderComponent',
    'SidebarComponent', 
    'FooterComponent',
    'ContentAreaComponent',
    'SpeciesManager',
    'ZonesManager',
    'ThemeManager',
    'Logger'
]
