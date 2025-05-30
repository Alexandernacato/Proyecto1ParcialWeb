package com.mycompany.sistemaforestalfinal.service.server;

import com.mycompany.sistemaforestalfinal.dao.TreeSpeciesDAO;
import com.mycompany.sistemaforestalfinal.model.TreeSpecies;
import com.mycompany.sistemaforestalfinal.model.EstadoConservacion;
import com.mycompany.sistemaforestalfinal.model.Zone;
import jakarta.jws.WebService;
import jakarta.jws.WebMethod;
import jakarta.jws.WebParam;
import java.util.List;
import java.util.ArrayList;
import java.util.logging.Logger;

@WebService(serviceName = "TreeSpeciesCrudService")
public class CrudSpeciesService {
    
    private static final Logger LOGGER = Logger.getLogger(CrudSpeciesService.class.getName());
    private final TreeSpeciesDAO treeSpeciesDAO;
    
    public CrudSpeciesService() {
        this.treeSpeciesDAO = new TreeSpeciesDAO();
        LOGGER.info("TreeSpeciesCrudService inicializado correctamente");
    }
      // Constructor alternativo para inyección de dependencias en testing
    public CrudSpeciesService(TreeSpeciesDAO treeSpeciesDAO) {
        this.treeSpeciesDAO = treeSpeciesDAO;
        LOGGER.info("TreeSpeciesCrudService inicializado con DAO personalizado");
    }
    
    // ================= MÉTODOS CRUD COMPLETOS =================
    
    // CREATE - Crear nueva especie
    @WebMethod(operationName = "createTreeSpecies")
    public boolean createTreeSpecies(
            @WebParam(name = "nombreComun") String nombreComun,
            @WebParam(name = "nombreCientifico") String nombreCientifico,
            @WebParam(name = "estadoConservacionId") Integer estadoConservacionId,
            @WebParam(name = "zonaId") Integer zonaId,
            @WebParam(name = "activo") boolean activo) {
        
        LOGGER.info("Creando nueva especie: " + nombreComun);
        
        try {
            // Validaciones básicas
            if (nombreComun == null || nombreComun.trim().isEmpty()) {
                LOGGER.warning("Error: Nombre común es requerido");
                return false;
            }
            
            // Verificar si ya existe una especie con ese nombre
            if (existsSpeciesByName(nombreComun, 0)) {
                LOGGER.warning("Error: Ya existe una especie con ese nombre común");
                return false;
            }
            
            TreeSpecies species = new TreeSpecies();
            species.setNombreComun(nombreComun.trim());
            species.setNombreCientifico(nombreCientifico);
            species.setEstadoConservacionId(estadoConservacionId);
            species.setZonaId(zonaId);
            species.setActivo(activo);
            
            treeSpeciesDAO.insert(species);
            LOGGER.info("Especie creada exitosamente: " + nombreComun);
            return true;
            
        } catch (Exception e) {
            LOGGER.severe("Error al crear especie: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }
    
    // READ - Obtener todas las especies
    @WebMethod(operationName = "getAllTreeSpecies")
    public List<TreeSpeciesInfo> getAllTreeSpecies() {
        LOGGER.info("Obteniendo todas las especies");
        List<TreeSpeciesInfo> result = new ArrayList<>();
        
        try {
            List<TreeSpecies> allSpecies = treeSpeciesDAO.findAll();
            List<EstadoConservacion> conservationStates = treeSpeciesDAO.getAllEstadosConservacion();
            List<Zone> zones = treeSpeciesDAO.getAllZones();
            
            for (TreeSpecies species : allSpecies) {
                TreeSpeciesInfo info = convertToTreeSpeciesInfo(species, conservationStates, zones);
                if (info != null) {
                    result.add(info);
                }
            }
            
            LOGGER.info("Obtenidas " + result.size() + " especies");
            
        } catch (Exception e) {
            LOGGER.severe("Error al obtener especies: " + e.getMessage());
            e.printStackTrace();
        }
        
        return result;
    }
    
    // READ - Obtener especie por ID
    @WebMethod(operationName = "getTreeSpeciesById")
    public TreeSpeciesInfo getTreeSpeciesById(@WebParam(name = "id") int id) {
        LOGGER.info("Obteniendo especie con ID: " + id);
        
        try {
            TreeSpecies species = treeSpeciesDAO.findById(id);
            if (species != null) {
                List<EstadoConservacion> conservationStates = treeSpeciesDAO.getAllEstadosConservacion();
                List<Zone> zones = treeSpeciesDAO.getAllZones();
                return convertToTreeSpeciesInfo(species, conservationStates, zones);
            }
        } catch (Exception e) {
            LOGGER.severe("Error al obtener especie por ID: " + e.getMessage());
            e.printStackTrace();
        }
        
        return null;
    }
    
    // UPDATE - Actualizar especie
    @WebMethod(operationName = "updateTreeSpecies")
    public boolean updateTreeSpecies(
            @WebParam(name = "id") int id,
            @WebParam(name = "nombreComun") String nombreComun,
            @WebParam(name = "nombreCientifico") String nombreCientifico,
            @WebParam(name = "estadoConservacionId") Integer estadoConservacionId,
            @WebParam(name = "zonaId") Integer zonaId,
            @WebParam(name = "activo") boolean activo) {
        
        LOGGER.info("Actualizando especie con ID: " + id);
        
        try {
            // Validaciones básicas
            if (nombreComun == null || nombreComun.trim().isEmpty()) {
                LOGGER.warning("Error: Nombre común es requerido");
                return false;
            }
            
            // Verificar si ya existe otra especie con ese nombre (excluyendo la actual)
            if (existsSpeciesByName(nombreComun, id)) {
                LOGGER.warning("Error: Ya existe otra especie con ese nombre común");
                return false;
            }
            
            TreeSpecies species = new TreeSpecies();
            species.setId(id);
            species.setNombreComun(nombreComun.trim());
            species.setNombreCientifico(nombreCientifico);
            species.setEstadoConservacionId(estadoConservacionId);
            species.setZonaId(zonaId);
            species.setActivo(activo);
            
            treeSpeciesDAO.update(species);
            LOGGER.info("Especie actualizada exitosamente: " + nombreComun);
            return true;
            
        } catch (Exception e) {
            LOGGER.severe("Error al actualizar especie: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }
    
    // DELETE - Eliminar especie (borrado lógico)
    @WebMethod(operationName = "deleteTreeSpecies")
    public boolean deleteTreeSpecies(@WebParam(name = "id") int id) {
        LOGGER.info("Eliminando especie con ID: " + id);
        
        try {
            treeSpeciesDAO.delete(id);
            LOGGER.info("Especie eliminada exitosamente con ID: " + id);
            return true;
            
        } catch (Exception e) {
            LOGGER.severe("Error al eliminar especie: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }
    
    // UTILITY - Obtener zonas disponibles
    @WebMethod(operationName = "getAllZones")
    public List<ZoneInfo> getAllZones() {
        LOGGER.info("Obteniendo todas las zonas");
        List<ZoneInfo> result = new ArrayList<>();
        
        try {
            List<Zone> zones = treeSpeciesDAO.getAllZones();
            for (Zone zone : zones) {
                ZoneInfo info = new ZoneInfo();
                info.setId(zone.getId());
                info.setNombre(zone.getNombre());
                info.setTipoBosque(zone.getTipoBosque());
                info.setAreaHa(zone.getAreaHa() != null ? zone.getAreaHa().doubleValue() : 0.0);
                result.add(info);
            }
            LOGGER.info("Obtenidas " + result.size() + " zonas");
            
        } catch (Exception e) {
            LOGGER.severe("Error al obtener zonas: " + e.getMessage());
            e.printStackTrace();
        }
        
        return result;
    }
    
    // UTILITY - Obtener estados de conservación
    @WebMethod(operationName = "getAllConservationStates")
    public List<ConservationStateInfo> getAllConservationStates() {
        LOGGER.info("Obteniendo todos los estados de conservación");
        List<ConservationStateInfo> result = new ArrayList<>();
        
        try {
            List<EstadoConservacion> states = treeSpeciesDAO.getAllEstadosConservacion();
            for (EstadoConservacion state : states) {
                ConservationStateInfo info = new ConservationStateInfo();
                info.setId(state.getId());
                info.setNombre(state.getNombre());
                info.setDescripcion(state.getDescripcion());
                result.add(info);
            }
            LOGGER.info("Obtenidos " + result.size() + " estados de conservación");
            
        } catch (Exception e) {
            LOGGER.severe("Error al obtener estados de conservación: " + e.getMessage());
            e.printStackTrace();
        }
        
        return result;
    }
    
    // ================= MÉTODOS AUXILIARES =================
    
    /**
     * Verificar si existe una especie con el nombre dado (excluyendo el ID dado)
     */
    private boolean existsSpeciesByName(String nombreComun, int excludeId) {
        try {
            List<TreeSpecies> allSpecies = treeSpeciesDAO.findAll();
            for (TreeSpecies species : allSpecies) {
                if (species.getNombreComun().equalsIgnoreCase(nombreComun.trim()) 
                    && species.isActivo() 
                    && species.getId() != excludeId) {
                    return true;
                }
            }
        } catch (Exception e) {
            LOGGER.severe("Error al verificar existencia de especie: " + e.getMessage());
        }
        return false;
    }
    
    /**
     * Convertir TreeSpecies a TreeSpeciesInfo
     */
    private TreeSpeciesInfo convertToTreeSpeciesInfo(TreeSpecies species, 
            List<EstadoConservacion> conservationStates, List<Zone> zones) {
        if (species == null) {
            return null;
        }
        
        TreeSpeciesInfo info = new TreeSpeciesInfo();
        info.setId(species.getId());
        info.setNombreComun(species.getNombreComun());
        info.setNombreCientifico(species.getNombreCientifico());
        info.setEstadoConservacionId(species.getEstadoConservacionId());
        info.setZonaId(species.getZonaId());
        info.setActivo(species.isActivo());
        
        // Buscar nombre del estado de conservación
        if (species.getEstadoConservacionId() != null) {
            for (EstadoConservacion state : conservationStates) {
                if (state.getId() == species.getEstadoConservacionId()) {
                    info.setEstadoConservacion(state.getNombre());
                    break;
                }
            }
        }
        
        // Buscar nombre de la zona
        if (species.getZonaId() != null) {
            for (Zone zone : zones) {
                if (zone.getId() == species.getZonaId()) {
                    info.setZonaNombre(zone.getNombre());
                    break;
                }
            }
        }
        
        return info;
    }
    
    // ================= CLASES DE DATOS =================
    
    // Clase para información completa de especies
    public static class TreeSpeciesInfo {
        private int id;
        private String nombreComun;
        private String nombreCientifico;
        private Integer estadoConservacionId;
        private String estadoConservacion;
        private Integer zonaId;
        private String zonaNombre;
        private boolean activo;
        
        // Constructores
        public TreeSpeciesInfo() {}
        
        // Getters y Setters
        public int getId() { return id; }
        public void setId(int id) { this.id = id; }
        
        public String getNombreComun() { return nombreComun; }
        public void setNombreComun(String nombreComun) { this.nombreComun = nombreComun; }
        
        public String getNombreCientifico() { return nombreCientifico; }
        public void setNombreCientifico(String nombreCientifico) { this.nombreCientifico = nombreCientifico; }
        
        public Integer getEstadoConservacionId() { return estadoConservacionId; }
        public void setEstadoConservacionId(Integer estadoConservacionId) { this.estadoConservacionId = estadoConservacionId; }
        
        public String getEstadoConservacion() { return estadoConservacion; }
        public void setEstadoConservacion(String estadoConservacion) { this.estadoConservacion = estadoConservacion; }
        
        public Integer getZonaId() { return zonaId; }
        public void setZonaId(Integer zonaId) { this.zonaId = zonaId; }
        
        public String getZonaNombre() { return zonaNombre; }
        public void setZonaNombre(String zonaNombre) { this.zonaNombre = zonaNombre; }
        
        public boolean isActivo() { return activo; }
        public void setActivo(boolean activo) { this.activo = activo; }
    }
    
    // Clase para información de zonas
    public static class ZoneInfo {
        private int id;
        private String nombre;
        private String tipoBosque;
        private double areaHa;
        
        // Constructores
        public ZoneInfo() {}
        
        // Getters y Setters
        public int getId() { return id; }
        public void setId(int id) { this.id = id; }
        
        public String getNombre() { return nombre; }
        public void setNombre(String nombre) { this.nombre = nombre; }
        
        public String getTipoBosque() { return tipoBosque; }
        public void setTipoBosque(String tipoBosque) { this.tipoBosque = tipoBosque; }
        
        public double getAreaHa() { return areaHa; }
        public void setAreaHa(double areaHa) { this.areaHa = areaHa; }
    }
    
    // Clase para información de estados de conservación
    public static class ConservationStateInfo {
        private int id;
        private String nombre;
        private String descripcion;
        
        // Constructores
        public ConservationStateInfo() {}
        
        // Getters y Setters
        public int getId() { return id; }
        public void setId(int id) { this.id = id; }
        
        public String getNombre() { return nombre; }
        public void setNombre(String nombre) { this.nombre = nombre; }
        
        public String getDescripcion() { return descripcion; }
        public void setDescripcion(String descripcion) { this.descripcion = descripcion; }
    }
}
