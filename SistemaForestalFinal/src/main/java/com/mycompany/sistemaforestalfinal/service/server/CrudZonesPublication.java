package com.mycompany.sistemaforestalfinal.service.server;

import jakarta.xml.ws.Endpoint;

public class CrudZonesPublication {
    public static void main(String[] args) {
        try {
            // URL donde se publicará el servicio SOAP
            String address = "http://localhost:8081/SistemaForestalFinal/ZoneCrudService";
            
            // Crear una instancia del servicio
            CrudZonesService service = new CrudZonesService();
            
            // Publicar el servicio
            Endpoint.publish(address, service);
            
            System.out.println("=== Servicio SOAP de CRUD de Zonas Forestales ===");
            System.out.println("Servicio publicado exitosamente en: " + address);
            System.out.println("WSDL disponible en: " + address + "?wsdl");
            System.out.println("=====================================================");
            System.out.println("Operaciones disponibles:");
            System.out.println("- createZone: Crear nueva zona");
            System.out.println("- getAllZones: Obtener todas las zonas");
            System.out.println("- getZoneById: Obtener zona por ID");
            System.out.println("- updateZone: Actualizar zona existente");
            System.out.println("- deleteZone: Eliminar zona");
            System.out.println("=====================================================");
            System.out.println("Presiona Ctrl+C para detener el servicio...");
            
            // Mantener el servicio en ejecución
            while (true) {
                Thread.sleep(1000);
            }
            
        } catch (InterruptedException e) {
            System.out.println("Servicio interrumpido: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Error al publicar el servicio SOAP: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
