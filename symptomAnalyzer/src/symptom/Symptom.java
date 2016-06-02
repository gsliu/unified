package symptom;

import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Symptom implements IMatchable {
	
	private Pattern regex;
	private String version;
	private String product;
	private ArrayList<String> tags;
	
	
	public Symptom(String reg) {
		regex = Pattern.compile(reg);
	}

	

	@Override
	public boolean matchPattern(String input, Symptom symptom) {
		 Matcher m = regex.matcher(input);
		 boolean b = m.matches();
		 return b;
	}

}
