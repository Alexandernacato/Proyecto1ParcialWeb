<%@ include file="menudinamico.jsp" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Lista de Actividades de Conservación</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.3/css/bootstrap.min.css" rel="stylesheet" />
    <link href="https://cdn.datatables.net/2.3.0/css/dataTables.bootstrap5.css" rel="stylesheet" />
</head>
<body>
<div class="container mt-5">
    <h2 class="text-center mb-4">Lista de Actividades de Conservación</h2>
<c:choose>
    <c:when test="${sessionScope.userRole eq 'admin'}">
        <!-- Solo el administrador puede abrir el modal para agregar actividad -->
        <a href="${pageContext.request.contextPath}/conservationactivities?option=new" class="btn btn-primary mb-3" id="abrirModal">Agregar Nueva Actividad</a>    
    </c:when>
    <c:otherwise>
        <!-- Usuarios no administradores reciben una alerta -->
        <button type="button" class="btn btn-secondary mb-3" onclick="alert('Acceso denegado. Solo los administradores pueden agregar actividades.')">Agregar Nueva Actividad</button>
    </c:otherwise>
</c:choose>

    <table id="activitiesTable" class="table table-bordered table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre Actividad</th>
                <th>Fecha Actividad</th>
                <th>Responsable</th>
                <th>Tipo Actividad</th>
                <th>Zona</th>
                <th>Activo</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            <c:forEach var="ca" items="${conservationActivitiesList}">
                <tr>
                    <td>${ca.id}</td>
                    <td>${ca.nombreActividad}</td>
                    <td>${ca.fechaActividad}</td>
                    <td>${ca.responsable}</td>
                    <td>
                        <c:forEach var="ta" items="${tiposActividad}">
                            <c:if test="${ta.id == ca.tipoActividadId}">
                                ${ta.nombre}
                            </c:if>
                        </c:forEach>
                    </td>
                    <td>
                        <c:forEach var="z" items="${zones}">
                            <c:if test="${z.id == ca.zonaId}">
                                ${z.nombre}
                            </c:if>
                        </c:forEach>
                    </td>
                    <td>${ca.activo ? "Sí" : "No"}</td>
                    <td>
                        <c:choose>
    <c:when test="${sessionScope.userRole eq 'admin'}">
        <!-- Solo los administradores pueden editar -->
        <a href="${pageContext.request.contextPath}/conservationactivities?option=update&id=${ca.id}" class="btn btn-warning btn-sm editarBtn">Editar</a>
    </c:when>
    <c:otherwise>
        <!-- Los usuarios no administradores no tienen acceso a editar -->
        <button type="button" class="btn btn-warning btn-sm" onclick="alert('Acceso denegado. Solo los administradores pueden editar actividades.')">Editar</button>
    </c:otherwise>
</c:choose>

                       <c:choose>
    <c:when test="${sessionScope.userRole eq 'admin'}">
        <!-- Solo los administradores pueden eliminar -->
        <a href="${pageContext.request.contextPath}/conservationactivities?option=delete&id=${ca.id}" class="btn btn-danger btn-sm" onclick="return confirm('¿Eliminar esta actividad de conservación?')">Eliminar</a>
    </c:when>
    <c:otherwise>
        <!-- Los usuarios no administradores no tienen acceso a eliminar -->
        <button type="button" class="btn btn-danger btn-sm" onclick="alert('Acceso denegado. Solo los administradores pueden eliminar actividades.')">Eliminar</button>
    </c:otherwise>
</c:choose>
                    </td>
                </tr>
            </c:forEach>
        </tbody>
    </table>
</div>

<!-- Modal -->
<div class="modal fade" id="modalFormulario" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content" id="contenidoModal"></div>
    </div>
</div>

<div class="modal fade" id="modalFormularioTipos" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content" id="TiposModal"></div>
    </div>
</div>

<!-- JS -->
<script src="https://code.jquery.com/jquery-3.7.1.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.datatables.net/2.3.0/js/dataTables.js"></script>
<script src="https://cdn.datatables.net/2.3.0/js/dataTables.bootstrap5.js"></script>
<script>
$(document).ready(function () {
    $('#activitiesTable').DataTable();

    $('#abrirModal').click(function (e) {
        e.preventDefault();
        $('#contenidoModal').load($(this).attr('href'), function () {
            new bootstrap.Modal(document.getElementById('modalFormulario')).show();
            
        });
    });
    $('#abrirModalTipos').click(function (e) {
        e.preventDefault();
        $('#TiposModal').load($(this).attr('href'), function () {
            new bootstrap.Modal(document.getElementById('modalFormularioTipos')).show();
            
        });
    });


    $(document).on('click', 'a.editarBtn', function (e) {
        e.preventDefault();
        $('#contenidoModal').load($(this).attr('href'), function () {
            new bootstrap.Modal(document.getElementById('modalFormulario')).show();
        });
    });
});
</script>
</body>
</html>