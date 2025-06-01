"""
🌳 Species Manager - Gestor de operaciones de especies
"""

import customtkinter as ctk
import threading
from typing import List, Optional, Callable
from tkinter import messagebox
import sys
import os

# Add parent directories to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, client_dir)

from utils.theme_manager import ThemeManager
from utils.logger import Logger
from core.models import TreeSpecies


class SpeciesManager:
    """Gestor de operaciones CRUD para especies"""
    
    def __init__(self, data_manager, content_area, theme_manager: ThemeManager, logger: Logger):
        """Inicializar gestor de especies"""
        self.data_manager = data_manager
        self.content_area = content_area
        self.theme_manager = theme_manager
        self.logger = logger
        
        # Estado del gestor
        self.especies_actuales = []
        self.termino_busqueda = ""
        self.especies_scroll = None
        self.search_entry = None
        
        # Configurar pestaña de especies
        self._configurar_tab_especies()
    
    def _configurar_tab_especies(self):
        """Configurar pestaña de especies"""
        species_frame = self.content_area.obtener_tab("species")
        if not species_frame:
            self.logger.error("Species tab not found")
            return
        
        # Header de la pestaña
        self._crear_header_especies(species_frame)
        
        # Área de búsqueda
        self._crear_busqueda(species_frame)
        
        # Lista de especies (scrollable)
        self._crear_lista_especies(species_frame)
        
        # Cargar especies iniciales
        self.ver_todas()
    
    def _crear_header_especies(self, parent):
        """Crear header de la pestaña de especies"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="🌳 Species Management",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.theme_manager.obtener_color('primary')
        )
        title_label.pack(side="left")
        
        # Botones CRUD
        self._crear_botones_crud(header_frame)
    
    def _crear_botones_crud(self, parent):
        """Crear botones CRUD"""
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        botones = [
            ("➕ Add", self.crear, "success"),
            ("✏️ Edit", self.editar, "warning"),
           
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
    
    def _crear_busqueda(self, parent):
        """Crear área de búsqueda"""
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        # Search input
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search species...",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._al_cambiar_busqueda)
        
        # Search type selector
        self.search_type = ctk.CTkOptionMenu(
            search_frame,
            values=["Name", "ID"],
            width=80,
            height=35
        )
        self.search_type.pack(side="left", padx=5)
        self.search_type.set("Name")
    
    def _crear_lista_especies(self, parent):
        """Crear lista scrollable de especies"""
        self.especies_scroll = ctk.CTkScrollableFrame(
            parent,
            fg_color=self.theme_manager.obtener_color('background'),
            corner_radius=10
        )
        self.especies_scroll.pack(fill="both", expand=True, padx=20, pady=10)
    
    def ver_todas(self):
        """Ver todas las especies"""
        self.logger.info("🔍 Loading all species...")
        threading.Thread(target=self._cargar_todas_thread, daemon=True).start()
    
    def _cargar_todas_thread(self):
        """Hilo para cargar todas las especies"""
        try:
            especies_lista = self.data_manager.get_all_species()
            self.especies_actuales = especies_lista
            
            # Actualizar UI en el hilo principal
            if hasattr(self.content_area, 'parent'):
                self.content_area.parent.after(0, self._mostrar_especies, especies_lista, "All Species")
        except Exception as e:
            if hasattr(self.content_area, 'parent'):
                self.content_area.parent.after(0, self.logger.error, f"Error loading species: {e}")
    
    def _mostrar_especies(self, especies_lista, titulo="Species List"):
        """Mostrar lista de especies en la interfaz"""
        try:
            if not self.especies_scroll:
                self.logger.warning("Species display frame not ready")
                return
            
            # Limpiar display actual
            for widget in self.especies_scroll.winfo_children():
                widget.destroy()
            
            if not especies_lista:
                self._mostrar_sin_datos()
                return
            
            # Mostrar especies en diseño de tarjetas
            for especie in especies_lista:
                self._crear_tarjeta_especie(especie)
            
            self.logger.success(f"✅ {titulo}: Displayed {len(especies_lista)} species")
            
        except Exception as e:
            self.logger.error(f"Error displaying species list: {e}")
    
    def _crear_tarjeta_especie(self, especie):
        """Crear tarjeta individual para una especie"""
        # Tarjeta de especie
        tarjeta = ctk.CTkFrame(self.especies_scroll)
        tarjeta.pack(fill="x", padx=5, pady=5)
        
        # Header de la tarjeta
        self._crear_header_tarjeta(tarjeta, especie)
        
        # Detalles de la especie
        self._crear_detalles_tarjeta(tarjeta, especie)
        
        # Botones de acción
        self._crear_botones_tarjeta(tarjeta, especie)
    
    def _crear_header_tarjeta(self, parent, especie):
        """Crear header de tarjeta de especie"""
        header_frame = ctk.CTkFrame(parent)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # ID de la especie
        id_label = ctk.CTkLabel(
            header_frame,
            text=f"ID: {especie.id}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3B82F6"
        )
        id_label.pack(side="left", padx=(10, 5))
        
        # Nombre común
        nombre_label = ctk.CTkLabel(
            header_frame,
            text=f"🌳 {especie.nombreComun}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        nombre_label.pack(side="left", padx=5)
    
    def _crear_detalles_tarjeta(self, parent, especie):
        """Crear sección de detalles de la tarjeta"""
        detalles_frame = ctk.CTkFrame(parent)
        detalles_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Columna izquierda
        col_izq = ctk.CTkFrame(detalles_frame)
        col_izq.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        nombre_cientifico = getattr(especie, 'nombreCientifico', 'N/A')
        ctk.CTkLabel(
            col_izq,
            text=f"📖 Scientific: {nombre_cientifico}",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=5, pady=2)
        
        # Columna derecha
        col_der = ctk.CTkFrame(detalles_frame)
        col_der.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        zona_nombre = getattr(especie, 'zonaNombre', 'Unknown')
        ctk.CTkLabel(
            col_der,
            text=f"🗺️ Zone: {zona_nombre}",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=5, pady=2)
        
        estado_conservacion = getattr(especie, 'estadoConservacionNombre', 'Unknown')
        ctk.CTkLabel(
            col_der,
            text=f"🛡️ Status: {estado_conservacion}",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=5, pady=2)
    
    def _crear_botones_tarjeta(self, parent, especie):
        """Crear botones de acción para la tarjeta"""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Botón editar
        ctk.CTkButton(
            button_frame,
            text="✏️ Edit",
            width=80,
            height=30,
            command=lambda: self._editar_especie(especie),
            **self.theme_manager.obtener_estilo_boton("warning")
        ).pack(side="left", padx=(10, 5), pady=5)
          # Botón eliminar
        ctk.CTkButton(
            button_frame,
            text="🗑️ Delete",
            width=80,
            height=30,
            command=lambda: self._eliminar_especie(especie),
            **self.theme_manager.obtener_estilo_boton("error")
        ).pack(side="left", padx=5, pady=5)
    
    def _mostrar_sin_datos(self):
        """Mostrar mensaje cuando no hay datos"""
        no_data_label = ctk.CTkLabel(
            self.especies_scroll,
            text="📋 No species data to display",
            font=ctk.CTkFont(size=14)
        )
        no_data_label.pack(pady=20)
    
    def _al_cambiar_busqueda(self, evento=None):
        """Callback para cambio en búsqueda"""
        termino = self.search_entry.get() if self.search_entry else ""
        if termino != self.termino_busqueda:
            self.termino_busqueda = termino
            self._buscar()
    
    def _buscar(self):
        """Ejecutar búsqueda según el tipo seleccionado"""
        search_term = self.search_entry.get().strip()
        search_type = self.search_type.get()
        
        if not search_term:
            self.ver_todas()
            return
        
        self.logger.info(f"🔍 Searching by {search_type}: '{search_term}'")
        
        if search_type == "ID":
            self._buscar_por_id_directo(search_term)
        else:  # Name search
            self._buscar_por_nombre(search_term)
    
    def _buscar_por_id_directo(self, id_text):
        """Buscar especie por ID desde el campo de texto principal"""
        try:
            species_id = int(id_text)
            self._buscar_por_id_con_id(species_id)
        except ValueError:
            self.logger.error(f"❌ Invalid ID format: '{id_text}'. Please enter a valid number.")
            self._mostrar_especies([], f"Invalid ID: {id_text}")
    
    def _buscar_por_id(self):
        """Buscar especie por ID desde el campo específico"""
        id_text = self.search_id_entry.get().strip()
        
        if not id_text:
            self.logger.warning("⚠️ Please enter an ID to search")
            return
        
        try:
            species_id = int(id_text)
            self._buscar_por_id_con_id(species_id)
        except ValueError:
            self.logger.error(f"❌ Invalid ID format: '{id_text}'. Please enter a valid number.")
            messagebox.showerror("Invalid ID", f"'{id_text}' is not a valid ID. Please enter a number.")
    
    def _buscar_por_id_con_id(self, species_id: int):
        """Buscar especie por ID específico"""
        self.logger.info(f"🔍 Searching for species with ID: {species_id}")
        threading.Thread(target=self._buscar_por_id_thread, args=(species_id,), daemon=True).start()
    
    def _buscar_por_id_thread(self, species_id: int):
        """Thread para buscar especie por ID"""
        try:
            # Use DataManager to search by ID
            especie = self.data_manager.get_species_by_id(species_id)
            
            if especie:
                # Update UI in main thread
                self.content_area.parent.after(0, self._mostrar_especies, [especie], f"Species with ID: {species_id}")
            else:
                self.content_area.parent.after(0, self._mostrar_sin_resultados_id, species_id)
                
        except Exception as e:
            self.content_area.parent.after(0, self.logger.error, f"Error searching by ID {species_id}: {e}")
    
    def _mostrar_sin_resultados_id(self, species_id: int):
        """Mostrar mensaje cuando no se encuentra especie por ID"""
        # Limpiar display actual
        for widget in self.especies_scroll.winfo_children():
            widget.destroy()
        
        # Mensaje de no encontrado
        no_data_frame = ctk.CTkFrame(self.especies_scroll)
        no_data_frame.pack(fill="x", padx=5, pady=20)
        
        no_data_label = ctk.CTkLabel(
            no_data_frame,
            text=f"🔍 No species found with ID: {species_id}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.theme_manager.obtener_color('warning')
        )
        no_data_label.pack(pady=20)
        
        # Botón para ver todas las especies
        ctk.CTkButton(
            no_data_frame,
            text="🌳 View All Species",
            command=self.ver_todas,
            **self.theme_manager.obtener_estilo_boton("primary")
        ).pack(pady=10)
        
        self.logger.warning(f"No species found with ID: {species_id}")
    
    def _buscar_por_nombre(self, name_query: str):
        """Buscar especies por nombre"""
        self.logger.info(f"🔍 Searching for species with name: '{name_query}'")
        threading.Thread(target=self._buscar_por_nombre_thread, args=(name_query,), daemon=True).start()
    
    def _buscar_por_nombre_thread(self, name_query: str):
        """Thread para buscar especies por nombre"""
        try:
            # Use DataManager to search by name
            especies_encontradas = self.data_manager.search_species_by_name(name_query, exact_match=False)
            
            if especies_encontradas:
                # Update UI in main thread
                self.content_area.parent.after(0, self._mostrar_especies, especies_encontradas, f"Search results for: '{name_query}'")
            else:
                self.content_area.parent.after(0, self._mostrar_sin_resultados_nombre, name_query)
                
        except Exception as e:
            self.content_area.parent.after(0, self.logger.error, f"Error searching by name '{name_query}': {e}")
    
    def _mostrar_sin_resultados_nombre(self, name_query: str):
        """Mostrar mensaje cuando no se encuentran especies por nombre"""
        # Limpiar display actual
        for widget in self.especies_scroll.winfo_children():
            widget.destroy()
        
        # Mensaje de no encontrado
        no_data_frame = ctk.CTkFrame(self.especies_scroll)
        no_data_frame.pack(fill="x", padx=5, pady=20)
        
        no_data_label = ctk.CTkLabel(
            no_data_frame,
            text=f"🔍 No species found matching: '{name_query}'",
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
        
        # Botón para ver todas las especies
        ctk.CTkButton(
            no_data_frame,
            text="🌳 View All Species",
            command=self.ver_todas,
            **self.theme_manager.obtener_estilo_boton("primary")
        ).pack(pady=10)
        
        self.logger.warning(f"No species found matching: '{name_query}'")
    
    def _limpiar_busqueda(self):
        """Limpiar búsqueda y mostrar todas las especies"""
        self.search_entry.delete(0, 'end')
        self.search_id_entry.delete(0, 'end')
        self.termino_busqueda = ""
        self.logger.info("🗑️ Search cleared - showing all species")
        self.ver_todas()
    
    def crear(self):
        """Crear nueva especie"""
        self.logger.info("🆕 Opening create species dialog...")
        self._mostrar_dialogo_especie()
    
    def editar(self):
        """Editar especie seleccionada"""
        self.logger.info("✏️ Select species to edit...")
        messagebox.showinfo("Edit Species", "Please use the Edit button on individual species cards to edit them.")
    
    def eliminar(self):
        """Eliminar especie seleccionada"""
        self.logger.info("🗑️ Select species to delete...")
        messagebox.showinfo("Delete Species", "Please use the Delete button on individual species cards to delete them.")
    
    def _editar_especie(self, especie):
        """Editar especie específica"""
        self.logger.info(f"✏️ Editing species: {especie.nombreComun}")
        self._mostrar_dialogo_especie(especie)
    
    def _eliminar_especie(self, especie):
        """Eliminar especie específica"""
        self.logger.info(f"🗑️ Deleting species: {especie.nombreComun}")
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the species '{especie.nombreComun}'?\n\nThis action cannot be undone.",
            icon="warning"
        )
        
        if respuesta:
            def callback_delete(success, message):
                if success:
                    self.logger.success(message)
                    messagebox.showinfo("Success", message)
                    # Recargar lista de especies
                    self.ver_todas()
                else:
                    self.logger.error(message)
                    messagebox.showerror("Error", message)
            
            # Eliminar especie usando DataManager
            self.data_manager.delete_species(especie.id, callback_delete)
    
    def _mostrar_dialogo_especie(self, especie=None):
        """Mostrar diálogo para crear o editar especie"""
        is_edit = especie is not None
        title = "Edit Species" if is_edit else "Create New Species"
        
        # Crear ventana de diálogo
        dialog = ctk.CTkToplevel()
        dialog.title(title)
        dialog.geometry("500x600")
        dialog.transient()
        dialog.grab_set()
        
        # Centrar la ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Título del diálogo
        title_label = ctk.CTkLabel(
            dialog,
            text=f"🌳 {title}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame principal del formulario
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Variables para los campos
        nombre_comun_var = ctk.StringVar(value=especie.nombreComun if is_edit else "")
        nombre_cientifico_var = ctk.StringVar(value=especie.nombreCientifico if is_edit and especie.nombreCientifico else "")
        zona_var = ctk.StringVar()
        estado_var = ctk.StringVar()
        activo_var = ctk.BooleanVar(value=especie.activo if is_edit else True)
        
        # Campo Nombre Común
        ctk.CTkLabel(form_frame, text="Common Name:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        nombre_comun_entry = ctk.CTkEntry(
            form_frame,
            textvariable=nombre_comun_var,
            placeholder_text="Enter common name",
            width=400,
            height=40
        )
        nombre_comun_entry.pack(padx=20, pady=(0, 15))
        
        # Campo Nombre Científico
        ctk.CTkLabel(form_frame, text="Scientific Name:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(0, 5))
        nombre_cientifico_entry = ctk.CTkEntry(
            form_frame,
            textvariable=nombre_cientifico_var,
            placeholder_text="Enter scientific name (optional)",
            width=400,
            height=40
        )
        nombre_cientifico_entry.pack(padx=20, pady=(0, 15))
        
        # Combobox para Zona
        ctk.CTkLabel(form_frame, text="Zone:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(0, 5))
        
        # Cargar zonas
        zonas = self.data_manager.get_all_zones()
        zona_options = [f"{zona.id} - {zona.nombre}" for zona in zonas]
        
        zona_combobox = ctk.CTkComboBox(
            form_frame,
            values=zona_options,
            variable=zona_var,
            width=400,
            height=40
        )
        zona_combobox.pack(padx=20, pady=(0, 15))
        
        # Preseleccionar zona si estamos editando
        if is_edit and zona_options:
            for option in zona_options:
                if option.startswith(str(especie.zonaId)):
                    zona_var.set(option)
                    break
        
        # Combobox para Estado de Conservación
        ctk.CTkLabel(form_frame, text="Conservation State:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(0, 5))
        
        # Cargar estados de conservación
        estados = self.data_manager.get_all_conservation_states()
        estado_options = [f"{estado.id} - {estado.nombre}" for estado in estados]
        
        estado_combobox = ctk.CTkComboBox(
            form_frame,
            values=estado_options,
            variable=estado_var,
            width=400,
            height=40
        )
        estado_combobox.pack(padx=20, pady=(0, 15))
        
        # Preseleccionar estado si estamos editando
        if is_edit and estado_options:
            for option in estado_options:
                if option.startswith(str(especie.estadoConservacionId)):
                    estado_var.set(option)
                    break
        
        # Checkbox Activo
        activo_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Active",
            variable=activo_var,
            font=ctk.CTkFont(weight="bold")
        )
        activo_checkbox.pack(anchor="w", padx=20, pady=15)
        
        # Frame de botones
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        def guardar_especie():
            # Validar campos requeridos
            if not nombre_comun_var.get().strip():
                messagebox.showerror("Validation Error", "Common name is required.")
                return
            
            if not zona_var.get():
                messagebox.showerror("Validation Error", "Please select a zone.")
                return
            
            if not estado_var.get():
                messagebox.showerror("Validation Error", "Please select a conservation state.")
                return
            
            # Extraer IDs de los combobox
            zona_id = int(zona_var.get().split(" - ")[0])
            estado_id = int(estado_var.get().split(" - ")[0])
            
            # Crear objeto TreeSpecies
            nueva_especie = TreeSpecies(
                id=especie.id if is_edit else None,
                nombreComun=nombre_comun_var.get().strip(),
                nombreCientifico=nombre_cientifico_var.get().strip() or None,
                estadoConservacionId=estado_id,
                zonaId=zona_id,
                activo=activo_var.get()
            )
            
            def callback_save(success, message, result_id=None):
                if success:
                    self.logger.success(message)
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    # Recargar lista de especies
                    self.ver_todas()
                else:
                    self.logger.error(message)
                    messagebox.showerror("Error", message)
            
            # Guardar usando DataManager
            if is_edit:
                self.data_manager.update_species(nueva_especie, callback_save)
            else:
                self.data_manager.create_species(nueva_especie, callback_save)
        
        # Botón Guardar
        save_button = ctk.CTkButton(
            button_frame,
            text="💾 Save",
            command=guardar_especie,
            width=150,
            height=40,
            **self.theme_manager.obtener_estilo_boton("success")
        )
        save_button.pack(side="left", padx=(0, 10))
        
        # Botón Cancelar
        cancel_button = ctk.CTkButton(
            button_frame,
            text="❌ Cancel",
            command=dialog.destroy,
            width=150,
            height=40,
            **self.theme_manager.obtener_estilo_boton("error")
        )
        cancel_button.pack(side="left")
        
        # Enfocar el primer campo
        nombre_comun_entry.focus()
    
    # ===========================================
    # SEARCH METHODS IMPLEMENTATION
    # ===========================================
    
    def _buscar_por_id_con_id(self, species_id: int):
        """Buscar especie por ID específico"""
        self.logger.info(f"🔍 Searching for species with ID: {species_id}")
        threading.Thread(target=self._buscar_por_id_thread, args=(species_id,), daemon=True).start()
    
    def _buscar_por_id_thread(self, species_id: int):
        """Thread para buscar especie por ID"""
        try:
            # Use DataManager to search by ID
            especie = self.data_manager.get_species_by_id(species_id)
            
            if especie:
                # Update UI in main thread
                self.content_area.parent.after(0, self._mostrar_especies, [especie], f"Species with ID: {species_id}")
            else:
                self.content_area.parent.after(0, self._mostrar_sin_resultados_id, species_id)
                
        except Exception as e:
            self.content_area.parent.after(0, self.logger.error, f"Error searching by ID {species_id}: {e}")
    
    def _mostrar_sin_resultados_id(self, species_id: int):
        """Mostrar mensaje cuando no se encuentra especie por ID"""
        # Limpiar display actual
        for widget in self.especies_scroll.winfo_children():
            widget.destroy()
        
        # Mensaje de no encontrado
        no_data_frame = ctk.CTkFrame(self.especies_scroll)
        no_data_frame.pack(fill="x", padx=5, pady=20)
        
        no_data_label = ctk.CTkLabel(
            no_data_frame,
            text=f"🔍 No species found with ID: {species_id}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.theme_manager.obtener_color('warning')
        )
        no_data_label.pack(pady=20)
        
        # Botón para ver todas las especies
        ctk.CTkButton(
            no_data_frame,
            text="🌳 View All Species",
            command=self.ver_todas,
            **self.theme_manager.obtener_estilo_boton("primary")
        ).pack(pady=10)
        
        self.logger.warning(f"No species found with ID: {species_id}")
    
    def _buscar_por_nombre(self, name_query: str):
        """Buscar especies por nombre"""
        self.logger.info(f"🔍 Searching for species with name: '{name_query}'")
        threading.Thread(target=self._buscar_por_nombre_thread, args=(name_query,), daemon=True).start()
    
    def _buscar_por_nombre_thread(self, name_query: str):
        """Thread para buscar especies por nombre"""
        try:
            # Use DataManager to search by name
            especies_encontradas = self.data_manager.search_species_by_name(name_query, exact_match=False)
            
            if especies_encontradas:
                # Update UI in main thread
                self.content_area.parent.after(0, self._mostrar_especies, especies_encontradas, f"Search results for: '{name_query}'")
            else:
                self.content_area.parent.after(0, self._mostrar_sin_resultados_nombre, name_query)
                
        except Exception as e:
            self.content_area.parent.after(0, self.logger.error, f"Error searching by name '{name_query}': {e}")
    
    def _mostrar_sin_resultados_nombre(self, name_query: str):
        """Mostrar mensaje cuando no se encuentran especies por nombre"""
        # Limpiar display actual
        for widget in self.especies_scroll.winfo_children():
            widget.destroy()
        
        # Mensaje de no encontrado
        no_data_frame = ctk.CTkFrame(self.especies_scroll)
        no_data_frame.pack(fill="x", padx=5, pady=20)
        
        no_data_label = ctk.CTkLabel(
            no_data_frame,
            text=f"🔍 No species found matching: '{name_query}'",
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
        
        # Botón para ver todas las especies
        ctk.CTkButton(
            no_data_frame,
            text="🌳 View All Species",
            command=self.ver_todas,
            **self.theme_manager.obtener_estilo_boton("primary")
        ).pack(pady=10)
        
        self.logger.warning(f"No species found matching: '{name_query}'")
