from NeuralNetwork import NeuralNetwork
import numpy as np
import matplotlib.pyplot as plt
from helper_functions import *
from CollegeRater import CollegeRater
global LIST_OF_COLLEGES, DATA, MAJORS_DICTIONARY, COLLEGE_DICTIONARY

learning_rate = 0.01
NN = NeuralNetwork(learning_rate)

LIST_OF_COLLEGES = GetCollege()
COLLEGE_DICTIONARY = College_To_Number()

t_DATA = PrintTraining()
MAJORS_DICTIONARY = MajorDiction()
DATA = ReplaceMajor(t_DATA, MAJORS_DICTIONARY)
DATA = ReplaceCollege(DATA, COLLEGE_DICTIONARY)
print(DATA)
print(DATA.shape)
# Standarizing ALL data:
Standarized(DATA, DATA['Major_Codes'], 1, "S. Major Code")
Standarized(DATA, DATA['Area'], 2, "S. Area")
Standarized(DATA, DATA['Raw_Cost_Low'], 3, "S. Low Cost")
Standarized(DATA, DATA['Raw_Cost_High'], 4, "S. High Cost")
Standarized(DATA, DATA['Location_From_Home'], 6, "Standarized Location")
Standarized(DATA, DATA['SAT'], 7, "S. SAT")
Standarized(DATA, DATA['GPA'], 8, "S. GPA")
Standarized(DATA, DATA['Acceptance Rate Low'], 10, "S. Low Acceptance")
Standarized(DATA, DATA['Acceptance Rate High'], 11, "S. High Acceptance")
DATA = DATA.drop(["Major_Codes", "Area", "SAT", "GPA", "Acceptance Rate Low", "Acceptance Rate High", "Raw_Cost_Low", "Raw_Cost_High", "Location_From_Home"], axis=1)
print(DATA)
#Input = DATA columns 1 (major codes) to 11 (acceptance rate high)
# Output = college attended (12) --> SWITCH TO QUANTITATIVE
input_vectors = np.around(DATA[DATA.columns[1:10]].to_numpy(dtype=np.float64), 2)

#targets = np.array(DATA["College Attended"]) 
#targets not working because college attended has to be numeric data
quantitative_college_list = []


for row in DATA.itertuples():

    CR = CollegeRater(row[14], row[13])
    rank = CR.Run()
    quantitative_college_list.append(int(rank))

DATA.insert(11, "College_Rank", quantitative_college_list) 

print(quantitative_college_list)
targets = np.array(quantitative_college_list)
training_error = NN.train(input_vectors, targets, 10000)
plt.plot(training_error)
plt.show()
