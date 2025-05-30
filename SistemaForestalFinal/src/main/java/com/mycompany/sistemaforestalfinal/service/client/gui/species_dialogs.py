"""
Species Dialogs
Dialogos modales para operaciones CRUD de especies
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Callable, List
try:
    from core.models import TreeSpecies, Zone, ConservationState
except ImportError:
    from ..core.models import TreeSpecies, Zone, ConservationState


class SpeciesCreateDialog:
    """Dialogo para crear nueva especie"""
    
    def __init__(self, parent, zones: List[Zone], conservation_states: List[ConservationState], 
                 on_submit: Callable[[TreeSpecies], None]):
        self.parent = parent
        self.zones = zones
        self.conservation_states = conservation_states
        self.on_submit = on_submit
        self.dialog = None
        
        # Variables del formulario
        self.common_name_var = ctk.StringVar()
        self.scientific_name_var = ctk.StringVar()
        self.zone_var = ctk.StringVar()
        self.conservation_state_var = ctk.StringVar()
        self.active_var = ctk.BooleanVar(value=True)
        
    def show(self):
        """Mostrar el dialogo"""
        self._create_dialog()
        
    def _create_dialog(self):
        """Crear el dialogo"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Create New Species")
        self.dialog.geometry("500x650")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centrar dialogo
        self._center_dialog()
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titulo
        title = ctk.CTkLabel(
            main_frame,
            text="Create New Forest Species",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Campos del formulario
        self._create_form_fields(main_frame)
        
        # Botones
        self._create_buttons(main_frame)
        
    def _center_dialog(self):
        """Centrar el dialogo en pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (650 // 2)
        self.dialog.geometry(f"500x650+{x}+{y}")
        
    def _create_form_fields(self, parent):
        """Crear los campos del formulario"""
        # Nombre comun (requerido)
        name_frame = ctk.CTkFrame(parent)
        name_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            name_frame, 
            text="Common Name *", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        name_entry = ctk.CTkEntry(
            name_frame, 
            textvariable=self.common_name_var, 
            height=35,
            placeholder_text="Enter common name..."
        )
        name_entry.pack(fill="x", padx=15, pady=(0, 10))
        name_entry.focus()
        
        # Nombre cientifico (opcional)
        sci_frame = ctk.CTkFrame(parent)
        sci_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            sci_frame, 
            text="Scientific Name", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        ctk.CTkEntry(
            sci_frame, 
            textvariable=self.scientific_name_var, 
            height=35,
            placeholder_text="Enter scientific name (optional)..."
        ).pack(fill="x", padx=15, pady=(0, 10))
        
        # Zona (requerido)
        zone_frame = ctk.CTkFrame(parent)
        zone_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            zone_frame, 
            text="Zone *", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        zone_values = [f"{zone.id} - {zone.nombre}" for zone in self.zones]
        ctk.CTkComboBox(
            zone_frame,
            variable=self.zone_var,
            values=zone_values,
            height=35,
            state="readonly"
        ).pack(fill="x", padx=15, pady=(0, 10))
        
        # Estado de conservacion (requerido)
        state_frame = ctk.CTkFrame(parent)
        state_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            state_frame, 
            text="Conservation State *", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        state_values = [f"{state.id} - {state.nombre}" for state in self.conservation_states]
        ctk.CTkComboBox(
            state_frame,
            variable=self.conservation_state_var,
            values=state_values,
            height=35,
            state="readonly"
        ).pack(fill="x", padx=15, pady=(0, 10))
        
        # Estado activo
        active_frame = ctk.CTkFrame(parent)
        active_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            active_frame, 
            text="Status", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        ctk.CTkSwitch(
            active_frame, 
            text="Active Species", 
            variable=self.active_var
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
    def _create_buttons(self, parent):
        """Crear botones de accion"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        # Boton cancelar
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            fg_color="gray",
            hover_color="darkgray",
            width=120
        ).pack(side="left", padx=(0, 10))
        
        # Boton crear
        ctk.CTkButton(
            button_frame,
            text="Create Species",
            command=self._submit,
            fg_color="#2b7a0b",
            hover_color="#1e5a08",
            width=150
        ).pack(side="right")
        
    def _submit(self):
        """Enviar formulario"""
        # Validar campos obligatorios
        if not self.common_name_var.get().strip():
            messagebox.showerror("Error", "Common name is required")
            return
            
        if not self.zone_var.get():
            messagebox.showerror("Error", "Please select a zone")
            return
            
        if not self.conservation_state_var.get():
            messagebox.showerror("Error", "Please select a conservation state")
            return
            
        # Extraer IDs de los comboboxes
        try:
            zone_id = int(self.zone_var.get().split(" - ")[0])
            conservation_state_id = int(self.conservation_state_var.get().split(" - ")[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid zone or conservation state selection")
            return
            
        # Crear objeto TreeSpecies
        species = TreeSpecies(
            nombreComun=self.common_name_var.get().strip(),
            nombreCientifico=self.scientific_name_var.get().strip() or None,
            zonaId=zone_id,
            estadoConservacionId=conservation_state_id,
            activo=self.active_var.get()
        )
        
        # Llamar callback
        self.on_submit(species)
        
        # Cerrar dialogo
        self.dialog.destroy()


class SpeciesEditDialog:
    """Dialogo para editar especie existente"""
    
    def __init__(self, parent, species: TreeSpecies, zones: List[Zone], 
                 conservation_states: List[ConservationState], 
                 on_submit: Callable[[TreeSpecies], None]):
        self.parent = parent
        self.species = species
        self.zones = zones
        self.conservation_states = conservation_states
        self.on_submit = on_submit
        self.dialog = None
        
        # Variables del formulario
        self.common_name_var = ctk.StringVar(value=species.nombreComun)
        self.scientific_name_var = ctk.StringVar(value=species.nombreCientifico or "")
        self.zone_var = ctk.StringVar()
        self.conservation_state_var = ctk.StringVar()
        self.active_var = ctk.BooleanVar(value=species.activo)
        
        # Configurar valores iniciales de comboboxes
        self._set_initial_values()
        
    def _set_initial_values(self):
        """Configurar valores iniciales de los comboboxes"""
        # Buscar zona actual
        for zone in self.zones:
            if zone.id == self.species.zonaId:
                self.zone_var.set(f"{zone.id} - {zone.nombre}")
                break
                
        # Buscar estado de conservacion actual
        for state in self.conservation_states:
            if state.id == self.species.estadoConservacionId:
                self.conservation_state_var.set(f"{state.id} - {state.nombre}")
                break
                
    def show(self):
        """Mostrar el dialogo"""
        self._create_dialog()
        
    def _create_dialog(self):
        """Crear el dialogo"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title(f"Edit Species: {self.species.nombreComun}")
        self.dialog.geometry("500x650")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centrar dialogo
        self._center_dialog()
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titulo
        title = ctk.CTkLabel(
            main_frame,
            text=f"Edit: {self.species.nombreComun}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # ID de la especie (solo lectura)
        id_frame = ctk.CTkFrame(main_frame)
        id_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            id_frame,
            text="Species ID",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            id_frame,
            text=str(self.species.id),
            font=ctk.CTkFont(size=14),
            fg_color=("gray90", "gray20"),
            corner_radius=6
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        # Campos del formulario
        self._create_form_fields(main_frame)
        
        # Botones
        self._create_buttons(main_frame)
        
    def _center_dialog(self):
        """Centrar el dialogo en pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (650 // 2)
        self.dialog.geometry(f"500x650+{x}+{y}")
        
    def _create_form_fields(self, parent):
        """Crear los campos del formulario"""
        # Nombre comun (requerido)
        name_frame = ctk.CTkFrame(parent)
        name_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            name_frame, 
            text="Common Name *", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        name_entry = ctk.CTkEntry(
            name_frame, 
            textvariable=self.common_name_var, 
            height=35
        )
        name_entry.pack(fill="x", padx=15, pady=(0, 10))
        name_entry.focus()
        
        # Nombre cientifico (opcional)
        sci_frame = ctk.CTkFrame(parent)
        sci_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            sci_frame, 
            text="Scientific Name", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        ctk.CTkEntry(
            sci_frame, 
            textvariable=self.scientific_name_var, 
            height=35
        ).pack(fill="x", padx=15, pady=(0, 10))
        
        # Zona (requerido)
        zone_frame = ctk.CTkFrame(parent)
        zone_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            zone_frame, 
            text="Zone *", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        zone_values = [f"{zone.id} - {zone.nombre}" for zone in self.zones]
        ctk.CTkComboBox(
            zone_frame,
            variable=self.zone_var,
            values=zone_values,
            height=35,
            state="readonly"
        ).pack(fill="x", padx=15, pady=(0, 10))
        
        # Estado de conservacion (requerido)
        state_frame = ctk.CTkFrame(parent)
        state_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            state_frame, 
            text="Conservation State *", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        state_values = [f"{state.id} - {state.nombre}" for state in self.conservation_states]
        ctk.CTkComboBox(
            state_frame,
            variable=self.conservation_state_var,
            values=state_values,
            height=35,
            state="readonly"
        ).pack(fill="x", padx=15, pady=(0, 10))
        
        # Estado activo
        active_frame = ctk.CTkFrame(parent)
        active_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            active_frame, 
            text="Status", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        ctk.CTkSwitch(
            active_frame, 
            text="Active Species", 
            variable=self.active_var
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
    def _create_buttons(self, parent):
        """Crear botones de accion"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        # Boton cancelar
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            fg_color="gray",
            hover_color="darkgray",
            width=120
        ).pack(side="left", padx=(0, 10))
        
        # Boton actualizar
        ctk.CTkButton(
            button_frame,
            text="Update Species",
            command=self._submit,
            fg_color="#d4b106",
            hover_color="#b5960a",
            width=150
        ).pack(side="right")
        
    def _submit(self):
        """Enviar formulario"""
        # Validar campos obligatorios
        if not self.common_name_var.get().strip():
            messagebox.showerror("Error", "Common name is required")
            return
            
        if not self.zone_var.get():
            messagebox.showerror("Error", "Please select a zone")
            return
            
        if not self.conservation_state_var.get():
            messagebox.showerror("Error", "Please select a conservation state")
            return
            
        # Extraer IDs de los comboboxes
        try:
            zone_id = int(self.zone_var.get().split(" - ")[0])
            conservation_state_id = int(self.conservation_state_var.get().split(" - ")[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid zone or conservation state selection")
            return
            
        # Actualizar objeto TreeSpecies
        updated_species = TreeSpecies(
            id=self.species.id,  # Mantener ID original
            nombreComun=self.common_name_var.get().strip(),
            nombreCientifico=self.scientific_name_var.get().strip() or None,
            zonaId=zone_id,
            estadoConservacionId=conservation_state_id,
            activo=self.active_var.get()
        )
        
        # Llamar callback
        self.on_submit(updated_species)
        
        # Cerrar dialogo
        self.dialog.destroy()


class SpeciesDeleteDialog:
    """Dialogo para confirmar eliminacion de especie"""
    
    def __init__(self, parent, species: TreeSpecies, on_confirm: Callable[[int], None]):
        self.parent = parent
        self.species = species
        self.on_confirm = on_confirm
        self.dialog = None
        
    def show(self):
        """Mostrar el dialogo de confirmacion"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Delete Species")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centrar dialogo
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
        
        # Contenido
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icono y titulo
        ctk.CTkLabel(
            main_frame,
            text="WARNING",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="red"
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            main_frame,
            text="Delete Species",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(0, 20))
        
        # Informacion de la especie
        info_text = f"""Are you sure you want to delete this species?

ID: {self.species.id}
Name: {self.species.nombreComun}
Scientific: {self.species.nombreCientifico or 'Not specified'}

This action cannot be undone."""
        
        ctk.CTkLabel(
            main_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="center"
        ).pack(pady=20)
        
        # Botones
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            fg_color="gray",
            hover_color="darkgray",
            width=120
        ).pack(side="left", padx=(20, 10))
        
        ctk.CTkButton(
            button_frame,
            text="Delete",
            command=self._confirm_delete,
            fg_color="#cf1322",
            hover_color="#a10e1c",
            width=120
        ).pack(side="right", padx=(10, 20))
        
    def _confirm_delete(self):
        """Confirmar eliminacion"""
        self.on_confirm(self.species.id)
        self.dialog.destroy()
