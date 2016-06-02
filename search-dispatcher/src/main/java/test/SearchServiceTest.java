package test;

import static org.junit.Assert.*;

import org.junit.Test;

import com.vmware.unified.searchdispatcher.SearchService;

public class SearchServiceTest {

	@Test
	public void testSearch1() {
		System.out.println("hahaha");
		SearchService ss = new SearchService(); 
		String result = ss.DispatchSearchRequest("vmm");
		
		System.out.print(result);
	}
	

	@Test
	public void testConvert() {
		SearchService ss = new SearchService(); 
		String result = ss.DispatchSearchRequest("find_busiest_group");
		System.out.print("haha" + result);
	}

}
