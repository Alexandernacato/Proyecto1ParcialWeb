<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<div class="modal-header">
    <h5 class="modal-title">
        Tipos de Actividades
    </h5>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
</div>

<div class="modal-body">
    <c:if test="${not empty error}">
        <div class="alert alert-danger">${error}</div>
    </c:if>

    <form action="${pageContext.request.contextPath}/tipoactividad" method="post">
        <input type="hidden" name="id" value="${tipoActividad.id}" />

        <div class="mb-3">
            <label class="form-label">Nombre del Tipo de Actividad</label>
            <input type="text" name="nombre" class="form-control" value="${tipoActividad.nombre}" required />
        </div>
        
        <div class="mb-3">
            <label class="form-label">Descripción</label>
            <input type="text" name="descripcion" class="form-control" value="${tipoActividad.descripcion}" required />
        </div>

        <div class="form-check mb-3">
            <input class="form-check-input" type="checkbox" name="activo" id="activo" ${tipoActividad.activo ? "checked" : ""} />
            <label class="form-check-label" for="activo">Activo</label>
        </div>

        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="submit" class="btn btn-primary">Guardar</button>
        </div>
    </form>
</div>

