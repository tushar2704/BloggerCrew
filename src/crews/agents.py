##© 2024 Tushar Aggarwal. All rights reserved.(https://tushar-aggarwal.com)
##Botimus[Towards-GenAI] (https://github.com/Towards-GenAI)
##################################################################################################
#Importing dependencies
import streamlit as st
from pathlib import Path
import base64
import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))
import warnings
warnings.filterwarnings("ignore")
import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from BlogCrewAI import Crew, Process, Agent, Task
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional
from langchain_openai import ChatOpenAI
import logging
import warnings
warnings.filterwarnings('ignore')
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()
#Importing from SRC




##################################################################################################
##################################################################################################
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
##################################################################################################
##################################################################################################
#Environmental variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
##################################################################################################
##################################################################################################

#Check if api key loaded successfully with logging info
if google_api_key:
    logger.info("Google API Key loaded successfully.")
else:
    logger.error("Failed to load Google API Key.")
##################################################################################################
#Intializing llm
llm = ChatGoogleGenerativeAI(model="gemini-pro", verbose=True, 
                             temperature=0.2, google_api_key=google_api_key)








##################################################################################################

# Create a researcher agent
researcher = Agent(
  role='Senior Researcher',
  goal='Discover groundbreaking technologies',
  backstory='A curious mind fascinated by cutting-edge innovation and the potential to change the world, you know everything about tech.',
  verbose=True,
  tools=[search_tool],
  allow_delegation=False,
  llm=llm 
)

insight_researcher = Agent(
  role='Insight Researcher',
  goal='Discover Key Insights',
  backstory='You are able to find key insights from the data you are given.',
  verbose=True,
  allow_delegation=False,
  llm=llm 
)

writer = Agent(
  role='Tech Content Strategist',
  goal='Craft compelling content on tech advancements',
  backstory="""You are a content strategist known for 
  making complex tech topics interesting and easy to understand.""",
  verbose=True,
  allow_delegation=False,
  llm=llm 
)

formater = Agent(
  role='Markdown Formater',
  goal='Format the text in markdown',
  backstory='You are able to convert the text into markdown format',
  verbose=True,
  allow_delegation=False,
  llm=llm 
)

