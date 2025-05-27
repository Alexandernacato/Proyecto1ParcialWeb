<%@ include file="menudinamico.jsp" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Lista de Zonas</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.3/css/bootstrap.min.css" rel="stylesheet" />
    <link href="https://cdn.datatables.net/2.3.0/css/dataTables.bootstrap5.css" rel="stylesheet" />
</head>
<body>
<div class="container mt-5">
    <h2 class="text-center mb-4">Lista de Zonas</h2>
<c:choose>
    <c:when test="${sessionScope.userRole eq 'admin'}">
        <!-- Admin puede abrir el modal -->
        <a href="${pageContext.request.contextPath}/zones?option=new" class="btn btn-primary mb-3" id="abrirModal">Agregar Nueva Zona</a>
    </c:when>
    <c:otherwise>
        <!-- Usuario normal recibe alerta -->
        <button type="button" class="btn btn-secondary mb-3" onclick="alert('Acceso denegado. Solo los administradores pueden agregar zonas.')">Agregar Nueva Zona</button>
    </c:otherwise>
</c:choose>

    <table id="zonesTable" class="table table-bordered table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Tipo Bosque</th>
                <th>Área (ha)</th>
                <th>Fecha Registro</th>
                <th>Activo</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            <c:forEach var="zone" items="${zonesList}">
                <tr>
                    <td><c:out value="${zone.id}" /></td>
                    <td><c:out value="${zone.nombre}" /></td>
                    <td><c:out value="${zone.tipoBosque}" /></td>
                    <td><fmt:formatNumber value="${zone.areaHa}" maxFractionDigits="2" /></td>
                    <td>
                        <c:choose>
                            <c:when test="${not empty zone.creadoEn}">
                                <fmt:formatDate value="${zone.creadoEn}" pattern="dd/MM/yyyy HH:mm:ss" />
                            </c:when>
                            <c:otherwise>No registrado</c:otherwise>
                        </c:choose>
                    </td>
                    <td><c:out value="${zone.activo ? 'Sí' : 'No'}" /></td>
                    <td>
                        <c:choose>
    <c:when test="${sessionScope.userRole eq 'admin'}">
        <a href="${pageContext.request.contextPath}/zones?option=update&id=${zone.id}" class="btn btn-warning btn-sm editarBtn">Editar</a>
    </c:when>
    <c:otherwise>
        <button type="button" class="btn btn-secondary btn-sm" onclick="alert('Acceso denegado. Solo los administradores pueden editar zonas.')">Editar</button>
    </c:otherwise>
</c:choose>
                        <c:choose>
    <c:when test="${sessionScope.userRole eq 'admin'}">
        <!-- Solo los administradores pueden eliminar -->
        <a href="${pageContext.request.contextPath}/zones?option=delete&id=${zone.id}" class="btn btn-danger btn-sm" onclick="return confirm('¿Está seguro de eliminar esta zona?')">Eliminar</a>
    </c:when>
    <c:otherwise>
        <!-- Los usuarios no administradores no tienen acceso a eliminar -->
        <button type="button" class="btn btn-danger btn-sm" onclick="alert('Acceso denegado. Solo los administradores pueden eliminar zonas.')">Eliminar</button>
    </c:otherwise>
</c:choose>
                    </td>
                </tr>
            </c:forEach>
        </tbody>
    </table>
</div>

<!-- Modal para formulario -->
<div class="modal fade" id="modalFormulario" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content" id="contenidoModal"></div>
    </div>
</div>

<!-- Scripts -->
<script src="https://code.jquery.com/jquery-3.7.1.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.datatables.net/2.3.0/js/dataTables.js"></script>
<script src="https://cdn.datatables.net/2.3.0/js/dataTables.bootstrap5.js"></script>

<script>
$(document).ready(function () {
    $('#zonesTable').DataTable();

    // Abrir modal para nueva zona
    $('#abrirModal').click(function (e) {
        e.preventDefault();
        const url = $(this).attr('href');
        $('#contenidoModal').load(url, function () {
            const modal = new bootstrap.Modal(document.getElementById('modalFormulario'));
            modal.show();
        });
    });

    // Abrir modal para editar zona (delegación para botones generados dinámicamente)
    $(document).on('click', 'a.editarBtn', function (e) {
        e.preventDefault();
        const url = $(this).attr('href');
        $('#contenidoModal').load(url, function () {
            const modal = new bootstrap.Modal(document.getElementById('modalFormulario'));
            modal.show();
        });
    });
});
</script>

</body>
</html>
