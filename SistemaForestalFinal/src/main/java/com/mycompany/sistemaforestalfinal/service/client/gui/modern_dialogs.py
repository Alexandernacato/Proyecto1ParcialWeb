"""
Modern dialog components with React/HTML-like styling
"""
import customtkinter as ctk
from typing import List, Optional, Callable
import sys
from pathlib import Path

# Agregar el directorio padre para imports relativos
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from core.models import TreeSpecies

class ModernSpeciesSelector(ctk.CTkToplevel):
    """Modern species selector dialog with dropdown and search functionality"""
    
    def __init__(self, parent, species_list: List[TreeSpecies], title: str = "Select Species", 
                 message: str = "Choose a species:", callback: Optional[Callable] = None):
        super().__init__(parent)
        
        self.species_list = species_list
        self.selected_species = None
        self.callback = callback
        
        # Configure window
        self.title(title)
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.center_on_parent(parent)
        
        # Create UI
        self.create_widgets(message)
        
    def center_on_parent(self, parent):
        """Center dialog on parent window"""
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (500 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (400 // 2)
        self.geometry(f"500x400+{x}+{y}")
        
    def create_widgets(self, message: str):
        """Create modern UI components"""
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, height=60, fg_color="#2b2b2b", corner_radius=10)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🌳 Species Selection", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=15)
        
        # Message
        message_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="#cccccc"
        )
        message_label.pack(pady=(0, 10))
        
        # Search section
        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 15))
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍 Search Species:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        search_label.pack(anchor="w")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Type to filter species...",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.search_entry.pack(fill="x", pady=(5, 0))
        self.search_entry.bind("<KeyRelease>", self.on_search_changed)
        
        # Species dropdown section
        dropdown_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        dropdown_frame.pack(fill="x", pady=(0, 15))
        
        dropdown_label = ctk.CTkLabel(
            dropdown_frame,
            text="📋 Select Species:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        dropdown_label.pack(anchor="w")
        
        # Create dropdown options
        self.dropdown_options = self.create_dropdown_options()
        
        self.species_dropdown = ctk.CTkComboBox(
            dropdown_frame,
            values=self.dropdown_options,
            font=ctk.CTkFont(size=12),
            height=35,
            state="readonly"
        )
        self.species_dropdown.pack(fill="x", pady=(5, 0))
        self.species_dropdown.set("Choose a species...")
        
        # Species details section
        details_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a", corner_radius=10)
        details_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        details_title = ctk.CTkLabel(
            details_frame,
            text="ℹ️ Species Details",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        details_title.pack(pady=(10, 5))
        
        self.details_text = ctk.CTkTextbox(
            details_frame,
            font=ctk.CTkFont(size=11),
            height=100,
            state="disabled"
        )
        self.details_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Set up dropdown callback
        self.species_dropdown.configure(command=self.on_species_selected)
        
        # Buttons section
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="❌ Cancel",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#dc3545",
            hover_color="#c82333",
            height=40,
            width=120,
            command=self.cancel
        )
        cancel_button.pack(side="left")
        
        select_button = ctk.CTkButton(
            button_frame,
            text="✅ Select",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#28a745",
            hover_color="#218838",
            height=40,
            width=120,
            command=self.select_species
        )
        select_button.pack(side="right")
        
        # Focus on search entry
        self.search_entry.focus()
        
    def create_dropdown_options(self, filter_text: str = ""):
        """Create formatted dropdown options"""
        options = []
        for species in self.species_list:
            if filter_text and filter_text.lower() not in species.nombreComun.lower():
                continue
                
            status = "✅" if species.activo else "❌"
            zone_name = getattr(species, 'zonaNombre', 'Unknown')
            option = f"{status} {species.nombreComun} - {zone_name}"
            options.append(option)
        
        return options if options else ["No species found"]
    
    def on_search_changed(self, event):
        """Handle search text changes"""
        filter_text = self.search_entry.get()
        filtered_options = self.create_dropdown_options(filter_text)
        
        # Update dropdown
        self.species_dropdown.configure(values=filtered_options)
        if filtered_options and filtered_options[0] != "No species found":
            self.species_dropdown.set(filtered_options[0])
            self.on_species_selected(filtered_options[0])
        else:
            self.species_dropdown.set("No species found")
            self.update_details("")
    
    def on_species_selected(self, selected_option: str):
        """Handle species selection from dropdown"""
        if selected_option == "Choose a species..." or selected_option == "No species found":
            self.update_details("")
            return
            
        # Extract species name from formatted option
        species_name = selected_option.split(" ", 1)[1].split(" - ")[0]  # Remove status and zone
        
        # Find the actual species object
        for species in self.species_list:
            if species.nombreComun == species_name:
                self.selected_species = species
                self.update_details(self.format_species_details(species))
                break
    
    def format_species_details(self, species: TreeSpecies) -> str:
        """Format species details for display"""
        details = f"🌿 Common Name: {species.nombreComun}\n"
        details += f"🧬 Scientific Name: {getattr(species, 'nombreCientifico', 'N/A')}\n"
        details += f"🏔️ Zone: {getattr(species, 'zonaNombre', 'Unknown')}\n"
        details += f"📊 Conservation Status: {getattr(species, 'estadoConservacionNombre', 'Unknown')}\n"
        details += f"🔢 ID: {species.id}\n"
        details += f"✅ Active: {'Yes' if species.activo else 'No'}\n"
        
        if hasattr(species, 'descripcion') and species.descripcion:
            details += f"\n📝 Description:\n{species.descripcion}"
            
        return details
    
    def update_details(self, text: str):
        """Update the details text area"""
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")
        self.details_text.insert("1.0", text)
        self.details_text.configure(state="disabled")
    
    def select_species(self):
        """Handle species selection"""
        if self.selected_species:
            if self.callback:
                self.callback(self.selected_species)
            self.destroy()
        else:
            # Show error message
            error_dialog = ctk.CTkToplevel(self)
            error_dialog.title("Error")
            error_dialog.geometry("300x150")
            error_dialog.transient(self)
            error_dialog.grab_set()
            
            label = ctk.CTkLabel(
                error_dialog,
                text="❌ Please select a species first",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            label.pack(pady=30)
            
            ok_button = ctk.CTkButton(
                error_dialog,
                text="OK",
                command=error_dialog.destroy,
                width=100
            )
            ok_button.pack(pady=10)
    
    def cancel(self):
        """Handle cancel action"""
        self.selected_species = None
        if self.callback:
            self.callback(None)
        self.destroy()


class ModernConfirmationDialog(ctk.CTkToplevel):
    """Modern confirmation dialog with React-like styling"""
    
    def __init__(self, parent, title: str, message: str, 
                 confirm_text: str = "Confirm", cancel_text: str = "Cancel",
                 callback: Optional[Callable] = None):
        super().__init__(parent)
        
        self.result = False
        self.callback = callback
        
        # Configure window
        self.title(title)
        self.geometry("400x250")
        self.resizable(False, False)
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.center_on_parent(parent)
        
        # Create UI
        self.create_widgets(message, confirm_text, cancel_text)
        
    def center_on_parent(self, parent):
        """Center dialog on parent window"""
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (250 // 2)
        self.geometry(f"400x250+{x}+{y}")
        
    def create_widgets(self, message: str, confirm_text: str, cancel_text: str):
        """Create modern UI components"""
        
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icon and message
        icon_label = ctk.CTkLabel(
            main_frame,
            text="⚠️",
            font=ctk.CTkFont(size=48)
        )
        icon_label.pack(pady=(20, 10))
        
        message_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        )
        message_label.pack(pady=(0, 30))
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", side="bottom")
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text=cancel_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#6c757d",
            hover_color="#5a6268",
            height=40,
            width=120,
            command=self.cancel
        )
        cancel_button.pack(side="left")
        
        confirm_button = ctk.CTkButton(
            button_frame,
            text=confirm_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#dc3545",
            hover_color="#c82333",
            height=40,
            width=120,
            command=self.confirm
        )
        confirm_button.pack(side="right")
        
    def confirm(self):
        """Handle confirmation"""
        self.result = True
        if self.callback:
            self.callback(True)
        self.destroy()
        
    def cancel(self):
        """Handle cancellation"""
        self.result = False
        if self.callback:
            self.callback(False)
        self.destroy()
