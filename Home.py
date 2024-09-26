##© 2024 Tushar Aggarwal. All rights reserved.(https://tushar-aggarwal.com)
##BloggerCrew -Live Session with Tushar
##################################################################################################
# Importing dependencies

from BlogCrewAI import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
# Importing dependencies
import os
import logging
import streamlit as st
from pathlib import Path
import base64
import sys
import warnings
from dotenv import load_dotenv
from typing import Any, Dict
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
from fpdf import FPDF

from BlogCrewAI import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

from src.components.navigation import page_config, custom_style, footer

# Setting up Llama3 via Ollama server @http://localhost:11434/v1 
os.environ["OPENAI_API_KEY"] = "NA"

llm = ChatOpenAI(
    model="crewai-llama3",
    base_url="http://localhost:11434/v1"
)

search_tool = DuckDuckGoSearchRun()

class CustomHandler(BaseCallbackHandler):
    def __init__(self, agent_name: str) -> None:
        super().__init__()
        self.agent_name = agent_name

    def on_chain_start(self, serialized: Dict[str, Any], outputs: Dict[str, Any], **kwargs: Any) -> None:
        st.session_state.messages.append({"role": "assistant", "content": outputs['input']})
        st.chat_message("assistant").write(outputs['input'])

    def on_agent_action(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        st.session_state.messages.append({"role": "assistant", "content": inputs['input']})
        st.chat_message("assistant").write(inputs['input'])

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        st.session_state.messages.append({"role": self.agent_name, "content": outputs['output']})
        st.chat_message(self.agent_name).write(outputs['output'])


class BlogCrew:
    def __init__(self, topic: str, content_type: str):
        self.topic = topic
        self.content_type = content_type
        self.output_placeholder = st.empty()

    def run(self):
        # Define agents
        researcher = Agent(
            role='Senior Research Analyst',
            goal='Uncover cutting-edge developments in AI and data science',
            backstory="""You work at a leading tech think tank. Your expertise lies in identifying emerging trends. You have a knack for dissecting complex data and presenting actionable insights.""",
            verbose=True,
            allow_delegation=False,
            tools=[search_tool],
            llm=llm
        )

        writer = Agent(
            role='Tech Content Strategist',
            goal='Craft compelling content on tech advancements',
            backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles. You transform complex concepts into compelling narratives.""",
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

        # Define tasks
        task1 = Task(
            description=f"""Conduct a comprehensive analysis of the latest advancements in {self.topic}. Identify key trends, breakthrough technologies, and potential industry impacts.""",
            expected_output="Full analysis report in bullet points",
            agent=researcher
        )

        task2 = Task(
            description=f"""Using the insights provided, develop an engaging {self.content_type.lower()} that highlights the most significant advancements in {self.topic}. Your post should be informative yet accessible, catering to a tech-savvy audience. Make it sound cool, avoid complex words so it doesn't sound like AI.""",
            expected_output=f"Full {self.content_type.lower()} of at least 4 paragraphs",
            agent=writer
        )

        # Instantiate the crew with a sequential process
        crew = Crew(
            agents=[researcher, writer],
            tasks=[task1, task2],
            process=Process.sequential,
            verbose=2
        )

        # Get the crew to work
        result = crew.kickoff()
        self.output_placeholder.markdown(result)

        # Create a PDF and write the output to it
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for line in result.split("\n"):
            pdf.write(5, line)
            pdf.ln()  # move to next line

        # Save the PDF file
        pdf_file = "blog.pdf"
        pdf.output(pdf_file)

        with open(pdf_file, 'rb') as file:
            file_content = file.read()

        # Create download button
        st.download_button(
            label=f"Download {pdf_file}",
            data=file_content,
            file_name=pdf_file,
            mime="application/pdf"
        )

        return result


def main():
    # Streamlit Page Setup
    page_config("Pixella", "🤖", "wide") 
    custom_style()
    st.sidebar.image('./src/logo.png')

    st.title("🤖Pixella🤖")
    st.markdown(
        '''
        <style>
            div.block-container{padding-top:0px;}
            font-family: 'Roboto', sans-serif; /* Add Roboto font */
            color: blue; /* Make the text blue */
        </style>
        ''',
        unsafe_allow_html=True
    )
    st.markdown(
        """
        ### Write Structured blogs with AI Agents, powered by Llamma3 via Ollama & CrewAI  [Towards-GenAI](https://github.com/Towards-GenAI)
        """
    )

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    col1, col2 = st.columns(2)
    
    # Input for blog topic
    with col1:
        blog_topic = st.text_input("Enter the blog topic:")

    # Dropdown for selecting the type of content  
    with col2:
        content_type = st.selectbox(
            "Select the type of content:", 
            ["Blog Post", "Research Paper", "Technical Report"]
        )

    if st.button("Start Blogging Crew"):
        if blog_topic:
            blog_crew = BlogCrew(blog_topic, content_type)
            result = blog_crew.run()
            st.write(result)
        else:
            st.error("Please enter a blog topic.")


if __name__ == "__main__":
    main()
    with st.sidebar:
        footer()