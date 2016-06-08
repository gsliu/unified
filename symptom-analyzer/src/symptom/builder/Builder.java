package symptom.builder;

import java.util.ArrayList;

import resource.KnowledgeBase;
import symptom.algorithm.Algorithm;
import symptom.Symptom;
import symptom.convertor.Convertor;

public abstract class Builder {
	
	Algorithm ag;
	Convertor co;
	
	public Algorithm getAg() {
		return ag;
	}

	public void setAg(Algorithm ag) {
		this.ag = ag;
	}

	public Convertor getCo() {
		return co;
	}

	public void setCo(Convertor co) {
		this.co = co;
	}

	public KnowledgeBase getAr() {
		return ar;
	}

	public void setAr(KnowledgeBase ar) {
		this.ar = ar;
	}

	KnowledgeBase ar;
	
	public ArrayList<Symptom> build() {
		ArrayList<Symptom> symptoms;;
		
		ArrayList<String> input = ar.splitIntoStrings();
		ArrayList<String> possibleRegs = ag.find(input);
		symptoms = co.convert(possibleRegs);
		return symptoms;
	}

}
