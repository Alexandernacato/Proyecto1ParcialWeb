<%@ include file="menu.jsp" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Lista de Especies</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.3/css/bootstrap.min.css" rel="stylesheet" />
    <link href="https://cdn.datatables.net/2.3.0/css/dataTables.bootstrap5.css" rel="stylesheet" />
</head>
<body>
<div class="container mt-5">
    <h2 class="text-center mb-4">Lista de Especies de Árbol</h2>
    <a href="${pageContext.request.contextPath}/treespecies?option=new" class="btn btn-primary mb-3" id="abrirModal">Agregar Nueva Especie</a>

    <table id="speciesTable" class="table table-bordered table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre Común</th>
                <th>Nombre Científico</th>
                <th>Zona</th>
                <th>Estado Conservación</th>
                <th>Activo</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            
            <c:forEach var="sp" items="${treeSpeciesList}">
                <tr>
                    <td>${sp.id}</td>
                    <td>${sp.nombreComun}</td>
                    <td>${sp.nombreCientifico}</td>
                    <td>${sp.zonaId}</td> <!-- O cambiar por zonaNombre si lo agregas -->
                    <td>
                        <c:forEach var="ec" items="${estados}">
                            <c:if test="${ec.id == sp.estadoConservacionId}">
                                ${ec.nombre}
                            </c:if>
                        </c:forEach>
                    </td>
                    <td>${sp.activo ? "Sí" : "No"}</td>
                    <td>
                        <a href="${pageContext.request.contextPath}/treespecies?option=update&id=${sp.id}" class="btn btn-warning btn-sm editarBtn">Editar</a>
                        <a href="${pageContext.request.contextPath}/treespecies?option=delete&id=${sp.id}" class="btn btn-danger btn-sm" onclick="return confirm('¿Eliminar esta especie?')">Eliminar</a>
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

<!-- JS -->
<script src="https://code.jquery.com/jquery-3.7.1.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.datatables.net/2.3.0/js/dataTables.js"></script>
<script src="https://cdn.datatables.net/2.3.0/js/dataTables.bootstrap5.js"></script>
<script>
$(document).ready(function () {
    $('#speciesTable').DataTable();

    $('#abrirModal').click(function (e) {
        e.preventDefault();
        $('#contenidoModal').load($(this).attr('href'), function () {
            new bootstrap.Modal(document.getElementById('modalFormulario')).show();
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
