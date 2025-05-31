<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<div class="modal-header">
    <h5 class="modal-title">
        <c:choose>
            <c:when test="${conservationActivity.id != 0}">Editar Actividad de Conservación</c:when>
            <c:otherwise>Nueva Actividad de Conservación</c:otherwise>
        </c:choose>
    </h5>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
</div>

<div class="modal-body">
    <c:if test="${not empty error}">
        <div class="alert alert-danger">${error}</div>
    </c:if>

    <form action="${pageContext.request.contextPath}/conservationactivities" method="post">
        <input type="hidden" name="id" value="${conservationActivity.id}" />

        <div class="mb-3">
            <label class="form-label">Nombre de la Actividad</label>
            <input type="text" name="nombreActividad" class="form-control" value="${conservationActivity.nombreActividad}" required />
        </div>

        <div class="mb-3">
            <label class="form-label">Fecha de la Actividad</label>
            <input type="date" name="fechaActividad" class="form-control" value="${conservationActivity.fechaActividad}" required />
        </div>

        <div class="mb-3">
            <label class="form-label">Responsable</label>
            <input type="text" name="responsable" class="form-control" value="${conservationActivity.responsable}" required />
        </div>

        <div class="mb-3">
            <label class="form-label">Tipo de Actividad</label>
            <select name="tipoActividadId" class="form-select" required>
                <option value="">Seleccione un tipo de actividad</option>
                <c:forEach var="tipoActividad" items="${tiposActividad}">
                    <option value="${tipoActividad.id}" ${tipoActividad.id == conservationActivity.tipoActividadId ? "selected" : ""}>
                        ${tipoActividad.nombre}
                    </option>
                </c:forEach>
            </select>
        </div>

        <div class="mb-3">
            <label class="form-label">Zona</label>
            <select name="zonaId" class="form-select" required>
                <option value="">Seleccione una zona</option>
                <c:forEach var="zone" items="${zones}">
                    <option value="${zone.id}" ${zone.id == conservationActivity.zonaId ? "selected" : ""}>
                        ${zone.nombre}
                    </option>
                </c:forEach>
            </select>
        </div>

        <div class="form-check mb-3">
            <input class="form-check-input" type="checkbox" name="activo" id="activo" ${conservationActivity.activo ? "checked" : ""} />
            <label class="form-check-label" for="activo">Activo</label>
        </div>

        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="submit" class="btn btn-primary">Guardar</button>
        </div>
    </form>
</div>