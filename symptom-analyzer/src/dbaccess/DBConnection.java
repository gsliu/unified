package dbaccess;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class DBConnection {
	private static DBConnection dbc;
	private Connection con; 
	private DBConnection() {

		try {
			con = DriverManager.getConnection("jdbc:mariadb://unified.eng.vmware.com/unified", "root",
					"vmware");

		} catch (Exception e) {
			System.out.println(e.toString());
		}

	}

	public static DBConnection getInstance() {
		if (dbc == null) {
			dbc = new DBConnection();
		}
		return dbc;
	}
	
	public ResultSet query(String statement) throws SQLException {
		Statement stmt = null;
		ResultSet rs = null;
		stmt = con.createStatement();
		try {
			rs = stmt.executeQuery(statement);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return rs;
		
	}

}
