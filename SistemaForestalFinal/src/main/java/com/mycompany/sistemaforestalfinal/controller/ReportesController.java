package com.mycompany.sistemaforestalfinal.controller;

import com.mycompany.sistemaforestalfinal.model.*;
import com.mycompany.sistemaforestalfinal.service.*;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.util.List;

@WebServlet(name = "ReportesController", urlPatterns = {"/reportes"})
public class ReportesController extends HttpServlet {

    private final TreeSpeciesService treeSpeciesService = new TreeSpeciesService();
    private final ZoneService zoneService = new ZoneService();
    private final ConservationActivitiesService activitiesService = new ConservationActivitiesService();
    private final EstadoConservacionService estadoService = new EstadoConservacionService();
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

        try {
            // Obtener todos los datos necesarios para los reportes
            List<TreeSpecies> especies = treeSpeciesService.getAllTreeSpecies();
            List<Zone> zonas = zoneService.getAllZones();
            List<ConservationActivities> actividades = activitiesService.getAllActivities();
            List<EstadoConservacion> estados = estadoService.getAllEstados();
            List<TipoActividad> tipos = tipoActividadService.getAllTiposActividad();

            // Asignar a atributos de request
            request.setAttribute("especies", especies);
            request.setAttribute("zonas", zonas);
            request.setAttribute("actividades", actividades);
            request.setAttribute("estados", estados);
            request.setAttribute("tipos", tipos);

            // Redirigir a la página de dashboard de reportes
            request.getRequestDispatcher("/reportes.jsp").forward(request, response);

        } catch (Exception e) {
            e.printStackTrace();
            request.setAttribute("error", "Error al cargar datos para el dashboard: " + e.getMessage());
        }
    }
}


