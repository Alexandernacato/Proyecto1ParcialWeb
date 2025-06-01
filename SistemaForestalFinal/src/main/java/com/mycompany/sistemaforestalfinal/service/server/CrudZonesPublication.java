package com.mycompany.sistemaforestalfinal.service.server;

import jakarta.xml.ws.Endpoint;

public class CrudZonesPublication {
    public static void main(String[] args) {
        // Asegúrate de que la URL sea accesible y no entre en conflicto con otros servicios
        String url = "http://localhost:8081/SistemaForestalFinal/ZoneCrudService"; 
        System.out.println("Publicando CrudZonesService en: " + url);
        Endpoint.publish(url, new CrudZonesService());
        System.out.println("Servicio CrudZonesService publicado exitosamente.");
        System.out.println("Presiona Ctrl+C para detener el servicio.");
    }
}
