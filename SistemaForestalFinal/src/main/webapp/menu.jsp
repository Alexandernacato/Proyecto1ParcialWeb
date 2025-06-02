<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Conservación Forestal</title>

    
    <link rel="stylesheet" href="css/menu.css">


    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

   
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">


    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<nav class="navbar navbar-expand-lg fixed-top">
    <div class="container">
        <a class="navbar-brand" href="${pageContext.request.contextPath}/Index.jsp">
            <i class="fas fa-tree"></i>
            Conservación Forestal
        </a>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                data-bs-target="#navbarMain" aria-controls="navbarMain" 
                aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarMain">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link ${pageContext.request.servletPath eq '/Index.jsp' ? 'active' : ''}" 
                       href="${pageContext.request.contextPath}/Index.jsp">
                        <i class="fas fa-home"></i> Inicio
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="${pageContext.request.contextPath}/reportes">
                        <i class="fas fa-chart-column"></i> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link ${pageContext.request.servletPath eq '/zones' ? 'active' : ''}" 
                       href="${pageContext.request.contextPath}/zones">
                        <i class="fas fa-map-marked-alt"></i> Zonas
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link ${pageContext.request.servletPath eq '/treespecies' ? 'active' : ''}" 
                       href="${pageContext.request.contextPath}/treespecies">
                        <i class="fas fa-seedling"></i> Especies
                    </a>
                </li>               
                <li class="nav-item">
                    <a class="nav-link" href="${pageContext.request.contextPath}/ConservationActivities">
                        <i class="fas fa-book-open"></i> Actividades de Conservación
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>


<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
