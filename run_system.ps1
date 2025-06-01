# 🌳 Sistema Forestal SOAP - Launcher Final
# Este script inicia el servidor SOAP y el cliente GUI automaticamente

Write-Host "🌳 === SISTEMA FORESTAL - INICIANDO ===" -ForegroundColor Green

# 1. Verificar que no haya procesos Java anteriores
Write-Host "⏹️  Deteniendo procesos Java anteriores..." -ForegroundColor Yellow
Get-Process -Name "java" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Ir al directorio del proyecto
Set-Location ".\SistemaForestalFinal"

# 3. Compilar si es necesario
if (-not (Test-Path "target\classes")) {
    Write-Host "🔧 Compilando proyecto..." -ForegroundColor Cyan
    mvn clean compile -q
}

# 4. Iniciar servidor SOAP en background
Write-Host "🚀 Iniciando servidor SOAP en puerto 8282..." -ForegroundColor Cyan
$serverJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    mvn exec:java
}

# 5. Esperar a que el servidor esté disponible
Write-Host "⏳ Esperando a que el servidor esté listo..." -ForegroundColor Yellow
$maxWait = 60
$waited = 0

do {
    Start-Sleep -Seconds 2
    $waited += 2
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8282/TreeSpeciesCrudService?wsdl" -TimeoutSec 3 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Servidor SOAP disponible!" -ForegroundColor Green
            break
        }
    } catch {
        if ($waited % 10 -eq 0) {
            Write-Host "   Esperando... ($waited/$maxWait segundos)" -ForegroundColor Yellow
        }
    }
    
} while ($waited -lt $maxWait)

# Volver al directorio principal
Set-Location ".."

# 6. Verificar Python e instalar dependencias
Write-Host "🐍 Verificando Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   Python encontrado: $pythonVersion" -ForegroundColor Green
    
    if (Test-Path "requirements.txt") {
        Write-Host "📦 Instalando dependencias..." -ForegroundColor Cyan
        pip install -r requirements.txt --quiet 2>&1 | Out-Null
    }
} catch {
    Write-Host "❌ Error con Python: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 7. Iniciar cliente GUI
$clientPath = ".\SistemaForestalFinal\src\main\java\com\mycompany\sistemaforestalfinal\service\client\client.py"

if (Test-Path $clientPath) {
    Write-Host "🖥️  Iniciando cliente GUI simplificado..." -ForegroundColor Green
    Write-Host "📋 El cliente mostrará errores en su propia ventana" -ForegroundColor Cyan
    Start-Process python -ArgumentList $clientPath -WindowStyle Normal
    
    Write-Host ""
    Write-Host "🎉 === SISTEMA INICIADO CORRECTAMENTE ===" -ForegroundColor Green
    Write-Host "🌐 Servidor SOAP: http://localhost:8282/TreeSpeciesCrudService?wsdl" -ForegroundColor Cyan
    Write-Host "🖥️  Cliente GUI: Ejecutándose en ventana separada" -ForegroundColor Cyan
    Write-Host "📊 Log de errores: client_debug.log" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Para detener el servidor:" -ForegroundColor Yellow
    Write-Host "   Get-Job | Stop-Job; Get-Job | Remove-Job" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Presiona cualquier tecla para salir (el servidor seguirá ejecutándose)..." -ForegroundColor White
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
} else {
    Write-Host "❌ Cliente no encontrado en: $clientPath" -ForegroundColor Red
    Write-Host "🛑 Deteniendo servidor..." -ForegroundColor Yellow
    Get-Job | Stop-Job; Get-Job | Remove-Job
}
