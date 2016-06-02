package com.vmware.unified.searchdispatcher;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

public class SearchResultFilter {

	
	public static String FilterText(String text, String query) {
		ArrayList<String> keywords = new ArrayList<String>(Arrays.asList(query.split(" "))); 
		
		
		
		
		
		String ret = "";

		System.out.println(keywords.toString());
		for(int i = 0; i < keywords.size() ; i ++) {
			int pos = text.indexOf(keywords.get(i));
			if(pos != -1) {
				int start = pos - 200;
				int end = pos + 200;
				if(start < 0) {
					start = 0;
				}
				if(end >= text.length()) {
					end = text.length() - 1;
				}
				System.out.println("start=" + start + "end=" + end + "size=" + text.length());
				ret += text.substring(start, end);
			}
			System.out.println(ret);
		}
		
		if(ret.length() > 400) {
			ret = ret.substring(0, 180);
		}
		
		
		for(int i = 0; i < keywords.size() ; i ++) {
			ret = ret.replaceAll("/" + keywords.get(i) + "/", "<b>" + keywords.get(i) + "</b>");
		}
		
		return ret;
	}

	public static String FilterSummary(String summary, String query) {
		if (summary.length() > 60){
			summary = summary.substring(0, 60);
			summary += "...";
		}
		return summary;

	}

}
