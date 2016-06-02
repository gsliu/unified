package com.vmware.unified.searchdispatcher;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.common.inject.Injector;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.InetSocketTransportAddress;
import org.elasticsearch.index.query.QueryBuilders;

import java.net.InetAddress;

public class ElasticSearchClient {
	
	private Client client;
	
	public ElasticSearchClient() {

		try {
			client = TransportClient.builder().build()
			        .addTransportAddress(new InetSocketTransportAddress(InetAddress.getByName("unified.eng.vmware.com"), 9300));
			System.out.println("succeeded to create client");
		} catch(Exception e) {
			System.out.println("failed to create client");
			System.out.println(e.toString());
		}
		 
	}
		
	public Client getClient() {
		return client;
	}
	public void setClient(Client client) {
		this.client = client;
	}
	
	public String query(String query) {
		SearchResponse response = client.prepareSearch("ikb", "bugzilla")
		        .setTypes("kb", "text")
		        //.setSearchType(SearchType.DFS_QUERY_THEN_FETCH)
		        .setQuery(QueryBuilders.queryStringQuery(query))      // Query
		        .execute()
		        .actionGet();
		return response.toString();
	}
	

}
