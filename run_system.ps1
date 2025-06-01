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

# 6. Verificar Python e instalar dependencias
Write-Host "Verificando Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   Python encontrado: $pythonVersion" -ForegroundColor Green
    
    if (Test-Path "requirements.txt") {
        Write-Host "Instalando dependencias..." -ForegroundColor Cyan
        pip install -r requirements.txt --quiet 2>&1 | Out-Null
    }
} catch {
    Write-Host "ERROR con Python: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 7. Iniciar cliente GUI
$clientPath = ".\SistemaForestalFinal\src\main\java\com\mycompany\sistemaforestalfinal\service\client\client.py"

if (Test-Path $clientPath) {
    Write-Host "Iniciando cliente GUI..." -ForegroundColor Green
    Write-Host "El cliente mostrara errores en su propia ventana" -ForegroundColor Cyan
    Start-Process python -ArgumentList $clientPath -WindowStyle Normal
    
    Write-Host ""    Write-Host "=== SISTEMA INICIADO CORRECTAMENTE ===" -ForegroundColor Green
    Write-Host "Servicio Species: http://localhost:8282/TreeSpeciesCrudService?wsdl" -ForegroundColor Cyan
    Write-Host "Servicio Zones: http://localhost:8081/SistemaForestalFinal/ZoneCrudService?wsdl" -ForegroundColor Cyan
    Write-Host "Cliente GUI: Ejecutandose en ventana separada" -ForegroundColor Cyan
    Write-Host "Log de errores: client_debug.log" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Para detener los servidores:" -ForegroundColor Yellow
    Write-Host "   Get-Job | Stop-Job; Get-Job | Remove-Job" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Presiona cualquier tecla para salir (los servidores seguiran ejecutandose)..." -ForegroundColor White
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
} else {
    Write-Host "ERROR: Cliente no encontrado en: $clientPath" -ForegroundColor Red
    Write-Host "Deteniendo servidores..." -ForegroundColor Yellow
    Get-Job | Stop-Job; Get-Job | Remove-Job
}
