#!/usr/bin/env python
# coding: utf-8

# # Analyzing Successful Free App Profiles in the AppleStore and Google Play Markets
# ## Determine differentiates the boring apps from the cool ones
# In this proyect we are working with a team of appdevelopers and our task as junior data scientists is to find the profile of the most successful types of apps in both the **Appstore** and **googleplaystore**

# In[1]:


# Opened Files
opened_ios = open('AppleStore.csv')
opened_android = open('googleplaystore.csv')

# Read as a list of lists 
from csv import reader
AppleStore = list(reader(opened_ios))
googleplaystore = list(reader(opened_android))


# In[2]:


# Created a function to expolre data
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[3]:


# AppleStore
explore_data(AppleStore, 1, 5, True)

# Google Play Store
explore_data(googleplaystore, 1, 5, True)


# In[4]:


# Checking Headers
print(AppleStore[:1])
print('\n')
print(googleplaystore[:1])


# ## Unifying the Data for our purposes
# To unify the data we must be aware that the number of columns are not the same on both data files. We must select the columns that will be useful for our analysis and disregard the rest. When unifing the columns of the **AppleStore** data and the **googlestore** data we must make sure that the values are kept under their corresponding header column.
# 

# In[5]:


#Checking row ranges with apparent error (found on a blog site)
print(len(googleplaystore[10472]))
print(len(googleplaystore[10473]))
print(len(googleplaystore[10474]))

#Row 10473 has one fewer data point


# In[6]:


#Row 10473 has a missing value
print(googleplaystore[10473])


# In[7]:


#We are going to Delete the row with missing info on the googleplaystore dataset
del googleplaystore[10473]


# In[8]:


#We check again to make sure that the row has been deleted
print(googleplaystore[10473])


# ### Duplicate entries in the googleplaystore data set
# By reading the Kaggle blogs online we have discovered if that the dataset has some duplicate entries for some apps. In the following few cells we will try to identify and delete the duplicate entries (we will delete the "less relevant"/older duplicates)

# In[9]:


# We are checking for duplicate app entries and identify how many unique app are in the Google Play Store dataset
unique_apps = []
duplicate_apps = []
for app in googleplaystore[1:]:
    app_name = app[0]
    if app_name in unique_apps:
        duplicate_apps.append(app_name)
    else:
        unique_apps.append(app_name)
        
print('Number of duplicate apps: ', len(duplicate_apps))
print('\n')
print('Number of unique apps: ', len(unique_apps))
print('\n')
print('Example of duplicate entry for apps: ', duplicate_apps[:10])


# In order to be more precise with our data, instead of removing the duplicated apps randomly we will delete the entries with less reviews, assuming that those entries are older

# In[10]:


# Create a dictionary and alow only one entry per app (the entry with the highest review count) 
reviews_max = {}
for app in googleplaystore[1:]:
    name = app[0]
    n_reviews = float(app[3])
    if name in reviews_max and n_reviews > reviews_max[name]:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        
print('Number of items in our new dictionary', len(reviews_max)) # Must equal 9659 as show above
for key in list(reviews_max)[:5]:
    print("key: {}, value: {} ".format(key, reviews_max[key]), '\n')


# In[11]:


# With the help of the created list reviews_max we are going to clean the main list and leave only the app we are interested in
# The list "already_added" prevents entries with the same number of reviews to be included twice

android_clean = []
already_added = []
for app in googleplaystore[1:]:
    name = app[0]
    n_reviews = float(app[3])
    if n_reviews == reviews_max[name] and name not in already_added:
        android_clean.append(app)
        already_added.append(name)
    
print(len(android_clean))
print(android_clean[:10])    


# In[12]:


# Ceating a function to identify english app names
def is_english(phrase):
    non_english = 0
    for letter in phrase:
        if ord(letter) > 127:
            non_english += 1
        if non_english > 3:  #Since some apps contain emojis and other characters we only exclude those with +3 non-english characters
            return False
    return True
        
print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))
print(is_english('😜 Instachat '))
#Testing our new function


# Although our function is not perfect and some english apps might have been excluded (those with more than three non-english characters like emojis) the function is pretty accurate for our purposes

# In[13]:


#We use the above function to create a new lists and include only apps whose title pass the is_english function
ios_clean = []
andr_clean = []

for app in android_clean:
    if is_english(app[0]):
        andr_clean.append(app)
        
for app in AppleStore:
    if is_english(app[1]):
        ios_clean.append(app)

#We print the new lengths to see how mane rows we will be working with        
print(len(andr_clean))
print(len(ios_clean))


# In[14]:


# Lastly, we create 2 final lists and only include the free apps, since that is what we are interested in
free_ios = []
free_android = []
for app in ios_clean[1:]:
    price = float(app[4])
    if price == 0:
        free_ios.append(app)
        
for app in andr_clean:
    app_type = app[6]
    if app_type != 'Paid': #Employed another method than above to practice
        free_android.append(app)


# In[15]:


# Display the rows in each final version of the datasets
print('Android Free: ', len(free_android))
print('IOS Free: ', len(free_ios))


# ### Most common app profiles for both IOS and Android
# Since we want to help our team build an app that will work well on Android and IOS, we have to identify what app profiles thrive on both of these platforms. In the next cells we are goind to explore the most common genres of the apps that run on both platforms.

# In[16]:


# Creating a function to show the frequency data tables
def freq_table(dataset, index):
    frequency = {}
    for row in dataset:
        genre = row[index]
        if genre in frequency:
            frequency[genre] += 1
        else:
            frequency[genre] = 1
    for element in frequency:
        frequency[element] /= len(dataset)
    return frequency    


# In[17]:


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[18]:


#Showing frequency tables for genres in AppleStore and for genres & catergories in Google Play Store
print(display_table(free_ios, 11))
print('\n')
print(display_table(free_android, 9))
print('\n')
print(display_table(free_android, 1))


# In[19]:


#Showing a table for the average number of rating per app in each genre in the AppleStore dataset
genre_ios = freq_table(free_ios, 11)
for genre in genre_ios:
    total = 0
    len_genre = 0
    for app in free_ios:
        genre_app = app[11]
        if genre_app == genre:
            rating = float(app[5])
            total += rating
            len_genre += 1
    avg_user_ratings = round(total / len_genre,2)
    print(genre, ': ', avg_user_ratings)


# Navigation seeems like the genre with the most average number of ratings in the IOS platform. That is some what strange, lets see what might be causing that...

# In[20]:


for app in free_ios:
    if app [11] == 'Navigation':
        print(app[1], ': ', app[5])


# What about the *Reference* apps? What the heck are those anyways?

# In[21]:


for app in free_ios:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


# ## Now lets check out the most popular apps by genre on the google play platform

# In[22]:


# Repeting the process of crating a table with the average number of rating per app in each category
category_android = freq_table(free_android, 1)
for category in category_android:
    total = 0 
    len_category = 0 
    popular_apps = 0 #creating a variable for very popular apps with more than 10M reviews
    for app in free_android:
        if app[1] == category:
            n_installs = app[5]
            n_installs = n_installs.replace('+', '')
            n_installs = float(n_installs.replace(',', ''))
            total += n_installs
            #above we have cleaned the strings such as "+" and "," from the data and transformed it to a float to perform calculations 
            len_category += 1
            if n_installs > 10000000:
                popular_apps += 1
    avg_num_installs = total / len_category
    print(category, ': ', round(avg_num_installs,2), 'Number of apps: ', len_category, 'Apps with +10M reviews', ': ', popular_apps)
    #print('\n')           


# We see that the are some categories that have an impresive amount of average rating that might be skewed by very popular apps (Popular apps are app with more than 10M reviews). Lets explore this phenomena in the communications & NEws and magazines category.

# In[23]:


#Exploring the apps with high review in the Communication category 
for app in free_android:
    if app[1] == "COMMUNICATION" and (app[5] == '1,000,000,000+' or
                                      app[5] == '500,000,000+'):
        print(app[0], ': ', app[5])


# In[24]:


#Recalculating the average reviews per app in the category "Comunications" without including apps with over 100M reviews
under_100M = []
for app in free_android:
    category = app[1]
    n_installs = app[5]
    n_installs = n_installs.replace('+', '')
    n_installs = float(n_installs.replace(',', ''))
    if category == 'COMMUNICATION' and n_installs < 100000000:
        under_100M.append(n_installs)
        
print('Average installs for cummunicaion apps excluding apps with over 100M installs: ', sum(under_100M) / len(under_100M))


# In[25]:


#Exploring the apps with high review in the News & Magazines category
for app in free_android:
    if app[1] == "NEWS_AND_MAGAZINES" and (app[5] == '1,000,000,000+' or
                                      app[5] == '500,000,000+'):
        print(app[0], ': ', app[5])


# In[26]:


#Recalculating the average reviews per app in the category "News and Magazines" without including apps with over 100M reviews (Outliers)
under_100M = []
for app in free_android:
    category = app[1]
    n_installs = app[5]
    n_installs = n_installs.replace('+', '')
    n_installs = float(n_installs.replace(',', ''))
    if category == 'NEWS_AND_MAGAZINES' and n_installs < 100000000:
        under_100M.append(n_installs)
        
print('Average installs for news and magazines apps excluding apps with over 100M installs: ', sum(under_100M) / len(under_100M))


# In[27]:


#Recalculating the average reviews per app in the category "Entertainment" without including apps with over 100M reviews
under_100M = []
for app in free_android:
    category = app[1]
    n_installs = app[5]
    n_installs = n_installs.replace('+', '')
    n_installs = float(n_installs.replace(',', ''))
    if category == 'ENTERTAINMENT' and n_installs < 10000000:
        under_100M.append(n_installs)
        
print('Average installs for entertainment apps excluding apps with over 10M installs: ', sum(under_100M) / len(under_100M))


# In[28]:


#Recalculating the average reviews per app in the category "Books and Reference" without including apps with over 100M reviews
under_100M = []
for app in free_android:
    category = app[1]
    n_installs = app[5]
    n_installs = n_installs.replace('+', '')
    n_installs = float(n_installs.replace(',', ''))
    if category == 'BOOKS_AND_REFERENCE' and n_installs < 10000000:
        under_100M.append(n_installs)
        
print('Average installs for books and reference apps excluding apps with over 10M installs: ', sum(under_100M) / len(under_100M))


# In[29]:


#Recalculating the average reviews per app in the category "Photography" without including apps with over 100M reviews
under_100M = []
for app in free_android:
    category = app[1]
    n_installs = app[5]
    n_installs = n_installs.replace('+', '')
    n_installs = float(n_installs.replace(',', ''))
    if category == 'PHOTOGRAPHY' and n_installs < 10000000:
        under_100M.append(n_installs)
        
print('Average installs for Photography apps excluding apps with over 10M installs: ', sum(under_100M) / len(under_100M))


# ## Recomendation for App developers
# #### Start with an app in the entertainment or photography category
# When looking at the highest average ratings per category of apps in the googleplay platform we notice some great performing categories and some not so good ones. 
# After ignoring the ouliers that drastically change the averages we can say to our developers is that the best categories to focus on are the *Photography* category. 
# The new app could be in the form of a *photo editor or a easy instagram filter creator* (which are popular right now). Another essential questions that is left unanswerred in this proyect is how could the team develop in app purchases and how effective is this category in monetizing in app purchases. That could be a great proyect if we were to continue with this proyecto of developing an app.
