
# coding: utf-8

# In[1]:


import requests


# In[2]:


response = requests.get('https://api.darksky.net/forecast/APIKEY/40.7128,-74.0060')
data = response.json()


# In[3]:


data.keys()


# ## This is my sentence

# In[4]:


#Right now it is TEMPERATURE degrees out and SUMMARY. Today will be TEMP_FEELING with a high of HIGH_TEMP and a low of LOW_TEMP. RAIN_WARNING.


# In[5]:


TEMPERATURE = round(data['currently']['temperature'])
TEMPERATURE


# In[6]:


SUMMARY = data['currently']['summary'].lower()
SUMMARY 


# In[7]:


if data['daily']['data'][0]['temperatureHigh'] > 87:
    TEMP_FEELING = "hot AF, and probably a little swampy"
elif data['daily']['data'][0]['temperatureHigh'] > 80:
    TEMP_FEELING = "warm, but not nearly as bad as it could be"
elif data['daily']['data'][0]['temperatureHigh'] > 60:
    TEMP_FEELING = "(borat voice) very nice"
else:
    TEMP_FEELING = "the chill-zone"


# In[8]:


HIGH_TEMP = round(data['daily']['data'][0]['temperatureHigh'])
HIGH_TEMP


# In[9]:


LOW_TEMP = round(data['daily']['data'][0]['temperatureLow'])
LOW_TEMP


# In[10]:


if data['daily']['data'][0]['precipProbability'] > 0.5:
    RAIN_WARNING = ' Don\'t go outside, it\'s not worth it.'
else:
    RAIN_WARNING = ''


# In[11]:


weather_warning = "Right now it is {} degrees out and {}. Today will be {} with a high of {} and a low of {}.{}".format(TEMPERATURE, SUMMARY, TEMP_FEELING, HIGH_TEMP, LOW_TEMP, RAIN_WARNING)


# In[12]:


print(weather_warning)


# In[13]:


import datetime
right_now = datetime.datetime.now()
date_string = right_now.strftime("%B %d, %Y")
date_string


# In[15]:


response = requests.post(
        "https://api.mailgun.net/v3/sandboxa96884de1840475d9cec9cd9b83147d5.mailgun.org/messages",
        auth=("api", "APIKEY"),
        data={"from": "Weatherman Sam <mailgun@sandboxa96884de1840475d9cec9cd9b83147d5.mailgun.org>",
              "to": ["EMAIL"],
              "subject": "8 AM Weather forecast: " + date_string,
              "text": weather_warning}) 
response.text

