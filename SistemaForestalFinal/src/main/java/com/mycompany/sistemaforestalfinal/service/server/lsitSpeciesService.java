package com.mycompany.sistemaforestalfinal.service.server;

import com.mycompany.sistemaforestalfinal.dao.TreeSpeciesDAO;
import com.mycompany.sistemaforestalfinal.model.TreeSpecies;
import com.mycompany.sistemaforestalfinal.model.EstadoConservacion;
import jakarta.jws.WebService;
import jakarta.jws.WebMethod;
import jakarta.jws.WebParam;
import java.util.List;
import java.util.ArrayList;
import java.util.logging.Logger;

@WebService(serviceName = "ConservationSpeciesService")
public class lsitSpeciesService {
    
    private static final Logger LOGGER = Logger.getLogger(lsitSpeciesService.class.getName());
    private final TreeSpeciesDAO treeSpeciesDAO;
    
    public lsitSpeciesService() {
        this.treeSpeciesDAO = new TreeSpeciesDAO();
        LOGGER.info("ConservationSpeciesService inicializado correctamente");
    }
    
    // Constructor alternativo para inyección de dependencias en testing
    public lsitSpeciesService(TreeSpeciesDAO treeSpeciesDAO) {
        this.treeSpeciesDAO = treeSpeciesDAO;
        LOGGER.info("ConservationSpeciesService inicializado con DAO personalizado");
    }
      @WebMethod(operationName = "getSpeciesInConservation")
    public List<ConservationSpeciesInfo> getSpeciesInConservation() {
        LOGGER.info("Solicitando todas las especies en conservación");
        List<ConservationSpeciesInfo> result = new ArrayList<>();
        
        try {
            // Obtener todas las especies activas usando TreeSpeciesDAO
            List<TreeSpecies> allSpecies = treeSpeciesDAO.findAll();
            LOGGER.info("Obtenidas " + allSpecies.size() + " especies de la base de datos");
            
            // Obtener todos los estados de conservación usando TreeSpeciesDAO
            List<EstadoConservacion> conservationStates = treeSpeciesDAO.getAllEstadosConservacion();
            LOGGER.info("Obtenidos " + conservationStates.size() + " estados de conservación");
            
            // Filtrar especies que tienen estado de conservación asignado
            int speciesWithConservationStatus = 0;
            for (TreeSpecies species : allSpecies) {
                if (species.getEstadoConservacionId() != null && species.isActivo()) {
                    ConservationSpeciesInfo info = convertToConservationInfo(species, conservationStates);
                    if (info != null) {
                        result.add(info);
                        speciesWithConservationStatus++;
                    }
                }
            }
            
            LOGGER.info("Proceso completado: " + speciesWithConservationStatus + " especies en conservación encontradas");
            
        } catch (Exception e) {
            LOGGER.severe("Error al obtener especies en conservación: " + e.getMessage());
            e.printStackTrace();
        }
        
        return result;
    }
      @WebMethod(operationName = "getSpeciesByConservationState")
    public List<ConservationSpeciesInfo> getSpeciesByConservationState(@WebParam(name = "estadoId") int estadoId) {
        LOGGER.info("Solicitando especies con estado de conservación ID: " + estadoId);
        List<ConservationSpeciesInfo> result = new ArrayList<>();
        
        try {
            List<TreeSpecies> allSpecies = treeSpeciesDAO.findAll();
            List<EstadoConservacion> conservationStates = treeSpeciesDAO.getAllEstadosConservacion();
            
            int foundSpecies = 0;
            for (TreeSpecies species : allSpecies) {
                if (species.getEstadoConservacionId() != null && 
                    species.getEstadoConservacionId() == estadoId && 
                    species.isActivo()) {
                    
                    ConservationSpeciesInfo info = convertToConservationInfo(species, conservationStates);
                    if (info != null) {
                        result.add(info);
                        foundSpecies++;
                    }
                }
            }
            
            LOGGER.info("Encontradas " + foundSpecies + " especies con estado de conservación ID: " + estadoId);
            
        } catch (Exception e) {
            LOGGER.severe("Error al obtener especies por estado de conservación: " + e.getMessage());
            e.printStackTrace();
        }
        
        return result;
    }
    
    /**
     * Método helper para convertir TreeSpecies a ConservationSpeciesInfo
     * Refactorización para evitar duplicación de código
     */
    private ConservationSpeciesInfo convertToConservationInfo(TreeSpecies species, List<EstadoConservacion> conservationStates) {
        if (species == null) {
            return null;
        }
        
        ConservationSpeciesInfo info = new ConservationSpeciesInfo();
        info.setId(species.getId());
        info.setNombreComun(species.getNombreComun());
        info.setNombreCientifico(species.getNombreCientifico());
        info.setZonaId(species.getZonaId());
        info.setEstadoConservacionId(species.getEstadoConservacionId());
        
        // Buscar el nombre del estado de conservación de manera eficiente
        for (EstadoConservacion state : conservationStates) {
            if (state.getId() == species.getEstadoConservacionId()) {
                info.setEstadoConservacion(state.getNombre());
                break;
            }
        }
          return info;
    }
    
    /**
     * Nuevo método para obtener estadísticas de conservación
     * Refactorización para agregar funcionalidad analítica
     */
    @WebMethod(operationName = "getConservationStatistics")
    public ConservationStatistics getConservationStatistics() {
        LOGGER.info("Solicitando estadísticas de conservación");
        ConservationStatistics stats = new ConservationStatistics();
        
        try {
            List<TreeSpecies> allSpecies = treeSpeciesDAO.findAll();
            List<EstadoConservacion> conservationStates = treeSpeciesDAO.getAllEstadosConservacion();
            
            stats.setTotalActiveSpecies(allSpecies.size());
            
            int speciesWithConservationStatus = 0;
            int speciesWithoutConservationStatus = 0;
            
            for (TreeSpecies species : allSpecies) {
                if (species.getEstadoConservacionId() != null && species.isActivo()) {
                    speciesWithConservationStatus++;
                } else if (species.isActivo()) {
                    speciesWithoutConservationStatus++;
                }
            }
            
            stats.setSpeciesInConservation(speciesWithConservationStatus);
            stats.setSpeciesWithoutConservationStatus(speciesWithoutConservationStatus);
            stats.setTotalConservationStates(conservationStates.size());
            
            LOGGER.info("Estadísticas generadas correctamente");
            
        } catch (Exception e) {
            LOGGER.severe("Error al generar estadísticas de conservación: " + e.getMessage());
            e.printStackTrace();
        }
        
        return stats;
    }
    
    // Clase interna para estadísticas de conservación
    public static class ConservationStatistics {
        private int totalActiveSpecies;
        private int speciesInConservation;
        private int speciesWithoutConservationStatus;
        private int totalConservationStates;
        
        // Getters y Setters
        public int getTotalActiveSpecies() {
            return totalActiveSpecies;
        }
        
        public void setTotalActiveSpecies(int totalActiveSpecies) {
            this.totalActiveSpecies = totalActiveSpecies;
        }
        
        public int getSpeciesInConservation() {
            return speciesInConservation;
        }
        
        public void setSpeciesInConservation(int speciesInConservation) {
            this.speciesInConservation = speciesInConservation;
        }
        
        public int getSpeciesWithoutConservationStatus() {
            return speciesWithoutConservationStatus;
        }
        
        public void setSpeciesWithoutConservationStatus(int speciesWithoutConservationStatus) {
            this.speciesWithoutConservationStatus = speciesWithoutConservationStatus;
        }
        
        public int getTotalConservationStates() {
            return totalConservationStates;
        }
        
        public void setTotalConservationStates(int totalConservationStates) {
            this.totalConservationStates = totalConservationStates;
        }
    }
    
    // Clase interna para la información de especies en conservación
    public static class ConservationSpeciesInfo {
        private int id;
        private String nombreComun;
        private String nombreCientifico;
        private Integer zonaId;
        private int estadoConservacionId;
        private String estadoConservacion;
        
        // Getters y Setters
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
        
        public Integer getZonaId() {
            return zonaId;
        }
        
        public void setZonaId(Integer zonaId) {
            this.zonaId = zonaId;
        }
        
        public int getEstadoConservacionId() {
            return estadoConservacionId;
        }
        
        public void setEstadoConservacionId(int estadoConservacionId) {
            this.estadoConservacionId = estadoConservacionId;
        }
        
        public String getEstadoConservacion() {
            return estadoConservacion;
        }
        
        public void setEstadoConservacion(String estadoConservacion) {
            this.estadoConservacion = estadoConservacion;
        }
    }
}
