package com.mycompany.sistemaforestalfinal.dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConnectionBdd {
        private static final String URL = "jdbc:mysql://localhost:3306/sistemaforestalfinal?useSSL=false&allowPublicKeyRetrieval=true";
    private static final String USER = "root";
    private static final String PASSWORD = "";
    
    static {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            System.err.println("No se encontro el driver JDBC");
            e.printStackTrace();
        }
    }
    
    public static Connection getConexion() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
    
}
