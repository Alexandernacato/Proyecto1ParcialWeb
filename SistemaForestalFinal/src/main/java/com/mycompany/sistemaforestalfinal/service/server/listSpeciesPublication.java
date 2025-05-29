package com.mycompany.sistemaforestalfinal.service.server;

import jakarta.xml.ws.Endpoint;
public class listSpeciesPublication {
    
    public static void main(String[] args) {
        try {
            // URL donde se publicará el servicio SOAP
            String address = "http://localhost:8282/ConservationSpeciesService";
              // Crear una instancia del servicio
            lsitSpeciesService service = new lsitSpeciesService();
            
            // Publicar el servicio
            Endpoint.publish(address, service);
            
            System.out.println("=== Servicio SOAP de Especies en Conservación ===");
            System.out.println("Servicio publicado exitosamente en: " + address);
            System.out.println("WSDL disponible en: " + address + "?wsdl");
            System.out.println("=================================================");
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
    
    /**
     * Método para detener el servicio (puede ser usado desde otros lugares)
     */
    public static void stopService() {
        System.out.println("Deteniendo servicio SOAP...");
        System.exit(0);
    }
}
