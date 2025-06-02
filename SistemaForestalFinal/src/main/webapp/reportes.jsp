<%@ include file="menudinamico.jsp" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dashboard de Reportes Forestales</title>
  
    <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.3/css/bootstrap.min.css" rel="stylesheet" />
   
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" />

    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
   
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>

    <style>
        body {
            background-color: #f8f9fa;
            font-family: 'Poppins', sans-serif;
            padding-top: 10px;
        }
        .page-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 0;
            margin-bottom: 30px;
            border-radius: 0.75rem;
            text-align: center;
        }
        .stats-card {
            border-radius: 0.75rem;
            color: white;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            margin-bottom: 20px;
        }
        .stats-card:hover {
            transform: translateY(-5px);
        }
        .stats-card .icon-large {
            font-size: 3rem;
            opacity: 0.8;
        }
        .stats-card.green { background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); }
        .stats-card.blue  { background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); }
        .stats-card.orange{ background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%); }
        .stats-card.red   { background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%); }

        .chart-container {
            background: white;
            border-radius: 0.75rem;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        .chart-container h5 {
            font-weight: 600;
            margin-bottom: 20px;
            color: #343a40;
        }
        h2.section-title {
            margin-top: 40px;
            margin-bottom: 20px;
            font-weight: 600;
            color: #343a40;
        }
        .table-responsive {
            margin-bottom: 30px;
        }
        table.table {
            background: white;
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        table.table th, table.table td {
            vertical-align: middle !important;
        }
    </style>
</head>
<body>
<div class="container-fluid">
    <!-- Header -->
    <div class="row">
        <div class="col-12">
            <div class="page-header">
                <h1><i class="fas fa-chart-line me-2"></i>Dashboard de Reportes Forestales</h1>
                <p class="lead">Visión general del sistema de conservación forestal</p>
            </div>
        </div>
    </div>

  
    <div class="row">
        <div class="col-lg-3 col-md-6">
            <div class="stats-card green">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h3 class="mb-0">${especies.size()}</h3>
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
                        <h3 class="mb-0">${zonas.size()}</h3>
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
                        <h3 class="mb-0">${actividades.size()}</h3>
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
                        <h3 class="mb-0">${tipos.size()}</h3>
                        <p class="mb-0">Tipos de Actividad</p>
                    </div>
                    <i class="fas fa-cogs icon-large"></i>
                </div>
            </div>
        </div>
    </div>

   
    <c:if test="${not empty error}">
        <div class="row">
            <div class="col-12">
                <div class="alert alert-danger mt-3">${error}</div>
            </div>
        </div>
    </c:if>

  
    <h2 class="section-title">Distribución de Especies y Actividades</h2>
    <div class="row">
      
        <div class="col-lg-6 col-md-12">
            <div class="chart-container">
                <h5><i class="fas fa-leaf me-2"></i>Especies por Estado de Conservación</h5>
                <canvas id="especiesEstadoChart"></canvas>
            </div>
        </div>
        <!-- Actividades por Tipo -->
        <div class="col-lg-6 col-md-12">
            <div class="chart-container">
                <h5><i class="fas fa-chart-pie me-2"></i>Actividades por Tipo</h5>
                <canvas id="actividadesTipoChart"></canvas>
            </div>
        </div>
    </div>

    <div class="row">
  
        <div class="col-lg-6 col-md-12">
            <div class="chart-container">
                <h5><i class="fas fa-map me-2"></i>Especies por Zona</h5>
                <canvas id="especiesZonaChart"></canvas>
            </div>
        </div>
       
        <div class="col-lg-6 col-md-12">
            <div class="chart-container">
                <h5><i class="fas fa-calendar-alt me-2"></i>Actividades por Mes</h5>
                <canvas id="actividadesMesChart"></canvas>
            </div>
        </div>
    </div>

 
    <h2 class="section-title">Datos Detallados</h2>

  
    <div class="row">
        <div class="col-12">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-light">
                        <tr>
                            <th>ID</th>
                            <th>Nombre Común</th>
                            <th>Nombre Científico</th>
                            <th>Estado de Conservación</th>
                            <th>Zona</th>
                        </tr>
                    </thead>
                    <tbody>
                        <c:forEach var="especie" items="${especies}">
                            <tr>
                                <td>${especie.id}</td>
                                <td>${especie.nombreComun}</td>
                                <td>${especie.nombreCientifico}</td>
                                <td>
                                    <c:forEach var="estado" items="${estados}">
                                        <c:if test="${estado.id == especie.estadoConservacionId}">
                                            ${estado.nombre}
                                        </c:if>
                                    </c:forEach>
                                </td>
                                <td>
                                    <c:forEach var="zona" items="${zonas}">
                                        <c:if test="${zona.id == especie.zonaId}">
                                            ${zona.nombre}
                                        </c:if>
                                    </c:forEach>
                                </td>
                            </tr>
                        </c:forEach>
                    </tbody>
                </table>
            </div>
        </div>
    </div>


    <div class="row">
        <div class="col-12">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-light">
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Tipo de Bosque</th>
                            <th>Área (ha)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <c:forEach var="zona" items="${zonas}">
                            <tr>
                                <td>${zona.id}</td>
                                <td>${zona.nombre}</td>
                                <td>${zona.tipoBosque}</td>
                                <td><fmt:formatNumber value="${zona.areaHa}" type="number" minFractionDigits="2" /></td>
                            </tr>
                        </c:forEach>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

   
    <div class="row">
        <div class="col-12">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-light">
                        <tr>
                            <th>ID</th>
                            <th>Nombre Actividad</th>
                            <th>Fecha</th>
                            <th>Responsable</th>
                            <th>Tipo de Actividad</th>
                            <th>Zona</th>
                        </tr>
                    </thead>
                    <tbody>
                        <c:forEach var="actividad" items="${actividades}">
                            <tr>
                                <td>${actividad.id}</td>
                                <td>${actividad.nombreActividad}</td>
                                <td>${actividad.fechaActividad}</td>
                                <td>${actividad.responsable}</td>
                                <td>
                                    <c:forEach var="tipo" items="${tipos}">
                                        <c:if test="${tipo.id == actividad.tipoActividadId}">
                                            ${tipo.nombre}
                                        </c:if>
                                    </c:forEach>
                                </td>
                                <td>
                                    <c:forEach var="zona" items="${zonas}">
                                        <c:if test="${zona.id == actividad.zonaId}">
                                            ${zona.nombre}
                                        </c:if>
                                    </c:forEach>
                                </td>
                            </tr>
                        </c:forEach>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>


<script src="https://code.jquery.com/jquery-3.7.1.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>

<script>
  
    const estados = [
        <c:forEach var="estado" items="${estados}" varStatus="st">
            { id: ${estado.id}, nombre: '${estado.nombre}' }<c:if test="${!st.last}">,</c:if>
        </c:forEach>
    ];
    const especies = [
        <c:forEach var="especie" items="${especies}" varStatus="st2">
            { estadoId: ${especie.estadoConservacionId} }<c:if test="${!st2.last}">,</c:if>
        </c:forEach>
    ];
    const dataEspeciesEstado = estados.map(e => ({
        estado: e.nombre,
        count: especies.filter(s => s.estadoId === e.id).length
    }));
    new Chart(document.getElementById('especiesEstadoChart'), {
        type: 'doughnut',
        data: {
            labels: dataEspeciesEstado.map(d => d.estado),
            datasets: [{
                data: dataEspeciesEstado.map(d => d.count),
                backgroundColor: ['#4CAF50', '#2196F3', '#FF9800', '#f44336', '#9C27B0', '#00BCD4'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });

  
    const tipos = [
        <c:forEach var="tipo" items="${tipos}" varStatus="st3">
            { id: ${tipo.id}, nombre: '${tipo.nombre}' }<c:if test="${!st3.last}">,</c:if>
        </c:forEach>
    ];
    const actividades = [
        <c:forEach var="actividad" items="${actividades}" varStatus="st4">
            { tipoId: ${actividad.tipoActividadId} }<c:if test="${!st4.last}">,</c:if>
        </c:forEach>
    ];
    const dataActividadesTipo = tipos.map(t => ({
        tipo: t.nombre,
        count: actividades.filter(a => a.tipoId === t.id).length
    }));
    new Chart(document.getElementById('actividadesTipoChart'), {
        type: 'pie',
        data: {
            labels: dataActividadesTipo.map(d => d.tipo),
            datasets: [{
                data: dataActividadesTipo.map(d => d.count),
                backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#17a2b8', '#6f42c1'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'right', labels: { font: { size: 14 } } }
            }
        }
    });

  
    const zonas = [
        <c:forEach var="zona" items="${zonas}" varStatus="st5">
            { id: ${zona.id}, nombre: '${zona.nombre}' }<c:if test="${!st5.last}">,</c:if>
        </c:forEach>
    ];
    const dataEspeciesZona = zonas.map(z => ({
        zona: z.nombre,
        count: especies.filter(s => s.zonaId === z.id).length
    }));
    new Chart(document.getElementById('especiesZonaChart'), {
        type: 'bar',
        data: {
            labels: dataEspeciesZona.map(d => d.zona),
            datasets: [{
                label: 'Cantidad de Especies',
                data: dataEspeciesZona.map(d => d.count),
                backgroundColor: '#28a745',
                borderColor: '#1e7e34',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, ticks: { stepSize: 1 } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

 
    const actividadesMes = [
        <c:forEach var="actividad" items="${actividades}" varStatus="st6">
            { fecha: '${actividad.fechaActividad}' }<c:if test="${!st6.last}">,</c:if>
        </c:forEach>
    ];
    const agrupadoMes = {};
    actividadesMes.forEach(a => {
        const dateObj = new Date(a.fecha);
        const mesAno = dateObj.toLocaleDateString('es-ES', { year: 'numeric', month: 'long' });
        agrupadoMes[mesAno] = (agrupadoMes[mesAno] || 0) + 1;
    });
    const mesesLabels = Object.keys(agrupadoMes).sort((a,b) => {
        const [ma, ya] = a.split(' ');
        const [mb, yb] = b.split(' ');
        const da = new Date(`${ma} 1, ${ya}`);
        const db = new Date(`${mb} 1, ${yb}`);
        return da - db;
    });
    const actividadesPorMesData = mesesLabels.map(m => agrupadoMes[m]);
    new Chart(document.getElementById('actividadesMesChart'), {
        type: 'line',
        data: {
            labels: mesesLabels,
            datasets: [{
                label: 'Actividades Realizadas',
                data: actividadesPorMesData,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#fff',
                pointBorderColor: '#667eea'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, ticks: { stepSize: 1 } }
            },
            plugins: {
                legend: { display: true, position: 'top' },
                title: {
                    display: true,
                    text: 'Evolución Mensual de Actividades'
                }
            }
        }
    });
</script>
</body>
</html>
