package com.mycompany.sistemaforestalfinal.service;

import com.mycompany.sistemaforestalfinal.dao.ConservationActivitiesDAO;
import com.mycompany.sistemaforestalfinal.model.ConservationActivities;

import java.util.List;

public class ConservationActivitiesService {

    private ConservationActivitiesDAO conservationActivitiesDAO;

    public ConservationActivitiesService() {
        this.conservationActivitiesDAO = new ConservationActivitiesDAO();
    }

    // Listar todas las actividades activas
    public List<ConservationActivities> getAllActivities() {
        return conservationActivitiesDAO.findAll();
    }

    // Buscar actividad por ID
    public ConservationActivities getActivityById(int id) {
        return conservationActivitiesDAO.findById(id);
    }

    // Crear nueva actividad con validaciones
    public void createActivity(ConservationActivities ca) throws Exception {
        validarActividad(ca);
        conservationActivitiesDAO.insert(ca);
    }

    // Actualizar actividad con validaciones
    public void updateActivity(ConservationActivities ca) throws Exception {
        validarActividad(ca);
        conservationActivitiesDAO.update(ca);
    }

    // Borrado lógico
    public void deleteActivity(int id) {
        conservationActivitiesDAO.delete(id);
    }

    // Validaciones básicas
    private void validarActividad(ConservationActivities ca) throws Exception {
        if (ca.getNombreActividad() == null || ca.getNombreActividad().trim().isEmpty()) {
            throw new Exception("El nombre de la actividad es obligatorio.");
        }
        if (ca.getFechaActividad() == null || ca.getFechaActividad().trim().isEmpty()) {
            throw new Exception("La fecha de la actividad es obligatoria.");
        }
        if (ca.getResponsable() == null || ca.getResponsable().trim().isEmpty()) {
            throw new Exception("El responsable de la actividad es obligatorio.");
        }
        if (ca.getTipoActividadId() <= 0) {
            throw new Exception("El tipo de actividad debe ser válido.");
        }
        if (ca.getZonaId() <= 0) {
            throw new Exception("La zona debe ser válida.");
        }
        // Puedes agregar más validaciones según tu modelo
    }
}

