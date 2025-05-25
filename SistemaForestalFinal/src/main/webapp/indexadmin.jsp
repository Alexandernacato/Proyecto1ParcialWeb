<%@ page contentType="text/html;charset=UTF-8" language="java" %>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel de Administración</title>

    <!-- Estilos propios -->
    <link rel="stylesheet" href="css/indexadmin.css">

    <!-- Iconos y Frameworks -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<!-- NAVBAR -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
    <div class="container">
        <a class="navbar-brand" href="${pageContext.request.contextPath}/AdminIndex.jsp">
            <i class="fas fa-user-shield"></i> Admin Forestal
        </a>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarMain" aria-controls="navbarMain"
                aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarMain">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link" href="${pageContext.request.contextPath}/reportes"><i class="fas fa-chart-line"></i> Reportes</a></li>
                <li class="nav-item"><a class="nav-link" href="${pageContext.request.contextPath}/usuarios"><i class="fas fa-users-cog"></i> Usuarios</a></li>
                <li class="nav-item"><a class="nav-link" href="${pageContext.request.contextPath}/actividades"><i class="fas fa-leaf"></i> Actividades</a></li>
                <li class="nav-item"><a class="nav-link" href="${pageContext.request.contextPath}/zonas"><i class="fas fa-map"></i> Zonas</a></li>
                <li class="nav-item"><a class="nav-link" href="${pageContext.request.contextPath}/especies"><i class="fas fa-seedling"></i> Especies</a></li>
                <li class="nav-item"><a class="nav-link text-danger" href="${pageContext.request.contextPath}/logout"><i class="fas fa-sign-out-alt"></i> Cerrar Sesión</a></li>
            </ul>
        </div>
    </div>
</nav>

<!-- DASHBOARD -->
<main class="admin-dashboard container mt-5">
    <h1 class="mb-4 text-center"><i class="fas fa-tachometer-alt"></i> Panel de Administración</h1>

    <div class="row g-4 mb-5">
        <!-- Tarjeta 1 -->
        <div class="col-md-4">
            <div class="card dash-card bg-primary text-white shadow">
                <div class="card-body">
                    <h5 class="card-title"><i class="fas fa-chart-pie"></i> Reportes</h5>
                    <p class="card-text">Estadísticas detalladas de conservación, reforestación y más.</p>
                    <a href="${pageContext.request.contextPath}/reportes" class="btn btn-light">Ver más</a>
                </div>
            </div>
        </div>
        <!-- Tarjeta 2 -->
        <div class="col-md-4">
            <div class="card dash-card bg-success text-white shadow">
                <div class="card-body">
                    <h5 class="card-title"><i class="fas fa-users-cog"></i> Gestión de Usuarios</h5>
                    <p class="card-text">Permisos, roles y perfiles del sistema.</p>
                    <a href="${pageContext.request.contextPath}/usuarios" class="btn btn-light">Administrar</a>
                </div>
            </div>
        </div>
        <!-- Tarjeta 3 -->
        <div class="col-md-4">
            <div class="card dash-card bg-warning text-dark shadow">
                <div class="card-body">
                    <h5 class="card-title"><i class="fas fa-tasks"></i> Actividades</h5>
                    <p class="card-text">Control de campañas de conservación y plantaciones.</p>
                    <a href="${pageContext.request.contextPath}/actividades" class="btn btn-dark">Ver Actividades</a>
                </div>
            </div>
        </div>
    </div>

    <!-- Segunda fila -->
    <div class="row g-4">
        <!-- Zonas -->
        <div class="col-md-6">
            <div class="card dash-card bg-info text-white shadow">
                <div class="card-body">
                    <h5 class="card-title"><i class="fas fa-map-marked-alt"></i> Zonas</h5>
                    <p class="card-text">Mapa y gestión de zonas geográficas de conservación.</p>
                    <a href="${pageContext.request.contextPath}/zonas" class="btn btn-light">Ver Zonas</a>
                </div>
            </div>
        </div>

        <!-- Especies -->
        <div class="col-md-6">
            <div class="card dash-card bg-secondary text-white shadow">
                <div class="card-body">
                    <h5 class="card-title"><i class="fas fa-seedling"></i> Especies Forestales</h5>
                    <p class="card-text">Listado y control de especies en los ecosistemas.</p>
                    <a href="${pageContext.request.contextPath}/especies" class="btn btn-light">Ver Especies</a>
                </div>
            </div>
        </div>
    </div>
</main>
<footer class="admin-footer bg-dark text-light pt-5 pb-4">
    <div class="container">
        <div class="row">

            <!-- Misión -->
            <div class="col-md-4 mb-4">
                <h5 class="footer-title">Nuestra Misión</h5>
                <p>
                    Proteger y conservar los ecosistemas forestales para garantizar un futuro sostenible,
                    promoviendo la investigación, educación y la acción comunitaria.
                </p>
            </div>

            <!-- Enlaces Útiles -->
            <div class="col-md-3 mb-4">
                <h5 class="footer-title">Enlaces Rápidos</h5>
                <ul class="footer-links list-unstyled">
                    <li><a href="${pageContext.request.contextPath}/reportes">Dashboard</a></li>
                    <li><a href="${pageContext.request.contextPath}/usuarios">Gestión de Usuarios</a></li>
                    <li><a href="${pageContext.request.contextPath}/actividades">Proyectos</a></li>
                    <li><a href="${pageContext.request.contextPath}/zonas">Zonas</a></li>
                    <li><a href="${pageContext.request.contextPath}/especies">Especies</a></li>
                </ul>
            </div>

            <!-- Contacto -->
            <div class="col-md-5 mb-4">
                <h5 class="footer-title">Contacto</h5>
                <p><i class="fas fa-map-marker-alt"></i> Avenida Bosque Verde 123, Quito, Ecuador</p>
                <p><i class="fas fa-phone"></i> +593 2 555 1234</p>
                <p><i class="fas fa-envelope"></i> contacto@conservacionforestal.ec</p>
                <div class="social-icons mt-3">
                    <a href="#" aria-label="Facebook" class="social-link"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" aria-label="Twitter" class="social-link"><i class="fab fa-twitter"></i></a>
                    <a href="#" aria-label="Instagram" class="social-link"><i class="fab fa-instagram"></i></a>
                    <a href="#" aria-label="LinkedIn" class="social-link"><i class="fab fa-linkedin-in"></i></a>
                </div>
            </div>
        </div>

        <hr class="footer-divider">

        <div class="text-center small">
            &copy; 2025 Conservación Forestal. Todos los derechos reservados. | Diseñado por Equipo Conservación Forestal
        </div>
    </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
