#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending 645-675 per student actually underperformed compared to schools with smaller budgets (585 per student).
# 
# * As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# * As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
# ---

# In[1]:


# Dependencies and Setup
import pandas as pd
from pathlib import Path

# File to Load (Remember to Change These)
school_data_to_load = Path("Resources/schools_complete.csv")
student_data_to_load = Path("Resources/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete


# ## District Summary

# In[2]:


# Calculate the total number of unique schools
school_count = len(school_data_complete["school_name"].unique())
school_count_total = school_data_complete["Student ID"].count()
school_count_total


# In[3]:


# Calculate the total number of students #correct
student_count = school_data_complete["Student ID"].nunique()
student_count


# In[4]:


# Calculate the total budget
total_budget = school_data_complete["budget"].unique().sum()
total_budget


# In[5]:


# Calculate the average (mean) math score
average_math_score = school_data_complete["math_score"].sum()/len(school_data_complete["math_score"])
average_math_score


# In[6]:


# Calculate the average (mean) reading score
average_reading_score = school_data_complete["reading_score"].sum()/len(school_data_complete["reading_score"])
average_reading_score


# In[7]:


# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage


# In[8]:


# Calculate the percentage of students who passeed reading (hint: look at how the math percentage was calculated)  
student_count = school_data_complete["Student ID"].nunique()
passing_reading_count = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage


# In[9]:


# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count / float(student_count) * 100
overall_passing_rate


# In[10]:


##Checl % overall passing and total schools
average_math_score = school_data_complete["math_score"].mean()
average_reading_score = school_data_complete["reading_score"].mean()
overall_passing_rate = (average_math_score + average_reading_score)/2

# Create a high-level snapshot of the district's key metrics in a DataFrame


district_summary = pd.DataFrame(
          [{"Total Schools": school_count, 
          "Total Students": student_count, 
          "Total Budget": total_budget,
          "Average Math Score": average_math_score, 
        "Average Reading Score": average_reading_score,
          "% Passing Math": passing_math_percentage,
         "% Passing Reading": passing_reading_percentage,
            "%Overall Passing Rate" : overall_passing_rate
      }])


# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)

# Display the DataFrame
district_summary


# ## School Summary

# In[11]:


# Use the code provided to select the school type
school_types = school_data.set_index(["school_name"])["type"]


# In[12]:


# Calculate the total student count
per_school_counts = school_data_complete['student_name'].count()


# In[13]:


# Calculate the total school budget and per capita spending
per_school_budget = school_data_complete.groupby(["school_name"]).mean()["budget"]
per_school_capita = per_school_budget / per_school_counts



# In[14]:


# Calculate the average test scores
per_school_math = school_data_complete.groupby(["school_name"]).mean()["math_score"]
per_school_reading = school_data_complete.groupby(["school_name"]).mean()["reading_score"]
per_school_math


# In[15]:


# Calculate the number of schools with math scores of 70 or higherco
school_passing_math = school_data_complete[(school_data_complete["math_score"] >= 70)]


# In[16]:


# Calculate the number of schools with reading scores of 70 or higher
school_passing_reading = school_data_complete[(school_data_complete["reading_score"] >= 70)]


# In[17]:


# Use the provided code to calculate the schools that passed both math and reading with scores of 70 or higher
passing_math_and_reading = school_data_complete[
    (school_data_complete["reading_score"] >= 70) & (school_data_complete["math_score"] >= 70)]
passing_math_and_reading


# In[18]:


# Use the provided code to calculate the passing rates
##pd.DataFame
per_school_passing_math = school_passing_math.groupby(["school_name"]).count()["student_name"]/per_school_counts * 100
per_school_passing_reading = school_passing_reading.groupby(["school_name"]).count()["student_name"] /per_school_counts * 100
overall_passing_rate = passing_math_and_reading.groupby(["school_name"]).count()["student_name"] /per_school_counts * 100



# In[19]:


# Create a DataFrame called `per_school_summary` with columns for the calculations above.
per_school_summary = pd.DataFrame({"School Type": school_types,
                                  "Total Students": per_school_counts,
                                  "Total School Budget": per_school_budget,
                                  "Per Student Budget": per_school_capita,
                                  "Average Math Score": per_school_math,
                                  "Average Reading Score": per_school_reading,
                                  "% Passing Math" : per_school_passing_math,
                                  "% Passing Reading" : per_school_passing_reading,
                                  "% Overall Passing" : overall_passing_rate})

# Formatting
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)

# Display the DataFrame
per_school_summary


# ## Highest-Performing Schools (by % Overall Passing)

# In[20]:


# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values(["% Overall Passing"], ascending=False)
top_schools.head(5)


# ## Bottom Performing Schools (By % Overall Passing)

# In[21]:


# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values(["% Overall Passing"], ascending= True)
bottom_schools.head(5)


# ## Math Scores by Grade

# In[22]:


# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by "school_name" and take the mean of each.
ninth_graders_scores = ninth_graders.groupby(["school_name"]).mean()
tenth_graders_scores = tenth_graders.groupby(["school_name"]).mean()
eleventh_graders_scores = eleventh_graders.groupby(["school_name"]).mean()
twelfth_graders_scores = twelfth_graders.groupby(["school_name"]).mean()

# Use the code to select only the `math_score`.
ninth_grader_math_scores = ninth_graders_scores["math_score"]
tenth_grader_math_scores = tenth_graders_scores["math_score"]
eleventh_grader_math_scores = eleventh_graders_scores["math_score"]
twelfth_grader_math_scores = twelfth_graders_scores["math_score"]

# Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_scores_by_grade = pd.DataFrame({"9th": ninth_grader_math_scores, "10th": tenth_grader_math_scores, 
                                     "11th": eleventh_grader_math_scores,
                                    "12th": twelfth_grader_math_scores})


# Minor data wrangling
math_scores_by_grade.index.name = None

# Display the DataFrame
math_scores_by_grade


# ## Reading Score by Grade 

# In[23]:


# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by "school_name" and take the mean of each.
ninth_graders_scores = ninth_graders.groupby(["school_name"]).mean()
tenth_graders_scores = tenth_graders.groupby(["school_name"]).mean()
eleventh_graders_scores = eleventh_graders.groupby(["school_name"]).mean()
twelfth_graders_scores = twelfth_graders.groupby(["school_name"]).mean()

# Use the code to select only the `reading_score`.
ninth_grader_reading_scores = ninth_graders_scores["reading_score"]
tenth_grader_reading_scores = tenth_graders_scores["reading_score"]
eleventh_grader_reading_scores = eleventh_graders_scores["reading_score"]
twelfth_grader_reading_scores = twelfth_graders_scores["reading_score"]

# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade = pd.DataFrame({"9th": ninth_grader_reading_scores, "10th": tenth_grader_reading_scores, 
                                     "11th": eleventh_grader_reading_scores,
                                    "12th": twelfth_grader_reading_scores})


# Minor data wrangling
reading_scores_by_grade = reading_scores_by_grade[["9th", "10th", "11th", "12th"]]
reading_scores_by_grade.index.name = None

# Display the DataFrame
reading_scores_by_grade


# ## Scores by School Spending

# In[24]:


# Establish the bins 
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]


# In[ ]:





# In[25]:


# Create a copy of the school summary since it has the "Per Student Budget" 
school_spending_df = per_school_summary.copy()


# In[26]:


# Use `pd.cut` to categorize spending based on the bins.
school_spending_df["Spending Ranges (Per Student)"] = pd.cut(per_school_capita, bins = spending_bins , labels = labels)
school_spending_df


# In[27]:


#  Calculate averages for the desired columns. 
spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Math Score"]
spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Reading Score"]
spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Math"]
spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Reading"]
overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Overall Passing"]


# In[28]:


# Assemble into DataFrame
spending_summary = pd.DataFrame ({"Spending Math Scores":spending_math_scores, "Spending Reading Scores" : spending_reading_scores,
                            
                                  "Spending Passing Math": spending_passing_math,
                                  "Spending Passing Reading" :spending_passing_reading,
                                  "Overall Passing Spending" :overall_passing_spending 
                                 })

# Display results
spending_summary


# ## Scores by School Size

# In[29]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[30]:


# Categorize the spending based on the bins
# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

per_school_summary["School Size"] = pd.cut(per_school_summary["Total Students"],bins=size_bins, labels =labels)
per_school_summary


# In[31]:


# Calculate averages for the desired columns. 
size_math_scores = per_school_summary.groupby(["School Size"]).mean()["Average Math Score"]
size_reading_scores = per_school_summary.groupby(["School Size"]).mean()["Average Reading Score"]
size_passing_math = per_school_summary.groupby(["School Size"]).mean()["% Passing Math"]
size_passing_reading = per_school_summary.groupby(["School Size"]).mean()["% Passing Reading"]
size_overall_passing = per_school_summary.groupby(["School Size"]).mean()["% Overall Passing"]


# In[32]:


# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_summary = pd.DataFrame({"Average Math Score" : size_math_scores, "Average Reading Score" : size_reading_scores, "% Passing Math" :size_passing_math,
"% Passing Reading" : size_passing_reading, "% Overall Passing" : size_overall_passing})                    
# Display results
size_summary


# ## Scores by School Type

# In[34]:


# Group the per_school_summary DataFrame by "School Type" and average the results.
type_math_scores = per_school_summary.groupby("School Type").mean()
type_reading_scores = per_school_summary.groupby("School Type").mean()
type_passing_math = per_school_summary.groupby("School Type").mean()
type_passing_reading = per_school_summary.groupby("School Type").mean()
type_overall_passing = per_school_summary.groupby("School Type").mean()

# Use the code provided to select new column data
average_math_score_by_type = type_math_scores["Average Math Score"]
average_reading_score_by_type = type_reading_scores["Average Reading Score"]
average_percent_passing_math_by_type = type_passing_math["% Passing Math"]
average_percent_passing_reading_by_type = type_passing_reading["% Passing Reading"]
average_percent_overall_passing_by_type = type_overall_passing["% Overall Passing"]


# In[37]:


# Assemble the new data by type into a DataFrame called `type_summary`
type_summary = pd.DataFrame({"Average Math Score": average_math_score_by_type ,
                "Average Reading Score":average_reading_score_by_type,
                "% Passing Math": average_percent_passing_math_by_type,
                "% Passing Reading": average_percent_passing_reading_by_type,
                "% Overall Passing Rate": average_percent_overall_passing_by_type})

# Display results
type_summary


# In[ ]:





# In[ ]:




