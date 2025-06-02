package com.mycompany.sistemaforestalfinal.service.server;

import jakarta.xml.ws.Endpoint;
public class CrudSpeciesPublication {   
    
    public static void main(String[] args) {
        try {
          
            String address = "http://localhost:8282/TreeSpeciesCrudService";
             
            CrudSpeciesService service = new CrudSpeciesService();            
          
            Endpoint.publish(address, service);
            
            System.out.println("=== Servicio SOAP de CRUD de Especies Forestales ===");
            System.out.println("Servicio publicado exitosamente en: " + address);
            System.out.println("WSDL disponible en: " + address + "?wsdl");
            System.out.println("=====================================================");
            System.out.println("Operaciones disponibles:");
            System.out.println("- createTreeSpecies: Crear nueva especie");
            System.out.println("- getAllTreeSpecies: Obtener todas las especies");
            System.out.println("- getTreeSpeciesById: Obtener especie por ID");
            System.out.println("- updateTreeSpecies: Actualizar especie existente");
            System.out.println("- deleteTreeSpecies: Eliminar especie");
            System.out.println("- getAllZones: Obtener todas las zonas");
            System.out.println("- getAllConservationStates: Obtener estados de conservación");
            System.out.println("=====================================================");
            System.out.println("Presiona Ctrl+C para detener el servicio...");
            
          
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
    
    public static void stopService() {
        System.out.println("Deteniendo servicio SOAP CRUD...");
        System.exit(0);
    }
}
