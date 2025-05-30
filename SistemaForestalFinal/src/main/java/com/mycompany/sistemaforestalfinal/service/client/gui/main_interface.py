"""
🌳 Main Interface Components
Componentes principales de la interfaz de usuario
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Callable, List, Any
from datetime import datetime


class HeaderComponent:
    """Componente del header con título y estado de conexión"""
    
    def __init__(self, parent, title: str = "🌳 Forest Species Management System"):
        self.parent = parent
        self.title = title
        self.connection_callback: Optional[Callable] = None
        self.setup_header()
    
    def setup_header(self):
        """Crear header moderno con título y estado"""
        # Header frame
        self.header_frame = ctk.CTkFrame(self.parent, height=80, corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Título principal
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=self.title,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#1f538d", "#7fb7e8")
        )
        self.title_label.pack(side="left", padx=20, pady=20)
        
        # Frame para estado de conexión
        self.connection_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.connection_frame.pack(side="right", padx=20, pady=15)
        
        # Indicador de estado
        self.status_indicator = ctk.CTkLabel(
            self.connection_frame,
            text="●",
            font=ctk.CTkFont(size=20),
            text_color="red"
        )
        self.status_indicator.pack(side="left", padx=(0, 5))
        
        self.status_label = ctk.CTkLabel(
            self.connection_frame,
            text="Disconnected",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.status_label.pack(side="left", padx=(0, 10))
        
        # Botón de reconexión
        self.reconnect_btn = ctk.CTkButton(
            self.connection_frame,
            text="🔄 Reconnect",
            width=100,
            height=32,
            command=self.on_reconnect,
            fg_color=("#3b8ed0", "#1f538d"),
            hover_color=("#2d6ca8", "#153f6b")
        )
        self.reconnect_btn.pack(side="left")
    
    def set_reconnect_callback(self, callback: Callable):
        """Establecer callback para reconexión"""
        self.connection_callback = callback
    
    def on_reconnect(self):
        """Manejar evento de reconexión"""
        if self.connection_callback:
            self.connection_callback()
    
    def update_connection_status(self, connected: bool):
        """Actualizar estado de conexión"""
        if connected:
            self.status_indicator.configure(text_color="green")
            self.status_label.configure(text="Connected")
        else:
            self.status_indicator.configure(text_color="red")
            self.status_label.configure(text="Disconnected")


class SidebarComponent:
    """Componente del sidebar con controles organizados"""
    
    def __init__(self, parent, width: int = 300):
        self.parent = parent
        self.width = width
        self.callbacks = {}
        self.setup_sidebar()
    
    def setup_sidebar(self):
        """Crear sidebar moderno con controles organizados"""
        # Sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self.parent, width=self.width, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 2), pady=0)
        self.sidebar_frame.grid_propagate(False)
        
        # Scroll frame para el sidebar
        self.sidebar_scroll = ctk.CTkScrollableFrame(
            self.sidebar_frame,
            label_text="🎛️ Control Panel",
            label_font=ctk.CTkFont(size=16, weight="bold")
        )
        self.sidebar_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear secciones
        self.create_query_section()
        self.create_management_section()
        self.create_settings_section()
    
    def create_query_section(self):
        """Crear sección de consultas"""
        # Header de sección
        query_header = ctk.CTkLabel(
            self.sidebar_scroll,
            text="📊 Data Queries",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        query_header.pack(fill="x", pady=(0, 10))
        
        # Botones de consulta
        buttons_config = [
            ("📋 View All Species", "view_all_species", "#2b7a0b", "#52c41a"),
            ("🔍 Search by ID", "search_by_id", "#d46b08", "#fa8c16"),
            ("🔎 Advanced Search", "advanced_search", "#722ed1", "#b37feb"),
            ("🌍 View Zones", "view_zones", "#722ed1", "#b37feb"),
            ("🛡️ Conservation States", "view_conservation_states", "#c41d7f", "#f759ab"),
            ("📈 Statistics", "view_statistics", "#1677ff", "#69b1ff")
        ]
        
        for text, callback_key, fg_color, hover_color in buttons_config:
            btn = ctk.CTkButton(
                self.sidebar_scroll,
                text=text,
                command=lambda key=callback_key: self.execute_callback(key),
                height=40,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=fg_color,
                hover_color=hover_color,
                corner_radius=8
            )
            btn.pack(fill="x", pady=3)
        
        # Separador
        separator1 = ctk.CTkFrame(self.sidebar_scroll, height=2, fg_color=("#d0d0d0", "#404040"))
        separator1.pack(fill="x", pady=15)
    
    def create_management_section(self):
        """Crear sección de gestión"""
        # Header de sección
        mgmt_header = ctk.CTkLabel(
            self.sidebar_scroll,
            text="⚙️ Species Management",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        mgmt_header.pack(fill="x", pady=(0, 10))
        
        # Botones de gestión
        mgmt_buttons = [
            ("➕ Create New Species", "create_species", "#389e0d", "#73d13d"),
            ("📝 Edit Species", "edit_species", "#d4b106", "#fadb14"),
            ("🗑️ Delete Species", "delete_species", "#cf1322", "#ff4d4f")
        ]
        
        for text, callback_key, fg_color, hover_color in mgmt_buttons:
            btn = ctk.CTkButton(
                self.sidebar_scroll,
                text=text,
                command=lambda key=callback_key: self.execute_callback(key),
                height=40,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=fg_color,
                hover_color=hover_color,
                corner_radius=8
            )
            btn.pack(fill="x", pady=3)
        
        # Separador
        separator2 = ctk.CTkFrame(self.sidebar_scroll, height=2, fg_color=("#d0d0d0", "#404040"))
        separator2.pack(fill="x", pady=15)
    
    def create_settings_section(self):
        """Crear sección de configuración"""
        # Header de sección
        settings_header = ctk.CTkLabel(
            self.sidebar_scroll,
            text="🎨 Appearance & Tools",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        settings_header.pack(fill="x", pady=(0, 10))
        
        # Switch para tema
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar_scroll,
            text="🌙 Dark Mode",
            command=lambda: self.execute_callback("toggle_theme"),
            font=ctk.CTkFont(size=12)
        )
        self.theme_switch.pack(fill="x", pady=5)
        self.theme_switch.select()  # Dark mode por defecto
        
        # Botones de utilidad
        utility_buttons = [
            ("🧹 Clear Results", "clear_results", "#595959", "#8c8c8c"),
            ("📄 Export Data", "export_data", "#1890ff", "#40a9ff"),
            ("🔄 Refresh Data", "refresh_all_data", "#096dd9", "#1890ff")
        ]
        
        for text, callback_key, fg_color, hover_color in utility_buttons:
            btn = ctk.CTkButton(
                self.sidebar_scroll,
                text=text,
                command=lambda key=callback_key: self.execute_callback(key),
                height=32,
                font=ctk.CTkFont(size=11),
                fg_color=fg_color,
                hover_color=hover_color,
                corner_radius=6
            )
            btn.pack(fill="x", pady=2)
    
    def set_callback(self, action: str, callback: Callable):
        """Establecer callback para una acción"""
        self.callbacks[action] = callback
    
    def execute_callback(self, action: str):
        """Ejecutar callback para una acción"""
        if action in self.callbacks:
            self.callbacks[action]()
    
    def get_theme_state(self) -> bool:
        """Obtener estado del tema"""
        return self.theme_switch.get()


class TabbedContentArea:
    """Área de contenido con pestañas"""
    
    def __init__(self, parent):
        self.parent = parent
        self.log_callbacks: List[Callable[[str], None]] = []
        self.setup_content_area()
    
    def setup_content_area(self):
        """Crear área de contenido principal"""
        # Content frame
        self.content_frame = ctk.CTkFrame(self.parent, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(2, 0), pady=0)
        
        # Crear tabview
        self.tabview = ctk.CTkTabview(
            self.content_frame,
            width=800,
            height=600
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Crear pestañas
        self.setup_results_tab()
        self.setup_species_tab()
        self.setup_analytics_tab()
        self.setup_logs_tab()
    
    def setup_results_tab(self):
        """Configurar pestaña de resultados"""
        self.tabview.add("📊 Results")
        results_frame = self.tabview.tab("📊 Results")
        
        # Header con filtros
        filter_frame = ctk.CTkFrame(results_frame, height=60)
        filter_frame.pack(fill="x", padx=10, pady=(10, 5))
        filter_frame.pack_propagate(False)
        
        filter_label = ctk.CTkLabel(
            filter_frame,
            text="🔍 Search & Filter",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        filter_label.pack(side="left", padx=15, pady=15)
        
        # Campo de búsqueda
        self.search_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Search species by name...",
            width=250,
            height=32
        )
        self.search_entry.pack(side="right", padx=15, pady=15)
        
        # Área de resultados
        self.results_textbox = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.results_textbox.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Mensaje inicial
        self.log_message("🌟 Welcome to Forest Species Management System!")
        self.log_message("Connect to the SOAP service to start managing forest species data.")
        self.log_message("=" * 60)
    
    def setup_species_tab(self):
        """Configurar pestaña de lista de especies"""
        self.tabview.add("🌳 Species List")
        species_frame = self.tabview.tab("🌳 Species List")
        
        # Header
        header_frame = ctk.CTkFrame(species_frame, height=50)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        species_title = ctk.CTkLabel(
            header_frame,
            text="🌲 Forest Species Database",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        species_title.pack(side="left", padx=15, pady=10)
        
        # Scroll frame para la lista
        self.species_scroll = ctk.CTkScrollableFrame(species_frame)
        self.species_scroll.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Placeholder message
        placeholder = ctk.CTkLabel(
            self.species_scroll,
            text="🔄 Load species data to see the list here",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        placeholder.pack(pady=50)
    
    def setup_analytics_tab(self):
        """Configurar pestaña de análisis"""
        self.tabview.add("📈 Analytics")
        analytics_frame = self.tabview.tab("📈 Analytics")
        
        # Stats container
        self.stats_container = ctk.CTkFrame(analytics_frame)
        self.stats_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        stats_title = ctk.CTkLabel(
            self.stats_container,
            text="📊 Conservation Statistics",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        stats_title.pack(pady=20)
        
        # Placeholder
        stats_placeholder = ctk.CTkLabel(
            self.stats_container,
            text="📈 Statistical data will appear here when loaded",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        stats_placeholder.pack(pady=50)
    
    def setup_logs_tab(self):
        """Configurar pestaña de logs"""
        self.tabview.add("📝 Activity Log")
        logs_frame = self.tabview.tab("📝 Activity Log")
        
        # Header
        logs_header = ctk.CTkFrame(logs_frame, height=50)
        logs_header.pack(fill="x", padx=10, pady=(10, 5))
        logs_header.pack_propagate(False)
        
        logs_title = ctk.CTkLabel(
            logs_header,
            text="📋 System Activity Log",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        logs_title.pack(side="left", padx=15, pady=10)
        
        # Clear logs button
        clear_logs_btn = ctk.CTkButton(
            logs_header,
            text="🧹 Clear",
            width=80,
            height=30,
            command=self.clear_logs
        )
        clear_logs_btn.pack(side="right", padx=15, pady=10)
        
        # Logs textbox
        self.logs_textbox = ctk.CTkTextbox(
            logs_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        self.logs_textbox.pack(fill="both", expand=True, padx=10, pady=(5, 10))
    
    def log_message(self, message: str):
        """Agregar mensaje a resultados y logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        # Agregar a results
        if hasattr(self, 'results_textbox') and self.results_textbox:
            self.results_textbox.insert("end", formatted_message)
            self.results_textbox.see("end")
        
        # Agregar a logs
        if hasattr(self, 'logs_textbox') and self.logs_textbox:
            self.logs_textbox.insert("end", formatted_message)
            self.logs_textbox.see("end")
        
        # Notificar callbacks
        for callback in self.log_callbacks:
            callback(message)
    
    def clear_results(self):
        """Limpiar área de resultados"""
        if hasattr(self, 'results_textbox') and self.results_textbox:
            self.results_textbox.delete("1.0", "end")
    
    def clear_logs(self):
        """Limpiar logs"""
        if hasattr(self, 'logs_textbox') and self.logs_textbox:
            self.logs_textbox.delete("1.0", "end")
    
    def add_log_callback(self, callback: Callable[[str], None]):
        """Añadir callback para mensajes de log"""
        self.log_callbacks.append(callback)
    
    def get_search_query(self) -> str:
        """Obtener texto de búsqueda"""
        if hasattr(self, 'search_entry') and self.search_entry:
            return self.search_entry.get()
        return ""


class FooterComponent:
    """Componente del footer informativo"""
    
    def __init__(self, parent, text: str = "🌳 Forest Species Management System v2.0 | Modern GUI Edition | SOAP Client Ready"):
        self.parent = parent
        self.text = text
        self.setup_footer()
    
    def setup_footer(self):
        """Crear footer informativo"""
        self.footer_frame = ctk.CTkFrame(self.parent, height=40, corner_radius=0)
        self.footer_frame.pack(fill="x", side="bottom")
        self.footer_frame.pack_propagate(False)
        
        # Información del sistema
        footer_text = ctk.CTkLabel(
            self.footer_frame,
            text=self.text,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        footer_text.pack(pady=10)
    
    def update_text(self, new_text: str):
        """Actualizar texto del footer"""
        self.text = new_text
        # Actualizar el label si existe
        for widget in self.footer_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text=new_text)
                break
