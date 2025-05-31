package com.mycompany.sistemaforestalfinal.service;

import com.mycompany.sistemaforestalfinal.dao.TipoActividadDAO;
import com.mycompany.sistemaforestalfinal.model.TipoActividad;

import java.util.List;

public class TipoActividadService {

    private TipoActividadDAO tipoActividadDAO;

    public TipoActividadService() {
        this.tipoActividadDAO = new TipoActividadDAO();
    }

    // Listar todos los tipos de actividad activos
    public List<TipoActividad> getAllTiposActividad() {
        return tipoActividadDAO.findAll();
    }

    // Buscar tipo de actividad por ID
    public TipoActividad getTipoActividadById(int id) {
        return tipoActividadDAO.findById(id);
    }

    // Crear nuevo tipo de actividad con validaciones
    public void createTipoActividad(TipoActividad tipo) throws Exception {
        validarTipoActividad(tipo);
        tipoActividadDAO.insert(tipo);
    }

    // Actualizar tipo de actividad con validaciones
    public void updateTipoActividad(TipoActividad tipo) throws Exception {
        validarTipoActividad(tipo);
        tipoActividadDAO.update(tipo);
    }

    // Borrado lógico
    public void deleteTipoActividad(int id) {
        tipoActividadDAO.delete(id);
    }

    // Validaciones básicas
    private void validarTipoActividad(TipoActividad tipo) throws Exception {
        if (tipo.getNombre() == null || tipo.getNombre().trim().isEmpty()) {
            throw new Exception("El nombre del tipo de actividad es obligatorio.");
        }
        if (tipo.getDescripcion() == null || tipo.getDescripcion().trim().isEmpty()) {
            throw new Exception("La descripción del tipo de actividad es obligatoria.");
        }
    }
}
