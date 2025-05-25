package com.mycompany.sistemaforestalfinal.service;

import com.mycompany.sistemaforestalfinal.dao.ZoneDAO;
import com.mycompany.sistemaforestalfinal.model.Zone;

import java.util.List;

public class ZoneService {

    private ZoneDAO zoneDAO;

    public ZoneService() {
        this.zoneDAO = new ZoneDAO();
    }

    // Listar zonas activas
    public List<Zone> getAllZones() {
        return zoneDAO.findAll();
    }

    // Obtener una zona por ID
    public Zone getZoneById(int id) {
        return zoneDAO.findById(id);
    }

    // Crear nueva zona con validaciones
    public void createZone(Zone zone) throws Exception {
        validarZona(zone);
        zoneDAO.insert(zone);
    }

    // Actualizar zona con validaciones
    public void updateZone(Zone zone) throws Exception {
        validarZona(zone);
        zoneDAO.update(zone);
    }

    // Borrado lógico de zona
    public void deleteZone(int id) {
        zoneDAO.delete(id);
    }

    // Validaciones básicas
    private void validarZona(Zone zone) throws Exception {
        if (zone.getNombre() == null || zone.getNombre().trim().isEmpty()) {
            throw new Exception("El nombre de la zona es obligatorio.");
        }
        if (zone.getTipoBosque() == null || zone.getTipoBosque().trim().isEmpty()) {
            throw new Exception("El tipo de bosque es obligatorio.");
        }
        if (zone.getAreaHa() == null || zone.getAreaHa().doubleValue() <= 0) {
            throw new Exception("El área debe ser mayor a cero.");
        }
    }
}
