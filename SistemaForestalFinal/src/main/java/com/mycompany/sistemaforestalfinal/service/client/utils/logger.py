"""
📋 Logger - Sistema de registro de actividades
"""

from datetime import datetime
from typing import Callable, Optional
import customtkinter as ctk


class Logger:
    """Sistema de logging para la aplicación"""
    
    def __init__(self, log_widget: Optional[ctk.CTkTextbox] = None):
        """Inicializar logger"""
        self.log_widget = log_widget
        self.callbacks = []
    
    def agregar_widget(self, widget: ctk.CTkTextbox):
        """Agregar widget de texto para mostrar logs"""
        self.log_widget = widget
    
    def agregar_callback(self, callback: Callable):
        """Agregar callback para eventos de log"""
        self.callbacks.append(callback)
    
    def log(self, mensaje: str, tipo: str = "info"):
        """Registrar mensaje con tipo"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        icono = self._obtener_icono(tipo)
        mensaje_formateado = f"[{timestamp}] {icono} {mensaje}\n"
        
        # Mostrar en widget si está disponible
        if self.log_widget:
            self.log_widget.insert("end", mensaje_formateado)
            self.log_widget.see("end")
        
        # Llamar callbacks
        for callback in self.callbacks:
            try:
                callback(mensaje, tipo)
            except Exception as e:
                print(f"Error in log callback: {e}")
        
        # También imprimir en consola
        print(f"{icono} {mensaje}")
    
    def _obtener_icono(self, tipo: str) -> str:
        """Obtener icono según tipo de mensaje"""
        iconos = {
            "info": "ℹ️",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "debug": "🐛"
        }
        return iconos.get(tipo, "📝")
    
    def limpiar(self):
        """Limpiar el log"""
        if self.log_widget:
            self.log_widget.delete("1.0", "end")
            self.log("📋 Log cleared", "info")
    
    def success(self, mensaje: str):
        """Log de éxito"""
        self.log(mensaje, "success")
    
    def error(self, mensaje: str):
        """Log de error"""
        self.log(mensaje, "error")
    
    def warning(self, mensaje: str):
        """Log de advertencia"""
        self.log(mensaje, "warning")
    
    def info(self, mensaje: str):
        """Log de información"""
        self.log(mensaje, "info")
