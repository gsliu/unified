package resource;

import java.util.ArrayList;


public class KnowledgeBase {
	private String title;
	private String symptoms;
	private String resolution;
	private String solution;
	private String cause;
	

	private String purpose;
	private String details;
	private String tags;
	private String version;
	private String product;
	private int id;
	private String url;
	
	public String toString() {
		String print = "";
		print = this.getUrl() + "\n" +
				this.getSymptoms() + "\n" +
				this.getCause() + "\n" +
				this.getDetails() + "\n" +
				this.getPurpose() + "\n" +
				this.getResolution() + "\n" +
				this.getSolution() + "\n" +
				this.getProduct() + "\n" +
				this.getVersion() + "\n" +
				this.getTags() + "\n" ;
		return print;
				
	}
	public String getTitle() {
		return title;
	}


	public void setTitle(String title) {
		this.title = title;
	}


	public String getSymptoms() {
		return symptoms;
	}


	public void setSymptoms(String symptoms) {
		this.symptoms = symptoms;
	}


	public String getResolution() {
		return resolution;
	}


	public void setResolution(String resolution) {
		this.resolution = resolution;
	}


	public String getSolution() {
		return solution;
	}


	public void setSolution(String solution) {
		this.solution = solution;
	}


	public String getCause() {
		return cause;
	}


	public void setCause(String cause) {
		this.cause = cause;
	}


	public String getPurpose() {
		return purpose;
	}


	public void setPurpose(String purpose) {
		this.purpose = purpose;
	}


	public String getDetails() {
		return details;
	}


	public void setDetails(String details) {
		this.details = details;
	}


	public String getTags() {
		return tags;
	}


	public void setTags(String tags) {
		this.tags = tags;
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


	public int getId() {
		return id;
	}


	public void setId(int id) {
		this.id = id;
	}


	public String getUrl() {
		return url;
	}


	public void setUrl(String url) {
		this.url = url;
	}

	
	public ArrayList<String> splitIntoStrings() {
		// TODO Auto-generated method stub
		return null;
	}


}
