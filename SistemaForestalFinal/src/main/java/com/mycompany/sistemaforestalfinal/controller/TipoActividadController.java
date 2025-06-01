package com.mycompany.sistemaforestalfinal.controller;

import com.mycompany.sistemaforestalfinal.model.TipoActividad;
import com.mycompany.sistemaforestalfinal.model.Usuario;
import com.mycompany.sistemaforestalfinal.service.TipoActividadService;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.util.List;

@WebServlet(name = "ConservationActivitiesController", urlPatterns = {"/conservationactivities"})
public class TipoActividadController extends HttpServlet {

    private final TipoActividadService tipoActividadService = new TipoActividadService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
       
        HttpSession session = request.getSession(false);
        if (session == null) {
            response.sendRedirect("login.jsp");
            return;
        }
        Usuario usuario = (Usuario) session.getAttribute("usuario");
        if (usuario == null) {
            response.sendRedirect("login.jsp");
            return;
        }
        String rol = usuario.getRol();

        String option = request.getParameter("option");
        if (option == null) option = "list";

        // Bloquear operaciones CRUD a no admins
        if (option.equals("new") || option.equals("update") || option.equals("delete")) {
            if (!"admin".equals(rol)) {
                response.sendError(HttpServletResponse.SC_FORBIDDEN, "Acceso denegado.");
                return;
            }
        }

        try {
            switch (option) {
                case "new":
                    request.setAttribute("tiposActividad", new TipoActividad());
                    request.getRequestDispatcher("/TipoActividadFrm.jsp").forward(request, response);
                    break;

                case "update":
                    int id = Integer.parseInt(request.getParameter("id"));
                    TipoActividad ca = tipoActividadService.getTipoActividadById(id);
                    if (ca == null) {
                        request.setAttribute("error", "Tipo de Actividad no encontrada con id " + id);
                        request.getRequestDispatcher("/TipoActividadFrm.jsp").forward(request, response);
                        return;
                    }
                    request.setAttribute("tiposActividad", ca);
                    request.getRequestDispatcher("/TipoActividadFrm.jsp").forward(request, response);
                    break;

                case "delete":
                    int idDelete = Integer.parseInt(request.getParameter("id"));
                    tipoActividadService.deleteTipoActividad(idDelete);
                    response.sendRedirect(request.getContextPath() + "/conservationactivities");
                    break;

                default:
                    
                    List<TipoActividad> tiposActividad = tipoActividadService.getAllTiposActividad();
                   

                    request.setAttribute("tiposActividad", tiposActividad);
                    request.getRequestDispatcher("/TipoActividadFrm.jsp").forward(request, response);
                    break;
            }
        } catch (Exception e) {
            request.setAttribute("error", "Ocurrió un error: " + e.getMessage());
            request.getRequestDispatcher("/TipoActividadFrm.jsp").forward(request, response);
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String idParam = request.getParameter("id");
        String nombreTipoActividad = request.getParameter("nombreTipoActividad");
        String descripcionTipoActividad = request.getParameter("descripcionTipoActividad");

        TipoActividad tipoActividad = new TipoActividad();
        tipoActividad.setNombre(nombreTipoActividad);
        tipoActividad.setDescripcion(descripcionTipoActividad);

        tipoActividad.setActivo(request.getParameter("activo") != null); // Marca si está activo

        try {
            if (idParam == null || idParam.isEmpty() || "0".equals(idParam)) {
                tipoActividadService.createTipoActividad(tipoActividad);
            } else {
                tipoActividad.setId(Integer.parseInt(idParam));
                tipoActividadService.updateTipoActividad(tipoActividad);
            }
            response.sendRedirect(request.getContextPath() + "/tipoactividad");
        } catch (Exception e) {
            request.setAttribute("tipoactividad", tipoActividad);
            request.setAttribute("error", e.getMessage());
            request.getRequestDispatcher("/tipoActividadFrm.jsp").forward(request, response);
        }
    }
}