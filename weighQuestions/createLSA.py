'''
Kevin Dunn
3/9/2016

This program reads in an html of an LSA and seperates the important elements
This is essentially a helper script for runCreateLSAs and probably should not be used alone

It takes in via stdin the question you want to create and output file for. It then parses the html file looking for the tags of that question, and when those tags are found, saves and outputs the corresponding question response.
'''
import sys
import re
import csv
import HTMLParser
reload(sys)
sys.setdefaultencoding("utf-8")

try:
        htmlFile = open(sys.argv[1], "r")
except:
        print "Opening the html document failed. Exiting";
	print "Usage: python createLSAs.py input.html output.html";
        exit(0);

try:
        outputFile = open(sys.argv[2], "a+")
except:
        print "Opening the output document failed. Exiting";
	print "Usage: python createLSAs.py input.html output.html";
        exit(0);

OUTPUT = []
studentResponses = [];

studentID = "";
isStudentID = 0;

isExplainConcepts = 0;
isExplainPhenomenon = 0 
isKnowledgeBasis = 0 
isQuantUnderstanding = 0
isChallengingConcept = 0;
isChallengingConceptComment = 0;
isAddressChallenge = 0;
isExplainPhenomenonComment = 0 
isRankTopics = 0;

createExplainConcepts = 0;
createPhenomenon = 0;
createKnowledgeBasis = 0;
createQuantUnderstanding = 0;
createChallengingConcept = 0;
createChallengingConceptComments = 0;
createAddressChallenge = 0;
createPhenomenonComment = 0;
createRankTopics = 0;

print "Which subject are do you want to create a file for?"
print "Your options are:"
print "Explain Concepts: 1"
print "Phenomenon Topic: 2"
print "Phenomenon Comment: 3"
print "Knowledge Basis: 4"
print "Quant understanding: 5"
print "Challenging Concept: 6"
print "Challenging Concept Comment: 7"
print "Address Challenge Comment: 8"
print "Rank Topics: 9"

createIndex = 0;
while(createIndex == 0):
	createIndex = raw_input();
	if(createIndex == "1"):
		createExplainConcepts = 1;
	elif(createIndex == "2"):
		createPhenomenon = 1;
	elif(createIndex == "3"):
		createPhenomenonComment = 1;
	elif(createIndex == "4"):
		createKnowledgeBasis = 1;
	elif(createIndex == "5"):
		createQuantUnderstanding = 1;
	elif(createIndex == "6"):
		createChallengingConcept = 1;
	elif(createIndex == "7"):
		createChallengingConceptComments = 1;
	elif(createIndex == "8"):
		createAddressChallenge = 1;
	elif(createIndex == "9"):
		createRankTopics = 1;
	else:
		print "Sorry, give me a number 1-9 that corrosponds to thise topics"
		print "Explain Concepts: 1"
		print "Phenomenon Topic: 2"
		print "Phenomenon Comment: 3"
		print "Knowledge Basis: 4"
		print "Quant understanding: 5"
		print "Challenging Concept: 6"
		print "Challenging Concept Comment: 7"
		print "Address Challenge Comment: 8"
		print "Rank Topics: 9"
		createIndex = 0;



#The isQuestion variable is to indicate the script just saw that tag on the previous line. The createQuestion variable is the user input indicating to create output for that specific question
for index, line in enumerate(htmlFile):

	if(isStudentID):
		matchObj = re.match(r'^<td>(.*)</td>$', line.strip());
		studentID = matchObj.group(1);
		isStudentID = 0;
	
	if(isExplainPhenomenon and createPhenomenon):
		studentResponses.append(line);
		isExplainPhenomenon = 0; 
		
	if(isExplainPhenomenonComment and createPhenomenonComment):
		studentResponses.append(line);
		isExplainPhenomenonComment = 0; 

	if(isExplainConcepts and createExplainConcepts):
		studentResponses.append(line);
		isExplainConcepts = 0; 

	if(createKnowledgeBasis and isKnowledgeBasis):
		studentResponses.append(line);
		isKnowledgeBasis = 0; 
	 
	if(createQuantUnderstanding and isQuantUnderstanding):
		studentResponses.append(line);
		isQuantUnderstanding = 0

	if(isChallengingConcept and createChallengingConcept):
		studentResponses.append(line);
		isChallengingConcept = 0;

	if(isChallengingConceptComment and createChallengingConceptComments):
		studentResponses.append(line);
                isChallengingConceptComment = 0;

	if(isAddressChallenge and createAddressChallenge):
		studentResponses.append(line);
		isAddressChallenge = 0;

	if(isRankTopics and createRankTopics):
		studentResponses.append(line);
		isRankTopics = 0;

	matchObj = re.match(r'^<td>explainConcepts\[SQ(.*)\]</td>$', line.strip());
	if(matchObj):
		isExplainConcepts = 1 
	
	
	matchObj = re.match(r'^<td>knowled?geBasis\[SQ(.*)\]</td>$', line.strip());
	if(matchObj):
		isKnowledgeBasis = 1 


	matchObj = re.match(r'^<td>phenomenon.</td>$', line.strip());
	if(matchObj):
		isExplainPhenomenon = 1 

	matchObj = re.match(r'^<td>phenomenon.\[comment\]</td>$', line.strip());
	if(matchObj):
		isExplainPhenomenonComment = 1 


	matchObj = re.match(r'^<td>quantUnderstanding\[SQ(.*)\]</td>$', line.strip());
	if(matchObj):
		isQuantUnderstanding = 1 

	matchObj = re.match(r'^<td>rankTopics\[topic(.)\]</td>$', line.strip());
	if(matchObj):
		isRankTopics = 1 

	if(line.strip() == "<td>challengingConcept</td>"):
                isChallengingConcept = 1;

	if(line.strip() == "<td>challengingConcept[comment]</td>"):
                isChallengingConceptComment = 1;

	if(line.strip() == "<td>addressChallenge</td>"):
                isAddressChallenge = 1;


	if(line.strip() == "<td>studentID[SQ003]</td>"):
                isStudentID = 1;
	

	#If a </div> is reached, that means the reponse has ended. So change the lines of the output
	if("</div>" in line and studentID != ""):
		for response in studentResponses:
			try:
				h = HTMLParser.HTMLParser()
			except:
				print response;
			response = h.unescape(response);
			response = re.sub('<td>', '', response);
			response = re.sub('</td>', '', response);
			OUTPUT.append(studentID + "\t"  + response.strip());

		studentResponses = [];
		studentID = "";

for line in OUTPUT:
	print >>outputFile, line;
