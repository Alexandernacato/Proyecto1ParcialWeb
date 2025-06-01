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
        self._crear_botones_zonas(header_frame)
    
    def _crear_botones_zonas(self, parent):
        """Crear botones CRUD para zonas"""
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        botones = [
            ("➕ Add Zone", self.crear, "success"),
            ("🗑️ Delete Zone", self.eliminar, "error"),
            ("👁️ View Zones", self.ver_todas, "info")
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
                text_color=self.theme_manager.obtener_color('text_secondary')
            )
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
    
    def _mostrar_zonas(self, zonas_lista):
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
            
            self.logger.success(f"✅ Displayed {len(zonas_lista)} zones")
            
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
        self.logger.error(f"❌ Error updating zone: {error_msg}")
        messagebox.showerror("Error", f"Failed to update zone: {error_msg}")
    
    def eliminar(self):
        """Eliminar zona seleccionada"""
        self.logger.info("🗑️ Select zone to delete...")
        
        if not self.zonas_actuales:
            messagebox.showwarning("No Zones", "No zones available to delete. Please load zones first.")
            return
        
        # Show selection dialog
        self._show_zone_selection_dialog()
    
    def _show_zone_selection_dialog(self):
        """Mostrar diálogo de selección de zona para eliminar"""
        try:
            parent_window = self._get_parent_window()
            if not parent_window:
                return
            
            # Create selection dialog
            dialog = ctk.CTkToplevel(parent_window)
            dialog.title("Select Zone to Delete")
            dialog.geometry("400x500")
            dialog.resizable(False, False)
            dialog.transient(parent_window)
            dialog.grab_set()
            
            # Center dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (dialog.winfo_screenheight() // 2) - (500 // 2)
            dialog.geometry(f"400x500+{x}+{y}")
            
            # Title
            title_label = ctk.CTkLabel(
                dialog,
                text="Select Zone to Delete",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title_label.pack(pady=20)
            
            # Zones list
            zones_frame = ctk.CTkScrollableFrame(dialog)
            zones_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            for zona in self.zonas_actuales:
                zone_frame = ctk.CTkFrame(zones_frame)
                zone_frame.pack(fill="x", pady=5)
                
                # Zone info
                info_label = ctk.CTkLabel(
                    zone_frame,
                    text=f"ID: {zona.id} - {zona.nombre} ({zona.tipo_bosque})",
                    font=ctk.CTkFont(size=14)
                )
                info_label.pack(side="left", padx=10, pady=10)
                
                # Delete button
                delete_btn = ctk.CTkButton(
                    zone_frame,
                    text="🗑️ Delete",
                    width=80,
                    height=30,
                    fg_color="#dc2626",
                    hover_color="#b91c1c",
                    command=lambda z=zona: [dialog.destroy(), self._eliminar_zona(z)]
                )
                delete_btn.pack(side="right", padx=10, pady=10)
            
            # Cancel button
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
            
        except Exception as e:
            self.logger.error(f"Error showing zone selection dialog: {e}")
            messagebox.showerror("Error", f"Could not show zone selection: {str(e)}")
    
    def _eliminar_zona(self, zona):
        """Eliminar zona específica"""
        self.logger.info(f"🗑️ Deleting zone: {zona.nombre}")
        
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the zone '{zona.nombre}'?\n\n"
            f"Zone Details:\n"
            f"- ID: {zona.id}\n"
            f"- Type: {zona.tipo_bosque}\n"
            f"- Area: {zona.area_ha} hectares\n\n"
            f"This action cannot be undone."
        )
        
        if result:
            threading.Thread(target=self._delete_zone_thread, args=(zona,), daemon=True).start()
    
    def _delete_zone_thread(self, zona):
        """Hilo para eliminar zona del servidor"""
        try:
            # Delete zone via SOAP
            success = self.data_manager.delete_zone(zona.id)
            
            # Update UI in main thread
            parent = self._get_parent_window()
            if parent and success:
                parent.after(0, self._on_zone_deleted_success, zona.nombre)
                parent.after(0, self.ver_todas)  # Refresh zones list
            elif parent:
                parent.after(0, self._on_zone_deleted_error, "Failed to delete zone")
                
        except Exception as e:
            parent = self._get_parent_window()
            if parent:
                parent.after(0, self._on_zone_deleted_error, str(e))
    
    def _on_zone_deleted_success(self, zone_name: str):
        """Callback para éxito en eliminación de zona"""
        self.logger.success(f"✅ Zone '{zone_name}' deleted successfully!")
        messagebox.showinfo("Success", f"Zone '{zone_name}' has been deleted successfully!")
    
    def _on_zone_deleted_error(self, error_msg: str):
        """Callback para error en eliminación de zona"""
        self.logger.error(f"❌ Error deleting zone: {error_msg}")
        messagebox.showerror("Error", f"Failed to delete zone: {error_msg}")
    
    def _get_parent_window(self):
        """Obtener ventana padre para diálogos"""
        try:
            if hasattr(self.content_area, 'parent'):
                return self.content_area.parent
            elif hasattr(self.content_area, 'winfo_toplevel'):
                return self.content_area.winfo_toplevel()
            else:
                # Try to find a tkinter root window
                import tkinter as tk
                return tk._default_root
        except:
            return None
