package com.mycompany.sistemaforestalfinal.controller;

import com.mycompany.sistemaforestalfinal.model.EstadoConservacion;
import com.mycompany.sistemaforestalfinal.model.TreeSpecies;
import com.mycompany.sistemaforestalfinal.model.Usuario;
import com.mycompany.sistemaforestalfinal.model.Zone;
import com.mycompany.sistemaforestalfinal.service.EstadoConservacionService;
import com.mycompany.sistemaforestalfinal.service.TreeSpeciesService;
import com.mycompany.sistemaforestalfinal.service.ZoneService;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.util.List;

@WebServlet(name = "TreeSpeciesController", urlPatterns = {"/treespecies"})
public class TreeSpeciesController extends HttpServlet {

    private final TreeSpeciesService treeSpeciesService = new TreeSpeciesService();
    private final ZoneService zoneService = new ZoneService();
    EstadoConservacionService estadoService = new EstadoConservacionService();

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
        
        
        
        
        
        
        
        if (option == null) option = "list";

        try {
            switch (option) {
                case "new":
                    request.setAttribute("treeSpecies", new TreeSpecies());
                    request.setAttribute("zones", zoneService.getAllZones()); 
                    request.setAttribute("estados", estadoService.getAllEstados());
request.setAttribute("estados", estadoService.getAllEstados());// ✅ CAMBIO
                    request.getRequestDispatcher("/TreeSpeciesFrm.jsp").forward(request, response);
                    break;

                case "update":
                    int id = Integer.parseInt(request.getParameter("id"));
                    TreeSpecies ts = treeSpeciesService.getTreeSpeciesById(id);
                    if (ts == null) {
                        request.setAttribute("error", "Especie no encontrada con id " + id);
                        request.getRequestDispatcher("/TreeSpecies.jsp").forward(request, response);
                        return;
                    }
                    request.setAttribute("treeSpecies", ts);
                    request.setAttribute("zones", zoneService.getAllZones()); 
request.setAttribute("estados", estadoService.getAllEstados());// ✅ CAMBIO
                    request.getRequestDispatcher("/TreeSpeciesFrm.jsp").forward(request, response);
                    break;

                case "delete":
                    int idDelete = Integer.parseInt(request.getParameter("id"));
                    treeSpeciesService.deleteTreeSpecies(idDelete);
                    response.sendRedirect(request.getContextPath() + "/treespecies");
                    break;

                default:
    List<TreeSpecies> lista = treeSpeciesService.getAllTreeSpecies();

    List<EstadoConservacion> estados = estadoService.getAllEstados();
    System.out.println("📋 ESTADOS DE CONSERVACIÓN CARGADOS:");
    for (EstadoConservacion ec : estados) {
        System.out.println("ID: " + ec.getId() + " - Nombre: " + ec.getNombre());
    }

    request.setAttribute("treeSpeciesList", lista);
    request.setAttribute("estados", estados);
    request.getRequestDispatcher("/TreeSpecies.jsp").forward(request, response);
    break;
            }
        } catch (Exception e) {
            request.setAttribute("error", "Ocurrió un error: " + e.getMessage());
            request.getRequestDispatcher("/TreeSpecies.jsp").forward(request, response);
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String idParam = request.getParameter("id");
        String nombreComun = request.getParameter("nombreComun");
        String nombreCientifico = request.getParameter("nombreCientifico");
        String estadoConservacionIdParam = request.getParameter("estadoConservacionId");
        String zonaIdParam = request.getParameter("zonaId");

        TreeSpecies treeSpecies = new TreeSpecies();
        treeSpecies.setNombreComun(nombreComun);
        treeSpecies.setNombreCientifico(nombreCientifico);

        if (estadoConservacionIdParam != null && !estadoConservacionIdParam.isEmpty()) {
            treeSpecies.setEstadoConservacionId(Integer.parseInt(estadoConservacionIdParam));
        }

        if (zonaIdParam != null && !zonaIdParam.isEmpty()) {
            treeSpecies.setZonaId(Integer.parseInt(zonaIdParam));
        }

        treeSpecies.setActivo(request.getParameter("activo") != null); // Marca si está activo

        try {
            if (idParam == null || idParam.isEmpty() || "0".equals(idParam)) {
                treeSpeciesService.createTreeSpecies(treeSpecies);
            } else {
                treeSpecies.setId(Integer.parseInt(idParam));
                treeSpeciesService.updateTreeSpecies(treeSpecies);
            }
            response.sendRedirect(request.getContextPath() + "/treespecies");
        } catch (Exception e) {
            request.setAttribute("treeSpecies", treeSpecies);
            request.setAttribute("error", e.getMessage());
            request.setAttribute("estados", estadoService.getAllEstados());
            request.setAttribute("zones", zoneService.getAllZones()); // ✅ CAMBIO
            request.getRequestDispatcher("/TreeSpeciesFrm.jsp").forward(request, response);
        }
    }
}
