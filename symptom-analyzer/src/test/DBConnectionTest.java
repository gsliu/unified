package test;

import static org.junit.Assert.*;

import java.sql.ResultSet;
import java.sql.SQLException;

import org.junit.Test;

import dbaccess.DBConnection;

public class DBConnectionTest {

	@Test
	public void test()   {
		DBConnection dbc = DBConnection.getInstance();
		try {
			ResultSet rs = dbc.query("SELECT * FROM `kb` WHERE id = 2013437");
					while (rs.next()) {
						System.out.println(rs.getString("id"));
						System.out.println(rs.getString("title"));
						System.out.println(rs.getString("symptoms"));
						System.out.println(rs.getString("resolution"));
					}		    
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
