import pandas as pd
import matplotlib.pyplot as plt

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


def plotGraph(xAxisValues, yAxisValues, xLabel, yLabel, title, type, explode=None, pctdistance=0.6, radius=1,
              figsize=None, filename="blank.png"):
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
        plt.pie(x=yAxisValues, labels=xAxisValues, autopct='%1.1f%%', explode=explode, pctdistance=pctdistance,
                radius=radius)
        if figsize != None:
            plt.figure(figsize=figsize)

    # Set the X, Y, and Title labels
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)

    plt.savefig(filename)

    # Display the graph
    plt.show()
    plt.close()


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
    # Read the data from the CSV file and store it into a dataframe
    df = pd.read_csv("HackerRank-Developer-Survey-2018-Values.csv")


"""
Used to plot the Age Information
"""


def getAgeTheyStartedCoding():
    # Store the age data into a Series object
    ageSeries = df["q1AgeBeginCoding"]

    # Store the unique age entries and the number for each entry into a dictionary
    somedict = dict(ageSeries.value_counts())

    sortedDictionary = orderAges(somedict, ["#NULL!", "50+ years or older"])

    # Remove excess text from all the keys in the dictionary
    Keys = []
    for i in sortedDictionary.keys():
        Keys.append("         " + trimText(i) + "         ")

    plotGraph(Keys, sortedDictionary.values(), "Years Old", "Number of People", "When Did Most Users Start Coding?",
              "line", filename="AgeTheyStartedCoding.png")


"""
Used to plot Country information
"""


def getCountry():

    # get country responses from csv in list
    country_responses = df["CountryNumeric2"]

    # get count for each country code
    hackers_per_country = dict(country_responses.value_counts())

    sorted_values = sorted(hackers_per_country.values(), reverse=True)
    top_five_dict = {}
    other_count = 0

    for i in range(0, 5):
        for key in hackers_per_country:
            if hackers_per_country[key] == sorted_values[i]:
                top_five_dict[key] = hackers_per_country[key]
                del hackers_per_country[key]
                break

    for key in hackers_per_country:
        if not key in top_five_dict:
            other_count += hackers_per_country[key]

    top_five_dict["Other"] = other_count

    plotGraph(top_five_dict.keys(), top_five_dict.values(), "", "", "Top Countries HackerRank Users Reside In","pie",
              pctdistance=0.9, explode=(0.01, 0.01, 0.03, 0.03, 0.03, 0.03), filename="Countries.png")


"""
Used to plot how users learned to code
"""


def getLearnedToCodeBy():
    criteriaDataframe = df[
        ["q6LearnCodeUni", "q6LearnCodeSelfTaught",  "q6LearnCodeAccelTrain", "q6LearnCodeDontKnowHowToYet",
         "q6LearnCodeOther"]]

    totalDictionary = {}

    for i in criteriaDataframe:
        eachSeries = df[i]
        eachDict = dict(eachSeries.value_counts())
        totalDictionary.update(eachDict)

    sortedValues = sorted(totalDictionary.values(), reverse=True)
    topFiveDictionary = {}

    for i in range(0, 5):
        for key in totalDictionary:
            if totalDictionary[key] == sortedValues[i]:
                topFiveDictionary[key] = totalDictionary[key]
                del totalDictionary[key]
                break

    plotGraph(topFiveDictionary.keys(), topFiveDictionary.values(), "", "Total Number of Users",
              "How Users Learned to Code", "bar", filename="LearnedToCode.png")


"""
Used to plot user's job level
"""


def getJobLevel():
    # get country responses from csv in list
    job_level_responses = df["q8JobLevel"]

    # get count for each country code
    hackers_job = dict(job_level_responses.value_counts())

    hackers_job["Senior Developer"] = hackers_job.pop("Senior developer")
    hackers_job["Junior Developer"] = hackers_job.pop("Level 1 developer (junior)")
    hackers_job["New Grad"] = hackers_job.pop("New grad")
    hackers_job["Principal Engineer"] = hackers_job.pop("Principal engineer")
    hackers_job["Engineering Manager"] = hackers_job.pop("Engineering manager")

    sorted_values = sorted(hackers_job.values(), reverse=True)

    graph_dict = {}

    for i in range(0, len(sorted_values)):
        for key in hackers_job:
            if hackers_job[key] == sorted_values[i]:
                graph_dict[key] = hackers_job[key]
                del hackers_job[key]
                break

    plotGraph(graph_dict.keys(), graph_dict.values(), "", "", "Job Level","pie", pctdistance=0.9,
              explode=(0.02, 0.05, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1), filename="JobLevel.png")


"""
Used to plot user's degree focus (if user is a student)
"""


def getDegreeFocus():

    # get country responses from csv in list
    degree_responses = df["q5DegreeFocus"]

    # get count for each country code
    hackers_degrees = dict(degree_responses.value_counts())
    hackers_degrees["Other"] = hackers_degrees["Other STEM (science, technology, engineering, math)"]
    del hackers_degrees["#NULL!"]
    del hackers_degrees["Other STEM (science, technology, engineering, math)"]

    plotGraph(hackers_degrees.keys(), hackers_degrees.values(), "", "", "Degree Focus of Students Using HackerRank",
              "pie", explode=(0.01, 0.01), filename="DegreeFocus.png")


"""
Used to plot user's age
"""


def getCurrentAge():
    currentAgeSeries = df["q2Age"]

    ageDictionary = dict(currentAgeSeries.value_counts())

    sortedDictionary = orderAges(ageDictionary, ["#NULL!", "Under 12 years old", "75 years or older"])

    Keys = []
    for i in sortedDictionary.keys():
        Keys.append("         " + trimText(i) + "         ")

    plotGraph(Keys, sortedDictionary.values(), "Years Old", "Number of People", "How Old are the Users Now?", "bar",
              filename="CurrentAgePlot.png")


"""
Used to plot usesr's gender
"""


def getGender():
    genderSeries = df["q3Gender"]

    genderDictionary = dict(genderSeries.value_counts())

    del genderDictionary["#NULL!"]


    plotGraph(genderDictionary.keys(), genderDictionary.values(), "", "", "Gender of HackerRank Users", "pie",
              (0, 0.05, 0.05), filename="GenderPlot.png")


"""
Used to plot user's education level
"""


def getEducationLevel():
    educationSeries = df["q4Education"]

    educationDictionary = dict(educationSeries.value_counts())

    del educationDictionary["#NULL!"]

    plotGraph(educationDictionary.keys(), educationDictionary.values(), "", "", "Education Level of HackerRank Users",
              "pie", explode=(0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.2), radius=0.7, pctdistance=0.8,
              filename="EducationLevelPlot.png")


"""
Used to plot top employee job criteria
"""


def getEmployeeJobCriteria():
    criteriaDataframe = df[
        ["q12JobCritPrefTechStack", "q12JobCritCompMission", "q12JobCritCompCulture", "q12JobCritWorkLifeBal",
         "q12JobCritCompensation", "q12JobCritProximity", "q12JobCritPerks", "q12JobCritSmartPeopleTeam",
         "q12JobCritImpactwithProduct", "q12JobCritInterestProblems", "q12JobCritFundingandValuation",
         "q12JobCritStability", "q12JobCritProfGrowth", "q12JobCritOther"]]

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

    plotGraph(topFiveDictionary.keys(), topFiveDictionary.values(), "Five Criterias", "Total Number of Votes",
              "Employee Top Five Job Criterias", "bar", filename="EmployeeJobCriteria.png")



"""
Used to plot employee interview styles
"""


def getTopEmployeeInterviewStyles():
    interviewDataframe = df[
        ["q13EmpMeasWhiteboard", "q13EmpMeasHackerRank", "q13EmpMeasOtherCodingChallenge", "q13EmpMeasTechPhoneInt",
         "q13EmpMeasTakeHomeProject", "q13EmpMeasResume", "q13EmpMeasPastWork", "q13EmpMeasOther"]]

    totalDictionary = {}

    for i in interviewDataframe:
        totalDictionary.update(dict(df[i].value_counts()))

    plotGraph(totalDictionary.keys(), totalDictionary.values(), "",
              "", "Most Common Ways that Recruiters Measure Your Skills", "pie",
              explode=(0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01), radius=0.7, pctdistance=0.8,
              filename="EmployeeInterviewStyles.png")



"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~INITIAL METHOD~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

if __name__ == "__main__":
    readFile()
    getLearnedToCodeBy()
    getJobLevel()
    getDegreeFocus()
    getCountry()
    getAgeTheyStartedCoding()
    getCurrentAge()
    getGender()
    getEducationLevel()
    getEmployeeJobCriteria()
    getTopEmployeeInterviewStyles()