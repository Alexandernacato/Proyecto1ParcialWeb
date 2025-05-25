package com.mycompany.sistemaforestalfinal.controller;

import com.mycompany.sistemaforestalfinal.model.TipoBosque;
import com.mycompany.sistemaforestalfinal.model.Zone;
import com.mycompany.sistemaforestalfinal.service.ZoneService;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.math.BigDecimal;
import static java.time.temporal.TemporalQueries.zone;
import java.util.List;

@WebServlet(name = "ZoneController", urlPatterns = {"/zones"})
public class ZoneController extends HttpServlet {

    private final ZoneService zoneService = new ZoneService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String option = request.getParameter("option");
        if (option == null) option = "findAll";

        try {
            switch (option) {
                case "new":
    request.setAttribute("zone", new Zone());
    request.setAttribute("tiposBosque", TipoBosque.values());
    request.getRequestDispatcher("/ZonesFrm.jsp").forward(request, response);
    break;

case "update":
    int id = Integer.parseInt(request.getParameter("id"));
    Zone zone = zoneService.getZoneById(id);
    if (zone == null) {
        request.setAttribute("error", "Zona no encontrada con id " + id);
        request.getRequestDispatcher("/Zones.jsp").forward(request, response);
        return;
    }
    request.setAttribute("zone", zone);
    request.setAttribute("tiposBosque", TipoBosque.values());
    request.getRequestDispatcher("/ZonesFrm.jsp").forward(request, response);
    break;
                
                case "delete":
                    int idDelete = Integer.parseInt(request.getParameter("id"));
                    zoneService.deleteZone(idDelete);
                    response.sendRedirect(request.getContextPath() + "/zones");
                    break;

                default:
                    List<Zone> zonesList = zoneService.getAllZones();
                    request.setAttribute("zonesList", zonesList);
                    request.getRequestDispatcher("/Zones.jsp").forward(request, response);
                    break;
            }
        } catch (Exception e) {
            request.setAttribute("error", "Ocurrió un error: " + e.getMessage());
            request.getRequestDispatcher("/Zones.jsp").forward(request, response);
        }
    }
    @Override
protected void doPost(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {

    String idParam = request.getParameter("id");
    String nombre = request.getParameter("nombre");
    String tipoBosqueParam = request.getParameter("tipoBosque");
    String areaHaParam = request.getParameter("areaHa");
    
TipoBosque tipoBosqueEnum = TipoBosque.fromString(tipoBosqueParam);


   

    Zone zone = new Zone();
    zone.setNombre(nombre);
    zone.setTipoBosque(tipoBosqueEnum.getDisplayName());
    
    
  

    if (areaHaParam != null && !areaHaParam.isEmpty()) {
        try {
            zone.setAreaHa(new BigDecimal(areaHaParam.replace(",", ".")));
        } catch (NumberFormatException ex) {
            request.setAttribute("error", "Área inválida");
            request.setAttribute("zone", zone);
            request.setAttribute("tiposBosque", TipoBosque.values());
            request.getRequestDispatcher("/ZonesFrm.jsp").forward(request, response);
            return;
        }
    }

    try {
        if (idParam == null || idParam.isEmpty() || "0".equals(idParam)) {
            zoneService.createZone(zone);
        } else {
            zone.setId(Integer.parseInt(idParam));
            zoneService.updateZone(zone);
        }
        response.sendRedirect(request.getContextPath() + "/zones");
    } catch (Exception e) {
        request.setAttribute("zone", zone);
        request.setAttribute("error", e.getMessage());
        request.setAttribute("tiposBosque", TipoBosque.values());
        request.getRequestDispatcher("/ZonesFrm.jsp").forward(request, response);
    }
}

    }
