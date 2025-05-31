package com.mycompany.sistemaforestalfinal.dao;

import com.mycompany.sistemaforestalfinal.model.TipoActividad;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class TipoActividadDAO {

    // Crear
    public void insert(TipoActividad tipo) {
        String sql = "INSERT INTO tipo_actividad (nombre, descripcion, activo, creado_en, actualizado_en) VALUES (?, ?, ?, ?, ?)";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, tipo.getNombre());
            stmt.setString(2, tipo.getDescripcion());
            stmt.setBoolean(3, tipo.isActivo());
            stmt.setTimestamp(4, tipo.getCreado_en());
            stmt.setTimestamp(5, tipo.getActualizado_en());

            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    // Leer todos
    public List<TipoActividad> findAll() {
        List<TipoActividad> list = new ArrayList<>();
        String sql = "SELECT * FROM tipo_actividad WHERE activo = 1";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                TipoActividad tipo = new TipoActividad();
                tipo.setId(rs.getInt("id"));
                tipo.setNombre(rs.getString("nombre"));
                tipo.setDescripcion(rs.getString("descripcion"));
                tipo.setActivo(rs.getBoolean("activo"));
                tipo.setCreado_en(rs.getTimestamp("creado_en"));
                tipo.setActualizado_en(rs.getTimestamp("actualizado_en"));
                list.add(tipo);
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return list;
    }

    // Leer por ID
    public TipoActividad findById(int id) {
        TipoActividad tipo = null;
        String sql = "SELECT * FROM tipo_actividad WHERE id = ?";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setInt(1, id);
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                tipo = new TipoActividad();
                tipo.setId(rs.getInt("id"));
                tipo.setNombre(rs.getString("nombre"));
                tipo.setDescripcion(rs.getString("descripcion"));
                tipo.setActivo(rs.getBoolean("activo"));
                tipo.setCreado_en(rs.getTimestamp("creado_en"));
                tipo.setActualizado_en(rs.getTimestamp("actualizado_en"));
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return tipo;
    }

    // Actualizar
    public void update(TipoActividad tipo) {
        String sql = "UPDATE tipo_actividad SET nombre = ?, descripcion = ?, activo = ?, actualizado_en = ? WHERE id = ?";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, tipo.getNombre());
            stmt.setString(2, tipo.getDescripcion());
            stmt.setBoolean(3, tipo.isActivo());
            stmt.setTimestamp(4, tipo.getActualizado_en());
            stmt.setInt(5, tipo.getId());

            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    // Eliminación lógica
    public void delete(int id) {
        String sql = "UPDATE tipo_actividad SET activo = 0 WHERE id = ?";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setInt(1, id);
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
