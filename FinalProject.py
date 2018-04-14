import pandas as pd
import pygal
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = ""


"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~HELPER METHODS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


"""
Used to remove "years old" from each data entry for displaying to chart
"""
def trimText(text):
    update = str(text)[0:str(text).find(" years")].strip()
    newstring = ""
    for i in update:
        if i != " ":
            newstring = newstring + i
    return newstring

"""
Used to plot the graphs
"""
def plotGraph(xAxisValues, yAxisValues, xLabel, yLabel, title):
    # Plot the keys along with their values
    plt.plot(xAxisValues, yAxisValues)

    # Set the X, Y, and Title labels
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)

    # Display the graphe
    plt.show()







"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Main Methods~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


"""
Used to read the files
"""
def readFile():
    global df
    #Read the data from the CSV file and store it into a dataframe
    df = pd.read_csv("HackerRank-Developer-Survey-2018-Values.csv")

"""
Used to plot the Age Information
"""
def getAge():
    #Store the age data into a Series object
    ageSeries = df["q1AgeBeginCoding"]

    #Store the unique age entries and the number for each entry into a dictionary
    somedict = dict(ageSeries.value_counts())

    #Initialize a dictionary to order the ages
    updatingdict = {}

    #Go through each age group and receive only the first number
    for i in somedict:
        if i != "#NULL!" and i != "50+ years or older":
            updatingdict[int(i[0:str(i).find(" ")])] = i

    #Sort all of these numbers and store them into another dictionary with their corresponding values
    sortedDictionary = {}
    for i in sorted(updatingdict.keys()):
        sortedDictionary[updatingdict[i]] = somedict[updatingdict[i]]
    sortedDictionary["50+ years or older"] = somedict["50+ years or older"]

    #Remove excess text from all the keys in the dictionary
    Keys = []
    for i in sortedDictionary.keys():
        Keys.append( "         " + trimText(i) + "         " )

    plotGraph(Keys, sortedDictionary.values(), "Years Old", "Number of People", "When Did Most Users Start Coding?")




"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~INITIAL METHOD~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

if __name__ == "__main__":
    readFile()
    getAge()


