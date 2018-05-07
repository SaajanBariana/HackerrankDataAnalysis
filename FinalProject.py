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
    print("Update: " + update)
    newstring = ""
    for i in update:
        if i != " ":
            newstring = newstring + i
    return newstring

"""
Used to plot the graphs
"""
def plotGraph(xAxisValues, yAxisValues, xLabel, yLabel, title, type, explode = None, pctdistance = 0.6, radius = 1, figsize = None):


    # Plot the keys along with their values
    if type == "line":
        plt.plot(xAxisValues, yAxisValues)
    elif type == "bar":
        plt.bar(xAxisValues, yAxisValues)
    elif type == "pie":
        fig_size = plt.rcParams["figure.figsize"]
        fig_size[0] = 10
        fig_size[1] = 8
        plt.rcParams["figure.figsize"] = fig_size
        plt.pie(x=yAxisValues, labels=xAxisValues, autopct='%1.1f%%', explode=explode, pctdistance=pctdistance, radius= radius)
        if figsize != None:
            plt.figure(figsize=figsize)
        # fig = plt.gcf()
        # fig.set_size_inches(2.5, 5)
        # fig = plt.figure(figsize=[20, 20])
    # Set the X, Y, and Title labels
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)



    # Display the graph
    plt.show()

"""
Used to set the ages in order
"""
def orderAges(somedict, filters):
    # Initialize a dictionary to order the ages
    updatingdict = {}

    # Go through each age group and receive only the first number
    for i in somedict:
        if i not in filters:
            updatingdict[int(i[0:str(i).find(" ")])] = i

    # Sort all of these numbers and store them into another dictionary with their corresponding values
    sortedDictionary = {}
    if len(filters) == 3:
        sortedDictionary[filters[1]] = somedict[filters[1]]

    for i in sorted(updatingdict.keys()):
        sortedDictionary[updatingdict[i]] = somedict[updatingdict[i]]

    for j in range(2, len(filters)):
        temp = filters[j][0:filters[j].find(" ")].strip()
        temp += "+ " + filters[j][filters[j].find(" "):len(filters[j])]
        sortedDictionary[temp] = somedict[filters[j]]

    return sortedDictionary



"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Main Methods~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


"""
Used to read the files
"""
def readFile():
    global df
    global df_pygal_country_codes
    #Read the data from the CSV file and store it into a dataframe
    df = pd.read_csv("HackerRank-Developer-Survey-2018-Values.csv")
    df_pygal_country_codes = pd.read_csv("Pygal-Country-Codes.csv")

"""
Used to plot the Age Information
"""
def getAgeTheyStartedCoding():
    #Store the age data into a Series object
    ageSeries = df["q1AgeBeginCoding"]

    #Store the unique age entries and the number for each entry into a dictionary
    somedict = dict(ageSeries.value_counts())

    sortedDictionary = orderAges(somedict, ["#NULL!", "50+ years or older"])

    #Remove excess text from all the keys in the dictionary
    Keys = []
    for i in sortedDictionary.keys():
        Keys.append( "         " + trimText(i) + "         " )

    plotGraph(Keys, sortedDictionary.values(), "Years Old", "Number of People", "When Did Most Users Start Coding?", "line")

def getCurrentAge():
    currentAgeSeries = df["q2Age"]

    ageDictionary = dict(currentAgeSeries.value_counts())

    sortedDictionary = orderAges(ageDictionary, ["#NULL!", "Under 12 years old", "75 years or older"])

    print(str(sortedDictionary))

    Keys = []
    for i in sortedDictionary.keys():
        print("I: " + i)
        Keys.append("         " + trimText(i) + "         ")
    print(str(Keys))
    plotGraph(Keys, sortedDictionary.values(), "Years Old", "Number of People", "How Old are the Users Now?", "bar")

def getGender():
    genderSeries = df["q3Gender"]

    genderDictionary = dict(genderSeries.value_counts())

    del genderDictionary["#NULL!"]

    print(str(genderDictionary))

    plotGraph(genderDictionary.keys(), genderDictionary.values(), "", "", "Gender of HackerRank Users", "pie", (0, 0.05, 0.05))


def getEducationLevel():
    educationSeries = df["q4Education"]

    educationDictionary = dict(educationSeries.value_counts())

    del educationDictionary["#NULL!"]

    print(str(educationDictionary))

    plotGraph(educationDictionary.keys(), educationDictionary.values(), "", "", "Education Level of HackerRank Users", "pie", explode=(0.05, 0.05, 0.05, 0.05 ,0.05, 0.15, 0.2), radius=0.7, pctdistance=0.8)

def getEmployeeJobCriteria():
    criteriaDataframe = df[["q12JobCritPrefTechStack", "q12JobCritCompMission", "q12JobCritCompCulture", "q12JobCritWorkLifeBal", "q12JobCritCompensation", "q12JobCritProximity", "q12JobCritPerks", "q12JobCritSmartPeopleTeam", "q12JobCritImpactwithProduct", "q12JobCritInterestProblems", "q12JobCritFundingandValuation", "q12JobCritStability", "q12JobCritProfGrowth", "q12JobCritOther"]]

    totalDictionary = {}

    for i in criteriaDataframe:
        eachSeries = df[i]
        eachDict = dict(eachSeries.value_counts())
        totalDictionary.update(eachDict)

    del totalDictionary["#NULL!"]
    sortedValues = sorted(totalDictionary.values(), reverse=True)
    topFiveDictionary = {}

    for i in range(0, 5):
        for key in totalDictionary:
            if totalDictionary[key] == sortedValues[i]:
                topFiveDictionary[key] = totalDictionary[key]
                del totalDictionary[key]
                break

    plotGraph(topFiveDictionary.keys(), topFiveDictionary.values(), "Five Criterias", "Total Number of Votes", "Employee Top Five Job Criterias", "bar")

        # print(str(i))

def getTopEmployeeInterviewStyles():
    interviewDataframe = df[
        ["q13EmpMeasWhiteboard", "q13EmpMeasHackerRank", "q13EmpMeasOtherCodingChallenge", "q13EmpMeasTechPhoneInt",
         "q13EmpMeasTakeHomeProject", "q13EmpMeasResume", "q13EmpMeasPastWork", "q13EmpMeasOther"]]

    totalDictionary = {}

    for i in interviewDataframe:
        totalDictionary.update(dict(df[i].value_counts()))

    print(str(totalDictionary))

    # sortedValues = sorted(totalDictionary.values(), reverse=True)
    #
    # topFiveDictionary = {}
    #
    # for i in range(0, 5):
    #     for key in totalDictionary:
    #         if totalDictionary[key] == sortedValues[i]:
    #             topFiveDictionary[key] = totalDictionary[key]
    #             del totalDictionary[key]
    #             break

    plotGraph(totalDictionary.keys(), totalDictionary.values(), "",
              "", "Most Common Ways that Recruiters Measure Your Skills", "pie", explode=(0.01, 0.01, 0.01, 0.01 ,0.01, 0.01, 0.01, 0.01), radius=0.7, pctdistance=0.8)


    # criteriaDictionary = dict(criteriaSeries.value_counts())

    # print(str(criteriaSeries.info()))


    """
    What country are these hackers from?
    """
    def hackerCountryMap():

        # map country to pygal country code

        # get country responses from csv in list
        country_responses = df["CountryNumeric2"]

        # get count for each country code
        hackers_per_country = dict(country_responses.value_counts())

        # map country name to pygal country code
        pygal_countries = pd.Series(df_pygal_country_codes.code.values, index=df_pygal_country_codes.Country).to_dict()

        # make dict with key = pygal country code, value = number of hackers

        range_0_100 = []
        range_101_200 = []
        range_201_300 = []
        range_301_400 = []
        range_401_500 = []
        range_500_plus = []

        for key in pygal_countries:
            if key in hackers_per_country:
                if hackers_per_country[key] > 500:
                    range_500_plus.append(pygal_countries[key])
                elif hackers_per_country[key] > 400:
                    range_401_500.append(pygal_countries[key])
                elif hackers_per_country[key] > 300:
                    range_301_400.append(pygal_countries[key])
                elif hackers_per_country[key] > 200:
                    range_201_300.append(pygal_countries[key])
                elif hackers_per_country[key] > 100:
                    range_101_200.append(pygal_countries[key])
                else:
                    range_0_100.append(pygal_countries[key])

        worldmap_chart = pygal.maps.world.World()
        worldmap_chart.title = 'Some countries'
        worldmap_chart.add('0 to 100 users', range_0_100)
        worldmap_chart.add('101 to 200 users', range_101_200)
        worldmap_chart.add('201 to 300 users', range_201_300)
        worldmap_chart.add('301 to 400 users', range_301_400)
        worldmap_chart.add('401 to 500 users', range_401_500)
        worldmap_chart.add('More than 500 users', range_500_plus)
        worldmap_chart.render_to_png()


"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~INITIAL METHOD~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

if __name__ == "__main__":
    readFile()
    # getAgeTheyStartedCoding()
    # getCurrentAge()
    # getGender()
    # getEducationLevel()
    # getEmployeeJobCriteria()
    getTopEmployeeInterviewStyles()