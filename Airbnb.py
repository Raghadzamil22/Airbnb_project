#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


# In[29]:


#load the dataset
df = pd.read_csv("listings.csv")


# In[30]:


#display the first few rows of dataset
df.head()


# In[31]:


# Check the information of the dataset
df.info()


# In[49]:


# Statistical Summary
print("--- Statistical Summary ---")
print(df.describe())


# In[32]:


# Drop unnecessary columns
df.drop(['license','neighbourhood_group','last_review'], axis = 1, inplace = True)


# In[33]:


# Fill missing values
df['reviews_per_month'].fillna('No reviews', inplace=True)


# In[34]:


# Fill missing values
df['price'].fillna(df['price'].median(), inplace=True)


# In[35]:


# Check for missing values
df.isnull().sum()


# In[36]:


#print the dataset after Drop and fill missing values
df


# In[50]:


#Outlier Detection and Removal
z_scores = np.abs(stats.zscore(df['price']))
outliers = df[(z_scores > 3) | (z_scores < -3)]
df = df[(z_scores < 3) & (z_scores > -3)]


# In[51]:


#Updated Price Distribution without Outliers
sns.histplot(df['price'], bins=30, kde=True)
plt.title('Price Distribution (Without Outliers)')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()


# In[37]:


# Analyze demand for different property types
#Recommendation: 
#consider adjusting property portfolio based on demand for different property types.
sns.countplot(x='room_type', data=df)
plt.title('Distribution of Property Types')
plt.xlabel('Property Type')
plt.ylabel('Count')
plt.show()


# In[38]:


# Calculate price statistics
#Recommendation:
#ensure pricing falls within a competitive range based on market conditions.

print("--- Price Per Night ---")
print("Minimum Price in $:", min(df['price']))
print("Maximum Price in $:", max(df['price']))
print("Average Price in $:", df['price'].mean())


# In[63]:


# Grouping based on room types and calculating average prices
private_room = df['room_type'] == 'Private room'
entire_home = df['room_type'] == 'Entire home/apt'
shared_room = df['room_type'] == 'Shared room'
private_avg = df[private_room]['price'].mean()
entire_avg = df[entire_home]['price'].mean()
shared_avg = df[shared_room]['price'].mean()

# Recommendation: 
#Consider adjusting pricing strategies based on room type averages.
print("--- Average Price of the Room Types ---")
print("Private Room:", private_avg)
print("Entire Home/Apt:", entire_avg)
print("Shared room:", shared_avg)


# In[40]:


#price range visualization
price_range = df[df['price'] <= 1000]
sns.histplot(data=price_range, x="price", kde=True, bins = 80)


# In[41]:


#Cheapest Airbnbs in New York City
# Recommendation: 
#Assess value proposition compared to competitors

cheapest = df.sort_values(by = 'price', ascending = True)
cheapest.head(10)


# In[42]:


#Most Expensive Airbnbs in New York City

#Recommendation: 
#Analyze factors contributing to popularity of properties with most reviews.

luxury = df.sort_values(by = 'price', ascending = False)
luxury.head(10)


# In[43]:


# Properties with the most reviews
# Recommendation: 
#Tailor pricing strategies based on location-specific demand.


most_reviews = df.sort_values(by = 'number_of_reviews', ascending = False)
most_reviews.head(10)


# In[44]:


#average price of property according to the location
avg_preffered_price_df = df.groupby(['neighbourhood','room_type'], as_index=False)['price'].mean().rename(columns={'neighbourhood':'Location','price':'Average Price'})
avg_preffered_price_df


# In[45]:


#hosts based on availability
#Recommendations:
#Identify hosts with consistently high or low availability and provide support accordingly.

host_based_on_availability_df = df.groupby(['host_id','host_name'],as_index=False)['availability_365'].mean().sort_values(['availability_365'],ascending = True)
host_based_on_availability_df


# In[67]:


#Insights and Recommendations:
#use correlations to identify relationships between variables and optimize strategies.
f, ax = plt.subplots(figsize=(10, 8))
ax=sns.scatterplot(data=df,x='longitude', y='latitude', hue="availability_365",palette='coolwarm',size='availability_365',
    sizes=(20,300))

