package test;

import static org.junit.Assert.*;

import org.junit.Test;

import dbaccess.KnowledgeBaseAccess;
import resource.KnowledgeBase;

public class KnowledgeBaseAccessTest {

	@Test
	public void test() {
		KnowledgeBase kb = KnowledgeBaseAccess.read(2013437);
		System.out.println(kb.toString());
	}

}
