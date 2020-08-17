import os, re, json
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date, timedelta
import sync as sync
import copy
import datetime

# # Model Sensors

# In[2]:


sensor_EDM80OPC = {
    "name": "EDM80OPC",
    "description": "Particulate matter sensor for PM10, PM4, PM2.5 and PM1",
    "encodingType": "application/pdf",
    "metadata": "TODO",
    "@iot.id": "saqn:s:grimm-aerosol.com:EDM80OPC:SN-177340907"
}



furl = "http://193.196.38.108:8080/FROST-Server/v1.0/"

# # Post Sensors to Server

# In[4]:


sync.rest_request(furl + 'Sensors', json.dumps(sensor_EDM80OPC))

