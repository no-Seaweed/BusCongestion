# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 17:16:27 2019

@author: harki
"""

import pandas as pd
import os

def create_dataframe(filename): 
    """reads data from a csv file into a dataframe"""
    data = pd.read_csv(filename)
    return data

def remove_null_values(dataframe):
    """removes rows or columns containing null values from a dataframe"""
    dataframe.dropna()
    
def split_individual_bus_data(dataframe):
    """splits the data frame into multiple dataframes based on individual buses and returns 
       in the form of dictionary of dataframes"""
    UniqueBuses = dataframe.vendorhardwareid.unique()
    DataFrameDict = {elem : pd.DataFrame for elem in UniqueBuses}
    for key in DataFrameDict.keys():
        DataFrameDict[key] = dataframe[:][dataframe.vendorhardwareid == key]
    return DataFrameDict, UniqueBuses

def remove_seconds(DataFrameDict, UniqueBuses):
    """removes the seconds from the time column from each dataframe in DataFrameDict"""
    start, stop = 0, 5
    for key in UniqueBuses:
        DataFrameDict[key]['time'] = DataFrameDict[key]['time'].astype(str)
        DataFrameDict[key]["time"] = DataFrameDict[key]['time'].str.slice(start, stop)
    return DataFrameDict

def remove_time_duplicates(DataFrameDict, UniqueBuses):
    """Removes time duplicates"""
    for key in UniqueBuses:
        DataFrameDict[key] = DataFrameDict[key].drop_duplicates(subset='time', keep='last')
    return DataFrameDict

def get_length(DataFrameDict, UniqueBuses):
    """get the length of all dataframes in DataFrameDict"""
    length = 0
    for key in UniqueBuses:
        length += len(DataFrameDict[key].index)
    return length

def export_to_csv(DataframeDict, UniqueBuses, filepath, filename):
    """exports data to  csv"""
    for key in UniqueBuses:
        final_path = filepath + key + filename
        DataframeDict[key].to_csv(final_path)

def implement(directory_path, export_filepath):
    """Takes directory path containing files contsining Data splits the data based on individual buses, truncates seconds and removes time duplicates and exports data to export_filepath"""
    for file in os.listdir(directory_path):
        filename = os.fsdecode(file)
        print(filename)
        if filename.endswith(".csv"):
            print(filename)
            df = create_dataframe(directory_path+filename)
            #print("Total number of records in dataframe", len(df.index))
            remove_null_values(df)
            #print("Total number of records in dataframe after null values removed", len(df.index))
            DataFrameDict, UniqueBuses = split_individual_bus_data(df)
            #total_rec_after_split = get_length(DataFrameDict, UniqueBuses)
            #print("Total number of dataframes in dictionary", len(DataFrameDict), "and sum of all records in each dataframe", total_rec_after_split)
            DataFrameDict = remove_seconds(DataFrameDict, UniqueBuses)
            DataFrameDict = remove_time_duplicates(DataFrameDict, UniqueBuses)
            #total_rec_after_rem_duplicates = get_length(DataFrameDict, UniqueBuses)
            #print("Total number of dataframes in dictionary after removing duplicate time records", len(DataFrameDict), "and sum of all records in each dataframe", total_rec_after_rem_duplicates)
            #print(df)
            # print(DataFrameDict, UniqueBuses)
            export_to_csv(DataFrameDict, UniqueBuses, export_filepath, filename)

implement("dataFolder/","cleanedData/")