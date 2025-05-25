package com.mycompany.sistemaforestalfinal.dao;

import com.mycompany.sistemaforestalfinal.model.Zone;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ZoneDAO {

    private static final String SELECT_ALL_ACTIVE = "SELECT * FROM zones WHERE activo = 1";
    private static final String SELECT_BY_ID = "SELECT * FROM zones WHERE id = ?";
    private static final String INSERT = "INSERT INTO zones (nombre, tipo_bosque, area_ha, activo) VALUES (?, ?, ?, 1)";
    private static final String UPDATE = "UPDATE zones SET nombre = ?, tipo_bosque = ?, area_ha = ? WHERE id = ?";
    private static final String DELETE_LOGICO = "UPDATE zones SET activo = 0 WHERE id = ?";

    public List<Zone> findAll() {
        List<Zone> zonas = new ArrayList<>();

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(SELECT_ALL_ACTIVE);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                zonas.add(mapResultSetToZone(rs));
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return zonas;
    }
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
            zones.add(z);
        }

    } catch (SQLException e) {
        e.printStackTrace();
    }

    return zones;
}

    public Zone findById(int id) {
        Zone zone = null;

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(SELECT_BY_ID)) {

            stmt.setInt(1, id);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    zone = mapResultSetToZone(rs);
                }
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return zone;
    }

public void insert(Zone zone) {
    try (Connection conn = ConnectionBdd.getConexion();
         PreparedStatement stmt = conn.prepareStatement(INSERT)) {

        stmt.setString(1, zone.getNombre());
        stmt.setString(2, zone.getTipoBosque());
        stmt.setBigDecimal(3, zone.getAreaHa());

        stmt.executeUpdate();

    } catch (SQLException e) {
        e.printStackTrace();
    }
}

public void update(Zone zone) {
    try (Connection conn = ConnectionBdd.getConexion();
         PreparedStatement stmt = conn.prepareStatement(UPDATE)) {

        stmt.setString(1, zone.getNombre());
        stmt.setString(2, zone.getTipoBosque());
        stmt.setBigDecimal(3, zone.getAreaHa());
        stmt.setInt(4, zone.getId());

        stmt.executeUpdate();

    } catch (SQLException e) {
        e.printStackTrace();
    }
}
    public void delete(int id) {
        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(DELETE_LOGICO)) {

            stmt.setInt(1, id);
            stmt.executeUpdate();

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private Zone mapResultSetToZone(ResultSet rs) throws SQLException {
        Zone zone = new Zone();
        zone.setId(rs.getInt("id"));
        zone.setNombre(rs.getString("nombre"));
        zone.setTipoBosque(rs.getString("tipo_bosque"));
        zone.setAreaHa(rs.getBigDecimal("area_ha"));
        zone.setActivo(rs.getBoolean("activo"));
        zone.setCreadoEn(rs.getTimestamp("creado_en"));
        zone.setActualizadoEn(rs.getTimestamp("actualizado_en"));
        return zone;
    }
}
