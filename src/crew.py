##© 2024 Tushar Aggarwal. All rights reserved.(https://tushar-aggarwal.com)
##Pixella[Towards-GenAI] (https://github.com/Towards-GenAI)
##################################################################################################
#Importing dependencies

from BlogCrewAI import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
import logging
import streamlit as st
from pathlib import Path
import base64
import sys
import os
import warnings
from dotenv import load_dotenv
from typing import Any, Dict
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()
from fpdf import FPDF



#From src
from src.agents import *
from src.task import *
from src.crew import *




##################################################################################################
#Setting up Llama3
os.environ["OPENAI_API_KEY"] = "NA"

llm = ChatOpenAI(
    model = "crewai-llama3",
    base_url = "http://localhost:11434/v1")
##################################################################################################


writing_crew_1= Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)
