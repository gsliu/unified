package symptom;

import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class Symptom implements IMatchable {
	
	private Pattern regex;
	private String version;
	private String product;
	private ArrayList<String> tags;
	
	public Pattern getRegex() {
		return regex;
	}



	public void setRegex(Pattern regex) {
		this.regex = regex;
	}



	public String getVersion() {
		return version;
	}



	public void setVersion(String version) {
		this.version = version;
	}



	public String getProduct() {
		return product;
	}



	public void setProduct(String product) {
		this.product = product;
	}



	public ArrayList<String> getTags() {
		return tags;
	}



	public void setTags(ArrayList<String> tags) {
		this.tags = tags;
	}




	
	
	public Symptom(String reg) {
		regex = Pattern.compile(reg);
	}

	

	public boolean matchPattern(String input, Symptom symptom) {
		 Matcher m = regex.matcher(input);
		 boolean b = m.matches();
		 return b;
	}


}
