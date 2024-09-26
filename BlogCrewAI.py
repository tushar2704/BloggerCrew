# Importing dependencies
import os
from dotenv import load_dotenv
from BlogCrewAI import Agent, Task, Crew
from langchain_groq import ChatGroq
from IPython.display import Markdown


# Load environment variables
load_dotenv()


def create_llm():
    """
    Create and return a ChatGroq instance with the API key loaded from the environment.

    Returns:
        ChatGroq: An instance of ChatGroq with the specified configuration.
    """
    return ChatGroq(
        temperature=0.5,
        model_name="llama3-70b-8192",
        api_key=os.getenv('GROQ_API_KEY')
    )

#######
def create_agent(llm, role, goal, backstory):
    """
    Create and return an Agent instance with the specified parameters.

    Args:
        llm (ChatGroq): The language model to be used by the agent.
        role (str): The role of the agent.
        goal (str): The goal of the agent.
        backstory (str): The backstory of the agent.

    Returns:
        Agent: An instance of Agent with the specified configuration.
    """
    return Agent(
        llm=llm,
        role=role,
        goal=goal,
        backstory=backstory,
        allow_delegation=False,
        verbose=True
    )



def create_task(description, expected_output, agent):
    """
    Create and return a Task instance with the specified parameters.

    Args:
        description (str): The description of the task.
        expected_output (str): The expected output of the task.
        agent (Agent): The agent responsible for the task.

    Returns:
        Task: An instance of Task with the specified configuration.
    """
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )
    
    

def create_crew(agents, tasks):
    """
    Create and return a Crew instance with the specified agents and tasks.

    Args:
        agents (list): A list of Agent instances.
        tasks (list): A list of Task instances.

    Returns:
        Crew: An instance of Crew with the specified configuration.
    """
    return Crew(
        agents=agents,
        tasks=tasks,
        verbose=2
    )


def main():
    """
    Main function to orchestrate the content creation process.
    """
    llm = create_llm()

    planner = create_agent(
        llm,
        "Content Planner",
        "Plan engaging and factually accurate content on {topic}",
        "You're working on planning a blog article about the topic: {topic}. You collect information that helps the audience learn something and make informed decisions. Your work is the basis for the Content Writer to write an article on this topic."
    )

    writer = create_agent(
        llm,
        "Content Writer",
        "Write insightful and factually accurate opinion piece about the topic: {topic}",
        "You're working on writing a new opinion piece about the topic: {topic}. You base your writing on the work of the Content Planner, who provides an outline and relevant context about the topic. You follow the main objectives and direction of the outline, as provided by the Content Planner. You also provide objective and impartial insights and back them up with information provided by the Content Planner. You acknowledge in your opinion piece when your statements are opinions as opposed to objective statements."
    )

    editor = create_agent(
        llm,
        "Editor",
        "Edit a given blog post to align with the writing style of the organization.",
        "You are an editor who receives a blog post from the Content Writer. Your goal is to review the blog post to ensure that it follows journalistic best practices, provides balanced viewpoints when providing opinions or assertions, and also avoids major controversial topics or opinions when possible."
    )

    plan_task = create_task(
        "1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering their interests and pain points.\n"
        "3. Develop a detailed content outline including an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources.",
        "A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources.",
        planner
    )

    write_task = create_task(
        "1. Use the content plan to craft a compelling blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
        "3. Sections/Subtitles are properly named in an engaging manner.\n"
        "4. Ensure the post is structured with an engaging introduction, insightful body, and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and alignment with the brand's voice.",
        "A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
        writer
    )

    edit_task = create_task(
        "Proofread the given blog post for grammatical errors and alignment with the brand's voice.",
        "A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
        editor
    )

#######################################################

    crew = create_crew([planner, writer, editor], [plan_task, write_task, edit_task])

    result = crew.kickoff(inputs={"topic": "US Election 2024"})
    return Markdown(result)

if __name__ == "__main__":
    main()


