'''
Kevin Dunn

This program outputs the average of the self-identified student understanding level
'''

import operator;
import sys;

f1 = open("output.html", 'r')

understandingLevels = ["0 -- General lack of understanding of terms and ideas.", "0.5", "1 --Limited understanding: Could define key terms and topics", "1.5", "2 -- Basic understanding: Could discuss or explain topic with another student.","2.5", "3 -- Solid understanding: Could apply knowlege to solve basic problems.", "3.5", "4 -- Advanced understanding: Could analyze complex scenarios that require knowlege of more subtle points.", "4.5", "5 -- Deep understanding: Could  interpret and predict behavior of system in novel contexts"];

studentUnderstanding = {};

for line in f1:
	lineItems = line.split('\t');
	if(lineItems[0] not in studentUnderstanding):
		studentUnderstanding[lineItems[0]] = []; 
	studentUnderstanding[lineItems[0]].append(understandingLevels.index(lineItems[1].strip()));


#sorted_x = sorted(similarityToInstructor.items(), key=operator.itemgetter(1))

#print sorted_x;

for key in sorted(studentUnderstanding):
	sys.stdout.write("\'" + key + "\': " + str(sum(studentUnderstanding[key])) + ", ");
