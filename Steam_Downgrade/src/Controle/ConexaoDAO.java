/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Controle;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import javax.swing.JOptionPane;

/**
 *
 * @author artur
 */
public class ConexaoDAO {
    
    public static Connection conectaBD(){/*Faz a conexão com o banco de dados mysql local*/
       Connection conn = null;
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            conn = DriverManager.getConnection("jdbc:mysql://localhost/usuarios", "root", "246810");
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
        
        return conn;
    }
    
}
