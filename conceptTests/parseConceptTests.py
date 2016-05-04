#this program opens up the csv files 'pretest.csv' and 'posttest.csv' and parses them before printing their contents in the form: Student id, number of questions correctly answered

import csv; 

#When this is 1, the program will output extra information, like their improvement
verbose = 0;
#Because many questions are used in the post test that are not used in the pretest, you may only want to see results showing the scores on questions that were in both tests.
onlyUseQuestionsFromBothTests = 0;

#This question map links the questions in the post test to the questions in the pretest. So if the tests change, this should be updated to have mappings from post test to pretest
questionMap = {4: 17, 6: 1, 8: 8, 9: 13, 10: 7, 11: 23, 13: 10, 15: 14, 17: 2, 18: 3, 19: 6, 24: 16, 25: 18, 26: 20, 27: 22, 28: 24, 34: 15, 35: 4, 42: 5, 43: 9, 44: 21, 45: 19, 48: 25}

#These are the respective answer keys. These can be updated to current ansewr keys.
pretestKey =['E','C','C','A','C','C','D','B','B','C','D','C','D','C','C','B','E','C','B','C','C','D','A','D','B'];
posttestKey = ['E','B','E','E','C','E','C','B','D','D','A','C','C','C','D','B','C','C','A','B','D','A','D','B','C','C','D','D','C','B','B','E','C','C','A','A','C','A','B','B','B','C','B','C','B','A','B','B','B','C'];


with open('pretest.csv', 'rb') as csvfile:
	spamreader = csv.reader(x.replace('\0', '') for x in csvfile);
	count = 0;
	studentsToPretestAnswers = {};
	for index, row in enumerate(spamreader):
		studentID = row[0];
		studentsToPretestAnswers[studentID] = row[2:]

with open('posttest.csv', 'rb') as csvfile:
	spamreader = csv.reader(x.replace('\0', '') for x in csvfile);
	count = 0;
	studentsToPosttestAnswers = {};
	for index, row in enumerate(spamreader):
		studentID = row[0];
		studentsToPosttestAnswers[studentID] = row[2:]


studentsToPreScores = {};


for student in studentsToPretestAnswers:
	for index, answer in enumerate(studentsToPretestAnswers[student]):
		if(answer == 'BLANK' or answer == ""):
			continue;
		if(student not in studentsToPreScores):
			studentsToPreScores[student] = 0;
		if (answer == pretestKey[index] and answer != 'BLANK'):
			studentsToPreScores[student] += 1;

print "Student pretest Scores"
print studentsToPreScores;
print 
print;
print "Student Post Test scores";
studentsToScores = {};

for student in studentsToPosttestAnswers:
	for index, answer in enumerate(studentsToPosttestAnswers[student]):
		if(answer == 'BLANK' or answer == ""):
			continue;
		if(index + 1 not in questionMap and onlyUseQuestionsFromBothTests):
			continue;
		if(student not in studentsToScores):
			studentsToScores[student] = 0;
		if (answer == posttestKey[index] and answer != 'BLANK'):
			studentsToScores[student] += 1;



print studentsToScores;


total = 0;
totalResponses = 0;
if(verbose):
	for student in studentsToScores:
		if(student in studentsToPreScores):
			print "Student = " + student + "  Original Score = " + str(studentsToPreScores[student]) + "  Improvment = "  + str(studentsToScores[student] - studentsToPreScores[student]);
			total += studentsToScores[student] - studentsToPreScores[student];
			totalResponses += 1;
			
			
	print total;
	print totalResponses
	print "Improvement = "
	print total * 1.0 / totalResponses;
