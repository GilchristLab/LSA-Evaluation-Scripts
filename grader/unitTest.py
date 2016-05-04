'''
Kevin Dunn

This program runs grader on some predefined input and checks to see if the output matches what is expected. Obviously, if you change the weights of grader or add new metrics, the output will also change. So update the expected output file

'''
import os;


os.system("cp inputData.txt tempFileForUnitTesting.txt");
os.system("cp output.txt tempOutputFileForUnitTesting.txt");
os.system("cp unitTestingInputFile.txt inputData.txt");

os.system("python grader.py");

f1 = open('output.txt');

f2 = open('unitTestingExpectedOutputFile.txt');

output = [];
for line in f1:
	output.append(line);

filesDoNotMatch = 0;

for index, line in enumerate(f2):
	if(line != output[index]):
		print "Output.txt does not match expected output";
		print "Run 'diff -y actualUnitTestingOutput.txt unitTestingExpectedOutputFile.txt' To see what is different";
		filesDoNotMatch = 1;
		break;

if(filesDoNotMatch == 0):
	print "Unit test was successful";

os.system("mv tempFileForUnitTesting.txt inputData.txt");
os.system("cp output.txt actualUnitTestingOutput.txt");
os.system("mv tempOutputFileForUnitTesting.txt output.txt");
