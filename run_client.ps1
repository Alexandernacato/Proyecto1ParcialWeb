# Script PowerShell para ejecutar el cliente Python de Especies Forestales
# Activa el entorno virtual y ejecuta la aplicación

Write-Host "🌳 Iniciando Cliente SOAP de Especies Forestales..." -ForegroundColor Green
Write-Host ""

# Activar entorno virtual
& ".\venv\Scripts\Activate.ps1"

# Ejecutar la GUI
python "SistemaForestalFinal\src\main\java\com\mycompany\sistemaforestalfinal\service\client\tree_species_gui.py"

Write-Host ""
Write-Host "🏁 Aplicación cerrada" -ForegroundColor Yellow
Read-Host "Presiona Enter para continuar"
