"""
🔍 Advanced Search Module
Módulo de búsqueda filtrada avanzada para especies forestales
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Callable, List, Any, Dict
from datetime import datetime, date
import threading

from ..core.models import SearchFilter, TreeSpecies, Zone, ConservationState


class AdvancedSearchDialog:
    """Diálogo de búsqueda avanzada"""
    
    def __init__(self, parent, zones: List[Zone], conservation_states: List[ConservationState]):
        self.parent = parent
        self.zones = zones
        self.conservation_states = conservation_states
        self.result_callback: Optional[Callable[[SearchFilter], None]] = None
        self.dialog = None
        
        # Variables del formulario
        self.name_query = ctk.StringVar()
        self.selected_zone = ctk.StringVar()
        self.selected_conservation_state = ctk.StringVar()
        self.active_only = ctk.BooleanVar(value=True)
        self.date_from = ctk.StringVar()
        self.date_to = ctk.StringVar()
        self.scientific_name_query = ctk.StringVar()
        
        self.create_dialog()
    
    def create_dialog(self):
        """Crear diálogo de búsqueda avanzada"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("🔍 Advanced Species Search")
        self.dialog.geometry("600x700")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centrar diálogo
        self.center_dialog()
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="🔎 Advanced Search Filters",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Crear secciones del formulario
        self.create_name_filters(main_frame)
        self.create_location_filters(main_frame)
        self.create_status_filters(main_frame)
        self.create_date_filters(main_frame)
        self.create_buttons(main_frame)
    
    def center_dialog(self):
        """Centrar el diálogo en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (700 // 2)
        self.dialog.geometry(f"600x700+{x}+{y}")
    
    def create_name_filters(self, parent):
        """Crear filtros de nombre"""
        # Frame para filtros de nombre
        name_frame = ctk.CTkFrame(parent)
        name_frame.pack(fill="x", pady=10)
        
        # Header
        ctk.CTkLabel(
            name_frame,
            text="📝 Name Filters",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Nombre común
        ctk.CTkLabel(
            name_frame,
            text="🌿 Common Name Contains:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 5))
        
        common_name_entry = ctk.CTkEntry(
            name_frame,
            textvariable=self.name_query,
            placeholder_text="Enter part of common name...",
            height=35
        )
        common_name_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        # Nombre científico
        ctk.CTkLabel(
            name_frame,
            text="🧬 Scientific Name Contains:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 5))
        
        scientific_name_entry = ctk.CTkEntry(
            name_frame,
            textvariable=self.scientific_name_query,
            placeholder_text="Enter part of scientific name...",
            height=35
        )
        scientific_name_entry.pack(fill="x", padx=15, pady=(0, 15))
    
    def create_location_filters(self, parent):
        """Crear filtros de ubicación"""
        # Frame para filtros de ubicación
        location_frame = ctk.CTkFrame(parent)
        location_frame.pack(fill="x", pady=10)
        
        # Header
        ctk.CTkLabel(
            location_frame,
            text="🌍 Location Filters",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Zona
        ctk.CTkLabel(
            location_frame,
            text="📍 Zone:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 5))
        
        zone_values = ["All Zones"] + [f"{zone.id} - {zone.nombre}" for zone in self.zones]
        zone_combo = ctk.CTkComboBox(
            location_frame,
            variable=self.selected_zone,
            values=zone_values,
            height=35,
            state="readonly"
        )
        zone_combo.set("All Zones")
        zone_combo.pack(fill="x", padx=15, pady=(0, 15))
    
    def create_status_filters(self, parent):
        """Crear filtros de estado"""
        # Frame para filtros de estado
        status_frame = ctk.CTkFrame(parent)
        status_frame.pack(fill="x", pady=10)
        
        # Header
        ctk.CTkLabel(
            status_frame,
            text="🛡️ Status Filters",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Estado de conservación
        ctk.CTkLabel(
            status_frame,
            text="🛡️ Conservation State:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 5))
        
        state_values = ["All States"] + [f"{state.id} - {state.nombre}" for state in self.conservation_states]
        state_combo = ctk.CTkComboBox(
            status_frame,
            variable=self.selected_conservation_state,
            values=state_values,
            height=35,
            state="readonly"
        )
        state_combo.set("All States")
        state_combo.pack(fill="x", padx=15, pady=(0, 10))
        
        # Estado activo
        active_switch = ctk.CTkSwitch(
            status_frame,
            text="✅ Show only active species",
            variable=self.active_only
        )
        active_switch.pack(anchor="w", padx=15, pady=(0, 15))
    
    def create_date_filters(self, parent):
        """Crear filtros de fecha"""
        # Frame para filtros de fecha
        date_frame = ctk.CTkFrame(parent)
        date_frame.pack(fill="x", pady=10)
        
        # Header
        ctk.CTkLabel(
            date_frame,
            text="📅 Date Filters",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Instrucciones
        ctk.CTkLabel(
            date_frame,
            text="📝 Use format: YYYY-MM-DD (e.g., 2024-01-15)",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        # Fecha desde
        ctk.CTkLabel(
            date_frame,
            text="📅 Created From:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 5))
        
        date_from_entry = ctk.CTkEntry(
            date_frame,
            textvariable=self.date_from,
            placeholder_text="YYYY-MM-DD",
            height=35
        )
        date_from_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        # Fecha hasta
        ctk.CTkLabel(
            date_frame,
            text="📅 Created To:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(5, 5))
        
        date_to_entry = ctk.CTkEntry(
            date_frame,
            textvariable=self.date_to,
            placeholder_text="YYYY-MM-DD",
            height=35
        )
        date_to_entry.pack(fill="x", padx=15, pady=(0, 15))
    
    def create_buttons(self, parent):
        """Crear botones de acción"""
        # Frame para botones
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        # Botón cancelar
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Cancel",
            command=self.close_dialog,
            fg_color="gray",
            hover_color="darkgray",
            width=120
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        # Botón limpiar
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🧹 Clear All",
            command=self.clear_filters,
            fg_color="#f59e0b",
            hover_color="#d97706",
            width=120
        )
        clear_btn.pack(side="left", padx=(0, 10))
        
        # Botón buscar
        search_btn = ctk.CTkButton(
            button_frame,
            text="🔍 Search",
            command=self.execute_search,
            fg_color="#059669",
            hover_color="#047857",
            width=120
        )
        search_btn.pack(side="right")
    
    def clear_filters(self):
        """Limpiar todos los filtros"""
        self.name_query.set("")
        self.scientific_name_query.set("")
        self.selected_zone.set("All Zones")
        self.selected_conservation_state.set("All States")
        self.active_only.set(True)
        self.date_from.set("")
        self.date_to.set("")
    
    def validate_dates(self) -> bool:
        """Validar fechas ingresadas"""
        def parse_date(date_str: str) -> Optional[datetime]:
            if not date_str.strip():
                return None
            try:
                return datetime.strptime(date_str.strip(), "%Y-%m-%d")
            except ValueError:
                return False
        
        # Validar fecha desde
        if self.date_from.get().strip():
            date_from_parsed = parse_date(self.date_from.get())
            if date_from_parsed is False:
                messagebox.showerror("Error", "Invalid 'From' date format. Use YYYY-MM-DD")
                return False
        
        # Validar fecha hasta
        if self.date_to.get().strip():
            date_to_parsed = parse_date(self.date_to.get())
            if date_to_parsed is False:
                messagebox.showerror("Error", "Invalid 'To' date format. Use YYYY-MM-DD")
                return False
        
        # Validar que fecha desde sea menor que fecha hasta
        if (self.date_from.get().strip() and self.date_to.get().strip()):
            date_from_parsed = parse_date(self.date_from.get())
            date_to_parsed = parse_date(self.date_to.get())
            if date_from_parsed and date_to_parsed and date_from_parsed > date_to_parsed:
                messagebox.showerror("Error", "'From' date must be earlier than 'To' date")
                return False
        
        return True
    
    def execute_search(self):
        """Ejecutar búsqueda con los filtros seleccionados"""
        # Validar fechas
        if not self.validate_dates():
            return
        
        # Crear objeto SearchFilter
        search_filter = SearchFilter()
        
        # Nombres
        if self.name_query.get().strip():
            search_filter.name_query = self.name_query.get().strip()
        
        if self.scientific_name_query.get().strip():
            # Para búsqueda por nombre científico, combinar con name_query
            if search_filter.name_query:
                search_filter.name_query += f" {self.scientific_name_query.get().strip()}"
            else:
                search_filter.name_query = self.scientific_name_query.get().strip()
        
        # Zona
        if self.selected_zone.get() != "All Zones":
            zone_id = int(self.selected_zone.get().split(" - ")[0])
            search_filter.zone_id = zone_id
        
        # Estado de conservación
        if self.selected_conservation_state.get() != "All States":
            state_id = int(self.selected_conservation_state.get().split(" - ")[0])
            search_filter.conservation_state_id = state_id
        
        # Estado activo
        if self.active_only.get():
            search_filter.active_only = True
        
        # Fechas
        if self.date_from.get().strip():
            search_filter.created_after = datetime.strptime(self.date_from.get().strip(), "%Y-%m-%d")
        
        # Ejecutar callback
        if self.result_callback:
            self.result_callback(search_filter)
        
        self.close_dialog()
    
    def set_result_callback(self, callback: Callable[[SearchFilter], None]):
        """Establecer callback para resultados"""
        self.result_callback = callback
    
    def close_dialog(self):
        """Cerrar diálogo"""
        if self.dialog:
            self.dialog.destroy()
    
    def show(self):
        """Mostrar diálogo"""
        if self.dialog:
            self.dialog.deiconify()
            self.dialog.lift()


class SearchEngine:
    """Motor de búsqueda para especies forestales"""
    
    def __init__(self, soap_client):
        self.soap_client = soap_client
        self.last_results: List[TreeSpecies] = []
    
    def search_with_filter(self, search_filter: SearchFilter, 
                          callback: Optional[Callable[[bool, str, List[TreeSpecies]], None]] = None):
        """Ejecutar búsqueda con filtros en hilo separado"""
        threading.Thread(
            target=self._search_thread,
            args=(search_filter, callback),
            daemon=True
        ).start()
    
    def _search_thread(self, search_filter: SearchFilter, 
                      callback: Optional[Callable[[bool, str, List[TreeSpecies]], None]]):
        """Hilo de búsqueda"""
        try:
            # Obtener todas las especies primero
            all_species = self.soap_client.get_all_tree_species()
            if not all_species:
                if callback:
                    callback(True, "No species found in database", [])
                return
            
            # Aplicar filtros
            filtered_species = self._apply_filters(all_species, search_filter)
            
            # Guardar resultados
            self.last_results = filtered_species
            
            # Ejecutar callback
            if callback:
                message = f"Found {len(filtered_species)} species matching criteria"
                callback(True, message, filtered_species)
                
        except Exception as e:
            if callback:
                callback(False, f"Search error: {str(e)}", [])
    
    def _apply_filters(self, species_list: List[Any], search_filter: SearchFilter) -> List[TreeSpecies]:
        """Aplicar filtros a la lista de especies"""
        filtered = []
        
        for species in species_list:
            # Convertir a TreeSpecies si es necesario
            if hasattr(species, 'nombreComun'):
                tree_species = TreeSpecies(
                    id=getattr(species, 'id', None),
                    nombreComun=getattr(species, 'nombreComun', ''),
                    nombreCientifico=getattr(species, 'nombreCientifico', None),
                    estadoConservacionId=getattr(species, 'estadoConservacionId', 0),
                    estadoConservacionNombre=getattr(species, 'estadoConservacionNombre', ''),
                    zonaId=getattr(species, 'zonaId', 0),
                    zonaNombre=getattr(species, 'zonaNombre', ''),
                    activo=getattr(species, 'activo', True),
                    fechaCreacion=getattr(species, 'fechaCreacion', None),
                    fechaModificacion=getattr(species, 'fechaModificacion', None)
                )
            else:
                tree_species = species
            
            # Aplicar filtros
            if self._matches_filter(tree_species, search_filter):
                filtered.append(tree_species)
        
        return filtered
    
    def _matches_filter(self, species: TreeSpecies, search_filter: SearchFilter) -> bool:
        """Verificar si una especie coincide con los filtros"""
        
        # Filtro por nombre (común o científico)
        if search_filter.name_query:
            query_lower = search_filter.name_query.lower()
            common_name_match = query_lower in species.nombreComun.lower()
            scientific_name_match = (
                species.nombreCientifico and 
                query_lower in species.nombreCientifico.lower()
            )
            if not (common_name_match or scientific_name_match):
                return False
        
        # Filtro por zona
        if search_filter.zone_id is not None:
            if species.zonaId != search_filter.zone_id:
                return False
        
        # Filtro por estado de conservación
        if search_filter.conservation_state_id is not None:
            if species.estadoConservacionId != search_filter.conservation_state_id:
                return False
        
        # Filtro por estado activo
        if search_filter.active_only is not None:
            if search_filter.active_only and not species.activo:
                return False
        
        # Filtro por fecha de creación
        if search_filter.created_after and species.fechaCreacion:
            if species.fechaCreacion < search_filter.created_after:
                return False
        
        return True
    
    def get_last_results(self) -> List[TreeSpecies]:
        """Obtener últimos resultados de búsqueda"""
        return self.last_results.copy()
    
    def clear_results(self):
        """Limpiar resultados de búsqueda"""
        self.last_results.clear()
