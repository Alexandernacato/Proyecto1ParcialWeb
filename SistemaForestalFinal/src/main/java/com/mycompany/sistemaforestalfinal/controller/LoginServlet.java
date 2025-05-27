/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/JSP_Servlet/Servlet.java to edit this template
 */
package com.mycompany.sistemaforestalfinal.controller;

import com.mycompany.sistemaforestalfinal.model.Usuario;
import com.mycompany.sistemaforestalfinal.service.UsuarioService;
import java.io.IOException;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.sql.SQLException;


/**
 *
 * @author Administrador
 */
@WebServlet(name = "LoginServlet", urlPatterns = {"/login"})
public class LoginServlet extends HttpServlet {

    private final UsuarioService usuarioService = new UsuarioService();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String username = request.getParameter("username");
        String password = request.getParameter("password");

        try {
            Usuario usuario = usuarioService.autenticar(username, password);

            if (usuario != null) {
                HttpSession session = request.getSession();
                session.setAttribute("usuario", usuario);
                session.setAttribute("userRole", usuario.getRol()); 

                String rol = usuario.getRol();
                if (rol == null) {
                    session.invalidate();
                    response.sendRedirect("login.jsp?error=true");
                } else {
                    switch (rol) {
                        case "admin":
                            response.sendRedirect("indexadmin.jsp");
                            break;
                        case "usuario":
                            response.sendRedirect("Index.jsp");
                            break;
                        default:
                            session.invalidate();
                            response.sendRedirect("login.jsp?error=true");
                            break;
                    }
                }
            } else {
                // Usuario o contraseña incorrectos
                response.sendRedirect("login.jsp?error=true");
            }
        } catch (SQLException e) {
            e.printStackTrace();
            response.sendRedirect("login.jsp?error=true");
        }
    }
}