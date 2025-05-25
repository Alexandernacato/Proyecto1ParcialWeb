package com.mycompany.sistemaforestalfinal.service;

import com.mycompany.sistemaforestalfinal.dao.EstadoConservacionDAO;
import com.mycompany.sistemaforestalfinal.dao.TreeSpeciesDAO;
import com.mycompany.sistemaforestalfinal.model.EstadoConservacion;

import java.sql.SQLException;
import java.util.List;

public class EstadoConservacionService {

  private final TreeSpeciesDAO dao = new TreeSpeciesDAO();

    public List<EstadoConservacion> getAllEstados() {
        return dao.getAllEstadosConservacion();
    }
    }
    
