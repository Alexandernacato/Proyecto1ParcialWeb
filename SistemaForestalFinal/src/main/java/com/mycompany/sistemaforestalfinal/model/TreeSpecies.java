/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.sistemaforestalfinal.model;

import java.sql.Timestamp;

/**
 *
 * @author Administrador
 */
public class TreeSpecies {
     private int id;
    private String nombreComun;
    private String nombreCientifico;
    private Integer estadoConservacionId;
    private Integer zonaId;
    private boolean activo;
    private Timestamp creadoEn;
    private Integer EstadoCId;
    private Timestamp actualizadoEn;

    // --- Getters y Setters ---

    public Integer getEstadoCId() {
        return EstadoCId;
    }

    public void setEstadoCId(Integer EstadoCId) {
        this.EstadoCId = EstadoCId;
    }
    
    

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNombreComun() {
        return nombreComun;
    }

    public void setNombreComun(String nombreComun) {
        this.nombreComun = nombreComun;
    }

    public String getNombreCientifico() {
        return nombreCientifico;
    }

    public void setNombreCientifico(String nombreCientifico) {
        this.nombreCientifico = nombreCientifico;
    }

    public Integer getEstadoConservacionId() {
        return estadoConservacionId;
    }

    public void setEstadoConservacionId(Integer estadoConservacionId) {
        this.estadoConservacionId = estadoConservacionId;
    }

    public Integer getZonaId() {
        return zonaId;
    }

    public void setZonaId(Integer zonaId) {
        this.zonaId = zonaId;
    }

    public boolean isActivo() {
        return activo;
    }

    public void setActivo(boolean activo) {
        this.activo = activo;
    }

    public Timestamp getCreadoEn() {
        return creadoEn;
    }

    public void setCreadoEn(Timestamp creadoEn) {
        this.creadoEn = creadoEn;
    }

    public Timestamp getActualizadoEn() {
        return actualizadoEn;
    }

    public void setActualizadoEn(Timestamp actualizadoEn) {
        this.actualizadoEn = actualizadoEn;
    }
    
}
