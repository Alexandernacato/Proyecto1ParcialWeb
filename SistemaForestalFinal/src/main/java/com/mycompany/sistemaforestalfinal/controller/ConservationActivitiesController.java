package com.mycompany.sistemaforestalfinal.controller;

import com.mycompany.sistemaforestalfinal.model.ConservationActivities;
import com.mycompany.sistemaforestalfinal.model.TipoActividad;
import com.mycompany.sistemaforestalfinal.model.Usuario;
import com.mycompany.sistemaforestalfinal.model.Zone;
import com.mycompany.sistemaforestalfinal.service.ConservationActivitiesService;
import com.mycompany.sistemaforestalfinal.service.TipoActividadService;
import com.mycompany.sistemaforestalfinal.service.ZoneService;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.util.List;

@WebServlet(name = "ConservationActivitiesController", urlPatterns = {"/conservationactivities"})
public class ConservationActivitiesController extends HttpServlet {

    private final ConservationActivitiesService conservationActivitiesService = new ConservationActivitiesService();
    private final ZoneService zoneService = new ZoneService();
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
                    request.setAttribute("conservationActivity", new ConservationActivities());
                    request.setAttribute("zones", zoneService.getAllZones()); 
                    request.setAttribute("tiposActividad", tipoActividadService.getAllTiposActividad());
                    request.getRequestDispatcher("/ConservationActivitiesFrm.jsp").forward(request, response);
                    break;

                case "update":
                    int id = Integer.parseInt(request.getParameter("id"));
                    ConservationActivities ca = conservationActivitiesService.getActivityById(id);
                    if (ca == null) {
                        request.setAttribute("error", "Actividad de conservación no encontrada con id " + id);
                        request.getRequestDispatcher("/ConservationActivities.jsp").forward(request, response);
                        return;
                    }
                    request.setAttribute("conservationActivity", ca);
                    request.setAttribute("zones", zoneService.getAllZones()); 
                    request.setAttribute("tiposActividad", tipoActividadService.getAllTiposActividad());
                    request.getRequestDispatcher("/ConservationActivitiesFrm.jsp").forward(request, response);
                    break;

                case "delete":
                    int idDelete = Integer.parseInt(request.getParameter("id"));
                    conservationActivitiesService.deleteActivity(idDelete);
                    response.sendRedirect(request.getContextPath() + "/conservationactivities");
                    break;

                default:
                    List<ConservationActivities> lista = conservationActivitiesService.getAllActivities();

                    List<TipoActividad> tiposActividad = tipoActividadService.getAllTiposActividad();
                    System.out.println("📋 TIPOS DE ACTIVIDAD CARGADOS:");
                    for (TipoActividad ta : tiposActividad) {
                        System.out.println("ID: " + ta.getId() + " - Nombre: " + ta.getNombre());
                    }

                    List<Zone> zones = zoneService.getAllZones();
                    System.out.println("📋 ZONAS CARGADAS:");
                    for (Zone z : zones) {
                        System.out.println("ID: " + z.getId() + " - Nombre: " + z.getNombre());
                    }

                    request.setAttribute("conservationActivitiesList", lista);
                    request.setAttribute("tiposActividad", tiposActividad);
                    request.setAttribute("zones", zones);
                    request.getRequestDispatcher("/ConservationActivities.jsp").forward(request, response);
                    break;
            }
        } catch (Exception e) {
            request.setAttribute("error", "Ocurrió un error: " + e.getMessage());
            request.getRequestDispatcher("/ConservationActivities.jsp").forward(request, response);
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String idParam = request.getParameter("id");
        String nombreActividad = request.getParameter("nombreActividad");
        String fechaActividad = request.getParameter("fechaActividad");
        String responsable = request.getParameter("responsable");
        String tipoActividadIdParam = request.getParameter("tipoActividadId");
        String zonaIdParam = request.getParameter("zonaId");

        ConservationActivities conservationActivity = new ConservationActivities();
        conservationActivity.setNombreActividad(nombreActividad);
        conservationActivity.setFechaActividad(fechaActividad);
        conservationActivity.setResponsable(responsable);

        if (tipoActividadIdParam != null && !tipoActividadIdParam.isEmpty()) {
            conservationActivity.setTipoActividadId(Integer.parseInt(tipoActividadIdParam));
        }

        if (zonaIdParam != null && !zonaIdParam.isEmpty()) {
            conservationActivity.setZonaId(Integer.parseInt(zonaIdParam));
        }

        conservationActivity.setActivo(request.getParameter("activo") != null); // Marca si está activo

        try {
            if (idParam == null || idParam.isEmpty() || "0".equals(idParam)) {
                conservationActivitiesService.createActivity(conservationActivity);
            } else {
                conservationActivity.setId(Integer.parseInt(idParam));
                conservationActivitiesService.updateActivity(conservationActivity);
            }
            response.sendRedirect(request.getContextPath() + "/conservationactivities");
        } catch (Exception e) {
            request.setAttribute("conservationActivity", conservationActivity);
            request.setAttribute("error", e.getMessage());
            request.setAttribute("tiposActividad", tipoActividadService.getAllTiposActividad());
            request.setAttribute("zones", zoneService.getAllZones());
            request.getRequestDispatcher("/ConservationActivitiesFrm.jsp").forward(request, response);
        }
    }
}