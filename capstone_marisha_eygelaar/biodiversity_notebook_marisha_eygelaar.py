
# coding: utf-8

# # Capstone 2: Biodiversity Project

# # Introduction
# You are a biodiversity analyst working for the National Parks Service.  You're going to help them analyze some data about species at various national parks.
# 
# Note: The data that you'll be working with for this project is *inspired* by real data, but is mostly fictional.

# # Step 1
# Import the modules that you'll be using in this assignment:
# - `from matplotlib import pyplot as plt`
# - `import pandas as pd`

# In[1]:


from matplotlib import pyplot as plt
import pandas as pd


# # Step 2
# You have been given two CSV files. `species_info.csv` with data about different species in our National Parks, including:
# - The scientific name of each species
# - The common names of each species
# - The species conservation status
# 
# Load the dataset and inspect it:
# - Load `species_info.csv` into a DataFrame called `species`

# In[2]:


species = pd.read_csv('species_info.csv')


# Inspect each DataFrame using `.head()`.

# In[3]:


species.head(10)


# # Step 3
# Let's start by learning a bit more about our data.  Answer each of the following questions.

# How many different species are in the `species` DataFrame?

# In[5]:


species.scientific_name.nunique()


# What are the different values of `category` in `species`?

# In[6]:


species.category.unique()


# What are the different values of `conservation_status`?

# In[7]:


species.conservation_status.unique()


# # Step 4
# Let's start doing some analysis!
# 
# The column `conservation_status` has several possible values:
# - `Species of Concern`: declining or appear to be in need of conservation
# - `Threatened`: vulnerable to endangerment in the near future
# - `Endangered`: seriously at risk of extinction
# - `In Recovery`: formerly `Endangered`, but currnetly neither in danger of extinction throughout all or a significant portion of its range
# 
# We'd like to count up how many species meet each of these criteria.  Use `groupby` to count how many `scientific_name` meet each of these criteria.

# In[8]:


conservation_status_count = species.groupby('conservation_status').scientific_name.count().reset_index()
conservation_status_count = conservation_status_count.rename(columns={'scientific_name': 'species_count'})
conservation_status_count.head()


# As we saw before, there are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  The rest have `conservation_status` equal to `None`.  Because `groupby` does not include `None`, we will need to fill in the null values.  We can do this using `.fillna`.  We pass in however we want to fill in our `None` values as an argument.
# 
# Paste the following code and run it to see replace `None` with `No Intervention`:
# ```python
# species.fillna('No Intervention', inplace=True)
# ```

# In[13]:


species.fillna('No Intervention', inplace=True)


# Great! Now run the same `groupby` as before to see how many species require `No Protection`.

# In[14]:


conservation_status_count = species.groupby('conservation_status').scientific_name.nunique().reset_index()
conservation_status_count = conservation_status_count.rename(columns={'scientific_name': 'species_count'})
conservation_status_count.head()


# Let's use `plt.bar` to create a bar chart.  First, let's sort the columns by how many species are in each categories.  We can do this using `.sort_values`.  We use the the keyword `by` to indicate which column we want to sort by.
# 
# Paste the following code and run it to create a new DataFrame called `protection_counts`, which is sorted by `scientific_name`:
# ```python
# protection_counts = species.groupby('conservation_status')\
#     .scientific_name.count().reset_index()\
#     .sort_values(by='scientific_name')
# ```

# In[15]:


protection_counts = species.groupby('conservation_status')    .scientific_name.count().reset_index()    .sort_values(by='scientific_name')
protection_counts.head()


# Now let's create a bar chart!
# 1. Start by creating a wide figure with `figsize=(10, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `scientific_name` column of `protection_counts`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `conservation_status` in `protection_counts`
# 5. Label the y-axis `Number of Species`
# 6. Title the graph `Conservation Status by Species`
# 7. Plot the grap using `plt.show()`

# In[16]:


plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts.scientific_name)),protection_counts.scientific_name)
ax.set_xticks(range(len(protection_counts.scientific_name)))
ax.set_xticklabels(protection_counts.conservation_status)
plt.xlabel('Conservation Status')
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
plt.show


# Step 4
# 
# Are certain types of species more likely to be endangered?

# Let's create a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise.

# In[17]:


protection = lambda x: 'True' if x != 'No Intervention'                        else 'False'
species['is_protected'] = species.conservation_status.apply(protection)
species.head(10)


# Let's group by *both* `category` and `is_protected`.  Save your results to `category_counts`.

# In[22]:


category_counts = species.groupby(['category', 'is_protected']) .scientific_name.nunique().reset_index()    .sort_values(by='scientific_name')


# Examine `category_count` using `head()`.

# In[23]:


category_counts.head(10)


# It's going to be easier to view this data if we pivot it.  Using `pivot`, rearange `category_counts` so that:
# - `columns` is `conservation_status`
# - `index` is `category`
# - `values` is `scientific_name`
# 
# Save your pivoted data to `category_pivot`. Remember to `reset_index()` at the end.

# In[24]:


category_pivot = category_counts.pivot(columns ='is_protected',index = 'category', values = 'scientific_name').reset_index()


# Examine `category_pivot`.

# In[25]:


category_pivot.head(10)


# Use the `.columns` property to  rename the categories `True` and `False` to something more description:
# - Leave `category` as `category`
# - Rename `False` to `not_protected`
# - Rename `True` to `protected`

# In[26]:


category_pivot.columns = ['category','not_protected','protected']
category_pivot.head(10)


# Let's create a new column of `category_pivot` called `percent_protected`, which is equal to `protected` (the number of species that are protected) divided by `protected` plus `not_protected` (the total number of species).

# In[27]:


percent_protected = lambda row:(row.protected / float(row.protected + row.not_protected))*100
category_pivot['percent_protected'] = category_pivot.apply(percent_protected,axis = 1).round(2)


# Examine `category_pivot`.

# In[28]:


category_pivot.head(10)


# It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`.  We're going to do a significance test to see if this statement is true.  Before you do the significance test, consider the following questions:
# - Is the data numerical or categorical?
# - How many pieces of data are you comparing?

# Based on those answers, you should choose to do a *chi squared test*.  In order to run a chi squared test, we'll need to create a contingency table.  Our contingency table should look like this:
# 
# ||protected|not protected|
# |-|-|-|
# |Mammal|?|?|
# |Bird|?|?|
# 
# Create a table called `contingency` and fill it in with the correct numbers

# In[32]:


contingency = [[30,146], [75,413]]


# In order to perform our chi square test, we'll need to import the correct function from scipy.  Past the following code and run it:
# ```py
# from scipy.stats import chi2_contingency
# ```

# In[33]:


from scipy.stats import chi2_contingency


# Now run `chi2_contingency` with `contingency`.

# In[34]:


_, pvalue, _, _ = chi2_contingency(contingency)
print pvalue


# It looks like this difference isn't significant!
# 
# Let's test another.  Is the difference between `Reptile` and `Mammal` significant?

# In[35]:


contingency = [[30,146], [5,73]]
_, pvalue, _, _ = chi2_contingency(contingency)
print pvalue


# Yes! It looks like there is a significant difference between `Reptile` and `Mammal`!

# # Step 5

# Conservationists have been recording sightings of different species at several national parks for the past 7 days.  They've saved sent you their observations in a file called `observations.csv`.  Load `observations.csv` into a variable called `observations`, then use `head` to view the data.

# In[36]:


observations = pd.read_csv('observations.csv')
observations.head(30)


# Some scientists are studying the number of sheep sightings at different national parks.  There are several different scientific names for different types of sheep.  We'd like to know which rows of `species` are referring to sheep.  Notice that the following code will tell us whether or not a word occurs in a string:

# In[37]:


# Does "Sheep" occur in this string?
str1 = 'This string contains Sheep'
'Sheep' in str1


# In[38]:


# Does "Sheep" occur in this string?
str2 = 'This string contains Cows'
'Sheep' in str2


# Use `apply` and a `lambda` function to create a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise.

# In[39]:


species['is_sheep'] = species.apply(lambda row: 'Sheep' in row.common_names, axis = 1)
species.head(10)


# Select the rows of `species` where `is_sheep` is `True` and examine the results.

# In[40]:


sheep_species = species.loc[species.is_sheep == True]
sheep_species.head(10)


# Many of the results are actually plants.  Select the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  Save the results to the variable `sheep_species`.

# In[43]:


sheep_species = species.loc[(species.is_sheep == True) & (species.category == 'Mammal')]
sheep_species.head()


# Now merge `sheep_species` with `observations` to get a DataFrame with observations of sheep.  Save this DataFrame as `sheep_observations`.

# In[44]:


sheep_observations = pd.merge(sheep_species,observations, how = 'inner')
sheep_observations.head()


# How many total sheep observations (across all three species) were made at each national park?  Use `groupby` to get the `sum` of `observations` for each `park_name`.  Save your answer to `obs_by_park`.
# 
# This is the total number of sheep observed in each park over the past 7 days.

# In[46]:


obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
obs_by_park.head()


# Create a bar chart showing the different number of observations per week at each park.
# 
# 1. Start by creating a wide figure with `figsize=(16, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `observations` column of `obs_by_park`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `park_name` in `obs_by_park`
# 5. Label the y-axis `Number of Observations`
# 6. Title the graph `Observations of Sheep per Week`
# 7. Plot the grap using `plt.show()`

# In[47]:


plt.figure(figsize=(16, 4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park.observations)),obs_by_park.observations)
ax.set_xticks(range(len(obs_by_park.observations)))
ax.set_xticklabels(obs_by_park.park_name)
plt.xlabel('National Parks')
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
plt.show


# Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  Park rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.  The scientists want to test whether or not this program is working.  They want to be able to detect reductions of at least 5 percentage point.  For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
# 
# Use the sample size calculator at <a href="https://www.optimizely.com/sample-size-calculator/">Optimizely</a> to calculate the number of sheep that they would need to observe from each park.  Use the default level of significance (90%).
# 
# Remember that "Minimum Detectable Effect" is a percent of the baseline.

# In[48]:


baseline = 15
mde = (5/15.0)*100
sample_size = 510
print baseline
print mde
print sample_size


# How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?  How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?

# In[49]:


bryce = (510/250.0)
yellowstone = (510/507.0)
print bryce
print yellowstone

