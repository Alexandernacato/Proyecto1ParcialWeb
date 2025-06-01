"""
🌍 Zones Manager - Gestor de operaciones de zonas
"""

import customtkinter as ctk
import threading
from typing import List, Optional
import sys
import os
from tkinter import messagebox

# Add parent directories to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, client_dir)

from utils.theme_manager import ThemeManager
from utils.logger import Logger

try:
    from gui.zone_dialogs import ZoneCreateDialog, ZoneEditDialog
    from core.models import ZoneData
except ImportError:
    # Alternative import paths if needed
    pass


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
        self.search_entry = None
        self.search_type = None
        self.termino_busqueda = ""
        
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
        
        # Área de búsqueda
        self._crear_busqueda_zonas(zones_frame)
        
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
        self._crear_botones_crud_zonas(header_frame) # Renamed from _crear_botones_zonas

    def _crear_botones_crud_zonas(self, parent): # Renamed from _crear_botones_zonas
        """Crear botones CRUD para la gestión de zonas."""
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(side="right")

        botones = [
            ("➕ Add", self.crear, "success"),
            ("✏️ Edit", self._editar_zona_seleccionada, "warning"), # Changed to a new method
            
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

    def _editar_zona_seleccionada(self):
        """Permite al usuario seleccionar una zona para editarla."""
        if not self.zonas_actuales:
            messagebox.showinfo("No Zones", "There are no zones to edit.")
            return

        # Similar a _show_zone_selection_dialog pero para editar
        dialog = ctk.CTkToplevel(self._get_parent_window())
        dialog.title("Select Zone to Edit")
        dialog.geometry("400x500")
        dialog.transient() 
        dialog.grab_set()

        title_label = ctk.CTkLabel(
            dialog,
            text="Select Zone to Edit",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=20)

        zones_frame = ctk.CTkScrollableFrame(dialog)
        zones_frame.pack(fill="both", expand=True, padx=20, pady=10)

        for zona in self.zonas_actuales:
            btn = ctk.CTkButton(
                zones_frame,
                text=f"{zona.nombre} (ID: {zona.id})",
                command=lambda z=zona: self._iniciar_edicion_zona(z, dialog)
            )
            btn.pack(fill="x", pady=5)

        cancel_btn = ctk.CTkButton(
            dialog,
            text="Cancel",
            command=dialog.destroy,
            width=100,
            height=35,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90")
        )
        cancel_btn.pack(pady=20)

    def _iniciar_edicion_zona(self, zona, parent_dialog):
        """Cierra el diálogo de selección e inicia la edición de la zona."""
        parent_dialog.destroy()
        self._editar_zona(zona)


    def _crear_busqueda_zonas(self, parent): # Renamed from _crear_busqueda
        """Crear área de búsqueda para zonas."""
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search zones...",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._al_cambiar_busqueda_zona)

        self.search_type = ctk.CTkOptionMenu(
            search_frame,
            values=["Name", "ID"], # Added ID here
            width=80,
            height=35
        )
        self.search_type.pack(side="left", padx=5)
        self.search_type.set("Name") # Default search type

        ctk.CTkButton(
            search_frame,
            text="🔍",
            width=35,
            command=self._buscar_zona,
            **self.theme_manager.obtener_estilo_boton("info")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame,
            text="🗑️",
            width=35,
            command=self._limpiar_busqueda_zona,
            **self.theme_manager.obtener_estilo_boton("warning")
        ).pack(side="left", padx=5)
        
        # Remove specific ID search entry and button as it's now part of the main search
        # self.search_id_entry = ctk.CTkEntry(...) 
        # ctk.CTkButton(...) for find by ID

    def _configurar_tab_zonas(self):
        """Configurar la pestaña de gestión de zonas."""
        zones_frame = self.content_area.obtener_tab("zones")
        if not zones_frame:
            self.logger.error("Zones tab not found")
            return

        self._crear_header_zonas(zones_frame)
        self._crear_busqueda_zonas(zones_frame) # Use renamed method
        self._crear_area_contenido(zones_frame) # Assuming this creates the scrollable list area
        self.ver_todas()
    
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
                text_color=self.theme_manager.obtener_color('text_secondary')            )
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
    
    def _mostrar_zonas(self, zonas_lista, titulo="Zones List"):
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
            
            self.logger.success(f"✅ {titulo}: Displayed {len(zonas_lista)} zones")
            
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
        
        # Zone details info
        details_frame = ctk.CTkFrame(button_frame)
        details_frame.pack(fill="x", padx=10, pady=5)
        details_text = (
            f"Type: {zona.tipo_bosque}\n"
            f"Area: {zona.area_ha} hectares\n"
            f"Status: {'Active' if zona.activo else 'Inactive'}"
        )
        details_label = ctk.CTkLabel(
            details_frame,
            text=details_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        details_label.pack(anchor="w", padx=10, pady=5)
        
        # Action buttons
        action_frame = ctk.CTkFrame(button_frame)
        action_frame.pack(fill="x", padx=10, pady=5)
        
        # Edit button
        ctk.CTkButton(
            action_frame,
            text="✏️ Edit",
            width=80,
            height=30,
            command=lambda: self._editar_zona(zona),
            fg_color="#059669",
            hover_color="#047857"
        ).pack(side="left", padx=(10, 5), pady=5)
        
        # Delete button
        ctk.CTkButton(
            action_frame,
            text="🗑️ Delete",
            width=80,
            height=30,
            command=lambda: self._eliminar_zona(zona),
            **self.theme_manager.obtener_estilo_boton("error")
        ).pack(side="left", padx=5, pady=5)
    
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
        try:
            # Get parent window for dialog
            parent_window = self._get_parent_window()
            if not parent_window:
                self.logger.error("Cannot find parent window for dialog")
                return
            
            # Create dialog
            dialog = ZoneCreateDialog(parent_window, self._on_zone_created)
            dialog.show()
            
        except Exception as e:
            self.logger.error(f"Error opening create zone dialog: {e}")
            messagebox.showerror("Error", f"Could not open zone creation dialog: {str(e)}")
    
    def _on_zone_created(self, zone_data: ZoneData):
        """Callback cuando se crea una nueva zona"""
        self.logger.info(f"Creating zone: {zone_data.nombre}")
        threading.Thread(target=self._create_zone_thread, args=(zone_data,), daemon=True).start()
    
    def _create_zone_thread(self, zone_data: ZoneData):
        """Hilo para crear zona en el servidor"""
        try:
            # Create zone via SOAP
            success = self.data_manager.create_zone(zone_data)
            
            # Update UI in main thread
            parent = self._get_parent_window()
            if parent and success:
                parent.after(0, self._on_zone_created_success, zone_data.nombre)
                parent.after(0, self.ver_todas)  # Refresh zones list
            elif parent:
                parent.after(0, self._on_zone_created_error, "Failed to create zone")
                
        except Exception as e:
            parent = self._get_parent_window()
            if parent:
                parent.after(0, self._on_zone_created_error, str(e))
    
    def _on_zone_created_success(self, zone_name: str):
        """Callback para éxito en creación de zona"""
        self.logger.success(f"✅ Zone '{zone_name}' created successfully!")
        messagebox.showinfo("Success", f"Zone '{zone_name}' has been created successfully!")
    
    def _on_zone_created_error(self, error_msg: str):
        """Callback para error en creación de zona"""
        self.logger.error(f"❌ Error creating zone: {error_msg}")
        messagebox.showerror("Error", f"Failed to create zone: {error_msg}")
    
    def _editar_zona(self, zona):
        """Editar zona específica"""
        self.logger.info(f"✏️ Editing zone: {zona.nombre}")
        try:
            # Get parent window for dialog
            parent_window = self._get_parent_window()
            if not parent_window:
                self.logger.error("Cannot find parent window for dialog")
                return
            
            # Create edit dialog
            dialog = ZoneEditDialog(parent_window, zona, self._on_zone_edited)
            dialog.show()
            
        except Exception as e:
            self.logger.error(f"Error opening edit zone dialog: {e}")
            messagebox.showerror("Error", f"Could not open zone edit dialog: {str(e)}")
    
    def _on_zone_edited(self, updated_zone: ZoneData):
        """Callback cuando se edita una zona"""
        self.logger.info(f"Updating zone: {updated_zone.nombre}")
        threading.Thread(target=self._update_zone_thread, args=(updated_zone,), daemon=True).start()
    
    def _update_zone_thread(self, zone_data: ZoneData):
        """Hilo para actualizar zona en el servidor"""
        try:
            # Update zone via SOAP
            success = self.data_manager.update_zone(zone_data)
            
            # Update UI in main thread
            parent = self._get_parent_window()
            if parent and success:
                parent.after(0, self._on_zone_updated_success, zone_data.nombre)
                parent.after(0, self.ver_todas)  # Refresh zones list
            elif parent:
                parent.after(0, self._on_zone_updated_error, "Failed to update zone")
                
        except Exception as e:
            parent = self._get_parent_window()
            if parent:
                parent.after(0, self._on_zone_updated_error, str(e))
    
    def _on_zone_updated_success(self, zone_name: str):
        """Callback para éxito en actualización de zona"""
        self.logger.success(f"✅ Zone '{zone_name}' updated successfully!")
        messagebox.showinfo("Success", f"Zone '{zone_name}' has been updated successfully!")
    
    def _on_zone_updated_error(self, error_msg: str):
        """Callback para error en actualización de zona"""
        messagebox.showerror("Error", f"Failed to update zone: {error_msg}")
        self.logger.error(f"❌ Error updating zone: {error_msg}")

    def _get_parent_window(self):
        """Obtener ventana padre para diálogos"""
        try:
            # Check if content_area itself is a CTk widget with a parent
            if hasattr(self.content_area, 'parent_frame') and self.content_area.parent_frame:
                 #This assumes content_area is a more complex component with a specific parent_frame attribute
                current_widget = self.content_area.parent_frame 
            elif hasattr(self.content_area, 'master') and self.content_area.master:
                current_widget = self.content_area # content_area itself might be the parent or a CTkFrame
            else: 
                # Fallback if content_area is not a direct widget or has no obvious master/parent
                # This part might need adjustment based on how content_area is structured
                # For now, let's assume it has a winfo_toplevel method if it's a widget
                if hasattr(self.content_area, 'winfo_toplevel'): 
                    return self.content_area.winfo_toplevel()
                else: # Absolute fallback
                    import tkinter as tk
                    return tk._default_root
            
            # Traverse up to the Toplevel window
            while current_widget and not isinstance(current_widget, ctk.windows.widgets.ctk_toplevel.CTkToplevel) and not isinstance(current_widget, ctk.CTk):
                if hasattr(current_widget, 'master'):
                    current_widget = current_widget.master
                else:
                    # If no master, we might be at the root or a non-tk widget. 
                    # If it has winfo_toplevel, use it.
                    if hasattr(current_widget, 'winfo_toplevel'):
                        return current_widget.winfo_toplevel()
                    return None # Cannot determine parent
            return current_widget
            
        except Exception as e:
            self.logger.error(f"Error getting parent window: {e}")
            # Fallback to default root if any error occurs
            import tkinter as tk
            return tk._default_root
    
    # ===========================================
    # SEARCH METHODS IMPLEMENTATION FOR ZONES
    # ===========================================
    
    def _al_cambiar_busqueda_zona(self, evento=None):
        """Callback para cambio en búsqueda de zonas"""
        termino = self.search_entry.get() if self.search_entry else ""
        if termino != self.termino_busqueda:
            self.termino_busqueda = termino
            self._buscar_zona()
    
    def _buscar_zona(self):
        """Ejecutar búsqueda de zonas según el tipo seleccionado"""
        search_term = self.search_entry.get().strip()
        search_type = self.search_type.get()
        
        if not search_term:
            self.ver_todas()
            return
        
        self.logger.info(f"🔍 Searching zones by {search_type}: '{search_term}'")
        
        if search_type == "ID":
            self._buscar_zona_por_id_directo(search_term)
        else:  # Name search
            self._buscar_zona_por_nombre(search_term)
    
    def _buscar_zona_por_id_directo(self, id_text):
        """Buscar zona por ID desde el campo de texto principal"""
        try:
            zone_id = int(id_text)
            self._buscar_zona_por_id_con_id(zone_id)
        except ValueError:
            self.logger.error(f"❌ Invalid ID format: '{id_text}'. Please enter a valid number.")
            self._mostrar_zonas([], f"Invalid ID: {id_text}")
    
    def _buscar_zona_por_id(self):
        """Buscar zona por ID desde el campo específico"""
        # This method is now OBSOLETE as search is unified.
        # Kept for potential internal calls or future refactoring, but UI element is removed.
        id_text = self.search_id_entry.get().strip() # search_id_entry is removed
        
        if not id_text:
            self.logger.warning("⚠️ Please enter an ID to search")
            return
        
        try:
            zone_id = int(id_text)
            self._buscar_zona_por_id_con_id(zone_id)
        except ValueError:
            self.logger.error(f"❌ Invalid ID format: '{id_text}'. Please enter a valid number.")
            messagebox.showerror("Invalid ID", f"'{id_text}' is not a valid ID. Please enter a number.")
    
    def _buscar_zona_por_id_con_id(self, zone_id: int):
        """Buscar zona por ID específico"""
        self.logger.info(f"🔍 Searching for zone with ID: {zone_id}")
        threading.Thread(target=self._buscar_zona_por_id_thread, args=(zone_id,), daemon=True).start()
    
    def _buscar_zona_por_id_thread(self, zone_id: int):
        """Thread para buscar zona por ID"""
        try:
            # Use DataManager to search by ID
            zona = self.data_manager.get_zone_by_id(zone_id)
            
            if zona:
                # Update UI in main thread
                self.content_area.parent.after(0, self._mostrar_zonas, [zona], f"Zone with ID: {zone_id}")
            else:
                self.content_area.parent.after(0, self._mostrar_sin_resultados_zona_id, zone_id)
                
        except Exception as e:
            self.content_area.parent.after(0, self.logger.error, f"Error searching zone by ID {zone_id}: {e}")
    
    def _buscar_zona_por_nombre(self, name_query: str):
        """Buscar zonas por nombre"""
        self.logger.info(f"🔍 Searching for zones with name: '{name_query}'")
        threading.Thread(target=self._buscar_zona_por_nombre_thread, args=(name_query,), daemon=True).start()
    
    def _buscar_zona_por_nombre_thread(self, name_query: str):
        """Thread para buscar zonas por nombre"""
        try:
            # Use DataManager to search by name
            zonas_encontradas = self.data_manager.search_zones_by_name(name_query, exact_match=False)
            
            if zonas_encontradas:
                # Update UI in main thread
                self.content_area.parent.after(0, self._mostrar_zonas, zonas_encontradas, f"Search results for: '{name_query}'")
            else:
                self.content_area.parent.after(0, self._mostrar_sin_resultados_zona_nombre, name_query)
                
        except Exception as e:
            self.content_area.parent.after(0, self.logger.error, f"Error searching zones by name '{name_query}': {e}")
    
    def _mostrar_sin_resultados_zona_id(self, zone_id: int):
        """Mostrar mensaje cuando no se encuentra zona por ID"""
        # Limpiar display actual
        for widget in self.zones_content.winfo_children():
            widget.destroy()
        
        # Mensaje de no encontrado
        no_data_frame = ctk.CTkFrame(self.zones_content)
        no_data_frame.pack(fill="x", padx=5, pady=20)
        
        no_data_label = ctk.CTkLabel(
            no_data_frame,
            text=f"🔍 No zone found with ID: {zone_id}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.theme_manager.obtener_color('warning')
        )
        no_data_label.pack(pady=20)
        
        # Sugerencia
        suggestion_label = ctk.CTkLabel(
            no_data_frame,
            text="💡 Please verify the ID number or try browsing all zones",
            font=ctk.CTkFont(size=12),
            text_color=self.theme_manager.obtener_color('secondary')
        )
        suggestion_label.pack(pady=5)
        
        # Botón para ver todas las zonas
        ctk.CTkButton(
            no_data_frame,
            text="🌍 View All Zones",
            command=self.ver_todas,
            **self.theme_manager.obtener_estilo_boton("primary")
        ).pack(pady=10)
        
        self.logger.warning(f"No zone found with ID: {zone_id}")
    
    def _mostrar_sin_resultados_zona_nombre(self, name_query: str):
        """Mostrar mensaje cuando no se encuentran zonas por nombre"""
        # Limpiar display actual
        for widget in self.zones_content.winfo_children():
            widget.destroy()
        
        # Mensaje de no encontrado
        no_data_frame = ctk.CTkFrame(self.zones_content)
        no_data_frame.pack(fill="x", padx=5, pady=20)
        
        no_data_label = ctk.CTkLabel(
            no_data_frame,
            text=f"🔍 No zones found matching: '{name_query}'",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.theme_manager.obtener_color('warning')
        )
        no_data_label.pack(pady=20)
        
        # Sugerencia de búsqueda
        suggestion_label = ctk.CTkLabel(
            no_data_frame,
            text="💡 Try searching with different keywords or check spelling",
            font=ctk.CTkFont(size=12),
            text_color=self.theme_manager.obtener_color('secondary')
        )
        suggestion_label.pack(pady=5)
        
        # Botón para ver todas las zonas
        ctk.CTkButton(
            no_data_frame,
            text="🌍 View All Zones",
            command=self.ver_todas,
            **self.theme_manager.obtener_estilo_boton("primary")
        ).pack(pady=10)
        
        self.logger.warning(f"No zones found matching: '{name_query}'")
    
    def _limpiar_busqueda_zona(self):
        """Limpiar búsqueda de zonas y mostrar todas las zonas"""
        self.search_entry.delete(0, 'end')
        self.termino_busqueda = ""
        self.logger.info("🗑️ Zone search cleared - showing all zones")
        self.ver_todas()
