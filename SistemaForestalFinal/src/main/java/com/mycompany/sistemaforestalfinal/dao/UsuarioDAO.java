/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.sistemaforestalfinal.dao;

import com.mycompany.sistemaforestalfinal.model.Usuario;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;


/**
 *
 * @author Administrador
 */
public class UsuarioDAO {
    public Usuario obtenerPorUsername(String username) throws SQLException {
        String sql = "SELECT * FROM usuarios WHERE username = ? AND activo = 1";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, username);

            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    Usuario u = new Usuario();
                    u.setId(rs.getInt("id"));
                    u.setUsername(rs.getString("username"));
                    u.setPassword(rs.getString("password"));
                    u.setEmail(rs.getString("email"));
                    u.setNombreCompleto(rs.getString("nombre_completo"));
                    u.setRol(rs.getString("rol"));
                    u.setActivo(rs.getBoolean("activo"));
                    return u;
                }
            }
        }

        return null;
    }
    
public Usuario autenticar(String username, String password) throws SQLException {
    Usuario usuario = obtenerPorUsername(username);
    if (usuario != null && usuario.getPassword().equals(password)) {
        return usuario;
    }
    return null;
}


   // Método para registrar un nuevo usuario
    public boolean registrarUsuario(Usuario usuario) throws SQLException {
        String sql = "INSERT INTO usuarios (username, password, email, nombre_completo, rol, activo) VALUES (?, ?, ?, ?, ?, ?)";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, usuario.getUsername());
            stmt.setString(2, usuario.getPassword());  // Aquí también debería ser un hash
            stmt.setString(3, usuario.getEmail());
            stmt.setString(4, usuario.getNombreCompleto());
            stmt.setString(5, usuario.getRol());
            stmt.setBoolean(6, usuario.isActivo());

            int rowsAffected = stmt.executeUpdate();
            return rowsAffected > 0;
        }
    }

    // Método para editar un usuario
    public boolean editarUsuario(Usuario usuario) throws SQLException {
        String sql = "UPDATE usuarios SET username = ?, password = ?, email = ?, nombre_completo = ?, rol = ?, activo = ? WHERE id = ?";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, usuario.getUsername());
            stmt.setString(2, usuario.getPassword());  // Debería ser un hash
            stmt.setString(3, usuario.getEmail());
            stmt.setString(4, usuario.getNombreCompleto());
            stmt.setString(5, usuario.getRol());
            stmt.setBoolean(6, usuario.isActivo());
            stmt.setInt(7, usuario.getId());

            int rowsAffected = stmt.executeUpdate();
            return rowsAffected > 0;
        }
    }

    // Método para eliminar un usuario
    public boolean eliminarUsuario(int id) throws SQLException {
        String sql = "DELETE FROM usuarios WHERE id = ?";

        try (Connection conn = ConnectionBdd.getConexion();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setInt(1, id);

            int rowsAffected = stmt.executeUpdate();
            return rowsAffected > 0;
        }
    }
}
