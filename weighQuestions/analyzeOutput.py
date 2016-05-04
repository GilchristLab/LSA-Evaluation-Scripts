#Finds the correlation between the generated score from grading the LSA and the student's final grade

import numpy
import operator;
def analyze():
	#If you want to divide a students total score by the number of LSAs they submitted, this should be set to 1;
	isUsingAverageScore = 1;



	#This file is the output from grader.py
	f1 = open("output.txt", "r");
	finalScores = open("finalScores.txt", "r");
	#this array should be set to be only students who didn't finsh the course, or perhaps any other students that should be excluded for some reason
	studentsWhoDidntFinish = ["ID042", "ID045", "ID051", "ID076", "ID096", "ID106", "ID122"]

	#This is a dictionary mapping student IDs to their final grades
	studentsToFinalGrades = {}

	#This is a dictionary mapping student IDs to the generated LSA Score
	studentsToScores = {}
	#Counts number of LSAs a student sumitted
	totalScores = {};


	#Go through the output file, split the ID and the Score and add the score to that student's grades.
	for line in f1:
		if(line != "\n"):
			line = line.split('  ');
			ID = line[0];
			score = line[1];
			#strip the \n
			score = score[0:-1];
			if(ID not in studentsToScores):
				studentsToScores[ID] = 0;
				totalScores[ID] = 0;
			studentsToScores[ID] += float(score);
			totalScores[ID] = totalScores[ID] + 1;

	sortedStudents = sorted(studentsToScores.items(), key=operator.itemgetter(1))

	#Create the dictionary for the students' final grades in the class
	for line in finalScores:
		line = line.split('\t');
		#Strip newline
		line[1] = line[1][0:-1];
		studentsToFinalGrades[line[0]] = line[1];

	finalGrades = []; 
	LSAScores =  [];
	for student  in studentsToScores:
		if student in studentsToFinalGrades and student not in studentsWhoDidntFinish:
			finalGrades.append(float(studentsToFinalGrades[student]))
			if(isUsingAverageScore):
				LSAScores.append(studentsToScores[student] / totalScores[student]);
			else:
				LSAScores.append(studentsToScores[student]);

	return(numpy.corrcoef(finalGrades, LSAScores)[0][1]);

if __name__ == "__main__":
	cor = analyze()
	print cor
