from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from dotenv import load_dotenv
import os

@CrewBase
class DataExplorerCrew():

    # Agents and Tasks configuration
    agents_config = os.path.join(os.path.dirname(__file__), '..', 'config', 'agents.yaml')
    tasks_config = os.path.join(os.path.dirname(__file__), '..', 'config', 'tasks.yaml')

    @before_kickoff
    def before_kickoff(self, inputs):
        # Load environment variables from .env file
        load_dotenv()
        return inputs

    @after_kickoff
    def after_kickoff(self, result):
        # Perform any necessary cleanup or finalization
        return result

    @agent
    def researcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_agent'],  # type: ignore[index]
            verbose=True,
    )

    @agent
    def summarizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer_agent'],  # type: ignore[index]
            verbose=True,
    )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'] # type: ignore[index]
    )

    @task
    def summarization_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarization_task'] # type: ignore[index]
    )

    @crew
    def crew(self) -> Crew:
        """Define the crew for the Data Explorer project."""
        return Crew(
            name="DataExplorerCrew",
            agents=self.agents, # type: ignore
            tasks=self.tasks, # type: ignore
            process=Process.sequential  # Define the process type
        )

