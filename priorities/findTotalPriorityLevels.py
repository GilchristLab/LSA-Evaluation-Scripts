import operator;
import sys

f1 = open("output.html", 'r')
#This needs to be changed to whatever the instructor ID is 
instructorID = "ID000"

similarityToInstructor = {};
responsePriorities = {};
instructorPriorities = [];
responseCounter = {};
response = 0;

for line in f1:
	if("LSA" in line):
		if(instructorID in responsePriorities):
			instructorPriorities = responsePriorities[instructorID];
			for student, response in responsePriorities.iteritems():
				if(student not in similarityToInstructor):
					similarityToInstructor[student] = 0;	
				for index, rank in enumerate(response):
					if(rank == instructorPriorities[index]):
						similarityToInstructor[student] += 1
		responsePriorities = {};
	else:
		lineItems = line.split('\t');
		if(lineItems[0] not in responsePriorities):
			responsePriorities[lineItems[0]] = []
		if(lineItems[0] not in responseCounter):
			responseCounter[lineItems[0]] = 0;
		responseCounter[lineItems[0]] += 1;
		responsePriorities[lineItems[0]].append(lineItems[1].strip());


total = 0;

for key in sorted(similarityToInstructor):
	if(key != instructorID):
		sys.stdout.write("\'" + key + "\': " + str(float(similarityToInstructor[key])) + ", ");

