# GENERATES DUMMY DATA
import os
import pandas as pd
import numpy as np
global array, data, majors, majors_dictionary
def GetCollege():
    college = pd.read_csv("FieldOfStudyData1415_1516_PP.csv")
    array = college[["UNITID", "INSTNM" ,"CONTROL"]]
    array = array.drop_duplicates("INSTNM")
    return array

def PrintTraining():
    data = pd.read_csv("TRAINING_DATA.csv")
    return data

def MajorDiction():
    majors = pd.read_csv("MAJORS1.csv")
    majors_dictionary = dict(zip((majors["FOD1P"]),majors["Major"]))
    return (majors_dictionary)

def ReplaceMajor(df, majors_dict):
    list_of_major_code = []
    for row in df.itertuples():
        if row.Major in majors_dict.values():
            #list_of_major_code.append(list(majors_dict.keys()) [list(majors_dict.values()).index(row.Major)])
            print(float(list(majors_dict.keys()) [list(majors_dict.values()).index(row.Major)]))
            list_of_major_code.append(float(list(majors_dict.keys()) [list(majors_dict.values()).index(row.Major)]))
        else:
            list_of_major_code.append(0)
    #df["Major_Codes"]  = list_of_major_code
    df.insert(1, "Major_Codes", list_of_major_code)
    #print(df)
    [float(i) for i in df["Major_Codes"]] #converts all strings to floats
    return df

def College_To_Number():
    college_df = pd.read_csv("CLEANED_UP_COLLEGES.csv")
    college_dictionary = dict(zip((college_df["INSTNM"]), college_df["UNITID"]))
    return college_dictionary

def ReplaceCollege(df, college_dictionary):
    list_of_college_code = []
    for row in df.itertuples():
        if row.College in college_dictionary.keys():
            list_of_college_code.append(college_dictionary.get(row.College))
        else:
            list_of_college_code.append(0)
    df.insert(11, "College_Codes", list_of_college_code) 
    return df

def Standarized(df, column, index, name):
    mean = column.mean()
    SD = column.std()
    res = []
    for i in column:
        res.append(Z_Score(mean, SD, i))
    #df.drop(df.columns[[index]], axis=1)
    df.insert(index, name, res)


def Z_Score(mean, SD, val):
    return (val-mean)/SD