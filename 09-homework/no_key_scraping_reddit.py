
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
driver = webdriver.Chrome()
import pandas as pd


# In[2]:


import time


# In[3]:


import requests


# In[4]:


driver.get('https://www.reddit.com/r/popular/')
time.sleep(1)


# In[5]:


posts = driver.find_elements_by_class_name('scrollerItem')
time.sleep(1)


# In[6]:


# Going to make an empty list that will be populated by dictionaries
all_post_info = []

for post in posts:
    driver.execute_script("arguments[0].scrollIntoView(true)", post)
    post_dict = {}
    
    # Finding the upvotes first
    upvotes = post.find_element_by_css_selector('button[aria-label=upvote] + *').text
    
    # I don't want ads in here, and ads don't have upvotes so this will filter it out
    if upvotes == '0':
        pass
    
    # Now I only have the good stuff
    else:

        # title
        title = post.find_element_by_tag_name('h2').text
        post_dict['title'] = title
        
        # upvotes
        post_dict['upvotes'] = upvotes
        
        # subreddit -- this may not be the most elegant way, but sometimes the sub name is located in two different places
        try: 
            subreddit = post.find_elements_by_class_name('s1uc7yii-0')[0].text
            post_dict['subreddit'] = subreddit
        except: 
            pass
        try:
            subreddit = post.find_elements_by_class_name('s1uc7yii-0')[1].text
            post_dict['subreddit'] = subreddit
        except:
            pass
       
        
        #link to post
        post_link = post.find_element_by_class_name('SQnoC3ObvgnGjWt90zD9Z').get_attribute('href')
        post_dict['post_link'] = post_link
        
        #img
        try:
            image_link = post.find_element_by_tag_name('img').get_attribute('src')
            post_dict['image_link'] = image_link
        except:
            pass
        
        #poster
        poster = post.find_element_by_class_name('_2tbHP6ZydRpjI44J3syuqC').text
        post_dict['poster'] = poster
        
        #time posted
        
        time_posted = post.find_element_by_class_name('_3jOxDPIQ0KaOWpzvSQo-1s').text
        post_dict['time_posted'] = time_posted
        
        # Add each dict to the list
        all_post_info.append(post_dict)
        
all_post_info


# In[7]:


# Gonna check it out in a dataframe
df = pd.DataFrame(all_post_info)
df


# ### Going to not do the CSV and instead put the scraped content in body of email

# In[8]:


import datetime


# In[9]:


right_now = datetime.datetime.now()
date_string = right_now.strftime("%B %d, %Y")
date_string
time_string = right_now.strftime("%H:%M")
time_string

greeting = "Welcome to your {} briefing on reddit.com/r/popular.".format(time_string)
text_body = []

count = 1
for post_info in all_post_info:
    # This try except will ignore all sponsored posts, bc they don't have a subreddit
    try:
        text_body.append("In the number {} position, we have a post from reddit user {} entitled '{}'. It was originally posted in the {} subreddit {}, and has received {} upvotes. If you want to check it out, follow this url ({}) to the original post.".format(count, post_info['poster'], post_info['title'], post_info['subreddit'], post_info['time_posted'], post_info['upvotes'], post_info['post_link']))
        count = count + 1
    except:
        pass
    
print(greeting + '\n')
print('\n\n'.join(text_body))




# ### Sending the email

# In[10]:


response = requests.post(
        "https://api.mailgun.net/v3/sandboxa96884de1840475d9cec9cd9b83147d5.mailgun.org/messages",
        auth=("api", "APIKEY"),
        data={"from": "xX_RedditGuyCoolMan_Xx <mailgun@sandboxa96884de1840475d9cec9cd9b83147d5.mailgun.org>",
              "to": ["EMAIL"],
              "subject": time_string + "Reddit Briefing",
              "text": greeting + '\n' +'\n' + '\n\n'.join(text_body)}) 
response.text

