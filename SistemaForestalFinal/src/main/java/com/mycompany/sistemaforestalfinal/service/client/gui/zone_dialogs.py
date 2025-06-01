"""
Zone Dialogs
Dialogos modales para operaciones CRUD de zonas
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Callable
from decimal import Decimal, InvalidOperation
try:
    from core.models import Zone, TipoBosque
except ImportError:
    from ..core.models import Zone, TipoBosque


class ZoneCreateDialog:
    """Dialogo para crear nueva zona"""
    
    def __init__(self, parent, on_submit: Callable[[Zone], None]):
        self.parent = parent
        self.on_submit = on_submit
        self.dialog = None
        
        # Variables del formulario
        self.nombre_var = ctk.StringVar()
        self.tipo_bosque_var = ctk.StringVar()
        self.area_ha_var = ctk.StringVar()
        self.activo_var = ctk.BooleanVar(value=True)
        
    def show(self):
        """Mostrar el dialogo"""
        self._create_dialog()
        
    def _create_dialog(self):
        """Crear el dialogo"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Create New Zone")
        self.dialog.geometry("500x550")
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
            text="Create New Forest Zone",
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
        y = (self.dialog.winfo_screenheight() // 2) - (550 // 2)
        self.dialog.geometry(f"500x550+{x}+{y}")
        
    def _create_form_fields(self, parent):
        """Crear los campos del formulario"""
        # Nombre (requerido)
        nombre_frame = ctk.CTkFrame(parent)
        nombre_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            nombre_frame, 
            text="Zone Name *", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        nombre_entry = ctk.CTkEntry(
            nombre_frame, 
            textvariable=self.nombre_var, 
            height=35,
            placeholder_text="Enter zone name..."
        )
        nombre_entry.pack(fill="x", padx=15, pady=(0, 10))
        nombre_entry.focus()
          # Tipo de bosque (requerido)
        tipo_frame = ctk.CTkFrame(parent)
        tipo_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            tipo_frame, 
            text="Forest Type *",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        tipo_combobox = ctk.CTkComboBox(
            tipo_frame,
            variable=self.tipo_bosque_var,
            values=[tipo.get_display_name() for tipo in TipoBosque],
            height=35,
            state="readonly"
        )
        tipo_combobox.pack(fill="x", padx=15, pady=(0, 10))
        tipo_combobox.set("Select forest type...")
        
        # Area en hectareas (requerido)
        area_frame = ctk.CTkFrame(parent)
        area_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            area_frame, 
            text="Area (Hectares) *",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        area_entry = ctk.CTkEntry(
            area_frame, 
            textvariable=self.area_ha_var, 
            height=35,
            placeholder_text="Enter area in hectares (e.g., 150.75)..."
        )
        area_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        # Estado activo
        status_frame = ctk.CTkFrame(parent)
        status_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            status_frame, 
            text="Status",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        status_checkbox = ctk.CTkCheckBox(
            status_frame,
            text="Active Zone",
            variable=self.activo_var
        )
        status_checkbox.pack(anchor="w", padx=15, pady=(0, 10))
        
    def _create_buttons(self, parent):
        """Crear botones del dialogo"""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Boton cancelar
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._cancel,
            width=120,
            height=35,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90")
        )
        cancel_btn.pack(side="left", padx=(15, 10), pady=15)
        
        # Boton crear
        create_btn = ctk.CTkButton(
            button_frame,
            text="Create Zone",
            command=self._submit,
            width=120,
            height=35
        )
        create_btn.pack(side="right", padx=(10, 15), pady=15)
        
    def _validate_form(self) -> bool:
        """Validar el formulario"""
        # Validar nombre
        if not self.nombre_var.get().strip():
            messagebox.showerror("Validation Error", "Zone name is required.")
            return False        # Validar tipo de bosque
        if not self.tipo_bosque_var.get() or self.tipo_bosque_var.get() == "Select forest type...":
            messagebox.showerror("Validation Error", "Forest type is required.")
            return False
        
        # Validar area
        area_str = self.area_ha_var.get().strip()
        if not area_str:
            messagebox.showerror("Validation Error", "Area is required.")
            return False
        
        try:
            area_value = Decimal(area_str)
            if area_value <= 0:
                messagebox.showerror("Validation Error", "Area must be greater than 0.")
                return False
        except (InvalidOperation, ValueError):
            messagebox.showerror("Validation Error", "Please enter a valid number for area.")
            return False
        
        return True
        
    def _submit(self):
        """Enviar formulario"""
        if not self._validate_form():
            return
        
        try:
            # Obtener el enum TipoBosque desde el display name
            selected_display = self.tipo_bosque_var.get()
            tipo_bosque = None
            for tipo in TipoBosque:
                if tipo.get_display_name() == selected_display:
                    tipo_bosque = tipo
                    break
            
            if not tipo_bosque:
                messagebox.showerror("Error", "Invalid forest type selected.")
                return
            
            # Crear objeto Zone
            zone = Zone(
                id=None,  # Se asignara por el servidor
                nombre=self.nombre_var.get().strip(),
                descripcion=None,
                tipo_bosque=tipo_bosque,
                area_ha=float(self.area_ha_var.get().strip()),
                activo=self.activo_var.get(),
                fecha_creacion=None,  # Se asignara por el servidor
                fecha_modificacion=None  # Se asignara por el servidor
            )
            
            # Llamar callback
            self.on_submit(zone)
            
            # Cerrar dialogo
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating zone: {str(e)}")
        
    def _cancel(self):
        """Cancelar dialogo"""
        self.dialog.destroy()


class ZoneEditDialog:
    """Dialogo para editar zona existente"""
    
    def __init__(self, parent, zone: Zone, on_submit: Callable[[Zone], None]):
        self.parent = parent
        self.zone = zone
        self.on_submit = on_submit
        self.dialog = None
        
        # Variables del formulario (pre-pobladas con datos existentes)
        self.nombre_var = ctk.StringVar(value=zone.nombre or "")
        self.tipo_bosque_var = ctk.StringVar(value=zone.tipo_bosque.get_display_name() if zone.tipo_bosque else "")
        self.area_ha_var = ctk.StringVar(value=str(zone.area_ha) if zone.area_ha else "")
        self.activo_var = ctk.BooleanVar(value=zone.activo if zone.activo is not None else True)
        
    def show(self):
        """Mostrar el dialogo"""
        self._create_dialog()
        
    def _create_dialog(self):
        """Crear el dialogo"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Edit Zone")
        self.dialog.geometry("500x550")
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
            text=f"Edit Zone: {self.zone.nombre}",
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
        y = (self.dialog.winfo_screenheight() // 2) - (550 // 2)
        self.dialog.geometry(f"500x550+{x}+{y}")
        
    def _create_form_fields(self, parent):
        """Crear los campos del formulario"""
        # Nombre (requerido)
        nombre_frame = ctk.CTkFrame(parent)
        nombre_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            nombre_frame, 
            text="Zone Name *", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        nombre_entry = ctk.CTkEntry(
            nombre_frame, 
            textvariable=self.nombre_var, 
            height=35,
            placeholder_text="Enter zone name..."
        )
        nombre_entry.pack(fill="x", padx=15, pady=(0, 10))
        nombre_entry.focus()
          # Tipo de bosque (requerido)
        tipo_frame = ctk.CTkFrame(parent)
        tipo_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            tipo_frame, 
            text="Forest Type *",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        tipo_combobox = ctk.CTkComboBox(
            tipo_frame,
            variable=self.tipo_bosque_var,
            values=[tipo.get_display_name() for tipo in TipoBosque],
            height=35,
            state="readonly"
        )
        tipo_combobox.pack(fill="x", padx=15, pady=(0, 10))
        
        # Area en hectareas (requerido)
        area_frame = ctk.CTkFrame(parent)
        area_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            area_frame, 
            text="Area (Hectares) *",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        area_entry = ctk.CTkEntry(
            area_frame, 
            textvariable=self.area_ha_var, 
            height=35,
            placeholder_text="Enter area in hectares (e.g., 150.75)..."
        )
        area_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        # Estado activo
        status_frame = ctk.CTkFrame(parent)
        status_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            status_frame, 
            text="Status",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        status_checkbox = ctk.CTkCheckBox(
            status_frame,
            text="Active Zone",
            variable=self.activo_var
        )
        status_checkbox.pack(anchor="w", padx=15, pady=(0, 10))
        
    def _create_buttons(self, parent):
        """Crear botones del dialogo"""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Boton cancelar
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._cancel,
            width=120,
            height=35,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90")
        )
        cancel_btn.pack(side="left", padx=(15, 10), pady=15)
        
        # Boton guardar
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Changes",
            command=self._submit,
            width=120,
            height=35
        )
        save_btn.pack(side="right", padx=(10, 15), pady=15)
        
    def _validate_form(self) -> bool:
        """Validar el formulario"""
        # Validar nombre
        if not self.nombre_var.get().strip():
            messagebox.showerror("Validation Error", "Zone name is required.")
            return False
          # Validar tipo de bosque
        if not self.tipo_bosque_var.get():
            messagebox.showerror("Validation Error", "Forest type is required.")
            return False
        
        # Validar area
        area_str = self.area_ha_var.get().strip()
        if not area_str:
            messagebox.showerror("Validation Error", "Area is required.")
            return False
        
        try:
            area_value = Decimal(area_str)
            if area_value <= 0:
                messagebox.showerror("Validation Error", "Area must be greater than 0.")
                return False
        except (InvalidOperation, ValueError):
            messagebox.showerror("Validation Error", "Please enter a valid number for area.")
            return False
        
        return True
        
    def _submit(self):
        """Enviar formulario"""
        """Enviar formulario"""
        if not self._validate_form():
            return
        
        try:
            # Obtener el enum TipoBosque desde el display name
            selected_display = self.tipo_bosque_var.get()
            tipo_bosque = None
            for tipo in TipoBosque:
                if tipo.get_display_name() == selected_display:
                    tipo_bosque = tipo
                    break
            
            if not tipo_bosque:
                messagebox.showerror("Error", "Invalid forest type selected.")
                return
            
            # Actualizar objeto zone con nuevos valores
            updated_zone = Zone(
                id=self.zone.id,  # Mantener el ID original
                nombre=self.nombre_var.get().strip(),
                descripcion=self.zone.descripcion,
                tipo_bosque=tipo_bosque,
                area_ha=float(self.area_ha_var.get().strip()),
                activo=self.activo_var.get(),
                fecha_creacion=self.zone.fecha_creacion,  # Mantener fecha original
                fecha_modificacion=None  # Se actualizara por el servidor
            )
            
            # Llamar callback
            self.on_submit(updated_zone)
            
            # Cerrar dialogo
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating zone: {str(e)}")
        
    def _cancel(self):
        """Cancelar dialogo"""
        self.dialog.destroy()
