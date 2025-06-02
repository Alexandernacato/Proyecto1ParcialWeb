<%@ page import="com.mycompany.sistemaforestalfinal.model.Usuario" %>
<%
    Usuario usuario = (Usuario) session.getAttribute("usuario");
    String rol = (usuario != null) ? usuario.getRol() : "";
    String path = request.getServletPath();
%>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
<% if ("admin".equals(rol)) { %>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
    <div class="container">
        <a class="navbar-brand" href="${pageContext.request.contextPath}/indexadmin.jsp">
            <i class="fas fa-user-shield"></i> Admin Forestal
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarMain" aria-controls="navbarMain"
                aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarMain">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link <%= path.equals("/reportes") ? "active" : "" %>" href="${pageContext.request.contextPath}/reportes"><i class="fas fa-chart-line"></i> Reportes</a></li>
               
                <li class="nav-item"><a class="nav-link <%= path.equals("/conservationactivities") ? "active" : "" %>" href="${pageContext.request.contextPath}/conservationactivities"><i class="fas fa-leaf"></i> Actividades de Conservación</a></li>
                <li class="nav-item"><a class="nav-link <%= path.equals("/zones") ? "active" : "" %>" href="${pageContext.request.contextPath}/zones"><i class="fas fa-map"></i> Zonas</a></li>
                <li class="nav-item"><a class="nav-link <%= path.equals("/treespecies") ? "active" : "" %>" href="${pageContext.request.contextPath}/treespecies"><i class="fas fa-seedling"></i> Especies</a></li>
                <li class="nav-item"><a class="nav-link text-danger" href="${pageContext.request.contextPath}/logout"><i class="fas fa-sign-out-alt"></i> Cerrar Sesión</a></li>
            </ul>
        </div>
    </div>
</nav>

<% } else if ("usuario".equals(rol)) { %>
<link rel="stylesheet" href="css/menu.css">
<nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
    <div class="container">
        <a class="navbar-brand" href="${pageContext.request.contextPath}/Index.jsp">
            <i class="fas fa-tree"></i> Conservación Forestal
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                data-bs-target="#navbarMain" aria-controls="navbarMain" 
                aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarMain">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link <%= path.equals("/Index.jsp") ? "active" : "" %>" href="${pageContext.request.contextPath}/Index.jsp"><i class="fas fa-home"></i> Inicio</a></li>
                <li class="nav-item"><a class="nav-link <%= path.equals("/reportes") ? "active" : "" %>" href="${pageContext.request.contextPath}/reportes"><i class="fas fa-chart-column"></i> Dashboard</a></li>
                <li class="nav-item"><a class="nav-link <%= path.equals("/zones") ? "active" : "" %>" href="${pageContext.request.contextPath}/zones"><i class="fas fa-map-marked-alt"></i> Zonas</a></li>
                <li class="nav-item"><a class="nav-link <%= path.equals("/treespecies") ? "active" : "" %>" href="${pageContext.request.contextPath}/treespecies"><i class="fas fa-seedling"></i> Especies</a></li>
                <li class="nav-item"><a class="nav-link <%= path.equals("/conservationactivities") ? "active" : "" %>" href="${pageContext.request.contextPath}/conservationactivities"><i class="fas fa-book-open"></i> Actividades</a></li>
                <li class="nav-item"><a class="nav-link text-danger" href="${pageContext.request.contextPath}/logout"><i class="fas fa-sign-out-alt"></i> Cerrar Sesión</a></li>
            </ul>
        </div>
    </div>
</nav>
<% } %>
