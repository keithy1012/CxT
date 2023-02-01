from CollegexTinder.NeuralNetwork import NeuralNetwork
import numpy as np
import matplotlib.pyplot as plt
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
        COLLEGE_DICTIONARY = College_To_Number()
        t_DATA = PrintTraining()
        DATA = ReplaceCollege(t_DATA, COLLEGE_DICTIONARY)

        # Standarizing ALL data:
        Standarized(DATA, DATA['Major_ID'], 1, "S. Major Code")
        Standarized(DATA, DATA['Area'], 2, "S. Area")
        Standarized(DATA, DATA['Raw_Cost_Low'], 3, "S. Low Cost")
        Standarized(DATA, DATA['Raw_Cost_High'], 4, "S. High Cost")
        Standarized(DATA, DATA['Location_From_Home'], 6, "Standarized Location")
        Standarized(DATA, DATA['SAT'], 7, "S. SAT")
        Standarized(DATA, DATA['GPA'], 8, "S. GPA")
        Standarized(DATA, DATA['Acceptance Rate Low'], 10, "S. Low Acceptance")
        Standarized(DATA, DATA['Acceptance Rate High'], 11, "S. High Acceptance")
        MAJOR_MEAN = DATA['Major_ID'].mean()
        MAJOR_SD = DATA['Major_ID'].std()
        AREA_MEAN = DATA['Area'].mean()
        AREA_SD = DATA['Area'].std()
        LOW_COST_MEAN = DATA['Raw_Cost_Low'].mean()
        LOW_COST_SD = DATA['Raw_Cost_Low'].std()
        HIGH_COST_MEAN = DATA['Raw_Cost_High'].mean()
        HIGH_COST_SD = DATA['Raw_Cost_High'].std()
        LOC_MEAN = DATA['Location_From_Home'].mean()
        LOC_SD = DATA['Location_From_Home'].std()
        SAT_MEAN = DATA['SAT'].mean()
        SAT_SD = DATA['SAT'].std()
        GPA_MEAN = DATA['GPA'].mean()
        GPA_SD = DATA['GPA'].std()
        LOW_ACCEPT_MEAN = DATA['Acceptance Rate Low'].mean()
        LOW_ACCEPT_SD = DATA['Acceptance Rate Low'].std()
        HIGH_ACCEPT_MEAN = DATA['Acceptance Rate High'].mean()
        HIGH_ACCEPT_SD = DATA['Acceptance Rate High'].std()
        MEANS = [MAJOR_MEAN, AREA_MEAN, LOW_COST_MEAN, HIGH_COST_MEAN, LOC_MEAN, SAT_MEAN, GPA_MEAN, LOW_ACCEPT_MEAN, HIGH_ACCEPT_MEAN]
        STAN_DEVS = [MAJOR_SD, AREA_SD, LOW_COST_SD, HIGH_COST_SD, LOC_SD, SAT_SD, GPA_SD, LOW_ACCEPT_SD, HIGH_ACCEPT_SD]


        DATA = DATA.drop(["Major_ID", "Area", "SAT", "GPA", "Acceptance Rate Low", "Acceptance Rate High", "Raw_Cost_Low", "Major", "Raw_Cost_High", "Location_From_Home"], axis=1)
        print(DATA)
        # Quantifying College Names by getting ranks
        quantitative_college_list = []  
        for row in DATA.itertuples():
            CR = CollegeRater(row[11], row[12])
            rank = CR.Run()
            quantitative_college_list.append(int(rank))
        DATA.insert(12, "College_Rank", quantitative_college_list) 


        Standarized(DATA, DATA['College_Rank'], 12, "S. College_Rank")
        C_RANK_MEAN = DATA['College_Rank'].mean()
        C_RANK_SD = DATA['College_Rank'].std()
        DATA = DATA.drop(["College_Rank"], axis=1)
        standarized_college_rank = DATA['S. College_Rank']
        targets = np.array(standarized_college_rank)
        # Input Vectors: [S. Major Code, S. Area, S.Low Cost, S. High Cost, S. Location, S. SAT, S. GPA, S.Low Acceptance, S.High Acceptance, Home Zip]
        input_vectors = np.around(DATA[DATA.columns[1:10]].to_numpy(dtype=np.float64), 2)
        training_error = NN.train(input_vectors, targets, 100000)
        #plt.plot(training_error)
        #plt.show()

        temp = np.float_(input_vector)
        standarized_input_vector = Standarized_List(temp, MEANS, STAN_DEVS)
        print("Input Vector", input_vector)
        print("Standarized Input", standarized_input_vector)
        #Standarized input values
        input_vector = np.float_(standarized_input_vector)
        test_output_1 = NN.predict(standarized_input_vector) 
        print("Standarized", test_output_1)
        print("Unstandarized" , Unstandardized(C_RANK_MEAN, C_RANK_SD, test_output_1))

        # Saves the college rank for later use
        college_rank = pd.read_csv("CollegexTinder\\csv\\COLLEGE_RANK.csv")
        college_rank = college_rank.sort_values(by = "SCORE")
        return Unstandardized(C_RANK_MEAN, C_RANK_SD, test_output_1)
    def other_colleges(self, score):
        res = []
        college_rank = pd.read_csv("CollegexTinder\\csv\\COLLEGE_RANK.csv")
        college_rank = college_rank.sort_values(by = "SCORE")  
        for row in college_rank.itertuples():
            if (abs(row.SCORE-score)<=100):
                res.append(row.INSTM + " ")
        print(res)
        return res

def PrintTraining():
    data = pd.read_csv("CollegexTinder\\csv\\TRAINING_DATA.csv")
    return data

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

def Standarized_List(list, mean_list, SD_list):
    print("Input Vector:", list)
    print("Mean List:" , mean_list)
    print("SD List:" , SD_list)
    standarized_list = []
    for i in range(0, len(list)):
        standarized_list.append(Z_Score(mean_list[i], SD_list[i], list[i]))
    return standarized_list

def Z_Score(mean, SD, val):
    return (val-mean)/SD

def Unstandardized(mean, SD, Z_score):
    #print("Mean " , mean)
    #print("SD:", SD)
    return Z_score * SD + mean;