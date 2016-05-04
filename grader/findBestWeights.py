'''
Kevin Dunn

This program attempts to use supervised machine learning to find the best weights for each metric. It individually attempts to increase/decrease each metric to see if the correlation improve. If it does, it keeps trying that direction until progress stops

'''

from shutil import copyfile
from grader import main;
import time;
import os;
from analyzeOutput import analyze
import random
import sys
import signal


maxScores = [0, 0, 0, 0, 0]
maxMetrics = [0, 0, 0, 0, 0];
def Main():
	metricNames = ['Length', 'Similarity to Instructor', 'Reading Level', 'Capital Letter Number', 'Vocab Usage', 'Conjunctive Words Used', 'Reflective Words Used'];
	f2 = open("metricOutput3.txt", "w+", 0);

	max = 0;
	cor = 0;
	metrics = [30, 30, 30, 30, 30, 30]
	print "Started";
	sys.stdout.flush();

	prevCor = 0;
	for i in range(0, 7):
		for j in range(0, 7):
			increaseMetric = 1;
			while(1):
				if(increaseMetric):
					#A metric should not increase past 65
					if(metrics[j] == 65):
						increaseMetric = 0;
						metrics[j] -= 1;
					else:
						metrics[j] += 1;
				else:
					#A metric should not go below 0
					if(metrics[j] == 0):
						break;
					metrics[j] -= 1;


				main(metrics[0], metrics[1], metrics[2], metrics[3], metrics[4], metrics[5], metrics[6]) 
				cor = analyze();

				print str(metrics) + " = " + str(cor);
				sys.stdout.flush();
	
				#The most recent change lowered the cor
				if(cor < prevCor):
					#Undo the change
					#Try the other direction
					if(increaseMetric):
						metrics[j] -= 1;
						increaseMetric = 0;
					else:
						metrics[j] += 1;
						break;
				else:
					prevCor = cor;
			



		
if __name__ == '__main__':
	try:
		Main()
	except KeyboardInterrupt:
		print maxScores;
		print maxMetrics;
