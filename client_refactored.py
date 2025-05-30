"""
🌳 Refactored Modern Forest Client

This is the refactored version of the SOAP client using modular components.
Total lines reduced from 867+ to under 500 by using:
- core/soap_client.py for SOAP operations
- core/data_manager.py for data management
- core/search_engine.py for advanced search functionality
- core/export_manager.py for data export
- gui/main_interface.py for UI components
- gui/species_dialogs.py for CRUD dialogs
"""

import customtkinter as ctk
from tkinter import messagebox
import threading
import logging
from datetime import datetime
from typing import List, Optional

# Import our modular components
from core.soap_client import SOAPClientManager
from core.data_manager import DataManager
from core.search_engine import AdvancedSearchDialog, SearchEngine
from core.export_manager import ExportManager
from core.models import TreeSpecies, SearchFilter
from gui.main_interface import (
    HeaderComponent, 
    SidebarComponent, 
    TabbedContentArea, 
    FooterComponent
)
from gui.species_dialogs import SpeciesCreateDialog, SpeciesEditDialog

# Configure modern theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class ModernForestClientApp:
    """Main application class using modular components."""
    
    def __init__(self):
        """Initialize the modern forest client application."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize main window
        self.setup_main_window()
        
        # Initialize core managers
        self.soap_client = SOAPClientManager()
        self.data_manager = DataManager(self.soap_client)
        self.search_engine = SearchEngine(self.data_manager)
        self.export_manager = ExportManager()
        
        # UI state
        self.current_species_list = []
        self.is_dark_mode = True
        
        # Setup UI components
        self.setup_ui_components()
        
        # Setup callbacks and event handlers
        self.setup_callbacks()
        
        # Auto-connect to service
        self.connect_to_service()
    
    def setup_main_window(self):
        """Setup the main application window."""
        self.root = ctk.CTk()
        self.root.title("🌳 Forest Species Management System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure grid weights for responsive layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)  # Main content area gets most space
    
    def setup_ui_components(self):
        """Setup all UI components using modular design."""
        
        # Header component
        self.header = HeaderComponent(
            self.root,
            connection_callback=self.connect_to_service,
            initial_status=False
        )
        self.header.pack(fill="x", pady=(0, 2))
        
        # Main container for sidebar and content
        main_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        # Sidebar component
        self.sidebar = SidebarComponent(
            main_container,
            callbacks={
                'view_all_species': self.view_all_species,
                'search_by_id': self.search_by_id,
                'advanced_search': self.show_advanced_search,
                'view_zones': self.view_zones,
                'view_conservation_states': self.view_conservation_states,
                'view_statistics': self.view_statistics,
                'create_species': self.create_species,
                'edit_species': self.edit_species,
                'delete_species': self.delete_species,
                'export_data': self.export_data,
                'export_summary': self.export_summary_report,
                'clear_results': self.clear_results,
                'refresh_data': self.refresh_all_data,
                'toggle_theme': self.toggle_theme
            }
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        
        # Tabbed content area
        self.content_area = TabbedContentArea(
            main_container,
            callbacks={
                'log_message': self.log_message,
                'clear_logs': self.clear_logs
            }
        )
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=(2, 0))
        
        # Footer component
        self.footer = FooterComponent(self.root)
        self.footer.pack(fill="x", side="bottom", pady=(2, 0))
        
        # Initial welcome messages
        self.log_message("🌟 Welcome to Forest Species Management System!")
        self.log_message("Modular architecture with advanced search and export capabilities.")
        self.log_message("=" * 70)
    
    def setup_callbacks(self):
        """Setup callbacks between components."""
        # Setup data manager callbacks
        self.data_manager.set_progress_callback(self.log_message)
        
        # Setup export manager callbacks
        def export_complete_callback(success: bool, filename: str):
            if success:
                self.log_message(f"📁 Export completed: {filename}")
            else:
                self.log_message(f"❌ Export failed: {filename}")
        
        # This callback will be set when export is called
        self.export_complete_callback = export_complete_callback
    
    def log_message(self, message: str):
        """Log a message to both results and activity log tabs."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        # Use content area's logging capability
        self.content_area.add_log_message(formatted_message)
        
        # Also log to application logger
        self.logger.info(message.replace("🌟", "").replace("❌", "").replace("✅", "").strip())
    
    # Connection Management
    def connect_to_service(self):
        """Connect to SOAP service asynchronously."""
        self.log_message("🔄 Connecting to SOAP service...")
        threading.Thread(target=self._connect_thread, daemon=True).start()
    
    def _connect_thread(self):
        """Connection thread."""
        try:
            success = self.soap_client.connect()
            self.root.after(0, self._handle_connection_result, success)
        except Exception as e:
            self.root.after(0, self._handle_connection_error, str(e))
    
    def _handle_connection_result(self, success: bool):
        """Handle connection result in main thread."""
        self.header.update_connection_status(success)
        
        if success:
            self.log_message("✅ Successfully connected to SOAP service")
            self.load_reference_data()
        else:
            self.log_message("❌ Failed to connect to SOAP service")
    
    def _handle_connection_error(self, error: str):
        """Handle connection error in main thread."""
        self.header.update_connection_status(False)
        self.log_message(f"❌ Connection error: {error}")
    
    def load_reference_data(self):
        """Load reference data (zones and conservation states)."""
        threading.Thread(target=self._load_reference_data_thread, daemon=True).start()
    
    def _load_reference_data_thread(self):
        """Thread for loading reference data."""
        try:
            # Load zones
            zones = self.data_manager.get_all_zones()
            if zones:
                self.root.after(0, self.log_message, f"📍 Loaded {len(zones)} zones")
            
            # Load conservation states
            states = self.data_manager.get_all_conservation_states()
            if states:
                self.root.after(0, self.log_message, f"🛡️ Loaded {len(states)} conservation states")
                
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Error loading reference data: {e}")
    
    # Data Query Methods
    def view_all_species(self):
        """View all species using data manager."""
        if not self.soap_client.is_connected():
            messagebox.showerror("Connection Error", "No connection to service. Please reconnect.")
            return
        
        self.log_message("🔍 Loading all species...")
        threading.Thread(target=self._view_all_species_thread, daemon=True).start()
    
    def _view_all_species_thread(self):
        """Thread for loading all species."""
        try:
            species_list = self.data_manager.get_all_species()
            self.root.after(0, self._display_species_results, species_list, "All Species")
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Error loading species: {e}")
    
    def search_by_id(self):
        """Search species by ID."""
        if not self.soap_client.is_connected():
            messagebox.showerror("Connection Error", "No connection to service. Please reconnect.")
            return
        
        dialog = ctk.CTkInputDialog(text="Enter Species ID:", title="🔍 Search by ID")
        species_id_str = dialog.get_input()
        
        if species_id_str:
            try:
                species_id = int(species_id_str)
                threading.Thread(target=self._search_by_id_thread, args=(species_id,), daemon=True).start()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric ID")
    
    def _search_by_id_thread(self, species_id: int):
        """Thread for searching by ID."""
        try:
            species = self.data_manager.get_species_by_id(species_id)
            if species:
                self.root.after(0, self._display_species_results, [species], f"Species ID: {species_id}")
            else:
                self.root.after(0, self.log_message, f"ℹ️ Species with ID {species_id} not found")
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Search error: {e}")
    
    def show_advanced_search(self):
        """Show advanced search dialog."""
        if not self.soap_client.is_connected():
            messagebox.showerror("Connection Error", "No connection to service. Please reconnect.")
            return
        
        # Get reference data for search dialog
        zones = self.data_manager.get_all_zones()
        conservation_states = self.data_manager.get_all_conservation_states()
        
        # Create and show advanced search dialog
        dialog = AdvancedSearchDialog(
            self.root,
            zones=zones,
            conservation_states=conservation_states,
            search_callback=self._perform_advanced_search
        )
    
    def _perform_advanced_search(self, search_filter: SearchFilter):
        """Perform advanced search with given filter."""
        self.log_message("🔍 Performing advanced search...")
        threading.Thread(target=self._advanced_search_thread, args=(search_filter,), daemon=True).start()
    
    def _advanced_search_thread(self, search_filter: SearchFilter):
        """Thread for advanced search."""
        try:
            # Get all species first
            all_species = self.data_manager.get_all_species()
            
            # Apply search filter
            filtered_species = self.search_engine.search_species(all_species, search_filter)
            
            self.root.after(0, self._display_species_results, filtered_species, "Advanced Search Results")
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Advanced search error: {e}")
    
    def view_zones(self):
        """Display all zones."""
        try:
            zones = self.data_manager.get_all_zones()
            if zones:
                self.log_message("🌍 Available zones:")
                self.log_message("=" * 40)
                for zone in zones:
                    self.log_message(f"📍 ID: {zone.id} - {zone.name}")
                self.log_message("=" * 40)
            else:
                self.log_message("ℹ️ No zones found")
        except Exception as e:
            self.log_message(f"❌ Error loading zones: {e}")
    
    def view_conservation_states(self):
        """Display all conservation states."""
        try:
            states = self.data_manager.get_all_conservation_states()
            if states:
                self.log_message("🛡️ Conservation states:")
                self.log_message("=" * 50)
                for state in states:
                    self.log_message(f"🛡️ ID: {state.id} - {state.name}")
                self.log_message("=" * 50)
            else:
                self.log_message("ℹ️ No conservation states found")
        except Exception as e:
            self.log_message(f"❌ Error loading conservation states: {e}")
    
    def view_statistics(self):
        """Display species statistics."""
        if not self.current_species_list:
            self.log_message("ℹ️ Load species data first to view statistics")
            return
        
        self.log_message("📊 Species Statistics:")
        self.log_message("=" * 50)
        
        total = len(self.current_species_list)
        active = sum(1 for s in self.current_species_list if s.is_active)
        inactive = total - active
        
        self.log_message(f"📈 Total Species: {total}")
        self.log_message(f"✅ Active Species: {active}")
        self.log_message(f"❌ Inactive Species: {inactive}")
        
        # Statistics by zone
        zone_stats = {}
        for species in self.current_species_list:
            zone_name = species.zone.name if species.zone else 'Unknown'
            zone_stats[zone_name] = zone_stats.get(zone_name, 0) + 1
        
        self.log_message("\n🌍 Species by Zone:")
        for zone, count in sorted(zone_stats.items(), key=lambda x: x[1], reverse=True):
            self.log_message(f"   {zone}: {count}")
        
        self.log_message("=" * 50)
    
    # Species Management Methods
    def create_species(self):
        """Create new species using dialog."""
        if not self.soap_client.is_connected():
            messagebox.showerror("Connection Error", "No connection to service. Please reconnect.")
            return
        
        zones = self.data_manager.get_all_zones()
        conservation_states = self.data_manager.get_all_conservation_states()
        
        if not zones or not conservation_states:
            self.log_message("⚠️ Loading reference data first...")
            self.load_reference_data()
            return
        
        dialog = SpeciesCreateDialog(
            self.root,
            zones=zones,
            conservation_states=conservation_states,
            data_manager=self.data_manager,
            success_callback=self._species_operation_success
        )
    
    def edit_species(self):
        """Edit existing species."""
        if not self.current_species_list:
            self.log_message("ℹ️ Load species data first to edit")
            return
        
        # Simple ID input for now - could be enhanced with a selection dialog
        dialog = ctk.CTkInputDialog(text="Enter Species ID to edit:", title="📝 Edit Species")
        species_id_str = dialog.get_input()
        
        if species_id_str:
            try:
                species_id = int(species_id_str)
                species = next((s for s in self.current_species_list if s.id == species_id), None)
                
                if species:
                    zones = self.data_manager.get_all_zones()
                    conservation_states = self.data_manager.get_all_conservation_states()
                    
                    edit_dialog = SpeciesEditDialog(
                        self.root,
                        species=species,
                        zones=zones,
                        conservation_states=conservation_states,
                        data_manager=self.data_manager,
                        success_callback=self._species_operation_success
                    )
                else:
                    messagebox.showerror("Error", f"Species with ID {species_id} not found in current list")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric ID")
    
    def delete_species(self):
        """Delete species."""
        if not self.current_species_list:
            self.log_message("ℹ️ Load species data first to delete")
            return
        
        dialog = ctk.CTkInputDialog(text="Enter Species ID to delete:", title="🗑️ Delete Species")
        species_id_str = dialog.get_input()
        
        if species_id_str:
            try:
                species_id = int(species_id_str)
                species = next((s for s in self.current_species_list if s.id == species_id), None)
                
                if species:
                    result = messagebox.askyesno(
                        "Confirm Deletion",
                        f"Are you sure you want to delete species:\n'{species.common_name}'?"
                    )
                    
                    if result:
                        threading.Thread(target=self._delete_species_thread, args=(species_id,), daemon=True).start()
                else:
                    messagebox.showerror("Error", f"Species with ID {species_id} not found in current list")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric ID")
    
    def _delete_species_thread(self, species_id: int):
        """Thread for deleting species."""
        try:
            success = self.data_manager.delete_species(species_id)
            if success:
                self.root.after(0, self.log_message, f"✅ Species with ID {species_id} deleted successfully")
                self.root.after(0, self._species_operation_success)
            else:
                self.root.after(0, self.log_message, f"❌ Failed to delete species with ID {species_id}")
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Error deleting species: {e}")
    
    def _species_operation_success(self):
        """Callback for successful species operations."""
        self.log_message("🔄 Refreshing species data...")
        # Refresh current species list if it was loaded
        if self.current_species_list:
            threading.Thread(target=self._view_all_species_thread, daemon=True).start()
    
    # Export Methods
    def export_data(self):
        """Export current species data."""
        if not self.current_species_list:
            self.log_message("ℹ️ Load species data first to export")
            return
        
        # Ask for export format
        format_dialog = ctk.CTkInputDialog(
            text="Enter export format (csv/excel/json):",
            title="📄 Export Data"
        )
        export_format = format_dialog.get_input()
        
        if export_format and export_format.lower() in ['csv', 'excel', 'json']:
            self.export_manager.export_species_data(
                self.current_species_list,
                export_format.lower(),
                callback=self.export_complete_callback
            )
        elif export_format:
            messagebox.showerror("Error", "Invalid format. Use: csv, excel, or json")
    
    def export_summary_report(self):
        """Export summary report."""
        if not self.current_species_list:
            self.log_message("ℹ️ Load species data first to export summary")
            return
        
        self.export_manager.export_summary_report(self.current_species_list)
    
    # UI Utility Methods
    def _display_species_results(self, species_list: List[TreeSpecies], title: str):
        """Display species results in the content area."""
        self.current_species_list = species_list
        
        self.log_message(f"✅ {title} - Found {len(species_list)} species:")
        self.log_message("=" * 80)
        
        if species_list:
            for i, species in enumerate(species_list, 1):
                self.log_message(f"🌿 {i}. {species.common_name}")
                self.log_message(f"   📋 ID: {species.id}")
                self.log_message(f"   🧬 Scientific: {species.scientific_name or 'Not specified'}")
                self.log_message(f"   🛡️ Status: {species.conservation_state.name if species.conservation_state else 'Unknown'}")
                self.log_message(f"   🌍 Zone: {species.zone.name if species.zone else 'Unknown'}")
                self.log_message(f"   ✅ Active: {'Yes' if species.is_active else 'No'}")
                if species.planting_date:
                    self.log_message(f"   📅 Planted: {species.planting_date.strftime('%Y-%m-%d')}")
                self.log_message("")
        else:
            self.log_message("ℹ️ No species found matching criteria")
        
        self.log_message("=" * 80)
        
        # Update species list tab
        self.content_area.update_species_list(species_list)
    
    def clear_results(self):
        """Clear results and reset UI."""
        self.content_area.clear_results()
        self.current_species_list = []
        self.log_message("🧹 Results cleared")
    
    def clear_logs(self):
        """Clear activity logs."""
        self.content_area.clear_logs()
    
    def refresh_all_data(self):
        """Refresh all data from service."""
        if not self.soap_client.is_connected():
            messagebox.showerror("Connection Error", "No connection to service. Please reconnect.")
            return
        
        self.log_message("🔄 Refreshing all data...")
        self.load_reference_data()
        
        # Refresh current species list if loaded
        if self.current_species_list:
            threading.Thread(target=self._view_all_species_thread, daemon=True).start()
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.is_dark_mode = not self.is_dark_mode
        
        if self.is_dark_mode:
            ctk.set_appearance_mode("dark")
            self.log_message("🌙 Switched to dark mode")
        else:
            ctk.set_appearance_mode("light")
            self.log_message("☀️ Switched to light mode")
        
        # Update sidebar switch state
        self.sidebar.update_theme_switch(self.is_dark_mode)
    
    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    try:
        app = ModernForestClientApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        logging.exception("Application startup error")


if __name__ == "__main__":
    main()
