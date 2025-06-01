package com.mycompany.sistemaforestalfinal.service.server;

import com.mycompany.sistemaforestalfinal.dao.ZoneDAO; // Assuming ZoneDAO exists
import com.mycompany.sistemaforestalfinal.model.Zone;
import jakarta.jws.WebService;
import jakarta.jws.WebMethod;
import jakarta.jws.WebParam;
import java.math.BigDecimal;
import java.util.List;
import java.util.ArrayList;
import java.util.logging.Logger;

@WebService(serviceName = "ZoneCrudService")
public class CrudZonesService {

    private static final Logger LOGGER = Logger.getLogger(CrudZonesService.class.getName());
    private final ZoneDAO zoneDAO;

    public CrudZonesService() {
        this.zoneDAO = new ZoneDAO(); 
        LOGGER.info("CrudZonesService inicializado correctamente");
    }

    // Constructor alternativo para inyección de dependencias en testing
    public CrudZonesService(ZoneDAO zoneDAO) {
        this.zoneDAO = zoneDAO;
        LOGGER.info("CrudZonesService inicializado con DAO personalizado");
    }

    // ================= MÉTODOS CRUD =================

    @WebMethod(operationName = "createZone")
    public boolean crearZona(
            @WebParam(name = "nombre") String nombre,
            @WebParam(name = "tipoBosque") String tipoBosque,
            @WebParam(name = "areaHa") BigDecimal areaHa,
            @WebParam(name = "activo") boolean activo) {
        
        LOGGER.info("Creando nueva zona: " + nombre);
        try {
            if (nombre == null || nombre.trim().isEmpty()) {
                LOGGER.warning("Error: Nombre de zona es requerido");
                return false;
            }
            if (existeZonaPorNombre(nombre.trim(), 0)) {
                LOGGER.warning("Error: Ya existe una zona con ese nombre");
                return false;
            }

            Zone zone = new Zone();
            zone.setNombre(nombre.trim());
            zone.setTipoBosque(tipoBosque);
            zone.setAreaHa(areaHa);
            zone.setActivo(activo);
            
            zoneDAO.insert(zone); // Assuming ZoneDAO has an insert method
            LOGGER.info("Zona creada exitosamente: " + nombre);
            return true;
        } catch (Exception e) {
            LOGGER.severe("Error al crear zona: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }

    @WebMethod(operationName = "getAllZones")
    public List<Zone> obtenerTodasLasZonas() {
        LOGGER.info("Obteniendo todas las zonas");
        List<Zone> result = new ArrayList<>();
        try {
            result = zoneDAO.findAll(); // Assuming ZoneDAO has a findAll method
            LOGGER.info("Obtenidas " + result.size() + " zonas");
        } catch (Exception e) {
            LOGGER.severe("Error al obtener zonas: " + e.getMessage());
            e.printStackTrace();
        }
        return result;
    }

    @WebMethod(operationName = "getZoneById")
    public Zone obtenerZonaPorId(@WebParam(name = "id") int id) {
        LOGGER.info("Obteniendo zona con ID: " + id);
        try {
            return zoneDAO.findById(id); // Assuming ZoneDAO has a findById method
        } catch (Exception e) {
            LOGGER.severe("Error al obtener zona por ID: " + e.getMessage());
            e.printStackTrace();
        }
        return null;
    }

    @WebMethod(operationName = "updateZone")
    public boolean actualizarZona(
            @WebParam(name = "id") int id,
            @WebParam(name = "nombre") String nombre,
            @WebParam(name = "tipoBosque") String tipoBosque,
            @WebParam(name = "areaHa") BigDecimal areaHa,
            @WebParam(name = "activo") boolean activo) {
        
        LOGGER.info("Actualizando zona con ID: " + id);
        try {
            if (nombre == null || nombre.trim().isEmpty()) {
                LOGGER.warning("Error: Nombre de zona es requerido");
                return false;
            }
            if (existeZonaPorNombre(nombre.trim(), id)) {
                LOGGER.warning("Error: Ya existe otra zona con ese nombre");
                return false;
            }

            Zone zone = new Zone();
            zone.setId(id);
            zone.setNombre(nombre.trim());
            zone.setTipoBosque(tipoBosque);
            zone.setAreaHa(areaHa);
            zone.setActivo(activo);
            
            zoneDAO.update(zone); // Assuming ZoneDAO has an update method
            LOGGER.info("Zona actualizada exitosamente: " + nombre);
            return true;
        } catch (Exception e) {
            LOGGER.severe("Error al actualizar zona: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }

    @WebMethod(operationName = "deleteZone")
    public boolean eliminarZona(@WebParam(name = "id") int id) {
        LOGGER.info("Eliminando zona con ID (lógico): " + id);
        try {
            // Implementación de borrado lógico (actualizar campo 'activo')
            Zone zone = zoneDAO.findById(id);
            if (zone == null) {
                LOGGER.warning("No se encontró zona con ID: " + id + " para eliminar.");
                return false;
            }
            zone.setActivo(false);
            zoneDAO.update(zone); // Reutiliza el método update para el borrado lógico
            LOGGER.info("Zona eliminada (lógicamente) exitosamente con ID: " + id);
            return true;
        } catch (Exception e) {
            LOGGER.severe("Error al eliminar zona: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }

    // ================= MÉTODOS AUXILIARES =================
    
    private boolean existeZonaPorNombre(String nombre, int excludeId) {
        try {
            List<Zone> allZones = zoneDAO.findAll();
            for (Zone zone : allZones) {
                if (zone.getNombre().equalsIgnoreCase(nombre) && zone.isActivo() && zone.getId() != excludeId) {
                    return true;
                }
            }
        } catch (Exception e) {
            LOGGER.severe("Error al verificar existencia de zona por nombre: " + e.getMessage());
            // Considerar si se debe propagar la excepción o retornar un valor específico
        }
        return false;
    }
}
