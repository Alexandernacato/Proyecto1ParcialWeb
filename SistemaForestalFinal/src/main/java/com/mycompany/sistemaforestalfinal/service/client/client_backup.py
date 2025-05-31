#!/usr/bin/env python3
"""
🌳 Forest Species Management Client - Refactorizado Modular
Arquitectura modular siguiendo lineamientos PLANNING.md (<500 líneas por archivo)
"""

import customtkinter as ctk
import sys
from pathlib import Path

# Configurar imports relativos
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Imports de módulos core existentes
from core.soap_client import SOAPClientManager
from core.data_manager import DataManager

# Imports de UI modular refactorizada
from ui.main_window import MainWindow

# Configuración del tema moderno
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ForestManagementClient:
    """Cliente forestal moderno refactorizado con interfaz React-style (< 500 líneas)"""
    
    def __init__(self):
        """Inicializar cliente con arquitectura modular y diseño moderno"""
        # Configurar ventana principal con estilo moderno
        self.root = ctk.CTk()
        self.root.title("🌳 Modern Forest Species Management")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configurar tema moderno mejorado
        self._setup_modern_theme()
        
        # Inicializar componentes core
        self.soap_client = SOAPClientManager()
        self.data_manager = DataManager(self.soap_client)
          # Estado de la aplicación
        self.current_species_list = []
        self.current_zones_list = []
        self.is_dark_mode = True
        self.last_search_term = ""
          # Configurar interfaz moderna
        self._setup_modern_interface()
        self._setup_callbacks()
        
        # Mensaje de bienvenida moderno
        self.log_message("🎉 Welcome to Modern Forest Management System", "success")
        
        # Programar conexión inicial para después de que la GUI esté lista
        self.root.after(1000, self._initial_connection_delayed)
    
    def _setup_modern_theme(self):
        """Configurar tema moderno estilo React/Material Design"""
        # Colores del tema moderno
        self.modern_colors = {
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
        
        # Aplicar configuración de tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
    
    def _setup_modern_interface(self):
        """Configurar interfaz moderna estilo React"""
        # Header moderno con gradiente
        self._create_modern_header()
        
        # Contenedor principal con diseño moderno
        main_container = ctk.CTkFrame(
            self.root, 
            fg_color="transparent",
            corner_radius=0
        )
        main_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Grid responsive
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        # Sidebar moderno
        self.sidebar = ctk.CTkFrame(
            self.root,
            width=220,
            fg_color=self.modern_colors['surface'],
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Área de contenido con diseño de tarjetas
        self._create_modern_content_area(main_container)
        
        # Footer moderno
        self._create_modern_footer()
    
    def _create_modern_header(self):
        """Crear header moderno estilo React"""
        header_frame = ctk.CTkFrame(
            self.root, 
            height=80, 
            fg_color=self.modern_colors['primary'],
            corner_radius=0
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Contenedor del header
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Logo y título
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(side="left", fill="y")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🌳 Modern Forest Management",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", pady=10)
        
        # Indicadores de estado
        status_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        status_frame.pack(side="right", fill="y")
        
        self.connection_indicator = ctk.CTkLabel(
            status_frame,
            text="🔴 Disconnected",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.connection_indicator.pack(side="right", padx=(0, 20), pady=10)
        
        self.species_counter = ctk.CTkLabel(
            status_frame,
            text="📊 Species: 0",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.species_counter.pack(side="right", padx=(0, 20), pady=10)
    
    def _create_modern_sidebar(self, parent):
        """Crear sidebar moderno con botones estilo Material Design"""
        self.sidebar_frame = ctk.CTkScrollableFrame(
            parent,
            width=280,
            fg_color=self.modern_colors['surface'],
            corner_radius=12
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Título de la sidebar
        sidebar_title = ctk.CTkLabel(
            self.sidebar_frame,
            text="🔧 Operations Panel",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.modern_colors['secondary']
        )
        sidebar_title.pack(pady=(10, 20))
        
        # Crear grupos de botones modernos
        try:
            self._create_connection_section()
            self._create_crud_section()
            self._create_data_section()
            self._create_utility_section()
        except Exception as e:
            print(f"Warning: Could not create sidebar sections: {e}")
            # Crear botones básicos como fallback
            self._create_basic_buttons()
    
    def _create_modern_content_area(self, parent):
        """Crear área de contenido con diseño de tarjetas"""
        self.content_frame = ctk.CTkFrame(
            parent,
            fg_color=self.modern_colors['background'],
            corner_radius=12
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        
        # Configurar notebook moderno
        self.tabview = ctk.CTkTabview(
            self.content_frame,
            height=400,
            fg_color=self.modern_colors['surface'],
            segmented_button_fg_color=self.modern_colors['primary'],
            segmented_button_selected_color=self.modern_colors['secondary']
        )
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)
          # Pestañas modernas
        self.tabview.add("🗂️ Species Data")
        self.tabview.add("🌍 Zones Management")
        self.tabview.add("📋 Activity Log")
        self.tabview.add("📊 Statistics")
        
        # Configurar contenido de pestañas
        self._setup_species_tab()
        self._setup_zones_tab()
        self._setup_log_tab()
        self._setup_stats_tab()
    
    def _create_modern_footer(self):
        """Crear footer moderno"""
        footer_frame = ctk.CTkFrame(
            self.root,
            height=40,
            fg_color=self.modern_colors['surface'],
            corner_radius=0
        )
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        footer_label = ctk.CTkLabel(
            footer_frame,
                    text="Modern Forest Species Management System v2.0 | Ready for modern operations",
            font=ctk.CTkFont(size=12),
            text_color=self.modern_colors['text_secondary']
        )
        footer_label.pack(pady=10)
    
    def _setup_interface(self):
        """Configurar interfaz moderna (método compatibility)"""
        # Este método ahora está integrado en _setup_modern_interface
        self.log_message("🌟 Modern Forest Species Management System Ready!", "success")
        self.log_message("✨ Enhanced with React-style modern dialogs", "info")
    
    def _setup_callbacks(self):
        """Configurar callbacks entre componentes"""
        # Callback para cambios de conexión
        # TODO: self.soap_client.add_connection_callback(self._on_connection_change)
        pass
    
    def _setup_species_tab(self):
        """Configurar pestaña de especies"""
        species_frame = self.tabview.tab("🗂️ Species Data")
        
        # Header de la pestaña
        header_frame = ctk.CTkFrame(species_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🌳 Species Management",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.modern_colors['primary']
        )
        title_label.pack(side="left")
          # Botones CRUD
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        ctk.CTkButton(
            buttons_frame,
            text="➕ Add Species",
            command=self.create_species,
            fg_color=self.modern_colors['success'],
            hover_color="#45a049",
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="✏️ Edit Species",
            command=self.edit_species,
            fg_color=self.modern_colors['warning'],
            hover_color="#e68900",
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🗑️ Delete Species",
            command=self.delete_species,
            fg_color=self.modern_colors['error'],
            hover_color="#c82333",
            width=120
        ).pack(side="left", padx=5)
          # Búsqueda
        search_frame = ctk.CTkFrame(species_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search species...",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search_changed)
          # Lista de especies (scrollable)
        self.species_scroll = ctk.CTkScrollableFrame(
            species_frame,
            fg_color=self.modern_colors['background'],
            corner_radius=10
        )
        self.species_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Cargar especies iniciales
        self.view_all_species()
    
    def _setup_zones_tab(self):
        """Configurar pestaña de zonas"""
        zones_frame = self.tabview.tab("🌍 Zones Management")
        
        # Header de la pestaña
        header_frame = ctk.CTkFrame(zones_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🌍 Zones Management",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.modern_colors['primary']
        )
        title_label.pack(side="left")
        
        # Botones CRUD para zonas
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        ctk.CTkButton(
            buttons_frame,
            text="➕ Add Zone",
            command=self.crear_zona,
            fg_color=self.modern_colors['success'],
            hover_color="#45a049",
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🗑️ Delete Zone",
            command=self.eliminar_zona,
            fg_color=self.modern_colors['error'],
            hover_color="#c82333",
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="👁️ View Zones",
            command=self.view_zones,
            fg_color=self.modern_colors['info'],
            hover_color="#117a8b",
            width=120
        ).pack(side="left", padx=5)
        
        # Área de contenido para zonas
        self.zones_content = ctk.CTkScrollableFrame(
            zones_frame,
            fg_color=self.modern_colors['background'],
            corner_radius=10
        )
        self.zones_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Mensaje inicial
        initial_label = ctk.CTkLabel(
            self.zones_content,
            text="🌍 Use the buttons above to manage zones",
            font=ctk.CTkFont(size=16),
            text_color=self.modern_colors['text_secondary']
        )
        initial_label.pack(pady=50)
    
    def _setup_log_tab(self):
        """Configurar pestaña de registro de actividades"""
        log_frame = self.tabview.tab("📋 Activity Log")
        
        # Header
        header_frame = ctk.CTkFrame(log_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📋 Activity Log",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.modern_colors['primary']
        )
        title_label.pack(side="left")
        
        # Botón para limpiar log
        clear_button = ctk.CTkButton(
            header_frame,
            text="🗑️ Clear Log",
            command=self._clear_log,
            fg_color=self.modern_colors['error'],
            hover_color="#c82333",
            width=100
        )
        clear_button.pack(side="right")
        
        # Crear área de texto para el log de actividades
        self.log_text = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.log_text.pack(fill="both", expand=True, padx=20, pady=10)
    
    def _setup_stats_tab(self):
        """Configurar pestaña de estadísticas"""
        stats_frame = self.tabview.tab("📊 Statistics")
        
        # Header
        header_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 System Statistics",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.modern_colors['primary']
        )
        title_label.pack(side="left")
        
        # Botón de actualizar estadísticas
        refresh_button = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            command=self._update_stats,
            fg_color=self.modern_colors['info'],
            hover_color="#117a8b",
            width=100
        )
        refresh_button.pack(side="right")
        
        # Grid de estadísticas
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Estadísticas básicas
        self.stats_cards = {}
        self._create_stats_cards(stats_grid)
    
    def _create_stats_cards(self, parent):
        """Crear tarjetas de estadísticas"""
        stats_data = [
            ("🌳", "Total Species", "0", self.modern_colors['success']),
            ("🌍", "Total Zones", "0", self.modern_colors['info']),
            ("📊", "Conservation States", "0", self.modern_colors['warning']),
            ("🔄", "Operations Today", "0", self.modern_colors['primary'])
        ]
        
        for i, (icon, title, value, color) in enumerate(stats_data):
            card = ctk.CTkFrame(parent, fg_color=color, corner_radius=15)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
            parent.grid_columnconfigure(i%2, weight=1)
            
            icon_label = ctk.CTkLabel(
                card,
                text=icon,
                font=ctk.CTkFont(size=32),
                text_color="white"
            )
            icon_label.pack(pady=(20, 5))
            
            title_label = ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="white"
            )
            title_label.pack()
            
            value_label = ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="white"
            )
            value_label.pack(pady=(5, 20))
            
            self.stats_cards[title] = value_label
    
    def _update_stats(self):
        """Actualizar estadísticas del sistema"""
        try:
            # Obtener estadísticas reales
            species_count = len(self.data_manager.get_all_species())
            zones_count = len(self.data_manager.get_all_zones())
            conservation_count = len(self.data_manager.get_all_conservation_states())
            
            # Actualizar las tarjetas
            if "Total Species" in self.stats_cards:
                self.stats_cards["Total Species"].configure(text=str(species_count))
            if "Total Zones" in self.stats_cards:
                self.stats_cards["Total Zones"].configure(text=str(zones_count))
            if "Conservation States" in self.stats_cards:
                self.stats_cards["Conservation States"].configure(text=str(conservation_count))
            
            self.log_message("📊 Statistics updated successfully", "success")
        except Exception as e:
            self.log_message(f"❌ Error updating statistics: {e}", "error")
    
    def _clear_log(self):
        """Limpiar el registro de actividades"""
        if hasattr(self, 'log_text'):
            self.log_text.delete("1.0", "end")
            self.log_message("🗑️ Activity log cleared", "info")
    
    def _load_reference_data(self):
        """Cargar datos de referencia en hilo separado"""
        def _load_thread():
            try:
                zones = self.data_manager.get_all_zones()
                states = self.data_manager.get_all_conservation_states()
                self.root.after(0, self.log_message, f"📍 Loaded {len(zones)} zones and {len(states)} conservation states")
            except Exception as exc:
                self.root.after(0, self.log_message, f"❌ Error loading reference data: {exc}")
        
        threading.Thread(target=_load_thread, daemon=True).start()
    
    # === Métodos de operaciones CRUD ===
    
    def view_all_species(self):
        """Ver todas las especies"""
        if not self._check_connection():
            return
        
        self.log_message("🔍 Loading all species...")
        threading.Thread(target=self._load_all_species_thread, daemon=True).start()
    
    def _load_all_species_thread(self):
        """Hilo para cargar todas las especies"""
        try:
            species_list = self.data_manager.get_all_species()
            self.current_species_list = species_list
            self.root.after(0, self._display_species_list, species_list, "All Species")
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Error loading species: {e}")
    
    def search_by_id(self):
        """Buscar especie por ID"""
        if not self._check_connection():
            return
        
        dialog = ctk.CTkInputDialog(text="Enter Species ID:", title="🔍 Search by ID")
        species_id_str = dialog.get_input()
        
        if species_id_str:
            try:
                species_id = int(species_id_str)
                threading.Thread(target=self._search_by_id_thread, args=(species_id,), daemon=True).start()
            except ValueError:                messagebox.showerror("Error", "Please enter a valid numeric ID")
    
    def search_by_name(self):
        """Buscar especie por nombre"""
        if not self._check_connection():
            return
        
        dialog = ctk.CTkInputDialog(text="Enter Species Name:", title="🔍 Search by Name")
        species_name = dialog.get_input()
        if species_name:
            threading.Thread(target=self._search_by_name_thread, args=(species_name,), daemon=True).start()
    
    def _search_by_name_thread(self, species_name: str):
        """Hilo para buscar por nombre"""
        try:
            # Buscar en la lista actual o cargar todas si no hay lista
            if not self.current_species_list:
                self.current_species_list = self.data_manager.get_all_species()
            
            # Buscar especies que coincidan con el nombre (búsqueda parcial)
            matching_species = [
                s for s in self.current_species_list 
                if species_name.lower() in s.nombreComun.lower()
            ]
            
            if matching_species:
                self.root.after(0, self._display_species_list, matching_species, f"Species matching '{species_name}'")
            else:
                self.root.after(0, self.log_message, f"❌ No species found matching '{species_name}'")
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Search error: {e}")

    def _search_by_id_thread(self, species_id: int):
        """Hilo para buscar por ID"""
        try:
            species = self.data_manager.get_species_by_id(species_id)
            if species:
                self.root.after(0, self._display_species_list, [species], f"Species ID: {species_id}")
            else:
                self.root.after(0, self.log_message, f"❌ Species with ID {species_id} not found")
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Search error: {e}")

    def _find_species_by_name(self, species_name: str):
        """Buscar especies por nombre - retorna lista de coincidencias"""
        if not self.current_species_list:
            return []
        
        # Buscar coincidencias exactas primero
        exact_matches = [
            s for s in self.current_species_list 
            if s.nombreComun.lower() == species_name.lower()
        ]
        
        if exact_matches:
            return exact_matches
        
        # Si no hay coincidencias exactas, buscar coincidencias parciales
        partial_matches = [
            s for s in self.current_species_list 
            if species_name.lower() in s.nombreComun.lower()
        ]
        
        return partial_matches

    def _display_species_list(self, species_list, title="Species List"):
        """Mostrar lista de especies en la interfaz"""
        try:
            # Use the existing species_scroll frame
            if hasattr(self, 'species_scroll') and self.species_scroll:
                # Clear current species display
                for widget in self.species_scroll.winfo_children():
                    widget.destroy()
                display_frame = self.species_scroll
            else:
                self.log_message("⚠️ Species display frame not ready yet")
                return
            
            if not species_list:
                no_data_label = ctk.CTkLabel(
                    display_frame,
                    text="📋 No species data to display",
                    font=ctk.CTkFont(size=14)
                )
                no_data_label.pack(pady=20)
                self.log_message(f"ℹ️ {title}: No data found")
                return
            
            # Display species in a modern card layout
            for i, species in enumerate(species_list):
                # Create species card
                species_card = ctk.CTkFrame(display_frame)
                species_card.pack(fill="x", padx=5, pady=5)
                  # Species header with ID and name
                header_frame = ctk.CTkFrame(species_card)
                header_frame.pack(fill="x", padx=10, pady=(10, 5))
                
                id_label = ctk.CTkLabel(
                    header_frame,
                    text=f"ID: {species.id}",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#3B82F6"
                )
                id_label.pack(side="left", padx=(10, 5))
                
                name_label = ctk.CTkLabel(
                    header_frame,
                    text=f"🌳 {species.nombreComun}",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                name_label.pack(side="left", padx=5)
                
                # Species details
                details_frame = ctk.CTkFrame(species_card)
                details_frame.pack(fill="x", padx=10, pady=(0, 10))
                  # Left column
                left_col = ctk.CTkFrame(details_frame)
                left_col.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
                
                scientific_label = ctk.CTkLabel(
                    left_col,
                    text=f"📖 Scientific: {getattr(species, 'nombreCientifico', 'N/A')}",
                    font=ctk.CTkFont(size=12)
                )
                scientific_label.pack(anchor="w", padx=5, pady=2)
                
                # Note: Family is not available in current model, so we'll skip it for now
                # family_label = ctk.CTkLabel(
                #     left_col,
                #     text=f"🏷️ Family: {getattr(species, 'familia', 'N/A')}",
                #     font=ctk.CTkFont(size=12)
                # )
                # family_label.pack(anchor="w", padx=5, pady=2)
                  # Right column
                right_col = ctk.CTkFrame(details_frame)
                right_col.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
                
                zone_name = getattr(species, 'zonaNombre', 'Unknown')
                if not zone_name or zone_name.strip() == '':
                    zone_name = "Unknown"
                
                zone_label = ctk.CTkLabel(
                    right_col,
                    text=f"🗺️ Zone: {zone_name}",
                    font=ctk.CTkFont(size=12)
                )
                zone_label.pack(anchor="w", padx=5, pady=2)
                
                conservation_state = getattr(species, 'estadoConservacionNombre', 'Unknown')
                if not conservation_state or conservation_state.strip() == '':
                    conservation_state = "Unknown"
                
                conservation_label = ctk.CTkLabel(
                    right_col,
                    text=f"🛡️ Status: {conservation_state}",
                    font=ctk.CTkFont(size=12)
                )
                conservation_label.pack(anchor="w", padx=5, pady=2)
                
                # Action buttons for each species
                button_frame = ctk.CTkFrame(species_card)
                button_frame.pack(fill="x", padx=10, pady=(0, 10))
                
                edit_btn = ctk.CTkButton(
                    button_frame,
                    text="✏️ Edit",
                    width=80,
                    height=30,
                    command=lambda s=species: self.edit_species_action(s)
                )
                edit_btn.pack(side="left", padx=(10, 5), pady=5)
                
                delete_btn = ctk.CTkButton(
                    button_frame,
                    text="🗑️ Delete",
                    width=80,
                    height=30,
                    fg_color="#DC2626",
                    hover_color="#B91C1C",
                    command=lambda s=species: self.delete_species_action(s)
                )
                delete_btn.pack(side="left", padx=5, pady=5)
            
            # Update stats
            self._update_stats()
            
            self.log_message(f"✅ {title}: Displayed {len(species_list)} species")
            
        except Exception as e:
            self.log_message(f"❌ Error displaying species list: {e}")
            print(f"Display error details: {e}")

    def _show_species_selection_dialog(self, title: str, message: str):
        """Mostrar diálogo de selección de especies"""
        if not self.current_species_list:
            self.log_message("ℹ️ No species data available")
            return None
            
        try:
            from gui.modern_dialogs import ModernSpeciesSelector
            
            def on_species_selected(selected_species):
                self._selected_species = selected_species
                
            dialog = ModernSpeciesSelector(
                parent=self.root,
                title=title,
                species_list=self.current_species_list,
                callback=on_species_selected
            )
            
            # Esperar a que se cierre el diálogo
            self.root.wait_window(dialog)
            
            # Retornar la especie seleccionada
            return getattr(self, '_selected_species', None)
            
        except Exception as e:
            self.log_message(f"❌ Error showing species selection dialog: {e}")
            return None
    
    def create_species(self):
        """Crear nueva especie"""
        if not self._check_connection():
            return
        
        try:
            zones = self.data_manager.get_all_zones()
            conservation_states = self.data_manager.get_all_conservation_states()
            if not zones or not conservation_states:
                self.log_message("⚠️ Loading reference data first...")
                self._load_reference_data()
                return
            
            dialog = SpeciesCreateDialog(
                self.root,
                zones=zones,
                conservation_states=conservation_states,
                on_submit=self._on_species_created
            )
            dialog.show()
        except Exception as e:
            self.log_message(f"❌ Error opening create dialog: {e}")

    def edit_species(self):
        """Editar especie existente"""
        if not self._check_connection():
            return
        
        if not self.current_species_list:
            self.log_message("ℹ️ Load species data first to edit")
            return
        
        # Mostrar lista de especies para seleccionar
        selected_species = self._show_species_selection_dialog(
            "📝 Edit Species", 
            "Select a species to edit:"
        )
        
        if selected_species:
            zones = self.data_manager.get_all_zones()
            conservation_states = self.data_manager.get_all_conservation_states()
            edit_dialog = SpeciesEditDialog(
                self.root,
                species=selected_species,
                zones=zones,
                conservation_states=conservation_states,
                on_submit=self._on_species_updated            )
            edit_dialog.show()

    def delete_species(self):
        """Eliminar especie usando diálogo moderno"""
        if not self._check_connection():
            return
        
        if not self.current_species_list:
            self.log_message("ℹ️ Load species data first to delete")
            return
        
        # Mostrar lista de especies para seleccionar usando el diálogo moderno
        selected_species = self._show_species_selection_dialog(
            "🗑️ Delete Species", 
            "Select a species to delete:"
        )
        
        if selected_species:
            # Usar diálogo de confirmación moderno
            def on_confirmation(confirmed):
                if confirmed:
                    self._delete_species_confirmed(selected_species)
            
            # Crear diálogo de confirmación moderno
            ModernConfirmationDialog(
                self.root,
                title="Confirm Deletion",
                message=f"Are you sure you want to delete '{selected_species.nombreComun}'?\n\nThis action cannot be undone.",
                confirm_text="🗑️ Delete",
                cancel_text="❌ Cancel",
                callback=on_confirmation
            )
    
    def _delete_species_confirmed(self, species):
        """Ejecutar la eliminación confirmada de una especie"""
        def delete_thread():
            try:
                self.log_message(f"🗑️ Deleting species: {species.nombreComun}")
                self.data_manager.delete_species(
                    species_id=species.id,
                    callback=lambda success, msg: self.root.after(0, self._on_species_deleted, species.id, success, msg)
                )
            except Exception as e:
                error_msg = f"Error deleting species: {str(e)}"
                self.root.after(0, self._on_species_deleted, species.id, False, error_msg)
        
        threading.Thread(target=delete_thread, daemon=True).start()
    
    def edit_species_action(self, species):
        """Editar una especie específica desde la lista"""
        if not self._check_connection():
            return
        
        try:
            zones = self.data_manager.get_all_zones()
            conservation_states = self.data_manager.get_all_conservation_states()
            if not zones or not conservation_states:
                self.log_message("⚠️ Loading reference data first...")
                self._load_reference_data()
                return
            
            edit_dialog = SpeciesEditDialog(
                self.root,
                species=species,
                zones=zones,
                conservation_states=conservation_states,
                on_submit=self._on_species_updated
            )
            edit_dialog.show()
        except Exception as e:
            self.log_message(f"❌ Error opening edit dialog: {e}")
    
    def delete_species_action(self, species):
        """Eliminar una especie específica desde la lista"""
        if not self._check_connection():
            return
        
        def on_confirmation(confirmed):
            if confirmed:
                self._delete_species_confirmed(species)
        
        # Crear diálogo de confirmación moderno
        ModernConfirmationDialog(
            self.root,
            title="Confirm Deletion",
            message=f"Are you sure you want to delete '{species.nombreComun}'?\n\nThis action cannot be undone.",
            confirm_text="🗑️ Delete",
            cancel_text="❌ Cancel",
            callback=on_confirmation
        )
    
    # === Callbacks para operaciones CRUD de Especies ===
    
    def _on_species_created(self, species, success: bool = None, message: str = None):
        """Callback para especie creada"""
        if success is None:
            # Caso cuando se llama desde el diálogo (species es TreeSpecies)
            try:
                self.data_manager.create_species(
                    species=species,
                    callback=lambda s, m, id=None: self.root.after(0, self._on_species_created_callback, s, m, id)                )
            except Exception as e:
                self.log_message(f"❌ Error creating species: {e}", "error")
        else:
            # Caso cuando se llama desde callback (species es id o similar)
            self._on_species_created_callback(success, message)

    def _on_species_created_callback(self, success: bool, message: str, species_id=None):
        """Callback interno para especie creada"""
        if success:
            self.log_message(f"✅ {message}", "success")
            self.view_all_species()  # Recargar lista
        else:
            self.log_message(f"❌ {message}", "error")
    
    def _on_species_updated(self, species, success: bool = None, message: str = None):
        """Callback para especie actualizada"""
        if success is None:
            # Caso cuando se llama desde el diálogo (species es TreeSpecies)
            try:
                self.data_manager.update_species(
                    species=species,
                    callback=lambda s, m: self.root.after(0, self._on_species_updated_callback, s, m)                )
            except Exception as e:
                self.log_message(f"❌ Error updating species: {e}", "error")
        else:
            # Caso cuando se llama desde callback
            self._on_species_updated_callback(success, message)

    def _on_species_updated_callback(self, success: bool, message: str):
        """Callback interno para especie actualizada"""
        if success:
            self.log_message(f"✅ {message}", "success")
            self.view_all_species()  # Recargar lista        else:
            self.log_message(f"❌ {message}", "error")
    
    def _on_species_deleted(self, species_id: int, success: bool, message: str):
        """Callback para especie eliminada"""
        if success:
            self.log_message(f"✅ {message}", "success")
            self.view_all_species()  # Recargar lista
        else:
            self.log_message(f"❌ {message}", "error")
    
    # === Implementaciones CRUD de Zonas faltantes ===
    
    def crear_zona(self):
        """Crear nueva zona"""
        if not self._check_connection():
            return
        
        try:
            zone_data = self._abrir_dialogo_detalles_zona()
            if zone_data:
                self._crear_zona_thread(zone_data)
        except Exception as e:
            self.log_message(f"❌ Error opening create zone dialog: {e}", "error")

    def _crear_zona_thread(self, zone_data):
        """Hilo para crear zona"""
        def create_thread():
            try:
                self.log_message(f"➕ Creating zone: {zone_data['nombre']}")
                success = self.data_manager.create_zone(
                    nombre=zone_data['nombre'],
                    descripcion=zone_data.get('descripcion', ''),
                    area=zone_data.get('area', 0.0)
                )
                
                if success:
                    message = f"Zone '{zone_data['nombre']}' created successfully"
                    self.root.after(0, self._on_zone_created, True, message)
                else:
                    message = f"Failed to create zone '{zone_data['nombre']}'"
                    self.root.after(0, self._on_zone_created, False, message)
                    
            except Exception as e:
                error_msg = f"Error creating zone: {str(e)}"
                self.root.after(0, self._on_zone_created, False, error_msg)
        
        threading.Thread(target=create_thread, daemon=True).start()

    def eliminar_zona(self):
        """Eliminar zona existente"""
        if not self._check_connection():
            return
        
        if not self.current_zones_list:
            self.log_message("ℹ️ Load zones data first to delete", "warning")
            return
        
        # Mostrar lista de zonas para seleccionar
        selected_zone = self._mostrar_dialogo_seleccion_zona(
            "🗑️ Delete Zone", 
            "Select a zone to delete:"
        )
        
        if selected_zone:
            # Usar diálogo de confirmación moderno
            def on_confirmation(confirmed):
                if confirmed:
                    self._eliminar_zona_confirmada(selected_zone)
            
            # Crear diálogo de confirmación moderno
            ModernConfirmationDialog(
                self.root,
                title="Confirm Zone Deletion",
                message=f"Are you sure you want to delete zone '{selected_zone.nombre}'?\n\nThis action cannot be undone.",
                confirm_text="🗑️ Delete",
                cancel_text="❌ Cancel",
                callback=on_confirmation
            )
    
    def _eliminar_zona_confirmada(self, zone):
        """Ejecutar la eliminación confirmada de una zona"""
        def delete_thread():
            try:
                self.log_message(f"🗑️ Deleting zone: {zone.nombre}")
                success = self.data_manager.delete_zone(zone_id=zone.id)
                
                if success:
                    message = f"Zone '{zone.nombre}' deleted successfully"
                    self.root.after(0, self._on_zone_deleted, True, message)
                else:
                    message = f"Failed to delete zone '{zone.nombre}'"
                    self.root.after(0, self._on_zone_deleted, False, message)
                    
            except Exception as e:
                error_msg = f"Error deleting zone: {str(e)}"
                self.root.after(0, self._on_zone_deleted, False, error_msg)
                
        threading.Thread(target=delete_thread, daemon=True).start()
    
    # === Callbacks para operaciones CRUD de Zonas ===
    
    def _on_zone_created(self, success: bool, message: str):
        """Callback para zona creada"""
        if success:
            self.log_message(f"✅ {message}", "success")
            self.load_zones()  # Recargar lista
        else:
            self.log_message(f"❌ {message}", "error")
    
    def _on_zone_updated(self, success: bool, message: str):
        """Callback para zona actualizada"""
        if success:
            self.log_message(f"✅ {message}", "success")
            self.load_zones()  # Recargar lista
        else:
            self.log_message(f"❌ {message}", "error")
    
    def _on_zone_deleted(self, success: bool, message: str):
        """Callback para zona eliminada"""
        if success:
            self.log_message(f"✅ {message}", "success")
            self.load_zones()  # Recargar lista
        else:
            self.log_message(f"❌ {message}", "error")
    
    # === Métodos de diálogos para Zonas ===
    
    def _mostrar_dialogo_seleccion_zona(self, title: str, message: str):
        """Mostrar diálogo de selección de zonas"""
        if not self.current_zones_list:
            self.log_message("ℹ️ No zones data available")
            return None
            
        try:
            from gui.modern_dialogs import ModernConfirmationDialog
            import tkinter as tk
            
            # Crear ventana de selección personalizada
            dialog = ctk.CTkToplevel(self.root)
            dialog.title(title)
            dialog.geometry("400x500")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Centrar diálogo
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (dialog.winfo_screenheight() // 2) - (500 // 2)
            dialog.geometry(f"400x500+{x}+{y}")
            
            selected_zone = [None]  # Lista para poder modificar desde funciones anidadas
            
            # Frame principal
            main_frame = ctk.CTkFrame(dialog)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Título
            title_label = ctk.CTkLabel(
                main_frame,
                text=title,
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title_label.pack(pady=(0, 10))
            
            # Mensaje
            message_label = ctk.CTkLabel(
                main_frame,
                text=message,
                font=ctk.CTkFont(size=14)
            )
            message_label.pack(pady=(0, 20))
            
            # Lista de zonas
            zones_frame = ctk.CTkScrollableFrame(main_frame)
            zones_frame.pack(fill="both", expand=True, pady=(0, 20))
            
            # Agregar botones para cada zona
            for zone in self.current_zones_list:
                zone_btn = ctk.CTkButton(
                    zones_frame,
                    text=f"🌲 {zone.nombre}",
                    command=lambda z=zone: self._select_zone(z, selected_zone, dialog),
                    fg_color=self.modern_colors['primary'],
                    hover_color=self._darken_color(self.modern_colors['primary']),
                    height=40
                )
                zone_btn.pack(fill="x", pady=5, padx=10)
            
            # Botón cancelar
            cancel_btn = ctk.CTkButton(
                main_frame,
                text="❌ Cancel",
                command=dialog.destroy,
                fg_color=self.modern_colors['error'],
                hover_color=self._darken_color(self.modern_colors['error']),
                width=120
            )
            cancel_btn.pack(pady=(10, 0))
            
            # Esperar a que se cierre el diálogo
            self.root.wait_window(dialog)
            
            return selected_zone[0]
            
        except Exception as e:
            self.log_message(f"❌ Error showing zone selection dialog: {e}")
            return None
    
    def _select_zone(self, zone, selected_zone_container, dialog):
        """Seleccionar zona y cerrar diálogo"""
        selected_zone_container[0] = zone
        dialog.destroy()

    # === Métodos de visualización adicionales ===
    
    def view_zones(self):
        """Ver zonas disponibles"""
        self.log_message("🌲 Loading zones view...")
        self.load_zones()
    
    def view_conservation_states(self):
        """Ver estados de conservación"""
        self.log_message("🛡️ Loading conservation states...")
        try:
            states = self.data_manager.get_all_conservation_states()
            if states:
                self.log_message(f"📋 Found {len(states)} conservation states")
                for state in states:
                    self.log_message(f"   • {state.nombre}")
            else:
                self.log_message("❌ No conservation states found")
        except Exception as e:
            self.log_message(f"❌ Error loading conservation states: {e}")

    # === Métodos de búsqueda ===
    
    def _on_search_changed(self, event):
        """Manejar cambios en búsqueda"""
        search_term = self.search_entry.get().lower()
        self._filter_species_display(search_term)
    
    def _filter_species_display(self, search_term):
        """Filtrar visualización de especies"""
        if not hasattr(self, 'current_species_list') or not self.current_species_list:
            return
        
        # Limpiar área de especies
        for widget in self.species_scroll.winfo_children():
            widget.destroy()
        
        # Filtrar y mostrar especies
        filtered_species = [
            species for species in self.current_species_list
            if search_term in species.nombreComun.lower() or 
               search_term in species.nombreCientifico.lower()
        ]
        
        if filtered_species:
            for species in filtered_species:
                self._create_species_card(species)
        else:
            no_results = ctk.CTkLabel(
                self.species_scroll,
                text="🔍 No species found matching your search",
                font=ctk.CTkFont(size=14),
                text_color=self.modern_colors['text_secondary']
            )
            no_results.pack(pady=50)

    # === Importaciones necesarias para los diálogos ===
    def _import_required_modules(self):
        """Importar módulos necesarios para operaciones CRUD"""
        global SpeciesCreateDialog, SpeciesEditDialog, SpeciesDeleteDialog, ModernConfirmationDialog
        try:
            from gui.species_dialogs import SpeciesCreateDialog, SpeciesEditDialog, SpeciesDeleteDialog
            from gui.modern_dialogs import ModernConfirmationDialog
        except ImportError as e:
            self.log_message(f"⚠️ Warning: Could not import dialog modules: {e}")    # === Método de inicialización de importaciones ===
    
    def _setup_dialog_imports(self):
        """Configurar importaciones de diálogos"""
        try:
            self._import_required_modules()
        except Exception as e:
            self.log_message(f"⚠️ Dialog import setup failed: {e}")

    # === Métodos de conexión ===
    
    def _initial_connection_delayed(self):
        """Conexión inicial retardada para ejecutar después de que la GUI esté lista"""
        self._initial_connection()
    
    def _initial_connection(self):
        """Conexión inicial al sistema"""
        try:
            self.log_message("🔌 Connecting to SOAP services...")
            success = self.soap_client.connect()
            if success:
                self.log_message("✅ Connected to SOAP services successfully", "success")
                self._update_connection_indicator(True)
                # Cargar datos de referencia
                self._load_reference_data()
            else:
                self.log_message("❌ Failed to connect to SOAP services", "error")
                self._update_connection_indicator(False)
        except Exception as e:
            self.log_message(f"❌ Connection error: {e}", "error")
            self._update_connection_indicator(False)
    
    def _check_connection(self):
        """Verificar y reconectar si es necesario"""
        try:
            if not self.soap_client.is_connected():
                self.log_message("🔄 Reconnecting to services...")
                success = self.soap_client.connect()
                if success:
                    self.log_message("✅ Reconnected successfully", "success")
                    self._update_connection_indicator(True)
                    return True
                else:
                    self.log_message("❌ Reconnection failed", "error")
                    self._update_connection_indicator(False)
                    return False
            return True
        except Exception as e:
            self.log_message(f"❌ Connection check error: {e}", "error")
            self._update_connection_indicator(False)
            return False

    # === Métodos de utilidad ===
    def log_message(self, message: str, type: str = "info"):
        """Registrar mensaje en el log con colores y timestamp"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Colores según el tipo
            colors = {
                "info": "#81C784",      # Verde claro
                "success": "#4CAF50",   # Verde
                "warning": "#FF9800",   # Naranja
                "error": "#F44336",     # Rojo
                "system": "#2196F3"     # Azul
            }
            
            color = colors.get(type, colors["info"])
            formatted_message = f"[{timestamp}] {message}"
            
            # Añadir al log si existe (solo después de que la GUI esté creada)
            if hasattr(self, 'log_text') and self.log_text:
                self.log_text.insert("end", formatted_message + "\n")
                self.log_text.see("end")
                
            # También imprimir en consola siempre
            print(formatted_message)
            
        except Exception as e:
            print(f"Error logging message: {e}")
    
    def _update_connection_indicator(self, connected: bool):
        """Actualizar indicador de conexión en la interfaz"""
        try:
            if hasattr(self, 'connection_indicator'):
                if connected:
                    self.connection_indicator.configure(
                        text="🟢 Connected",
                        text_color="#4CAF50"
                    )
                else:
                    self.connection_indicator.configure(
                        text="🔴 Disconnected", 
                        text_color="#F44336"
                    )
        except Exception as e:
            print(f"Error updating connection indicator: {e}")
    
    def load_zones(self):
        """Cargar zonas en hilo separado"""
        def _load_zones_thread():
            try:
                zones = self.data_manager.get_all_zones()
                self.current_zones_list = zones
                self.root.after(0, self._update_zones_display, zones)
                self.root.after(0, self.log_message, f"📍 Loaded {len(zones)} zones", "success")
            except Exception as e:
                self.root.after(0, self.log_message, f"❌ Error loading zones: {e}", "error")
        
        threading.Thread(target=_load_zones_thread, daemon=True).start()
    
    def _update_zones_display(self, zones):
        """Actualizar visualización de zonas"""
        try:
            if hasattr(self, 'zones_content'):
                # Limpiar contenido anterior
                for widget in self.zones_content.winfo_children():
                    widget.destroy()
                
                # Mostrar zonas como tarjetas
                for zone in zones:
                    zone_card = self._create_zone_card(self.zones_content, zone)
                    zone_card.pack(fill="x", padx=10, pady=5)
                    
        except Exception as e:
            self.log_message(f"❌ Error updating zones display: {e}", "error")
    
    def _create_zone_card(self, parent, zone):
        """Crear tarjeta visual para una zona"""
        try:
            card = ctk.CTkFrame(parent, fg_color=self.modern_colors['background'])
            
            # Información de la zona
            name_label = ctk.CTkLabel(
                card, 
                text=f"📍 {zone.nombre}",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            name_label.pack(anchor="w", padx=10, pady=(10,0))
            
            if hasattr(zone, 'descripcion') and zone.descripcion:
                desc_label = ctk.CTkLabel(
                    card,
                    text=zone.descripcion,
                    font=ctk.CTkFont(size=12),
                    text_color=self.modern_colors['text_secondary']
                )
                desc_label.pack(anchor="w", padx=10, pady=(0,10))
            
            return card
            
        except Exception as e:
            self.log_message(f"❌ Error creating zone card: {e}", "error")
            return ctk.CTkFrame(parent)  # Return empty frame as fallback
    
    def _abrir_dialogo_detalles_zona(self):
        """Abrir diálogo simple para crear zona (placeholder)"""
        try:
            # Simple input dialog for now
            dialog = ctk.CTkInputDialog(text="Enter Zone Name:", title="🏞️ Create New Zone")
            zone_name = dialog.get_input()
            
            if zone_name:
                return {
                    'nombre': zone_name,
                    'descripcion': f'Zone created: {zone_name}',
                    'area': 0.0
                }
            return None
            
        except Exception as e:
            self.log_message(f"❌ Error in zone dialog: {e}", "error")
            return None

# === Métodos de visualización ===
    
    def connect_soap(self):
        """Stub para conectar al servicio SOAP (debe implementar lógica real)"""
        self.log_message("🌐 [Stub] connect_soap called. Implement connection logic.")
    
    def run(self):
        """Ejecutar la aplicación principal"""
        try:
            # Configurar importaciones de diálogos al inicio
            self._setup_dialog_imports()
            self.root.mainloop()
        except Exception as e:
            print(f"❌ Error running application: {e}")
            raise

# Punto de entrada principal
def main():
    """Función principal moderna"""
    try:
        print("🌳 Starting Modern Forest Species Management System...")
        app = ForestManagementClient()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        return 1
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
