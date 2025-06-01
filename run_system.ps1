# Sistema Forestal SOAP - Launcher Fixed
# Este script inicia los servicios SOAP y el cliente GUI automaticamente

Write-Host "=== SISTEMA FORESTAL - INICIANDO ===" -ForegroundColor Green

# 1. Verificar que no haya procesos Java anteriores
Write-Host "Deteniendo procesos Java anteriores..." -ForegroundColor Yellow
Get-Process -Name "java" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Ir al directorio del proyecto
Set-Location ".\SistemaForestalFinal"

# 3. Compilar si es necesario
if (-not (Test-Path "target\classes")) {
    Write-Host "Compilando proyecto..." -ForegroundColor Cyan
    mvn clean compile -q
}

# 4. Iniciar servicios SOAP en background
Write-Host "Iniciando servicio Species SOAP en puerto 8282..." -ForegroundColor Cyan
$speciesJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    mvn exec:java "-Dexec.mainClass=com.mycompany.sistemaforestalfinal.service.server.CrudSpeciesPublication"
}

Write-Host "Iniciando servicio Zones SOAP en puerto 8081..." -ForegroundColor Cyan
$zonesJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    mvn exec:java "-Dexec.mainClass=com.mycompany.sistemaforestalfinal.service.server.CrudZonesPublication"
}

# 5. Esperar a que los servidores estén disponibles
Write-Host "Esperando a que los servidores estén listos..." -ForegroundColor Yellow
$maxWait = 60
$waited = 0
$speciesReady = $false
$zonesReady = $false

do {
    Start-Sleep -Seconds 2
    $waited += 2
    
    # Verificar servicio Species
    if (-not $speciesReady) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8282/TreeSpeciesCrudService?wsdl" -TimeoutSec 3 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-Host "Servicio Species SOAP disponible!" -ForegroundColor Green
                $speciesReady = $true
            }
        } catch {
            # Silently continue
        }
    }
      # Verificar servicio Zones
    if (-not $zonesReady) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8081/SistemaForestalFinal/ZoneCrudService?wsdl" -TimeoutSec 3 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-Host "Servicio Zones SOAP disponible!" -ForegroundColor Green
                $zonesReady = $true
            }
        } catch {
            # Silently continue
        }
    }
    
    if ($waited % 10 -eq 0) {
        Write-Host "   Esperando servicios... ($waited/$maxWait segundos)" -ForegroundColor Yellow
    }
    
} while ((-not $speciesReady -or -not $zonesReady) -and $waited -lt $maxWait)

# Volver al directorio principal
Set-Location ".."

# Verificar que al menos un servicio este disponible
if (-not $speciesReady -and -not $zonesReady) {
    Write-Host "ERROR: Ningun servicio SOAP pudo iniciarse despues de $maxWait segundos" -ForegroundColor Red
    Write-Host "Deteniendo procesos..." -ForegroundColor Yellow
    Get-Job | Stop-Job; Get-Job | Remove-Job
    exit 1
} elseif (-not $speciesReady) {
    Write-Host "ADVERTENCIA: Solo el servicio Zones esta disponible" -ForegroundColor Yellow
} elseif (-not $zonesReady) {
    Write-Host "ADVERTENCIA: Solo el servicio Species esta disponible" -ForegroundColor Yellow
}

# 6. Configurar entorno virtual de Python
Write-Host "Configurando entorno virtual de Python..." -ForegroundColor Cyan

# Verificar si existe el entorno virtual
if (-not (Test-Path "venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: No se pudo crear el entorno virtual" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
try {
    . .\\venv\\Scripts\\Activate.ps1
    Write-Host "Entorno virtual activado." -ForegroundColor Green
} catch {
    Write-Host "ERROR: No se pudo activar el entorno virtual." -ForegroundColor Red
    Write-Host $_.Exception.Message
    # Detener jobs de servicios si la activación falla
    Get-Job | Stop-Job | Remove-Job
    exit 1
}

Write-Host "Instalando dependencias desde requirements.txt..." -ForegroundColor Cyan
python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: No se pudieron instalar las dependencias de Python." -ForegroundColor Red
    Get-Job | Stop-Job | Remove-Job # Detener jobs de servicios
    exit 1
}
Write-Host "Dependencias instaladas." -ForegroundColor Green

Write-Host "Configurando consola para UTF-8..." -ForegroundColor Cyan
$OriginalConsoleEncoding = [Console]::OutputEncoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8" # Tell Python to use UTF-8

Write-Host "Iniciando cliente Python GUI..." -ForegroundColor Cyan
# Ejecutar el cliente Python y capturar su salida.
$pythonOutput = python .\\SistemaForestalFinal\\src\\main\\java\\com\\mycompany\\sistemaforestalfinal\\service\\client\\client.py 2>&1 | Tee-Object -Variable pythonExecutionOutput | Out-String
# $LASTEXITCODE will contain the exit code of the python script

Write-Host "--- Salida del Cliente Python ---" -ForegroundColor Magenta
Write-Host $pythonExecutionOutput
Write-Host "--- Fin de Salida del Cliente Python ---" -ForegroundColor Magenta

# Restaurar la codificación original de la consola y limpiar la variable de entorno
[Console]::OutputEncoding = $OriginalConsoleEncoding
Remove-Item Env:\\PYTHONIOENCODING -ErrorAction SilentlyContinue

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: El cliente Python terminó con errores (código: $LASTEXITCODE)." -ForegroundColor Red
} else {
    Write-Host "Cliente Python GUI cerrado (código: $LASTEXITCODE)." -ForegroundColor Yellow
}

# 7. Detener servicios SOAP y limpiar jobs
Write-Host "Deteniendo servicios SOAP..." -ForegroundColor Yellow
Get-Job | Stop-Job
Get-Job | Remove-Job

Write-Host "=== SISTEMA FORESTAL - FINALIZADO ===" -ForegroundColor Green

Write-Host "Presiona Enter para finalizar el script..."
Read-Host
