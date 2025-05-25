/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.sistemaforestalfinal.model;

/**
 *
 * @author Administrador
 */
public enum TipoBosque {
       SECO("Seco"),
    HUMEDO_TROPICAL("Húmedo Tropical"),
    MONTANO("Montano"),
    MANGLAR("Manglar"),
    OTRO("Otro");

    private final String displayName;

    TipoBosque(String displayName) {
        this.displayName = displayName;
    }

    public String getDisplayName() {
        return displayName;
    }

    public static TipoBosque fromString(String text) {
        if (text != null) {
            for (TipoBosque b : TipoBosque.values()) {
                if (text.equalsIgnoreCase(b.displayName)) {
                    return b;
                }
            }
        }
        return OTRO; 
    }
}
    

