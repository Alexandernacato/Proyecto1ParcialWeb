/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.sistemaforestalfinal.model;

import java.math.BigDecimal;
import java.sql.Timestamp;

public class Zone {
    private int id;
    private String nombre;
    private String tipoBosque;
    private BigDecimal areaHa;
    private boolean activo;
    private Timestamp creadoEn;
    private Timestamp actualizadoEn;

    // Getters y Setters
    public int getId() {
        return id;
    }
    public void setId(int id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getTipoBosque() {
        return tipoBosque;
    }
    public void setTipoBosque(String tipoBosque) {
        this.tipoBosque = tipoBosque;
    }

    public BigDecimal getAreaHa() {
        return areaHa;
    }
    public void setAreaHa(BigDecimal areaHa) {
        this.areaHa = areaHa;
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
