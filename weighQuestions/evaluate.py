'''
Kevin Dunn

This program uses supervised machine learning to attempt to find the optimal weights for each question. 
Ultimately regressions will be used instead.

This works by trying a set of weights and indivdually increasing or decreasing a weight and seeing if that improved the correlation. If the correlation improved, it keeps trying in that direction until progress is no longer made.
'''


from subprocess import Popen, PIPE
from shutil import copyfile
from grader import main;
import time;
import os;
from analyzeOutput import analyze
import random
import sys
import signal
from numpy import *
import re;

#If you want to divide LSA scores by number of LSAs submitted, this should be set to 1
usingAverage = 0;

#If this is 0 then the program will recreate the dictionaries. This increases runtime
usingPremadeDictionaries = 1;

#Scalars are used so that each question has the same effect on total score prior to setting weights
explainScalar = .4317
phenomenonScalar = .8377
knowledgeScalar = .8527
challengeScalar = 2.1457
understandingScalar = 25.7911
similarityScalar = 680.74


#In order to speed up the program, you can manually add the dictionary that maps IDs to scores for each respective question.
explainConceptScores = {'ID058': 23717.533454352, 'ID130': 11116.723269336, 'ID131': 17684.067250788004, 'ID132': 13910.164212791, 'ID133': 16748.483066411, 'ID134': 14126.203534476002, 'ID135': 3702.1955, 'ID136': 7817.253104622001, 'ID137': 13335.728748394002, 'ID138': 13900.765861591997, 'ID139': 3832.98213793, 'ID039': 18067.216971007, 'ID038': 15738.906437843998, 'ID031': 10776.577917438, 'ID030': 16505.989130542002, 'ID033': 12917.35731039, 'ID035': 17152.209763568, 'ID034': 11560.590439286001, 'ID037': 8489.804196930001, 'ID036': 18780.832268079, 'ID068': 25997.888061652, 'ID066': 6961.669176873001, 'ID067': 3148.6057992, 'ID147': 10422.165716208001, 'ID146': 21747.366966973997, 'ID145': 13211.093601769997, 'ID144': 15550.448436384, 'ID028': 12400.859382226003, 'ID029': 6482.579597524, 'ID141': 22922.722665563997, 'ID140': 12336.891630346998, 'ID143': 20218.705371245, 'ID142': 11074.612888709, 'ID022': 28038.164908466002, 'ID023': 23523.343325067006, 'ID020': 24531.094540439994, 'ID021': 25022.076516596, 'ID149': 8590.042261869, 'ID027': 19552.891399708, 'ID024': 22797.558392406, 'ID099': 5003.790764285999, 'ID098': 32416.116715259002, 'ID097': 6667.309028571999, 'ID026': 19064.978776102995, 'ID095': 24967.225598661, 'ID094': 10464.767311165999, 'ID093': 22750.315477133998, 'ID092': 14682.973190108, 'ID091': 23595.281195157997, 'ID090': 31659.085151176, 'ID017': 11636.974274192999, 'ID016': 13149.031072599002, 'ID015': 13562.003576141002, 'ID014': 21197.730873817, 'ID013': 29652.607806403998, 'ID012': 1442.637, 'ID011': 12828.161417399999, 'ID010': 5026.585128571, 'ID019': 1184.0578, 'ID018': 2176.988140909, 'ID150': 15686.071614723996, 'ID151': 54038.098096286994, 'ID088': 14512.957435994, 'ID089': 21422.54591748, 'ID080': 13033.452452572, 'ID081': 20903.730678947, 'ID082': 51037.045414619985, 'ID083': 23367.751019868003, 'ID084': 9944.68571872, 'ID085': 19562.28008733, 'ID086': 6191.933425000001, 'ID087': 10828.205732102, 'ID000': 8017.902127475999, 'ID001': 251.9346, 'ID002': 14761.386429787999, 'ID003': 7735.813550000001, 'ID004': 2170.629971429, 'ID005': 416.5416, 'ID006': 13717.703377455, 'ID007': 16658.060058388997, 'ID008': 13206.298991425996, 'ID009': 11205.221695488004, 'ID124': 9702.829896221001, 'ID075': 18758.089396233, 'ID074': 17285.356096566, 'ID077': 22372.167415926, 'ID070': 24758.623918972, 'ID073': 24798.470708948, 'ID072': 16530.598197848998, 'ID079': 21570.934356806, 'ID078': 9884.769756097, 'ID148': 206.628, 'ID109': 24914.137356002997, 'ID108': 18306.035074692, 'ID064': 23451.790093156, 'ID065': 25031.070112389003, 'ID062': 10626.508176840003, 'ID063': 14866.477849829003, 'ID060': 14278.842872727999, 'ID061': 35944.642683852, 'ID101': 20187.650003125997, 'ID100': 31998.39831073999, 'ID103': 14829.855106045, 'ID102': 16415.078650409996, 'ID105': 14742.869772357999, 'ID104': 14018.850027269, 'ID107': 30769.208515994997, 'ID069': 29951.422406809008, 'ID053': 25262.407260875, 'ID052': 21705.944492091, 'ID118': 38654.882808917995, 'ID119': 12414.23319402, 'ID057': 19659.031110753996, 'ID056': 23538.992085749996, 'ID055': 19014.005394314998, 'ID054': 2913.4748, 'ID113': 12141.031942856, 'ID110': 8726.736260739, 'ID111': 24411.297026517, 'ID116': 16677.941087254, 'ID117': 22950.397709882003, 'ID114': 18257.010956202997, 'ID115': 23725.407974558, 'ID127': 21375.354943544, 'ID126': 9054.496595898, 'ID125': 4228.8737, 'ID050': 14610.853003061002, 'ID123': 24742.026247009, 'ID121': 2622.4548, 'ID120': 16560.754126027998, 'ID129': 19952.855664488998, 'ID128': 24555.44813905, 'ID048': 19323.242680008003, 'ID049': 11318.795613752998, 'ID044': 23478.154339376997, 'ID046': 10270.418235687997, 'ID047': 16812.837383496, 'ID040': 25135.042654023993, 'ID043': 6282.23725, 'ID059': 22319.979742844003}

explainPhenomenonScores = {'ID111': 10183.31206464, 'ID130': 5037.728958598, 'ID131': 7528.786605573, 'ID132': 5005.5037223360005, 'ID133': 6384.312493141001, 'ID134': 5116.470620764, 'ID135': 1969.524190772, 'ID136': 1741.7412108019998, 'ID137': 4916.854496774, 'ID138': 5230.660834042001, 'ID139': 2272.2069652630003, 'ID039': 6575.802356188, 'ID038': 6606.591866823, 'ID031': 3768.269301332, 'ID030': 6381.179749139999, 'ID033': 3361.8740240124002, 'ID035': 7610.040989345001, 'ID034': 5825.234355679, 'ID037': 334.08978087, 'ID036': 7251.9021779800005, 'ID066': 1372.7858155630001, 'ID147': 5299.769242893999, 'ID146': 8898.552428438, 'ID145': 6102.548542329, 'ID144': 5837.585045874001, 'ID028': 5420.921255128, 'ID029': 3197.498763269, 'ID141': 6091.275011490001, 'ID140': 5427.5920643419995, 'ID143': 6438.168012753001, 'ID142': 2140.510057768, 'ID022': 8243.622477155, 'ID023': 11337.096575043, 'ID020': 8360.928313033999, 'ID021': 8757.115380897, 'ID149': 769.649615428, 'ID027': 7287.892284017001, 'ID024': 7929.005649195001, 'ID099': 3984.1424051000004, 'ID098': 9699.372781384001, 'ID097': 3752.357140761, 'ID026': 9380.355562205, 'ID095': 8720.654032801, 'ID094': 6488.086303613001, 'ID093': 8557.39950154, 'ID092': 6268.697275771, 'ID091': 9092.330163346, 'ID148': 373.50338050000005, 'ID017': 4314.415954012, 'ID016': 6027.484124398001, 'ID015': 5411.847109669, 'ID014': 7830.189865088001, 'ID013': 9829.747716524, 'ID107': 10902.046965051999, 'ID011': 8081.641761397, 'ID010': 1934.2899154800002, 'ID019': 297.726628571, 'ID018': 1823.4470951919998, 'ID150': 7129.454982192001, 'ID151': 13957.108106787698, 'ID088': 6300.305964608, 'ID089': 6866.717245332, 'ID080': 6551.627736189999, 'ID081': 8693.561690006, 'ID082': 13403.192935726001, 'ID083': 9086.909238663, 'ID084': 1121.4484862250001, 'ID085': 6784.82267065, 'ID086': 3888.687841931, 'ID087': 2968.647960113, 'ID000': 7574.063556831, 'ID001': 180.91436, 'ID002': 6099.7912473119995, 'ID003': 5019.6594485, 'ID004': 2039.865470732, 'ID005': 115.90227, 'ID006': 5577.227553997, 'ID007': 7294.877679450001, 'ID008': 3431.8104746159997, 'ID009': 2506.714695115, 'ID075': 7720.727188844, 'ID074': 4107.996327148, 'ID077': 9545.326339251998, 'ID071': 423.1198455, 'ID070': 7310.766144161002, 'ID073': 6563.19121046, 'ID072': 6628.085467821001, 'ID079': 8722.528095385, 'ID078': 6832.357368381001, 'ID090': 11614.770145293001, 'ID109': 7832.2596756249995, 'ID108': 5015.50648588, 'ID064': 8059.261254143001, 'ID065': 8824.32544924, 'ID062': 1517.872709878, 'ID063': 7828.144017295, 'ID060': 5320.5994836380005, 'ID061': 10347.728922822998, 'ID101': 7064.197048666, 'ID100': 8973.247760379, 'ID103': 5805.649565747, 'ID102': 551.347877412, 'ID105': 7131.532536457001, 'ID104': 4486.409791649, 'ID068': 9263.085659905999, 'ID069': 9332.957981595, 'ID110': 2681.5529563849996, 'ID053': 7087.538431633999, 'ID052': 7418.996858957, 'ID118': 9659.396476814001, 'ID050': 6184.689054109999, 'ID057': 7690.876084197998, 'ID056': 7550.178950043002, 'ID055': 5639.571921319, 'ID054': 759.307254118, 'ID112': 342.879499286, 'ID113': 7550.338871135, 'ID059': 11160.121133876, 'ID058': 10491.10600639, 'ID116': 6803.010898434999, 'ID117': 6390.276379184999, 'ID114': 9313.028925377, 'ID115': 7320.774597619, 'ID127': 6545.579614492, 'ID126': 3283.834236706, 'ID125': 1199.204586286, 'ID124': 4256.236848742, 'ID123': 8963.070912612999, 'ID121': 997.2989596939999, 'ID120': 5176.418945548, 'ID129': 7502.384857155299, 'ID128': 8003.332593705001, 'ID048': 5617.382754802, 'ID049': 4478.4934346360005, 'ID044': 8606.390238718, 'ID046': 3971.018552736, 'ID047': 8222.217303242, 'ID040': 10208.159387044, 'ID041': 401.218934286, 'ID043': 3429.7599639959, 'ID119': 7150.332027707}

knowledgeBasisScores = {'ID111': 35533.322100676, 'ID130': 14923.084426666997, 'ID131': 23819.460945454, 'ID132': 19562.166044265, 'ID133': 27366.610800000002, 'ID134': 13609.021356765, 'ID135': 5298.926200000001, 'ID136': 3113.4936000000002, 'ID137': 22018.506520000003, 'ID138': 21641.949711382003, 'ID139': 5537.031650909001, 'ID039': 33552.799, 'ID038': 16606.173779999997, 'ID031': 12078.301822674002, 'ID030': 22298.995335817002, 'ID033': 14611.199479999997, 'ID035': 29011.821800000005, 'ID034': 14413.079529999999, 'ID037': 1006.66324, 'ID036': 18873.086000000003, 'ID068': 32365.407701419997, 'ID066': 7615.0303699999995, 'ID108': 33472.52456575501, 'ID147': 9200.2396, 'ID029': 7216.013712500001, 'ID145': 15704.952981049999, 'ID144': 17259.394181052998, 'ID028': 12690.84184, 'ID146': 14699.757479480999, 'ID141': 24967.12272721299, 'ID140': 16834.409600000003, 'ID143': 32615.634269196, 'ID142': 13837.922932979001, 'ID022': 37916.708010947994, 'ID023': 44393.682215122, 'ID020': 29771.777919999997, 'ID021': 31847.200365156, 'ID149': 12363.295741052998, 'ID148': 1170.67536, 'ID024': 27800.177359999998, 'ID099': 7932.753882857999, 'ID098': 53981.70264716001, 'ID097': 7189.457697143001, 'ID026': 25142.6358, 'ID095': 24785.122332979, 'ID094': 14742.691240000002, 'ID093': 23056.46511336, 'ID092': 22264.744703890003, 'ID091': 25454.01768727, 'ID027': 26008.038514999997, 'ID017': 13406.336405881999, 'ID016': 17869.985239999998, 'ID015': 15663.580392499998, 'ID014': 25363.726612173996, 'ID013': 39549.92163999701, 'ID012': 785.33916, 'ID011': 27123.330719999998, 'ID010': 7160.0765200000005, 'ID019': 2033.73584, 'ID018': 5957.661497143, 'ID150': 19085.750982106, 'ID151': 60934.712835051, 'ID088': 20878.20845717399, 'ID089': 35446.775062504996, 'ID080': 19251.213419285996, 'ID081': 26272.751399999997, 'ID082': 55901.287641153984, 'ID083': 26280.20139999999, 'ID084': 16401.458048571, 'ID085': 32555.074527136003, 'ID086': 9810.66936, 'ID087': 11997.390547881003, 'ID000': 39988.77359144501, 'ID001': 374.42576, 'ID002': 20231.04304, 'ID003': 4685.83064, 'ID004': 5819.65212, 'ID005': 2769.0492800000006, 'ID006': 18304.96988, 'ID007': 23825.386426322, 'ID008': 13165.05148, 'ID009': 7107.188505, 'ID075': 21704.738784999994, 'ID074': 19193.881331429002, 'ID077': 40883.95731999998, 'ID070': 31821.620736329998, 'ID073': 40060.92768, 'ID072': 21005.111400000005, 'ID079': 27724.546242857, 'ID078': 16741.282272500004, 'ID090': 30263.157367700016, 'ID109': 45909.08660614802, 'ID067': 2755.70496, 'ID064': 30922.291424999996, 'ID065': 36214.257661052994, 'ID062': 6641.750239999999, 'ID063': 22180.133311429003, 'ID060': 11843.329737143002, 'ID061': 54779.38218349999, 'ID101': 18548.409999999996, 'ID100': 31551.016509425, 'ID103': 23870.608344999997, 'ID102': 12085.182057143, 'ID105': 19087.054517744997, 'ID104': 12738.770196289, 'ID107': 38630.442196250006, 'ID069': 44981.104320000006, 'ID119': 29050.07455459699, 'ID053': 42607.00367133199, 'ID052': 22136.326459999993, 'ID118': 48718.174251765005, 'ID050': 16273.548150000004, 'ID057': 29031.23883999999, 'ID056': 40587.692520000004, 'ID055': 26225.234226089997, 'ID054': 6763.822400000001, 'ID113': 9802.829079999998, 'ID110': 4115.045186667, 'ID058': 29545.618031328995, 'ID116': 20658.594634286, 'ID117': 34557.232449594994, 'ID114': 24559.755165714, 'ID115': 30316.133009628007, 'ID127': 22920.161625, 'ID126': 9564.191719999997, 'ID125': 6020.025319999999, 'ID124': 13720.388868635999, 'ID123': 30128.781831406006, 'ID121': 1341.8318800000002, 'ID120': 15474.591491764997, 'ID129': 27595.699790000002, 'ID128': 31389.77328000001, 'ID048': 15836.953619999998, 'ID049': 13929.4046, 'ID044': 30289.610581053003, 'ID046': 12570.465350000002, 'ID047': 24511.016848371997, 'ID040': 44064.26957739, 'ID041': 1329.41598, 'ID043': 4471.9270799999995, 'ID059': 29236.032008186994}

challengeConceptScores = {'ID111': 13253.677176877998, 'ID130': 2305.205730166, 'ID131': 8570.342515842, 'ID132': 6761.3639907510005, 'ID133': 5854.516199021, 'ID134': 2832.325032053, 'ID135': 1151.467553221, 'ID136': 1976.715925789, 'ID137': 7071.5356905730005, 'ID138': 6856.021716962, 'ID139': 1253.123572548, 'ID039': 12308.012517095998, 'ID038': 5930.733088753, 'ID031': 3318.257276736, 'ID030': 7921.238481592999, 'ID033': 3335.790803294, 'ID035': 7247.757139369, 'ID034': 5513.187949454001, 'ID037': 1385.1883520000001, 'ID036': 7931.901108919, 'ID109': 13842.476035529999, 'ID067': 889.33050875, 'ID028': 5063.742750019001, 'ID146': 7606.454390533, 'ID145': 6111.475925502, 'ID144': 6553.796464218998, 'ID147': 3996.912167728, 'ID029': 2475.684519618, 'ID141': 6444.711078898, 'ID140': 4438.903164953999, 'ID143': 10671.48987764, 'ID142': 3959.739582163, 'ID022': 9978.192349007, 'ID023': 14264.950178535, 'ID020': 8284.92419122, 'ID021': 10265.980559503998, 'ID026': 11614.141236961003, 'ID148': 244.443688421, 'ID024': 6897.588083034, 'ID099': 2057.5661315410002, 'ID098': 12298.644605447, 'ID097': 2306.991742894, 'ID149': 3219.543927337, 'ID095': 7126.135561219999, 'ID094': 5148.560758071, 'ID093': 7727.8767725239995, 'ID092': 7984.651655234999, 'ID091': 6681.848949155001, 'ID027': 8192.59634174, 'ID017': 5159.877412911, 'ID016': 6155.172862583, 'ID015': 3541.609916972, 'ID014': 8595.987336828, 'ID013': 13303.179686884, 'ID012': 321.35933, 'ID011': 9654.192654588, 'ID010': 1625.782120884, 'ID019': 354.349194286, 'ID018': 1579.995829207, 'ID150': 5472.768676938001, 'ID151': 15077.659671951002, 'ID088': 9019.423137803, 'ID089': 8638.347298901, 'ID080': 6155.7682632669985, 'ID081': 8470.068072319998, 'ID082': 18500.870620376998, 'ID083': 8958.44642815, 'ID084': 5041.793448498, 'ID085': 12494.327482708, 'ID086': 3980.919296279, 'ID087': 3025.3631075, 'ID001': 97.77212, 'ID002': 6738.744265927, 'ID003': 1660.727475545, 'ID004': 1812.532404646, 'ID005': 352.544673333, 'ID006': 3133.6441684740003, 'ID007': 8534.050509216002, 'ID008': 2829.356333625, 'ID009': 2821.794460975, 'ID075': 7154.192517985, 'ID074': 3161.76684317, 'ID077': 8524.275135888, 'ID071': 351.0816, 'ID070': 5036.087283073999, 'ID073': 9566.948014351, 'ID072': 5556.3030207150005, 'ID079': 6049.0143253609995, 'ID078': 5433.797401546999, 'ID090': 9998.341109345, 'ID066': 744.1288129760001, 'ID108': 5010.766785197999, 'ID064': 9662.189904121, 'ID065': 15880.295197374999, 'ID062': 1280.231249417, 'ID063': 9952.238701839999, 'ID060': 2652.8341049299997, 'ID061': 9848.986767656, 'ID101': 5285.782665168, 'ID100': 9734.349007161, 'ID103': 7931.270603710999, 'ID102': 2952.93782697, 'ID105': 6766.197626610999, 'ID104': 4756.057635377, 'ID068': 5353.511608895, 'ID069': 9938.982508068, 'ID119': 13615.123671725001, 'ID053': 7181.062760502999, 'ID052': 7474.167951009, 'ID118': 9398.861369251, 'ID050': 6370.978147281001, 'ID057': 7652.689039878, 'ID056': 10474.192837295, 'ID055': 6452.822898931001, 'ID054': 1021.763166985, 'ID112': 394.364742857, 'ID113': 5435.578225739, 'ID059': 14139.662362432, 'ID058': 10929.077777873998, 'ID116': 6091.666905788, 'ID117': 7900.417636917, 'ID114': 8554.74508519, 'ID115': 8395.585124793, 'ID107': 7938.94105598, 'ID127': 7525.12860433, 'ID126': 3501.108804607, 'ID125': 371.83465934000003, 'ID124': 3567.739878086, 'ID123': 13017.011724396998, 'ID121': 1198.25897082, 'ID120': 6051.397657264999, 'ID129': 5575.368829081, 'ID128': 15443.598079229, 'ID048': 3417.437506145, 'ID049': 5306.552840276, 'ID044': 11197.527548129, 'ID046': 3611.9340998249995, 'ID047': 6762.590843274999, 'ID040': 7950.859877575999, 'ID041': 360.882586667, 'ID043': 2064.955042559, 'ID110': 3207.533371568}

LSAScores = {};

#Create the inputData.txt file for optimizeMetrics to use
def createInputData(createIndex):
	f = open('inputData.txt', 'w+');
	for i in range(2, 16):
		p = Popen(['python', 'createLSA.py', '../Anonymous.LSAs/LSA' + str(i) + '.html', 'inputData.txt'], stdin=PIPE, stdout=PIPE);
		p.communicate(input=createIndex)[0];



#Total the scores in output.txt for each student
def createScoresList(studentsToScores):
        f1 = open("output.txt", "r");
        studentsWhoDidntFinish = ["ID042", "ID045", "ID051", "ID076", "ID096", "ID106", "ID122"]


        for line in f1:
                if(line != "\n"):
                        line = line.split('  ');
                        ID = line[0];
                        score = line[1];
                        #strip the \n
                        score = score[0:-1];
			if(ID in studentsWhoDidntFinish):
				continue;
                        if(ID not in studentsToScores):
                                studentsToScores[ID] = 0;
                        studentsToScores[ID] += float(score);

def createFinalGradesDict(studentsToFinalGrades):
        finalScores = open("finalScores.txt", "r");

	
	for line in finalScores:
		line = line.split('\t');
		line[1] = line[1][0:-1];
		studentsToFinalGrades[line[0]] = float(line[1]);

#Each question has a different optimal set of metrics to use, so this function just returns the best metric for the given question
def whichMetricToUse(questionNumber, usingAverage):
	if(usingAverage):
		if(questionNumber == 1):
			return [55, 65, 0, 31, 0, 0, 0]
		
		elif(questionNumber == 3):
			return [25, 64, 27, 0, 0, 2, 0]
		
		elif(questionNumber == 4):
			return [41, 65, 0, 37, 0, 0, 5]
		else:
			return [62, 0, 6, 28, 0, 0, 12]

	else:
		if(questionNumber == 1):
			return [0, 13, 65, 23, 0, 0, 18]
		
		elif(questionNumber == 3):
			return [10, 55, 65, 0, 0, 2, 1]
		
		elif(questionNumber == 4):
			return [5, 65, 24, 0, 2, 1, 1]
		else:
			return [1, 2, 60, 8, 0, 0, 2]

#This function tries 10000 random weight for each variable in the input vector and saves the weights that create the best correlation
def findBestMountain():
	bestCor = 0;
	bestWeights = [];
	questionWeights = [30, 30, 30, 30, 30, 30];
	for j in range(0, 10000):
		for i in range(0, 5):
			questionWeights[i] = random.randint(0, 65);
		cor = findCorOfAllQuestions(validStudents, questionWeights, totalLSAsToStudent, studentsToFinalGrades);
		if(cor > bestCor):
			bestWeights = questionWeights;
			bestCor = cor;

	print bestCor;
	print bestWeights;
	


def createSimilarityToInstructorDict(similarityToInstructor):
	f1 = open('priorityLevels.txt')
	
	for line in f1:
		lineArray = line.split();
		name = lineArray[0];
		score = lineArray[1];
		similarityToInstructor[name] = score;

	return similarityToInstructor

def createUnderstandingLevelDict(understandingLevel):
	f1 = open('understandingLevels.txt')
	
	for line in f1:
		lineArray = line.split();
		name = lineArray[0];
		score = lineArray[1];
		understandingLevel[name] = score;

	return understandingLevel

def createLSACount():
	totalLSAsToStudent = {};

	for i in range(2, 16):
		f1 = open('../Anonymous.LSAs/LSA' + str(i) + '.html');
		studentsAccountedFor = [];
		
		isStudentID = 0;

		for index, line in enumerate(f1):
			if(isStudentID):
				matchObj = re.match(r'^<td>(.*)</td>$', line.strip());
				studentID = matchObj.group(1);
				isStudentID = 0;

				if studentID not in totalLSAsToStudent:
					totalLSAsToStudent[studentID] = 0;

				totalLSAsToStudent[studentID] += 1;
	


			if(line.strip() == "<td>studentID[SQ003]</td>"):
				isStudentID = 1;

		
	return totalLSAsToStudent;

def findCor(scores, finalGrades, totalLSAsToStudent):
	grades = [];
	LSAScores = [];

	for student in scores:
		if(student in finalGrades):
			if(usingAverage):
				LSAScores.append(int(scores[student]) * 1.0 / totalLSAsToStudent[student]);
			else:
				LSAScores.append(int(scores[student]) * 1.0);
			grades.append(int(finalGrades[student]) * 1.0);

	cor = corrcoef(LSAScores, grades)[0][1];
	print cor;
	sys.stdout.flush();

def findCorOfAllQuestions(validStudents, questionWeights, totalLSAsToStudent, studentsToFinalGrades):
	LSAScores = [];
	finalGrades = []

	for student in validStudents:
		explainWeight = questionWeights[0];
		phenomenonWeight = questionWeights[1];
		knowledgeWeight = questionWeights[2];
		challengeWeight = questionWeights[3];
		understandingWeight = questionWeights[4];
		similarityWeight = questionWeights[5];
		LSAScore = explainConceptScores[student] * explainScalar * explainWeight + explainPhenomenonScores[student] * phenomenonScalar * phenomenonWeight + knowledgeBasisScores[student] * knowledgeScalar * knowledgeWeight + challengeConceptScores[student] * challengeScalar * challengeWeight + float(understandingLevels[student]) * understandingScalar * understandingWeight + float(similarityToInstructor[student]) * similarityScalar * similarityWeight;

		if(usingAverage):
			LSAScore /= totalLSAsToStudent[student];

		LSAScores.append(LSAScore);
		finalGrades.append(studentsToFinalGrades[student])

	cor = corrcoef(finalGrades, LSAScores)[0][1];
	return cor;


#This optimiazes the question weights by increasing and decreasing each metric until they no longer improve the final correlation
def climbMountain():
	prevCor = 0;
	for i in range(0, 50):
			for j in range(0, 6):
				increaseMetric = 1;
				while(1):
					if(increaseMetric):
						#A metric should not increase past 65
						if(questionWeights[j] == 65):
							increaseMetric = 0;
							questionWeights[j] -= 1;
						else:
							questionWeights[j] += 1;
					else:
						#A metric should not go below 0
						if(questionWeights[j] == 0):
							break;
						questionWeights[j] -= 1;

					
					cor = findCorOfAllQuestions(validStudents, questionWeights, totalLSAsToStudent, studentsToFinalGrades);

					print str(questionWeights) + " = " + str(cor)
					sys.stdout.flush();

					if(cor < prevCor):
						#Undo the change
						#Try the other direction
						if(increaseMetric):
							questionWeights[j] -= 1;
							increaseMetric = 0;
						else:
							questionWeights[j] += 1;
							break;
					else:
						prevCor = cor;





studentsToFinalGrades = {}
createFinalGradesDict(studentsToFinalGrades);

similarityToInstructor = {};
createSimilarityToInstructorDict(similarityToInstructor);

understandingLevels = {};
createUnderstandingLevelDict(understandingLevels);
createInputData("1\n");

totalLSAsToStudent = {};
totalLSAsToStudent = createLSACount();

if(usingPremadeDictionaries == 0):
	metrics = whichMetricToUse(1, usingAverage)
	main(metrics[0], metrics[1], metrics[2], metrics[3], metrics[4], metrics[5], metrics[6])
	explainConceptScores = {};
	createScoresList(explainConceptScores);
print "Explain Concept"
findCor(explainConceptScores, studentsToFinalGrades, totalLSAsToStudent);

print "simililarity"
findCor(similarityToInstructor, studentsToFinalGrades, totalLSAsToStudent);

print "understanding Level";
findCor(understandingLevels, studentsToFinalGrades, totalLSAsToStudent);

createInputData("3\n");
if(usingPremadeDictionaries == 0):
	metrics = whichMetricToUse(3, usingAverage)
	main(metrics[0], metrics[1], metrics[2], metrics[3], metrics[4], metrics[5], metrics[6])
	explainPhenomenonScores = {};
	createScoresList(explainPhenomenonScores);
print "Phenonmenon"
findCor(explainPhenomenonScores, studentsToFinalGrades, totalLSAsToStudent);


createInputData("4\n");


if(usingPremadeDictionaries == 0):
	metrics = whichMetricToUse(4, usingAverage)
	main(metrics[0], metrics[1], metrics[2], metrics[3], metrics[4], metrics[5], metrics[6])
	knowledgeBasisScores = {};
	createScoresList(knowledgeBasisScores);
print "Knowledge basis"
findCor(knowledgeBasisScores, studentsToFinalGrades, totalLSAsToStudent);


createInputData("7\n");
if(usingPremadeDictionaries == 0):
	metrics = whichMetricToUse(7, usingAverage)
	main(metrics[0], metrics[1], metrics[2], metrics[3], metrics[4], metrics[5], metrics[6])
	challengeConceptScores = {};
	createScoresList(challengeConceptScores);
print "Challenge Concept"
findCor(challengeConceptScores, studentsToFinalGrades, totalLSAsToStudent);

validStudents = [];

for key in explainConceptScores:
	if(key in explainPhenomenonScores and key in explainPhenomenonScores and key in knowledgeBasisScores and key in challengeConceptScores and key in understandingLevels and key in similarityToInstructor and key in studentsToFinalGrades):
		validStudents.append(key);

questionWeights = [18, 62, 43, 38, 20, 30]
climbMountain();
