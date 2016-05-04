#Kevin Dunn

'''
This program calls the createLSAScript for each LSA in the Anonymous.LSAs/LSA folder. It takes the question you are interested in via stdin and create a file named output.html that contains all the responses to the specified question. It will overwrite any existing data in output.html

It assumes that all the LSAs are titled 'LSA' + LSA Number + '.html';

'''

#These should be adjusted to the lowest and highest LSAs you are currently using. For example, if the lowest LSA you are using is titled "LSA2" lowestLSANumnber would be set to 2. The same applies to highestLSANumber;
lowestLSANumber = 2;
highestLSANumber = 15;
#This variable should be the path to the folder that contains LSAs
folderContainingLSAs = "../Anonymous.LSAs/"
#This variable should be the name you want for the output file
outputFileName = 'output.html';

import os
from subprocess import Popen, PIPE

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
createIndex = raw_input();
while(createIndex <= '0' or createIndex > '9'):
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
        createIndex = raw_input();
print "Running"






f = open('output.html', 'w+');
for i in range(lowestLSANumber, highestLSANumber + 1):
	p = Popen(['python', 'createLSA.py', folderContainingLSAs + "LSA" + str(i) + '.html', outputFileName], stdin=PIPE, stdout=PIPE);
	p.communicate(input=createIndex)[0];

