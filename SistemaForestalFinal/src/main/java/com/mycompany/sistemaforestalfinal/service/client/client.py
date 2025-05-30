"""
🌳 Modern Forest CLient
"""

import customtkinter as ctk
from tkinter import messagebox, simpledialog
import requests
from zeep import Client
from zeep.transports import Transport
import threading
from datetime import datetime
import json
from typing import List, Optional, Dict, Any

# Configuración del tema moderno
ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("blue")  # Tema azul

class ModernTreeSpeciesGUI:
    
    def __init__(self):
        # Configurar ventana principal
        self.root = ctk.CTk()
        self.root.title("🌳 Forest Species Management System")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        
        # Variables de configuración
        self.service_url = "http://localhost:8282/TreeSpeciesCrudService?wsdl"
        self.client = None
        self.connected = False
          # Datos de referencia
        self.zones = []
        self.conservation_states = []
        self.current_species_list = []
        
        # Cola de mensajes para antes de inicializar textboxes
        self.pending_messages = []
        
        # Crear la interfaz
        self.setup_interface()
        self.connect_to_service()
        
    def setup_interface(self):
        """Configurar la interfaz principal moderna"""
        
        # Header con título y estado de conexión
        self.create_header()
        
        # Contenedor principal con sidebar y content area
        self.create_main_container()
        
        # Sidebar con controles
        self.create_sidebar()
        
        # Área de contenido principal
        self.create_content_area()
        
        # Footer con información del sistema
        self.create_footer()
        
    def create_header(self):
        """Crear header moderno con título y estado"""
        # Header frame
        self.header_frame = ctk.CTkFrame(self.root, height=80, corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Título principal
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🌳 Forest Species Management System",
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
            command=self.connect_to_service,
            fg_color=("#3b8ed0", "#1f538d"),
            hover_color=("#2d6ca8", "#153f6b")
        )
        self.reconnect_btn.pack(side="left")
        
    def create_main_container(self):
        """Crear contenedor principal con layout moderno"""
        # Main container
        self.main_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Configurar grid para layout responsivo
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
    def create_sidebar(self):
        """Crear sidebar moderno con controles organizados"""
        # Sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self.main_container, width=300, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 2), pady=0)
        self.sidebar_frame.grid_propagate(False)
        
        # Scroll frame para el sidebar
        self.sidebar_scroll = ctk.CTkScrollableFrame(
            self.sidebar_frame,
            label_text="🎛️ Control Panel",
            label_font=ctk.CTkFont(size=16, weight="bold")
        )
        self.sidebar_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sección de consultas
        self.create_query_section()
        
        # Sección de gestión
        self.create_management_section()
        
        # Sección de configuración
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
        
        # Botones de consulta con iconos modernos
        buttons_config = [
            ("📋 View All Species", self.view_all_species, "#2b7a0b", "#52c41a"),
            ("🔍 Search by ID", self.search_by_id, "#d46b08", "#fa8c16"),
            ("🌍 View Zones", self.view_zones, "#722ed1", "#b37feb"),
            ("🛡️ Conservation States", self.view_conservation_states, "#c41d7f", "#f759ab"),
            ("📈 Statistics", self.view_statistics, "#1677ff", "#69b1ff")
        ]
        
        for text, command, fg_color, hover_color in buttons_config:
            btn = ctk.CTkButton(
                self.sidebar_scroll,
                text=text,
                command=command,
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
            ("➕ Create New Species", self.create_species, "#389e0d", "#73d13d"),
            ("📝 Update Species", self.update_species, "#d4b106", "#fadb14"),
            ("🗑️ Delete Species", self.delete_species, "#cf1322", "#ff4d4f")
        ]
        
        for text, command, fg_color, hover_color in mgmt_buttons:
            btn = ctk.CTkButton(
                self.sidebar_scroll,
                text=text,
                command=command,
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
            command=self.toggle_theme,
            font=ctk.CTkFont(size=12)
        )
        self.theme_switch.pack(fill="x", pady=5)
        self.theme_switch.select()  # Dark mode por defecto
        
        # Botones de utilidad
        utility_buttons = [
            ("🧹 Clear Results", self.clear_results, "#595959", "#8c8c8c"),
            ("📄 Export Data", self.export_data, "#1890ff", "#40a9ff"),
            ("🔄 Refresh Data", self.refresh_all_data, "#096dd9", "#1890ff")
        ]
        
        for text, command, fg_color, hover_color in utility_buttons:
            btn = ctk.CTkButton(
                self.sidebar_scroll,
                text=text,
                command=command,
                height=32,
                font=ctk.CTkFont(size=11),
                fg_color=fg_color,
                hover_color=hover_color,
                corner_radius=6
            )
            btn.pack(fill="x", pady=2)
        
    def create_content_area(self):
        """Crear área de contenido principal"""
        # Content frame
        self.content_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(2, 0), pady=0)
        
        # Crear notebook para pestañas
        self.create_tabbed_interface()
        
    def create_tabbed_interface(self):
        """Crear interfaz con pestañas modernas"""
        # Tabview principal
        self.tabview = ctk.CTkTabview(
            self.content_frame,
            width=800,
            height=600
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Pestaña de resultados
        self.tabview.add("📊 Results")
        self.setup_results_tab()
        
        # Pestaña de especies
        self.tabview.add("🌳 Species List")
        self.setup_species_tab()
        
        # Pestaña de estadísticas
        self.tabview.add("📈 Analytics")
        self.setup_analytics_tab()
        
        # Pestaña de logs
        self.tabview.add("📝 Activity Log")
        self.setup_logs_tab()
        
    def setup_results_tab(self):
        """Configurar pestaña de resultados"""
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
        
        # Área de resultados con texto scrollable
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
        
        # Mostrar mensajes pendientes ahora que los textboxes están listos
        self.flush_pending_messages()
        
    def create_footer(self):
        """Crear footer informativo"""
        self.footer_frame = ctk.CTkFrame(self.root, height=40, corner_radius=0)
        self.footer_frame.pack(fill="x", side="bottom")
        self.footer_frame.pack_propagate(False)
        
        # Información del sistema
        footer_text = ctk.CTkLabel(
            self.footer_frame,
            text="🌳 Forest Species Management System v2.0 | Modern GUI Edition | SOAP Client Ready",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        footer_text.pack(pady=10)
      # Métodos de funcionalidad principales
    def log_message(self, message: str):
        """Agregar mensaje al área de resultados"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        # Si los textboxes no están listos, guardar en cola
        if not hasattr(self, 'results_textbox') or not self.results_textbox or not hasattr(self, 'logs_textbox') or not self.logs_textbox:
            self.pending_messages.append(formatted_message)
            return
        
        # Agregar a results
        self.results_textbox.insert("end", formatted_message)
        self.results_textbox.see("end")
        
        # También agregar a logs
        self.logs_textbox.insert("end", formatted_message)
        self.logs_textbox.see("end")
    
    def flush_pending_messages(self):
        """Mostrar mensajes pendientes una vez que los textboxes están listos"""
        if hasattr(self, 'pending_messages') and self.pending_messages:
            for message in self.pending_messages:
                if hasattr(self, 'results_textbox') and self.results_textbox:
                    self.results_textbox.insert("end", message)
                    self.results_textbox.see("end")
                
                if hasattr(self, 'logs_textbox') and self.logs_textbox:
                    self.logs_textbox.insert("end", message)
                    self.logs_textbox.see("end")
            
            # Limpiar la cola
            self.pending_messages.clear()
        
    def update_connection_status(self, connected: bool):
        """Actualizar estado de conexión en la UI"""
        if connected:
            self.status_indicator.configure(text_color="green")
            self.status_label.configure(text="Connected")
            self.log_message("✅ Successfully connected to SOAP service")
        else:
            self.status_indicator.configure(text_color="red")
            self.status_label.configure(text="Disconnected")
            self.log_message("❌ Disconnected from SOAP service")
            
    def connect_to_service(self):
        """Conectar al servicio SOAP en un hilo separado"""
        self.log_message("🔄 Attempting to connect to SOAP service...")
        threading.Thread(target=self._connect_thread, daemon=True).start()
        
    def _connect_thread(self):
        """Hilo para conectar al servicio"""
        try:
            # Configurar transporte con timeout
            transport = Transport(timeout=10)
            
            # Crear cliente SOAP
            self.client = Client(self.service_url, transport=transport)
            self.connected = True
            
            # Actualizar UI en el hilo principal
            self.root.after(0, self.update_connection_status, True)
            
            # Cargar datos de referencia
            self.root.after(0, self.load_reference_data)
            
        except Exception as e:
            self.connected = False
            self.root.after(0, self.update_connection_status, False)
            self.root.after(0, self.log_message, f"❌ Connection error: {e}")
            
    def load_reference_data(self):
        """Cargar datos de referencia"""
        threading.Thread(target=self._load_reference_data_thread, daemon=True).start()
        
    def _load_reference_data_thread(self):
        """Hilo para cargar datos de referencia"""
        try:
            # Cargar zonas
            zones_result = self.client.service.getAllZones()
            if zones_result:
                self.zones = list(zones_result)
                self.root.after(0, self.log_message, f"📍 Loaded {len(self.zones)} zones")
            
            # Cargar estados de conservación
            states_result = self.client.service.getAllConservationStates()
            if states_result:
                self.conservation_states = list(states_result)
                self.root.after(0, self.log_message, f"🛡️ Loaded {len(self.conservation_states)} conservation states")
                
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Error loading reference data: {e}")
            
    def check_connection(self) -> bool:
        """Verificar si hay conexión"""
        if not self.connected:
            messagebox.showerror("Connection Error", "No connection to service. Please reconnect.")
            return False
        return True
        
    # Métodos de interfaz
    def toggle_theme(self):
        """Cambiar entre tema claro y oscuro"""
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
            self.log_message("🌙 Switched to dark mode")
        else:
            ctk.set_appearance_mode("light")
            self.log_message("☀️ Switched to light mode")
            
    def clear_results(self):
        """Limpiar área de resultados"""
        self.results_textbox.delete("1.0", "end")
        self.log_message("🧹 Results cleared")
        
    def clear_logs(self):
        """Limpiar logs"""
        self.logs_textbox.delete("1.0", "end")
        
    def export_data(self):
        """Exportar datos (placeholder)"""
        self.log_message("📄 Export functionality - Coming soon!")
        
    def refresh_all_data(self):
        """Refrescar todos los datos"""
        if self.check_connection():
            self.load_reference_data()
            self.log_message("🔄 Refreshing all data...")
            
    # Métodos SOAP (simplificados para esta versión)
    def view_all_species(self):
        """Ver todas las especies"""
        if not self.check_connection():
            return
        self.log_message("🔍 Loading all species...")
        threading.Thread(target=self._view_all_species_thread, daemon=True).start()
        
    def _view_all_species_thread(self):
        """Hilo para obtener todas las especies"""
        try:
            result = self.client.service.getAllTreeSpecies()
            if result:
                species_list = list(result)
                self.current_species_list = species_list
                self.root.after(0, self._display_species_list, species_list)
            else:
                self.root.after(0, self.log_message, "ℹ️ No species found")
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Error loading species: {e}")
            
    def _display_species_list(self, species_list):
        """Mostrar lista de especies en formato moderno"""
        self.log_message(f"✅ Found {len(species_list)} species:")
        self.log_message("=" * 80)
        
        for i, species in enumerate(species_list, 1):
            self.log_message(f"🌿 {i}. {species.nombreComun}")
            self.log_message(f"   📋 ID: {species.id}")
            self.log_message(f"   🧬 Scientific: {species.nombreCientifico or 'Not specified'}")
            self.log_message(f"   🛡️ Status: {species.estadoConservacionNombre}")
            self.log_message(f"   🌍 Zone: {species.zonaNombre}")
            self.log_message(f"   ✅ Active: {'Yes' if species.activo else 'No'}")
            self.log_message("")
            
    def search_by_id(self):
        """Buscar especie por ID"""
        if not self.check_connection():
            return
        
        # Diálogo moderno para entrada
        dialog = ctk.CTkInputDialog(
            text="Enter Species ID:",
            title="🔍 Search Species"
        )
        species_id_str = dialog.get_input()
        
        if species_id_str:
            try:
                species_id = int(species_id_str)
                threading.Thread(target=self._search_by_id_thread, args=(species_id,), daemon=True).start()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric ID")
                
    def _search_by_id_thread(self, species_id):
        """Hilo para buscar por ID"""
        try:
            self.root.after(0, self.log_message, f"🔍 Searching for species ID: {species_id}")
            result = self.client.service.getTreeSpeciesById(species_id)
            
            if result:
                self.root.after(0, self._display_single_species, result)
            else:
                self.root.after(0, self.log_message, f"ℹ️ Species with ID {species_id} not found")
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Search error: {e}")
            
    def _display_single_species(self, species):
        """Mostrar información de una especie"""
        self.log_message("✅ Species found:")
        self.log_message("=" * 60)
        self.log_message(f"🆔 ID: {species.id}")
        self.log_message(f"🌿 Common Name: {species.nombreComun}")
        self.log_message(f"🧬 Scientific Name: {species.nombreCientifico or 'Not specified'}")
        self.log_message(f"🛡️ Conservation Status: {species.estadoConservacionNombre}")
        self.log_message(f"🌍 Zone: {species.zonaNombre}")
        self.log_message(f"✅ Active: {'Yes' if species.activo else 'No'}")
        self.log_message("=" * 60)
        
    def view_zones(self):
        """Ver todas las zonas"""
        if not self.zones:
            self.log_message("⚠️ Load reference data first")
            return
            
        self.log_message("🌍 Available zones:")
        self.log_message("=" * 40)
        for zone in self.zones:
            self.log_message(f"📍 ID: {zone.id} - {zone.nombre}")
        self.log_message("=" * 40)
        
    def view_conservation_states(self):
        """Ver estados de conservación"""
        if not self.conservation_states:
            self.log_message("⚠️ Load reference data first")
            return
            
        self.log_message("🛡️ Conservation states:")
        self.log_message("=" * 50)
        for state in self.conservation_states:
            self.log_message(f"🛡️ ID: {state.id} - {state.nombre}")
        self.log_message("=" * 50)
        
    def view_statistics(self):
        """Ver estadísticas (placeholder)"""
        self.log_message("📈 Loading statistics...")
        self.log_message("📊 Statistics feature - Coming soon!")
        
    def create_species(self):
        """Crear nueva especie con diálogo moderno"""
        if not self.check_connection():
            return
            
        if not self.zones or not self.conservation_states:
            self.log_message("⚠️ Loading reference data first...")
            self.load_reference_data()
            return
        
        # Crear diálogo moderno
        self.create_species_dialog()
        
    def create_species_dialog(self):
        """Crear diálogo moderno para nueva especie"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("➕ Create New Species")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="🌱 Create New Forest Species",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Variables para formulario
        self.new_common_name = ctk.StringVar()
        self.new_scientific_name = ctk.StringVar()
        self.new_zone = ctk.StringVar()
        self.new_conservation_state = ctk.StringVar()
        self.new_active = ctk.BooleanVar(value=True)
        
        # Campos del formulario
        # Nombre común
        name_frame = ctk.CTkFrame(main_frame)
        name_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(name_frame, text="🌿 Common Name *", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        name_entry = ctk.CTkEntry(name_frame, textvariable=self.new_common_name, height=35)
        name_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        # Nombre científico
        sci_frame = ctk.CTkFrame(main_frame)
        sci_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(sci_frame, text="🧬 Scientific Name", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        sci_entry = ctk.CTkEntry(sci_frame, textvariable=self.new_scientific_name, height=35)
        sci_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        # Zona
        zone_frame = ctk.CTkFrame(main_frame)
        zone_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(zone_frame, text="🌍 Zone *", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        zone_combo = ctk.CTkComboBox(
            zone_frame, 
            variable=self.new_zone,
            values=[f"{zone.id} - {zone.nombre}" for zone in self.zones],
            height=35,
            state="readonly"
        )
        zone_combo.pack(fill="x", padx=15, pady=(0, 10))
        
        # Estado de conservación
        state_frame = ctk.CTkFrame(main_frame)
        state_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(state_frame, text="🛡️ Conservation State *", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        state_combo = ctk.CTkComboBox(
            state_frame,
            variable=self.new_conservation_state,
            values=[f"{state.id} - {state.nombre}" for state in self.conservation_states],
            height=35,
            state="readonly"
        )
        state_combo.pack(fill="x", padx=15, pady=(0, 10))
        
        # Estado activo
        active_frame = ctk.CTkFrame(main_frame)
        active_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(active_frame, text="✅ Status", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        active_switch = ctk.CTkSwitch(active_frame, text="Active Species", variable=self.new_active)
        active_switch.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Botones
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Cancel",
            command=dialog.destroy,
            fg_color="gray",
            hover_color="darkgray"
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        create_btn = ctk.CTkButton(
            button_frame,
            text="➕ Create Species",
            command=lambda: self.submit_new_species(dialog),
            fg_color="#2b7a0b",
            hover_color="#1e5a08"
        )
        create_btn.pack(side="right")
        
    def submit_new_species(self, dialog):
        """Enviar datos para crear nueva especie"""
        # Validaciones
        if not self.new_common_name.get().strip():
            messagebox.showerror("Error", "Common name is required")
            return
            
        if not self.new_zone.get():
            messagebox.showerror("Error", "Please select a zone")
            return
            
        if not self.new_conservation_state.get():
            messagebox.showerror("Error", "Please select a conservation state")
            return
        
        # Extraer IDs
        zone_id = int(self.new_zone.get().split(" - ")[0])
        state_id = int(self.new_conservation_state.get().split(" - ")[0])
        
        # Crear en hilo separado
        threading.Thread(
            target=self._create_species_thread,
            args=(
                self.new_common_name.get().strip(),
                self.new_scientific_name.get().strip() or None,
                state_id,
                zone_id,
                self.new_active.get(),
                dialog
            ),
            daemon=True
        ).start()
        
    def _create_species_thread(self, common_name, scientific_name, state_id, zone_id, active, dialog):
        """Hilo para crear nueva especie"""
        try:
            self.root.after(0, self.log_message, f"➕ Creating new species: {common_name}")
            
            result = self.client.service.createTreeSpecies(
                nombreComun=common_name,
                nombreCientifico=scientific_name,
                estadoConservacionId=state_id,
                zonaId=zone_id,
                activo=active
            )
            
            if result:
                self.root.after(0, self.log_message, f"✅ Species '{common_name}' created successfully with ID: {result}")
                self.root.after(0, messagebox.showinfo, "Success", f"Species created successfully with ID: {result}")
                self.root.after(0, dialog.destroy)
            else:
                self.root.after(0, self.log_message, f"❌ Failed to create species '{common_name}'")
                self.root.after(0, messagebox.showerror, "Error", "Failed to create species")
                
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Error creating species: {e}")
            self.root.after(0, messagebox.showerror, "Error", f"Error creating species: {e}")
        
    def update_species(self):
        """Actualizar especie (placeholder)"""
        self.log_message("📝 Update species feature - Coming soon!")
        
    def delete_species(self):
        """Eliminar especie (placeholder)"""
        self.log_message("🗑️ Delete species feature - Coming soon!")
        
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        app = ModernTreeSpeciesGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()
