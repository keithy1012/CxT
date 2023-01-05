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
DATA = DATA.drop(["Major_Codes", "Area", "SAT", "GPA", "Acceptance Rate Low", "Acceptance Rate High", "Raw_Cost_Low", "Major", "Raw_Cost_High", "Location_From_Home"], axis=1)

# Quantifying College Names
quantitative_college_list = []
#Finds ranking for college as quantitative data
for row in DATA.itertuples():
    CR = CollegeRater(row[13], row[14])
    print(row[13])
    rank = CR.Run()
    quantitative_college_list.append(int(rank))
DATA.insert(13, "College_Rank", quantitative_college_list) 

Standarized(DATA, DATA['College_Rank'], 13, "S. College_Rank")
DATA = DATA.drop(["College_Rank"], axis=1)

# Input Vectors: [S. Major Code, S. Area, S.Low Cost, S. High Cost, S. Location, S. SAT, S. GPA, S.Low Acceptance, S.High Acceptance, Home Zip]
input_vectors = np.around(DATA[DATA.columns[1:10]].to_numpy(dtype=np.float64), 2)
print(input_vectors)
standarized_college_rank = DATA['S. College_Rank']
targets = np.array(standarized_college_rank)
print(targets)
training_error = NN.train(input_vectors, targets, 100000)
plt.plot(training_error)
plt.show()

test_output_1 = NN.predict([.92, 1.13, -0.3, .6, -.4, -.5, -.7, -.3, -.01])
print(test_output_1)