package com.mycompany.sistemaforestalfinal.dao;

import com.mycompany.sistemaforestalfinal.model.EstadoConservacion;
import com.mycompany.sistemaforestalfinal.model.TreeSpecies;
import com.mycompany.sistemaforestalfinal.model.Zone;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class TreeSpeciesDAO {

    // Crear
    public void insert(TreeSpecies sp) {
        String sql = "INSERT INTO tree_species (nombre_comun, nombre_cientifico, estado_conservacion_id, zona_id, activo) VALUES (?, ?, ?, ?, ?)";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, sp.getNombreComun());
            stmt.setString(2, sp.getNombreCientifico());
            stmt.setObject(3, sp.getEstadoConservacionId(), Types.INTEGER);
            stmt.setObject(4, sp.getZonaId(), Types.INTEGER);
            stmt.setBoolean(5, sp.isActivo());

            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    // Leer todos
    public List<TreeSpecies> findAll() {
        List<TreeSpecies> list = new ArrayList<>();
        String sql = "SELECT * FROM tree_species WHERE activo = 1";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                TreeSpecies sp = new TreeSpecies();
                sp.setId(rs.getInt("id"));
                sp.setNombreComun(rs.getString("nombre_comun"));
                sp.setNombreCientifico(rs.getString("nombre_cientifico"));
                sp.setEstadoConservacionId(rs.getInt("estado_conservacion_id"));
                sp.setZonaId(rs.getInt("zona_id"));
                sp.setActivo(rs.getBoolean("activo"));
                sp.setCreadoEn(rs.getTimestamp("creado_en"));
                sp.setActualizadoEn(rs.getTimestamp("actualizado_en"));

                list.add(sp);
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return list;
    }

    // Leer por ID
    public TreeSpecies findById(int id) {
        TreeSpecies sp = null;
        String sql = "SELECT * FROM tree_species WHERE id = ?";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setInt(1, id);
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                sp = new TreeSpecies();
                sp.setId(rs.getInt("id"));
                sp.setNombreComun(rs.getString("nombre_comun"));
                sp.setNombreCientifico(rs.getString("nombre_cientifico"));
                sp.setEstadoConservacionId(rs.getInt("estado_conservacion_id"));
                sp.setZonaId(rs.getInt("zona_id"));
                sp.setActivo(rs.getBoolean("activo"));
                sp.setCreadoEn(rs.getTimestamp("creado_en"));
                sp.setActualizadoEn(rs.getTimestamp("actualizado_en"));
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return sp;
    }

    // Actualizar
    public void update(TreeSpecies sp) {
        String sql = "UPDATE tree_species SET nombre_comun = ?, nombre_cientifico = ?, estado_conservacion_id = ?, zona_id = ?, activo = ? WHERE id = ?";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, sp.getNombreComun());
            stmt.setString(2, sp.getNombreCientifico());
            stmt.setObject(3, sp.getEstadoConservacionId(), Types.INTEGER);
            stmt.setObject(4, sp.getZonaId(), Types.INTEGER);
            stmt.setBoolean(5, sp.isActivo());
            stmt.setInt(6, sp.getId());

            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    // Eliminar lógico
   public void delete(int id) {
    String sql = "UPDATE tree_species SET activo = 0 WHERE id = ?";

    try (Connection conn = ConnectionBdd.getConexion();
         PreparedStatement stmt = conn.prepareStatement(sql)) {

        stmt.setInt(1, id);
        stmt.executeUpdate();
    } catch (SQLException e) {
        e.printStackTrace();
    }
}

    // Obtener todas las zonas activas
    public List<Zone> getAllZones() {
        List<Zone> zones = new ArrayList<>();
        String sql = "SELECT * FROM zones WHERE activo = 1 ORDER BY nombre ASC";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                Zone z = new Zone();
                z.setId(rs.getInt("id"));
                z.setNombre(rs.getString("nombre"));
                z.setTipoBosque(rs.getString("tipo_bosque"));
                z.setAreaHa(rs.getBigDecimal("area_ha"));
                zones.add(z);
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return zones;
    }
    
    public List<EstadoConservacion> getAllEstadosConservacion() {
    List<EstadoConservacion> estados = new ArrayList<>();
    String sql = "SELECT * FROM estado_conservacion WHERE activo = 1 ORDER BY nombre ASC";

    try (Connection conn = ConnectionBdd.getConexion();
         PreparedStatement stmt = conn.prepareStatement(sql);
         ResultSet rs = stmt.executeQuery()) {

        while (rs.next()) {
            EstadoConservacion ec = new EstadoConservacion();
            ec.setId(rs.getInt("id"));
            ec.setNombre(rs.getString("nombre"));
            ec.setDescripcion(rs.getString("descripcion"));
            ec.setActivo(rs.getBoolean("activo"));
            estados.add(ec);
        }

    } catch (SQLException e) {
        e.printStackTrace();
    }
    System.out.println("Estados encontrados: " + estados.size());

    return estados;
}
}
