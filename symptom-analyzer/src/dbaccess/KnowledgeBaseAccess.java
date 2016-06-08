package dbaccess;

import java.sql.ResultSet;
import java.sql.SQLException;

import resource.KnowledgeBase;

public class KnowledgeBaseAccess {

	public static KnowledgeBase read(int id) {
		// TODO Auto-generated method stub
		String stateMent = "SELECT * FROM `kb` WHERE id = " + id;
		KnowledgeBase kb = null;
		DBConnection dbc = DBConnection.getInstance();
		try {
			kb = new KnowledgeBase();
			ResultSet rs = dbc.query(stateMent);
					while (rs.next()) {
						kb.setId(rs.getInt("id"));
						kb.setCause(rs.getString("cause"));
						kb.setDetails(rs.getString("details"));
						kb.setProduct(rs.getString("product"));
						kb.setPurpose(rs.getString("purpose"));
						kb.setResolution(rs.getString("resolution"));
						kb.setSolution(rs.getString("solution"));
						kb.setTitle(rs.getString("title"));
						kb.setSymptoms(rs.getString("symptoms"));
						kb.setTags(rs.getString("tags"));
						kb.setUrl(rs.getString("url"));
						kb.setVersion(rs.getString("version"));
					}		    
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return kb;
	}

	public static boolean write(KnowledgeBase kb) {
		// TODO Auto-generated method stub
		return false;
	}



}
