package com.mycompany.sistemaforestalfinal.dao;

import com.mycompany.sistemaforestalfinal.model.ConservationActivities;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ConservationActivitiesDAO {

    // Crear
    public void insert(ConservationActivities ca) {
        String sql = "INSERT INTO conservation_activities (nombre_actividad, fecha_actividad, responsable, tipo_actividad_id, zona_id, activo, creado_en, actualizado_en) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, ca.getNombreActividad());
            stmt.setString(2, ca.getFechaActividad());
            stmt.setString(3, ca.getResponsable());
            stmt.setInt(4, ca.getTipoActividadId());
            stmt.setInt(5, ca.getZonaId());
            stmt.setBoolean(6, ca.isActivo());
            stmt.setTimestamp(7, ca.getCreadoEn());
            stmt.setTimestamp(8, ca.getActualizadoEn());

            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    // Leer todos
    public List<ConservationActivities> findAll() {
        List<ConservationActivities> list = new ArrayList<>();
        String sql = "SELECT * FROM conservation_activities WHERE activo = 1";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                ConservationActivities ca = new ConservationActivities();
                ca.setId(rs.getInt("id"));
                ca.setNombreActividad(rs.getString("nombre_actividad"));
                ca.setFechaActividad(rs.getString("fecha_actividad"));
                ca.setResponsable(rs.getString("responsable"));
                ca.setTipoActividadId(rs.getInt("tipo_actividad_id"));
                ca.setZonaId(rs.getInt("zona_id"));
                ca.setActivo(rs.getBoolean("activo"));
                ca.setCreadoEn(rs.getTimestamp("creado_en"));
                ca.setActualizadoEn(rs.getTimestamp("actualizado_en"));
                list.add(ca);
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return list;
    }

    // Leer por ID
    public ConservationActivities findById(int id) {
        ConservationActivities ca = null;
        String sql = "SELECT * FROM conservation_activities WHERE id = ?";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setInt(1, id);
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                ca = new ConservationActivities();
                ca.setId(rs.getInt("id"));
                ca.setNombreActividad(rs.getString("nombre_actividad"));
                ca.setFechaActividad(rs.getString("fecha_actividad"));
                ca.setResponsable(rs.getString("responsable"));
                ca.setTipoActividadId(rs.getInt("tipo_actividad_id"));
                ca.setZonaId(rs.getInt("zona_id"));
                ca.setActivo(rs.getBoolean("activo"));
                ca.setCreadoEn(rs.getTimestamp("creado_en"));
                ca.setActualizadoEn(rs.getTimestamp("actualizado_en"));
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return ca;
    }

    // Actualizar
    public void update(ConservationActivities ca) {
        String sql = "UPDATE conservation_activities SET nombre_actividad = ?, fecha_actividad = ?, responsable = ?, tipo_actividad_id = ?, zona_id = ?, activo = ?, actualizado_en = ? WHERE id = ?";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, ca.getNombreActividad());
            stmt.setString(2, ca.getFechaActividad());
            stmt.setString(3, ca.getResponsable());
            stmt.setInt(4, ca.getTipoActividadId());
            stmt.setInt(5, ca.getZonaId());
            stmt.setBoolean(6, ca.isActivo());
            stmt.setTimestamp(7, ca.getActualizadoEn());
            stmt.setInt(8, ca.getId());

            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    // Eliminación lógica
    public void delete(int id) {
        String sql = "UPDATE conservation_activities SET activo = 0 WHERE id = ?";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setInt(1, id);
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
