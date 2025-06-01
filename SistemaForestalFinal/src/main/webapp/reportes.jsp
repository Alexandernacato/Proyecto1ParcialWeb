<%@ include file="menudinamico.jsp" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dashboard de Reportes Forestales</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.3/css/bootstrap.min.css" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" />
    <style>
        .stats-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .stats-card:hover {
            transform: translateY(-5px);
        }
        .stats-card.green {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        }
        .stats-card.orange {
            background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
        }
        .stats-card.red {
            background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        }
        .stats-card.blue {
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        }
        .chart-container {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        .page-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 0;
            margin-bottom: 30px;
            border-radius: 15px;
        }
        .icon-large {
            font-size: 3rem;
            opacity: 0.8;
        }
        body {
            background-color: #f8f9fa;
        }
    </style>
</head>
<body>
<div class="container-fluid mt-4">
    <!-- Header -->
    <div class="page-header text-center">
        <h1><i class="fas fa-chart-line me-3"></i>Dashboard de Reportes Forestales</h1>
        <p class="lead">Análisis completo del sistema de conservación forestal</p>
    </div>

    <!-- Cards de Estadísticas -->
    <div class="row mb-4">
        <div class="col-lg-3 col-md-6">
            <div class="stats-card green">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h3 class="mb-0" id="totalEspecies">${especies.size()}</h3>
                        <p class="mb-0">Especies Registradas</p>
                    </div>
                    <i class="fas fa-tree icon-large"></i>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6">
            <div class="stats-card blue">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h3 class="mb-0" id="totalZonas">${zonas.size()}</h3>
                        <p class="mb-0">Zonas de Conservación</p>
                    </div>
                    <i class="fas fa-map-marked-alt icon-large"></i>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6">
            <div class="stats-card orange">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h3 class="mb-0" id="totalActividades">${actividades.size()}</h3>
                        <p class="mb-0">Actividades Realizadas</p>
                    </div>
                    <i class="fas fa-tasks icon-large"></i>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6">
            <div class="stats-card red">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h3 class="mb-0" id="totalTipos">${tipos.size()}</h3>
                        <p class="mb-0">Tipos de Actividad</p>
                    </div>
                    <i class="fas fa-cogs icon-large"></i>
                </div>
            </div>
        </div>
    </div>

    <!-- Gráficos -->
    <div class="row">
        <!-- Gráfico de Especies por Estado -->
        <div class="col-lg-6">
            <div class="chart-container">
                <h4 class="text-center mb-4"><i class="fas fa-leaf me-2"></i>Especies por Estado de Conservación</h4>
                <canvas id="especiesEstadoChart" width="400" height="300"></canvas>
            </div>
        </div>

        <!-- Gráfico de Actividades por Tipo -->
        <div class="col-lg-6">
            <div class="chart-container">
                <h4 class="text-center mb-4"><i class="fas fa-chart-pie me-2"></i>Distribución de Actividades por Tipo</h4>
                <canvas id="actividadesTipoChart" width="400" height="300"></canvas>
            </div>
        </div>
    </div>

    <div class="row">
        <!-- Gráfico de Especies por Zona -->
        <div class="col-lg-8">
            <div class="chart-container">
                <h4 class="text-center mb-4"><i class="fas fa-map me-2"></i>Especies por Zona de Conservación</h4>
                <canvas id="especiesZonaChart" width="400" height="200"></canvas>
            </div>
        </div>

        <!-- Actividades Activas vs Inactivas -->
        <div class="col-lg-4">
            <div class="chart-container">
                <h4 class="text-center mb-4"><i class="fas fa-toggle-on me-2"></i>Estado de Actividades</h4>
                <canvas id="actividadesActivasChart" width="400" height="300"></canvas>
            </div>
        </div>
    </div>

    <!-- Timeline de Actividades Recientes -->
    <div class="row">
        <div class="col-12">
            <div class="chart-container">
                <h4 class="text-center mb-4"><i class="fas fa-calendar-alt me-2"></i>Actividades por Mes</h4>
                <canvas id="actividadesMesChart" width="400" height="150"></canvas>
            </div>
        </div>
    </div>
</div>

<!-- Scripts -->
<script src="https://code.jquery.com/jquery-3.7.1.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>

<script>
$(document).ready(function() {
    // Datos desde el servidor
    const especies = [
        <c:forEach var="especie" items="${especies}" varStatus="status">
            {
                id: ${especie.id},
                nombre: "${especie.nombre}",
                estadoId: ${especie.estadoConservacionId},
                zonaId: ${especie.zonaId}
            }<c:if test="${!status.last}">,</c:if>
        </c:forEach>
    ];

    const estados = [
        <c:forEach var="estado" items="${estados}" varStatus="status">
            {
                id: ${estado.id},
                nombre: "${estado.nombre}"
            }<c:if test="${!status.last}">,</c:if>
        </c:forEach>
    ];

    const zonas = [
        <c:forEach var="zona" items="${zonas}" varStatus="status">
            {
                id: ${zona.id},
                nombre: "${zona.nombre}"
            }<c:if test="${!status.last}">,</c:if>
        </c:forEach>
    ];

    const actividades = [
        <c:forEach var="actividad" items="${actividades}" varStatus="status">
            {
                id: ${actividad.id},
                nombre: "${actividad.nombreActividad}",
                tipoId: ${actividad.tipoActividadId},
                activo: ${actividad.activo},
                fecha: "${actividad.fechaActividad}"
            }<c:if test="${!status.last}">,</c:if>
        </c:forEach>
    ];

    const tipos = [
        <c:forEach var="tipo" items="${tipos}" varStatus="status">
            {
                id: ${tipo.id},
                nombre: "${tipo.nombre}"
            }<c:if test="${!status.last}">,</c:if>
        </c:forEach>
    ];

    // Gráfico: Especies por Estado de Conservación
    const especiesEstadoData = estados.map(estado => ({
        estado: estado.nombre,
        count: especies.filter(especie => especie.estadoId === estado.id).length
    }));

    new Chart(document.getElementById('especiesEstadoChart'), {
        type: 'doughnut',
        data: {
            labels: especiesEstadoData.map(item => item.estado),
            datasets: [{
                data: especiesEstadoData.map(item => item.count),
                backgroundColor: [
                    '#4CAF50', '#2196F3', '#FF9800', '#f44336', '#9C27B0', '#00BCD4'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Gráfico: Actividades por Tipo
    const actividadesTipoData = tipos.map(tipo => ({
        tipo: tipo.nombre,
        count: actividades.filter(actividad => actividad.tipoId === tipo.id).length
    }));

    new Chart(document.getElementById('actividadesTipoChart'), {
        type: 'pie',
        data: {
            labels: actividadesTipoData.map(item => item.tipo),
            datasets: [{
                data: actividadesTipoData.map(item => item.count),
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Gráfico: Especies por Zona
    const especiesZonaData = zonas.map(zona => ({
        zona: zona.nombre,
        count: especies.filter(especie => especie.zonaId === zona.id).length
    }));

    new Chart(document.getElementById('especiesZonaChart'), {
        type: 'bar',
        data: {
            labels: especiesZonaData.map(item => item.zona),
            datasets: [{
                label: 'Número de Especies',
                data: especiesZonaData.map(item => item.count),
                backgroundColor: 'rgba(54, 162, 235, 0.8)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });

    // Gráfico: Actividades Activas vs Inactivas
    const actividadesActivas = actividades.filter(a => a.activo).length;
    const actividadesInactivas = actividades.filter(a => !a.activo).length;

    new Chart(document.getElementById('actividadesActivasChart'), {
        type: 'doughnut',
        data: {
            labels: ['Activas', 'Inactivas'],
            datasets: [{
                data: [actividadesActivas, actividadesInactivas],
                backgroundColor: ['#4CAF50', '#f44336'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Gráfico: Actividades por Mes
    const actividadesPorMes = {};
    actividades.forEach(actividad => {
        const fecha = new Date(actividad.fecha);
        const mesAno = fecha.toLocaleDateString('es-ES', { year: 'numeric', month: 'long' });
        actividadesPorMes[mesAno] = (actividadesPorMes[mesAno] || 0) + 1;
    });

    const meses = Object.keys(actividadesPorMes).sort();
    const cantidades = meses.map(mes => actividadesPorMes[mes]);

    new Chart(document.getElementById('actividadesMesChart'), {
        type: 'line',
        data: {
            labels: meses,
            datasets: [{
                label: 'Actividades Realizadas',
                data: cantidades,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
});
</script>
</body>
</html>