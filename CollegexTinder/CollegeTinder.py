from CollegexTinder.NeuralNetwork import NeuralNetwork
import numpy as np
import matplotlib.pyplot as plt
#from CollegexTinder.helper_functions import *
from CollegexTinder.CollegeRater import CollegeRater
import csv
import os
import pandas as pd
global array, data, majors, majors_dictionary
global LIST_OF_COLLEGES, DATA, MAJORS_DICTIONARY, COLLEGE_DICTIONARY

class CollegeTinder:
    def __init__(self, learning_rate):
        self.learning_rate = learning_rate
    def run(self, input_vector):
        NN = NeuralNetwork(self.learning_rate)
        LIST_OF_COLLEGES = GetCollege()
        COLLEGE_DICTIONARY = College_To_Number()
        t_DATA = PrintTraining()
        MAJORS_DICTIONARY = MajorDiction()
        DATA = ReplaceMajor(t_DATA, MAJORS_DICTIONARY)
        DATA = ReplaceCollege(DATA, COLLEGE_DICTIONARY)

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
            rank = CR.Run()
            quantitative_college_list.append(int(rank))
        DATA.insert(13, "College_Rank", quantitative_college_list) 


        Standarized(DATA, DATA['College_Rank'], 13, "S. College_Rank")
        C_RANK_MEAN = DATA['College_Rank'].mean()
        C_RANK_SD = DATA['College_Rank'].std()
        DATA = DATA.drop(["College_Rank"], axis=1)
        #print(DATA)
        standarized_college_rank = DATA['S. College_Rank']
        targets = np.array(standarized_college_rank)

        # Input Vectors: [S. Major Code, S. Area, S.Low Cost, S. High Cost, S. Location, S. SAT, S. GPA, S.Low Acceptance, S.High Acceptance, Home Zip]
        input_vectors = np.around(DATA[DATA.columns[1:10]].to_numpy(dtype=np.float64), 2)
        training_error = NN.train(input_vectors, targets, 100000)
        #plt.plot(training_error)
        #plt.show()

        #Standarized input values
        test_output_1 = NN.predict(input_vectors) 
        print(test_output_1)
        print(Unstandardized(C_RANK_MEAN, C_RANK_SD, test_output_1))
        # this returns a college's "score": score = SAT25 + SAT75 + ACT25 + ACT75 / acceptance_rate

        college_rank = pd.read_csv("CollegexTinder\\csv\\COLLEGE_RANK.csv")
        college_rank = college_rank.sort_values(by = "SCORE")
        #print(college_rank)
        return test_output_1

def GetCollege():
    college = pd.read_csv("CollegexTinder\\csv\\FieldOfStudyData1415_1516_PP.csv")
    array = college[["UNITID", "INSTNM" ,"CONTROL"]]
    array = array.drop_duplicates("INSTNM")
    return array

def PrintTraining():
    data = pd.read_csv("CollegexTinder\\csv\\TRAINING_DATA.csv")
    return data

def MajorDiction():
    majors = pd.read_csv("CollegexTinder\\csv\\MAJORS1.csv")
    majors_dictionary = dict(zip((majors["FOD1P"]),majors["Major"]))
    return (majors_dictionary)

def ReplaceMajor(df, majors_dict):
    list_of_major_code = []
    for row in df.itertuples():
        if row.Major in majors_dict.values():
            list_of_major_code.append(float(list(majors_dict.keys()) [list(majors_dict.values()).index(row.Major)]))
        else:
            list_of_major_code.append(0)
    df.insert(1, "Major_Codes", list_of_major_code)
    #print(df)
    [float(i) for i in df["Major_Codes"]] #converts all strings to floats
    return df

def College_To_Number():
    college_df = pd.read_csv("CollegexTinder\\csv\\CLEANED_UP_COLLEGES.csv")
    college_dictionary = dict(zip((college_df["INSTNM"]), college_df["UNITID"]))
    return college_dictionary

def ReplaceCollege(df, college_dictionary):
    list_of_college_code = []
    for row in df.itertuples():
        if row.College in college_dictionary.keys():
            list_of_college_code.append(int(college_dictionary.get(row.College)))
        else:
            list_of_college_code.append(0)
    #df.insert(11, "College_Codes", list_of_college_code) 
    return df

def Standarized(df, column, index, name):
    mean = column.mean()
    SD = column.std()
    res = []
    for i in column:
        res.append(Z_Score(mean, SD, i))
    df.insert(index, name, res)

def Z_Score(mean, SD, val):
    return (val-mean)/SD

def Unstandardized(mean, SD, Z_score):
    print("Mean " , mean)
    print("SD:", SD)
    return Z_score * SD + mean;