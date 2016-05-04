'''
Kevin Dunn

This can be used to try random weights for each metric. This in theory can sometimes be better that running findBestMetrics. It can take a long time, so perhaps the best way to use it is running 'nohup python tryRandomWeights &' so that it can run in the background indefinitely
'''


from shutil import copyfile
from grader import main;
import time;
import os;
from analyzeOutput import analyze
import random
import sys
weights = [0, 5, 10, 25, 35]

maxScores = [0, 0, 0, 0, 0]
maxMetrics = [0, 0, 0, 0, 0];

max = 0;
cor = 0;
for i in range(1, 100000):
	f1 = open("output.txt", "w");
	var1 = random.choice (weights)
	var2 = random.choice (weights)
	var3 = random.choice (weights)
	var4 = random.choice (weights)
	var5 = random.choice (weights)
	var6 = random.choice (weights)
	var7 = random.choice (weights)

	#Add code here
	main(var1, var2, var3, var4, var5, var6, var7);
	if(i % 5 == 0):
		print maxScores
		print maxMetrics;

	cor = analyze();
	print cor
	if(cor > min(maxScores)):
		index = maxScores.index(min(maxScores));
		maxScores[index] = cor;
		metrics = [var1, var2, var3, var4, var5, var6, var7];
		maxMetrics[index] = metrics;
	f1.close();

	
print "Done!";
