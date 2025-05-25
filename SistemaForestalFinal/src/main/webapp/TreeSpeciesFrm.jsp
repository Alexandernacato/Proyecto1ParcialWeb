<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<div class="modal-header">
    <h5 class="modal-title">
        <c:choose>
            <c:when test="${treeSpecies.id != 0}">Editar Especie</c:when>
            <c:otherwise>Nueva Especie</c:otherwise>
        </c:choose>
    </h5>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
</div>

<div class="modal-body">
    <c:if test="${not empty error}">
        <div class="alert alert-danger">${error}</div>
    </c:if>

    <form action="${pageContext.request.contextPath}/treespecies" method="post">
        <input type="hidden" name="id" value="${treeSpecies.id}" />

        <div class="mb-3">
            <label class="form-label">Nombre Común</label>
            <input type="text" name="nombreComun" class="form-control" value="${treeSpecies.nombreComun}" required />
        </div>

        <div class="mb-3">
            <label class="form-label">Nombre Científico</label>
            <input type="text" name="nombreCientifico" class="form-control" value="${treeSpecies.nombreCientifico}" />
        </div>

        <div class="mb-3">
            <label class="form-label">Zona</label>
            <select name="zonaId" class="form-select" required>
                <c:forEach var="zone" items="${zones}">
                    <option value="${zone.id}" ${zone.id == treeSpecies.zonaId ? "selected" : ""}>
                        ${zone.nombre}
                    </option>
                </c:forEach>
            </select>
        </div>

        <div class="mb-3">
  <label for="estadoConservacionId">Estado de Conservación:</label>
<select name="estadoConservacionId" id="estadoConservacionId" class="form-control">
    <c:forEach var="estado" items="${estados}">
        <option value="${estado.id}"
            <c:if test="${treeSpecies.estadoConservacionId == estado.id}">selected</c:if>>
            ${estado.nombre}
        </option>
    </c:forEach>
</select>
</div>

        <div class="form-check mb-3">
            <input class="form-check-input" type="checkbox" name="activo" id="activo" ${treeSpecies.activo ? "checked" : ""} />
            <label class="form-check-label" for="activo">Activo</label>
        </div>

        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="submit" class="btn btn-primary">Guardar</button>
        </div>
    </form>
</div>
