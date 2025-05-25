package com.mycompany.sistemaforestalfinal.service;

import com.mycompany.sistemaforestalfinal.dao.TreeSpeciesDAO;
import com.mycompany.sistemaforestalfinal.model.TreeSpecies;

import java.util.List;

public class TreeSpeciesService {

    private TreeSpeciesDAO treeSpeciesDAO;

    public TreeSpeciesService() {
        this.treeSpeciesDAO = new TreeSpeciesDAO();
    }

    // Listar todas las especies activas
    public List<TreeSpecies> getAllTreeSpecies() {
        return treeSpeciesDAO.findAll();
    }

    // Buscar especie por id
    public TreeSpecies getTreeSpeciesById(int id) {
        return treeSpeciesDAO.findById(id);
    }

    // Crear nueva especie con validaciones
    public void createTreeSpecies(TreeSpecies treeSpecies) throws Exception {
        validarTreeSpecies(treeSpecies);

        if (existeNombre(treeSpecies.getNombreComun(), 0)) { // 0 porque es nueva especie
            throw new Exception("Ya existe una especie activa con ese nombre común.");
        }

        treeSpeciesDAO.insert(treeSpecies);
    }

    // Actualizar especie con validaciones
    public void updateTreeSpecies(TreeSpecies treeSpecies) throws Exception {
        validarTreeSpecies(treeSpecies);

        if (existeNombre(treeSpecies.getNombreComun(), treeSpecies.getId())) {
            throw new Exception("Ya existe otra especie activa con ese nombre común.");
        }

        treeSpeciesDAO.update(treeSpecies);
    }

    // Borrado lógico de especie
    public void deleteTreeSpecies(int id) {
        treeSpeciesDAO.delete(id);
    }

    // Método para validar campos básicos
    private void validarTreeSpecies(TreeSpecies treeSpecies) throws Exception {
        if (treeSpecies.getNombreComun() == null || treeSpecies.getNombreComun().trim().isEmpty()) {
            throw new Exception("El nombre común es obligatorio.");
        }
        // Puedes agregar más validaciones aquí, por ejemplo nombre científico, estado de conservación, etc.
    }

    // Método para verificar si existe especie con ese nombre distinto al id actual (para update)
    private boolean existeNombre(String nombreComun, int idExcluir) {
        List<TreeSpecies> lista = treeSpeciesDAO.findAll();
        for (TreeSpecies ts : lista) {
            if (ts.getNombreComun().equalsIgnoreCase(nombreComun.trim())
                && ts.isActivo()
                && ts.getId() != idExcluir) {
                return true;
            }
        }
        return false;
    }
}
