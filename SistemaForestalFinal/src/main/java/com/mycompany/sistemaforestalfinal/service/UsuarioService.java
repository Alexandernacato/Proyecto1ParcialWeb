/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.sistemaforestalfinal.service;

import com.mycompany.sistemaforestalfinal.dao.UsuarioDAO;
import com.mycompany.sistemaforestalfinal.model.Usuario;
import java.sql.SQLException;
import com.mycompany.sistemaforestalfinal.security.PasswordUtil;
import java.util.Optional;

/**
 *
 * @author Administrador
 */
public class UsuarioService {
   private final UsuarioDAO usuarioDAO = new UsuarioDAO();

    public Usuario autenticar(String username, String password) throws SQLException {
        Usuario user = usuarioDAO.obtenerPorUsername(username);
        if (user != null) {
            String hashedPassword = PasswordUtil.sha256(password);
            if (user.getPassword().equalsIgnoreCase(hashedPassword)) {
                return user;  // Contraseña válida
            }
        }
        return null;  // No autenticado
    }
}
