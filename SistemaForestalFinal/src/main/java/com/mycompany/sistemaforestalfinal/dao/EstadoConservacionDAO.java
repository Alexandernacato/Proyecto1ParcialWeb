package com.mycompany.sistemaforestalfinal.dao;

import com.mycompany.sistemaforestalfinal.model.EstadoConservacion;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class EstadoConservacionDAO {

    // Método original con conexión externa
    public List<EstadoConservacion> getAllEstados(Connection conn) throws SQLException {
        List<EstadoConservacion> lista = new ArrayList<>();
        String sql = "SELECT id, nombre FROM estado_conservacion";

        try (PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                EstadoConservacion ec = new EstadoConservacion();
                ec.setId(rs.getInt("id"));
                ec.setNombre(rs.getString("nombre"));
                lista.add(ec);
            }
        }
        return lista;
    }

    // Método nuevo que abre y cierra la conexión internamente
    public List<EstadoConservacion> getAllEstados() throws SQLException {
        try (Connection conn = getConnection()) {
            return getAllEstados(conn);
        }
    }

    // Método original con conexión externa
    public EstadoConservacion getEstadoById(Connection conn, int id) throws SQLException {
        String sql = "SELECT id, nombre FROM estado_conservacion WHERE id = ?";
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    EstadoConservacion ec = new EstadoConservacion();
                    ec.setId(rs.getInt("id"));
                    ec.setNombre(rs.getString("nombre"));
                    return ec;
                }
            }
        }
        return null;
    }

    // Método nuevo que abre y cierra la conexión internamente
    public EstadoConservacion getEstadoById(int id) throws SQLException {
        try (Connection conn = getConnection()) {
            return getEstadoById(conn, id);
        }
    }

    // Método para obtener la conexión a la base de datos
    private Connection getConnection() throws SQLException {
        // Cambia estos valores por los de tu base de datos
        String url = "jdbc:mysql://localhost:3306/tu_base_de_datos";
        String user = "tu_usuario";
        String password = "tu_contraseña";

        return DriverManager.getConnection(url, user, password);
    }
}
