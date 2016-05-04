#This program just finds how many questions a student answered.
#This assumes the LSAs can be found in ../Anonymous.LSAs

import os;
from subprocess import Popen, PIPE

p = Popen(['python', 'runCreateLSAs.py'], stdin=PIPE, stdout=PIPE);
p.communicate('1');

f1 = open("output.html");
studentsToQuestionsAnswered={};

for line in f1:
	lineArray = line.split('\t');
	ID = lineArray[0];
	if(ID not in studentsToQuestionsAnswered):
		studentsToQuestionsAnswered[ID] = [0, 0, 0, 0];
	studentsToQuestionsAnswered[ID][0] += 1;
	

p = Popen(['python', 'runCreateLSAs.py'], stdin=PIPE, stdout=PIPE);
p.communicate('3');

f1 = open("output.html");
for line in f1:
	lineArray = line.split('\t');
	ID = lineArray[0];
	if(ID not in studentsToQuestionsAnswered):
		studentsToQuestionsAnswered[ID] = [0, 0, 0, 0];
	studentsToQuestionsAnswered[ID][1] += 1;
	

p = Popen(['python', 'runCreateLSAs.py'], stdin=PIPE, stdout=PIPE);
p.communicate('4');

f1 = open("output.html");
for line in f1:
	lineArray = line.split('\t');
	ID = lineArray[0];
	if(ID not in studentsToQuestionsAnswered):
		studentsToQuestionsAnswered[ID] = [0, 0, 0, 0];
	studentsToQuestionsAnswered[ID][2] += 1;
	

p = Popen(['python', 'runCreateLSAs.py'], stdin=PIPE, stdout=PIPE);
p.communicate('7');

f1 = open("output.html");
for line in f1:
	lineArray = line.split('\t');
	ID = lineArray[0];
	if(ID not in studentsToQuestionsAnswered):
		studentsToQuestionsAnswered[ID] = [0, 0, 0, 0];
	studentsToQuestionsAnswered[ID][3] += 1;
	

for ID in studentsToQuestionsAnswered:
	totalQuestionsAnswered = 0;
	for questionCounter in range(0, 4):
		totalQuestionsAnswered += studentsToQuestionsAnswered[ID][questionCounter]
	studentsToQuestionsAnswered[ID].append(totalQuestionsAnswered);
		
		

print studentsToQuestionsAnswered
