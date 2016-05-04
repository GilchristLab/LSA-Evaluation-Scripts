'''
Kevin Dunn

This program takes 7 weights and evaluates a student responses to a question using the metrics: Length, Reading level, similarity to instructor, vocabulary usage, number of capital letters used, reflective words used, and conjunctive words used.

It takes the students responses from a file named 'inputData.txt' and writes the output to a file titled 'output.txt'

'''


# -*- coding: UTF-8 -*-
import sys;
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import io
import warnings
import re
import string



def main(v1, v2, v3, v4, v5, v6, v7):
	#This should be changed to whatever vocabulary list is relevant to the respective course;
	vocabularyWordsList = ["allele", "allele frequency", "allele-specific oligonucleotide testing", "allelic heterogeneity", "allelic variant of unknown significance", "alternate paternity", "Mutation scanning", "Sequence analysis", "analyte", "aneuploidy", "anticipation", "array comparative genomic hybridization", "Ashkenazi Jewish", "autosomal", "autosomal dominant", "autosomal recessive", "background risk", "band", "band level", "base pair", "benign variant", "Carrier", "carrier rate", "carrier testing", "centimorgan", "chromosomal microarray", "chromosome breakage studies", "cis configuration", "clone", "coding region", "codon", "comparative genomic hybridization", "compound heterozygote", "conformation-sensitive gel electrophoresis", "congenital", "consanguinity", "consultand", "contiguous gene syndrome", "cosegregation", "critical region", "crossing over", "cryptic chromosome translocation", "CSGE", "custom mutation analysis", "custom prenatal testing", "cytogenetics", "de novo mutation", "deletion", "deletion analysis", "duplication analysis", "denaturing gradient gel electrophoresis", "densitometry", "derivative chromosome", "DGGE", "diagnostic testing", "diploid", "direct DNA analysis", "disease-causing mutation", "DNA", "DNA banking", "DNA-based testing", "domain", "dominant", "dominant negative mutation", "dosage analysis", "double heterozygote", "duplication", "dysmorphology", "enzyme assay", "euploid", "exon", "exon scanning", "false negative result", "false paternity", "false positive result", "familial", "family history", "family-specific mutation", "first-degree relative", "FISH", "FISH-interphase", "FISH-metaphase", "flanking marker", "flanking microsatellite analysis", "fluorescent in situ hybridization", "founder effect", "frameshift mutation", "full penetrance allele", "gametogenesis", "gene", "gene conversion", "gene product", "gene symbol", "gene therapy", "gene transfer", "genetic counseling", "genetic predisposition", "genome", "genotype", "genotype-phenotype correlation", "genotyping", "germline", "germline mosaicism", "germline mutation", "gonadal mosaicism", "Haploid", "haploinsufficiency", "haplotype analysis", "hemizygous", "heteroplasmy", "heterozygote", "high-resolution chromosome studies", "homologous chromosomes", "homozygote", "hotspot mutation region", "immunohistochemistry", "imprinting", "in-frame mutation", "incomplete autosomal dominant", "informativeness", "informed consent", "insertion", "interfamilial variability", "intrafamilial variability", "intragenic marker", "intron", "intronic mutation", "inversion", "isoelectric focusing", "isoforms", "isolated", "karyotype", "kindred", "Known family-specific mutations", "linkage", "linkage analysis", "locus", "locus heterogeneity", "locus name", "loss of heterozygosity", "lyonization", "manifesting carrier", "mapped gene", "marker", "marker chromosome", "Related Terms: supernumary chromosome", "maternal contamination", "methylation", "methylation analysis", "microdeletion syndrome", "microsatellite", "microsatellite instability", "microsatellite instability testing", "mismatch repair mechanism", "missense mutation", "mitochondrial inheritance", "mode of inheritance", "molecular genetic testing", "monosomy", "mosaicism", "multifactorial inheritance", "mutable normal allele", "mutation", "mutation scanning", "Mutation scanning of select exons", "negative predictive value", "newborn screening", "nonsense mutation", "northern blot", "novel mutation", "nucleotide", "null allele", "obligate carrier", "obligate heterozygote", "open reading frame", "paracentric inversion", "parent-of-origin studies", "parentage testing", "PCR", "pedigree", "penetrance", "pericentric inversion", "phenotype", "phenotyping", "pleiotropy", "point mutation", "polygenic", "polymerase chain reaction (PCR)", "polymorphism", "polyploidy", "population risk", "positional cloning", "positive predictive value", "post-zygotic event", "predisposing mutation", "predispositional testing", "preimplantation diagnosis", "prenatal diagnosis", "presymptomatic testing", "private mutation", "proband", "probe", "promoter region", "protein analysis", "protein expression", "protein functional assay", "protein truncation testing", "pseudodominant inheritance", "pseudogene", "quantitative PCR", "radiosensitivity testing", "reading frame", "rearrangement", "recessive", "reciprocal translocation", "recombination", "recurrence risk", "reduced penetrance allele", "reflex testing", "replication analysis", "restriction fragment length polymorphism", "restriction fragment length polymorphism analysis", "restriction site", "risk assessment", "risk assessment modification", "RNA", "Robertsonian translocation", "screening", "second-degree relative", "segregation", "sensitivity", "sequence alteration", "sequence analysis", "simplex case", "single-stranded conformational polymorphism", "sister chromatid exchange", "somatic mosaicism", "Southern blot", "specificity", "splice-site mutation", "splicing", "sporadic", "SSCP", "subtelomeric FISH screen", "subtelomeric region", "supernumary chromosome", "susceptibility gene", "targeted analysis for pathogenic variants", "Targeted mutation analysis=", "telomere", "trans configuration", "transcription", "transcription factor", "translation", "translocation", "trinucleotide repeat", "trinucleotide repeat testing", "trisomy", "trisomy rescue", "unaffected", "unequal crossing over", "uniparental disomy", "uniparental disomy study", "variable expressivity", "variable number tandem repeats", "western blot", "wild-type allele", "X-chromosome inactivation", "X-chromosome inactivation study", "X-linked dominant", "X-linked lethal", "X-linked recessive", "zygosity testing"]



	output = open("output.txt", "w+")

	#The formula for generating a person's score is score = metric * scalar * weight + metric * scalar * weight ...
	#Assign the weights of each metric. For example, if you believe length is more inportant that reading level, you would give length a higher percentage of the final score. All the weights should probably add to 100
        lengthWeight = v1;
        similarityToInstructorWeight = v2;
        difficultyWeight = v3;
        numberOfCapitalLettersPerSentenceWeight = v4;
        vocabWordWeight = v5;
        conjunctiveWordWeight = v6;
	reflectiveWordWeight = v7;


	#The scalars are so that each metric will have the same order of magnitude. Ideally, when a metric is multiplied by it's scalar, it will on average be equal to every other metric multiplied by their respective scalars. 
	lengthScalar = .02068;
	similarityToInstructorScalar = 45.45;
	difficultyScalar = .407;
	numberOfCapitalLettersPerSentenceScalar = .744;
	vocabWordScalar = 1.98;
	conjunctiveWordScalar = 12.5;
	reflectiveWordScalar = 5.5;


	#This will be used to remove any characters that are not printable
	printable = set(string.printable)

	def textLength (text):
		return len(text);

	#Counts and returns the number of relective words used 
	def reflectiveRating (text):

		listOfReflectiveWords = ['attention', 'answer', 'answers', 'concept', 'concepts', 'effort', 'lecture', 'lectures', 'note', 'notes', 'notecards', 'notecard',  'problem', 'problems',  'quiz', 'quizzes', 'review', 'slide', 'slides', 'test',	'tests', 'time', 'topic', 'topics', 'answer', 'answered', 'answers', 'compare',	'compared', 'compares'  'confuse', 'confused', 'confuses', 'describe', 'described', 'describes', 'determine', 'determined', 'determines', 'develop',  'developed'  'developes', 'discuss', 'discussed',	'discusses', 'explain',	'explained', 'explanes', 'feel', 'felt', 'feels', 'help', 'helped', 'helps', 'know', 'knew', 'knows', 'learn', 'learned', 'learns', 'master', 'mastered', 'masters', 'need',	'needed', 'needs', 'plan', 'planned', 'plans', 'prefer', 'preferred', 'prefers', 'quiz', 'quizzed', 'quizzes', 'read',	'reads', 'review', 'reviewed', 'reviews', 'study', 'studied', 'studies', 'test', 'tested', 'tests', 'think', 'thought',	'thinks', 'understand',	'understood', 'understands', 'because', 'challenge', 'challenging', 'compare',	'comparison', 'comparable', 'confident', 'confidence', 'confuse', 'confused', 'difficult', 'difficulty', 'extra', 'good', 'how', 'important', 'importance', 'more', 'most', 'new', 'useful', 'well', 'why']

		reflectiveWords = 0;
		text = text.split()
		for word in text:
			word = word.lower();
			if(word in listOfReflectiveWords):
				reflectiveWords += 1;

		return reflectiveWords;

	#Counts and returns the number of conjunctive words used 
	def numberOfConjenctiveWords(text):
		text.lower()
		listOfConjunctiveWords = ['accordingly', 'again', 'also', 'as a result', 'besides', 'consequently', 'finally', 'for example', 'further', 'furthermore', 'hence', 'however', 'in addition', 'indeed', 'in fact', 'in particular', 'we reject', 'instead', 'likewise', 'meanwhile', 'moreover', 'namely', 'nevertheless', 'of course', 'otherwise', 'still', 'that is', 'then', 'therefore', 'thus', 'similarly', 'anyway', 'incidentally', 'next', 'thereafter', 'certainly', 'nonetheless', 'now', 'undoubtedly']


		conjunctiveWords = 0;
		for word in listOfConjunctiveWords:
			conjunctiveWords += text.count(word);
		

		return conjunctiveWords

	#Counts and returns the number of words used that are in the previous vocabulary list. 
	def numberOfVocabWords (text):
		text.lower()
		numberOfVocabularyWords = 0;
		for word in vocabularyWordsList:
			numberOfVocabularyWords += text.count(word);
			
		return numberOfVocabularyWords; 

	#Counts and returns the capital letters used
	def numberOfCapitalLettersPerSentence (text):
		capitalLetterCount = 0;
		
		for letter in text:
			if (letter.isupper()):
				capitalLetterCount += 1;

		return capitalLetterCount;
		
	#The reading level for the program is based on the Coleman_Laiu index. It is essentially finding the number of words in a sentence, and number of letters in the average word and applying a formula to those variables.
	def readingLevel (text):

		sents = sent_tokenize(text)

		words = word_tokenize(text);
		
		content = []
		for word in words:
			if(word.decode('utf8') not in stopwords.words('english')):
				content.append(word);

		
		
		lengthOfText = len(text) - text.count('"') - text.count(',') - text.count('!') - text.count(' ') - text.count('.');
		numberOfLettersPer100Words = 0;
		numberOfSentences = 0;

		text = text.split()
		wordCounter = 0;
		wordCounter = len(text) 
		numberOfSentences = len(sents) 
		
		if(wordCounter == 0):
			return 0;
		
		numberOfLettersPer100Words = lengthOfText * 1.0 / wordCounter * 100;
		numberOfSentencesPer100Words = numberOfSentences * 1.0 / wordCounter * 100;

		#This is the formula for the Coleman_Laiu index
		difficultyLevel = .0588 * numberOfLettersPer100Words - .296 * numberOfSentencesPer100Words - 15.8
		return difficultyLevel;
			
	#Counts number of words used in the student response that is also used in the instructor response. Common words such as 'The' 'A' 'and' are not counted.
	def similarityToInstructor (text1, instructorAnswer):
		text1.lower()
		instructorAnswer.lower()
		text1Set = word_tokenize(text1) 
		text2Set = word_tokenize(instructorAnswer)
		Stopwords = stopwords.words('english')
		Stopwords.append(',')
		Stopwords.append('.')
		content1 = []
		content2 = []


		for word in text1Set:
			if(word not in Stopwords):
				content1.append(word);

		for word in text2Set:
			if(word not in Stopwords):
				content2.append(word);

		totalWords = len(content1);	
		totalCommonWords = 0;
		for word in content1:
			if(word in content2):
				totalCommonWords += 1;

		if(totalWords == 0):
			return 0;
		
		return totalCommonWords * 1.0 / totalWords
			
	#This function just calls all the functions and creates arrays for the various scores
	def createScoresArrays(line, instructorAnswer):
		newText = "";
		for letter in line:
			if letter in printable:
				newText += letter;
		line = newText;

		textSize = textLength(line);
		vocabularyUsage = numberOfVocabWords(line);
		difficultyLevel = readingLevel(line);
		similarity = similarityToInstructor(line, instructorAnswer);
		reflectiveWords = reflectiveRating(line);
		capitalLetters = numberOfCapitalLettersPerSentence(line);
		conjunctiveWords = numberOfConjenctiveWords(line);
		
		lengthScores.append(textSize);
		vocabScores.append(vocabularyUsage);
		difficultyScores.append(difficultyLevel);
		similarityToInstructorScores.append(similarity);
		capitalLetterScores.append(capitalLetters);
		conjunctiveScores.append(conjunctiveWords);
		reflectiveScores.append(reflectiveWords);

	
	lengthScores = [];
	vocabScores = [];
	difficultyScores = [];
	similarityToInstructorScores = [];
	capitalLetterScores = [];
	conjunctiveScores = [];
	reflectiveScores = [];
		

	f = open('inputData.txt', 'r')

	text = f.read()

	instructorAnswer = "";
	with open('inputData.txt') as f:
		lines = f.readlines()



	finalScores = []
	for line in lines:
		#This assumes theres a tab seperating the instructor's ID and their answer;
		tmp = line.split('\t');
		#The instuctors ID should be ID000
		if("ID000" in line):
			instructorAnswer = line;
			lines.remove(line);
			
		#Remove blank lines
		if(line in ['\n', "\r\n"]):
			lines.remove(line);


	for line in lines:
		createScoresArrays(line, instructorAnswer);

	#Tally the scores by multiplying each metric by its scalar and weight
	for i, val in enumerate(lengthScores):
		score = 0;
		score = lengthScores[i] * lengthWeight * lengthScalar
		score += similarityToInstructorScores[i] * similarityToInstructorWeight * similarityToInstructorScalar
		if(difficultyScores[i] < 0):
			difficultyScores[i] = 0
		score += difficultyScores[i] * difficultyWeight * difficultyScalar
		score += capitalLetterScores[i] * numberOfCapitalLettersPerSentenceWeight * numberOfCapitalLettersPerSentenceScalar
		score += vocabScores[i] * vocabWordWeight * vocabWordScalar
		score += conjunctiveScores[i] * conjunctiveWordWeight * conjunctiveWordScalar
		score += reflectiveScores[i] * reflectiveWordWeight * reflectiveWordScalar
		finalScores.append( (score, lines[i]) );

	finalScores.sort()
	#output the student IDs and respective scores
	for score in finalScores:
		line = score[1];
		line = line.rstrip()
		matchObj = re.match(r'^(ID[0-9][0-9][0-9])', line);
		netID = matchObj.group(1);
		print >>output, netID + "  " + str(score[0]);
		print >>output, "\n"
		
	f.close()

if __name__ == "__main__":
        main(25, 10, 20, 5, 25, 15, 10);
