/*
 * JBoss, Home of Professional Open Source
 * Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual
 * contributors by the @authors tag. See the copyright.txt in the
 * distribution for a full listing of individual contributors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.vmware.unified.searchdispatcher;


import java.util.ArrayList;

import javax.inject.Inject;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * A simple CDI service which is able to say hello to someone
 *
 * @author Pete Muir
 *
 */
public class SearchService {
	
	public SearchService() {
		esClient = new ElasticSearchClient();
	}
	ElasticSearchClient esClient;
    @SuppressWarnings("unchecked")
	public String DispatchSearchRequest(String input) {
    	System.out.println("search input=" + input);
        String res = esClient.query(input);
        JSONObject job = new JSONObject(res);
       // if(job.has("hits") && Integer.parseInt(((JSONObject)job.get("hits")).getString("total")) > 0) {
        if(job.has("hits")) {
        	System.out.println("hits found");
        	JSONObject hits = job.getJSONObject("hits");
        	
        	
        	JSONArray hitsitem = hits.getJSONArray("hits");

        	for(int i = 0; i < hitsitem.length(); i ++) {
        		JSONObject bug = hitsitem.getJSONObject(i);
        		JSONObject source = bug.getJSONObject("_source");
        		String filteredText = SearchResultFilter.FilterText(source.getString("text"), input);
        		String filteredSummary = SearchResultFilter.FilterSummary(source.getString("summary"), input);
        		
        		source.put("text", filteredText);
        		source.put( "summary", filteredSummary);
        		System.out.println(filteredText.length());
        		bug.put("_source", source);
        		hitsitem.put(i, bug);
        		
        	}
        	
        	hits.put("hits", hitsitem);
        	job.put("hits", hits);
        	
        }
        
        res = job.toString();
		return res;
        
    }

}
