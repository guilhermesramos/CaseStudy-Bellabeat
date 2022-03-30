# 1 REQUIRED LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2 Set seaborn theme

sns.set_style("white")
sns.set_palette("hls")

# 3 READ-IN DATA
activityDataFrame = pd.read_csv("./data/dailyActivity_merged.csv")
print(activityDataFrame.info())
print(activityDataFrame.columns)
print(f"Activity Dataframe \n {activityDataFrame}")

# 4 PROCESS DATA

# A) Check for null values and duplicates rows.

print(activityDataFrame.isnull().sum())
print(activityDataFrame.duplicated().sum())

# There are no null values or multiple rows.

# B) Convert the ActivityDate column into  a datetime


activityDataFrame["ActivityDate"] = pd.to_datetime(activityDataFrame["ActivityDate"])
print(activityDataFrame.info())

# C) Summary of the data :


print(activityDataFrame.describe())

# Average number of steps is 7637.91steps
# Maximum number of steps is 36019.00
# Average distance by an individual is 5.49 Km
# Maximum distance by an individual is 28.03 Km

# Average amount of Calories burnt is 2303.61
# Maximum amount of Calories burnt is 4900.00

# 5 ANALYZE DATA

# A) Establish the relationship between Total Steps and Total Distance.


# This step is to determine if Total Steps variable can be used in place of Total Distance.

steps_distance_corr = activityDataFrame["TotalSteps"].corr(activityDataFrame["TotalDistance"])
print(f"Total Distance-Total Steps Corr is {steps_distance_corr}")

# This yields a correlation of 0.9853 and shows a  positive relationship between Total Distance and Total Steps taken.
# Given this correlation and that distance is derived from steps, Total Steps will be used in this analysis.

# B) Establish the relationship between Total Steps and Calories burned


# First, get the correlation

totalSteps_Calories = activityDataFrame["TotalSteps"].corr(activityDataFrame["Calories"])
print(f" Steps-Calories Correlation  is {totalSteps_Calories}")

# This correlation is 0.5916
# There is a large positive correlation between total steps taken and calories burnt.

# Plot data in a scatterplot
plt.figure(figsize=(8, 4.21), dpi=100, layout='constrained')
plt.title("Calories Burned vs Total Steps", pad=20, loc="left")
sns.scatterplot(data=activityDataFrame, x="TotalSteps", y="Calories")
plt.show()
#  Total Steps and Calories exhibit a linear relationship as shown above.


# C) Establish the relationship between very active minutes and calories burnt.


active_Calories = activityDataFrame["VeryActiveMinutes"].corr(activityDataFrame["Calories"])
print(f"Active Minutes-Calories Corr is {active_Calories}")

# This correlation is 0.6158.
# There is a large positive correlation between the two variables.

# Visualize the data in a scatter plot.
plt.figure(figsize=(8, 4.21), dpi=100)
plt.title("Calories Burned vs Very Active Minutes", pad=20, loc="left")
sns.scatterplot(data=activityDataFrame, x="VeryActiveMinutes", y="Calories")
plt.show()

# D) Establish the relationship between Sedentary minutes and Calories.


sedentary_Calories = activityDataFrame["SedentaryMinutes"].corr(activityDataFrame["Calories"])
print(f"Sedentary-Calories Corr is {sedentary_Calories}")

# This correlation  is -0.1069.
# This shows a small negative relationship between time being sedentary and Calories burnt

# Visualize the  data in a scatter plot.
plt.figure(figsize=(8, 4.21), dpi=100)
plt.title("Calories Burned vs Sedentary Minutes", pad=20, loc="left")
sns.scatterplot(data=activityDataFrame, x="SedentaryMinutes", y="Calories")
plt.show()

# E) Establish the days of the week when individuals are most active


# First, create a new column with ActivityDate represented as day of the week

activityDataFrame["day_of_week"] = activityDataFrame["ActivityDate"].dt.day_name()
activityDataFrame["day_number"] = activityDataFrame["ActivityDate"].dt.weekday
print(activityDataFrame)

# A list with days of the week and group then.

week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
activeMinutesPerDay = activityDataFrame.groupby(["day_number"])["VeryActiveMinutes"]

# Total Active Minutes
sumActiveMinutesPerDay = (
    activeMinutesPerDay.sum().rename_axis("Day").reset_index(name="Minutes")
)
print(sumActiveMinutesPerDay)

# Visualize the data
plt.figure(figsize=(8, 4.21), dpi=100)
plt.title("Total Active Minutes per Day", pad=20, loc="left")
sns.barplot(data=sumActiveMinutesPerDay, x=week, y="Minutes")
plt.show()

# From this visualization, Tuesday and Wednesday have the most active minutes.

# F) Average active minutes per day


meanActiveMinutesPerDay = (
    activeMinutesPerDay.mean().rename_axis("Day").reset_index(name="Minutes")
)
print(meanActiveMinutesPerDay)

# Visualize the data
plt.figure(figsize=(8, 4.21), dpi=100)
plt.title("Average Active Minutes per Day", pad=20, loc="left")
sns.barplot(data=meanActiveMinutesPerDay, x=week, y="Minutes")
plt.show()

# From this analysis, Monday and Tuesday have the highest active minutes.

# G) To explore difference between the sum and mean visualizations find the count of each day in the dataframe.


print(activityDataFrame["day_number"].value_counts())

# This indicates a variation in the count of days and thus the differences in mean.
# Meaning that we cannot say for sure which day are people most active using the sum.
# To get a fair conclusion, we shall rely on the mean.


# 7) Find out how movement (measured by total steps) varies per day

stepsPerDay = activityDataFrame.groupby(["day_number"])["TotalSteps"]
averageStepsPerDay = (
    stepsPerDay.mean().rename_axis("Day").reset_index(name="Steps")
)
print(averageStepsPerDay)

# Visualize the data
plt.figure(figsize=(8, 4.21), dpi=100)
plt.title("Average Steps per Day", pad=20, loc="left")
sns.barplot(data=averageStepsPerDay, x=week, y="Steps")
plt.show()
