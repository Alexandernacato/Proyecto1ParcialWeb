<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<div class="modal-header">
    <h5 class="modal-title">
        <c:choose>
            <c:when test="${zone.id != 0}">
                Editar Zona
            </c:when>
            <c:otherwise>
                Nueva Zona
            </c:otherwise>
        </c:choose>
    </h5>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
</div>

<div class="modal-body">
    <c:if test="${not empty error}">
        <div class="alert alert-danger">${error}</div>
    </c:if>

    <form action="${pageContext.request.contextPath}/zones" method="post" id="zoneForm">
        <input type="hidden" name="id" value="${zone.id}" />

        <div class="mb-3">
            <label for="nombre" class="form-label">Nombre</label>
            <input type="text" name="nombre" id="nombre" class="form-control" value="${zone.nombre}" required />
        </div>

  <div class="mb-3">
    <label for="tipoBosque" class="form-label">Tipo Bosque</label>
   <select name="tipoBosque" id="tipoBosque" required>
    <c:forEach var="tipo" items="${tiposBosque}">
        <option value="${tipo.displayName}" 
            ${tipo.displayName == zone.tipoBosque ? "selected" : ""}>
            ${tipo.displayName}
        </option>
    </c:forEach>
</select>
</div>

        <div class="mb-3">
            <label for="areaHa" class="form-label">Área (ha)</label>
            <input type="number" step="0.01" name="areaHa" id="areaHa" class="form-control" 
                   value="${zone.areaHa}" min="0" />
        </div>

        <div class="form-check mb-3">
            <input type="checkbox" name="activo" id="activo" class="form-check-input" 
                   <c:if test="${zone.activo}">checked</c:if> />
            <label for="activo" class="form-check-label">Activo</label>
        </div>

        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="submit" class="btn btn-primary">Guardar</button>
        </div>
    </form>
</div>
