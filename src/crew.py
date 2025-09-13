from typing import List
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os

from crewai_tools import SerperDevTool, ScrapeWebsiteTool, PDFSearchTool

from tools.recam import calculate_recamscore_all
from schemas.agent_schemas import RecamKeyInfo, RecamResult, RecamAssessmentReport, RecamReviewReport


@CrewBase
class RecamCrew():
    """RECAM crew for DILI causality assessment"""

    # --------------------------- config ---------------------------
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # --------------------------- LLMs ---------------------------
    llm_deepseek_reasoner = LLM(
        model="deepseek/deepseek-reasoner",
        base_url="https://api.deepseek.com",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0
    )

    llm_deepseek_chat = LLM(
        model="deepseek/deepseek-chat",
        base_url="https://api.deepseek.com",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0
    )

    llm_gpt_oss_120b = LLM(
        model="openrouter/gpt-oss-120b",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0
    )

    llm_gpt_5 = LLM(
        model="openrouter/openai/gpt-5",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0
    )

    llm_gpt_5_chat = LLM(
        model="openrouter/openai/gpt-5-chat",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0
    )

    llm_gpt_5_nano = LLM(
        model="gpt-5-nano",
        base_url="https://api.openai.com/v1",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    llm_gpt_4o = LLM(
        model="gpt-4o",
        base_url="https://api.openai.com/v1",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    llm_claude_sonnet_4 = LLM(
        model="openrouter/anthropic/claude-sonnet-4",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0
    )

    llm_grok_4 = LLM(
        model="openrouter/x-ai/grok-4",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0
    )

    llm_gemini_2_5_pro = LLM(
        model="openrouter/google/gemini-2.5-pro",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0
    )

    llm_qwen3_max = LLM(
        model="openrouter/qwen/qwen3-max",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0
    )

    llm_qwen3_coder = LLM(
        model="openrouter/qwen/qwen3-coder",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0
    )

    # selected LLM to use
    llm = llm_gpt_5_chat

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    @agent
    def dili_informatician(self) -> Agent:
        return Agent(
            config=self.agents_config['dili_informatician'],
            tools=[
                PDFSearchTool(),
                SerperDevTool(),
                ScrapeWebsiteTool()
            ],
            verbose=True,
            llm=self.llm,
            output_json=RecamKeyInfo
        )

    @agent
    def dili_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['dili_analyst'],
            tools=[
                calculate_recamscore_all,
            ],
            verbose=True,
            llm=self.llm,
            output_json=RecamResult
        )

    @agent
    def dili_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['dili_writer'],
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool()
            ],
            verbose=True,
            llm=self.llm,
            output_pydantic=RecamAssessmentReport
        )

    @agent
    def lead_dili_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_dili_expert'],
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool()
            ],
            verbose=True,
            llm=self.llm,
            output_pydantic=RecamReviewReport
        )

    @task
    def information_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config['information_extraction_task'],
            agent=self.dili_informatician(),
        )

    @task
    def causality_scoring_task(self) -> Task:
        return Task(
            config=self.tasks_config['causality_scoring_task'],
            agent=self.dili_analyst(),
        )

    @task
    def report_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_writing_task'],
            agent=self.dili_writer(),
        )

    @task
    def expert_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['expert_review_task'],
            agent=self.lead_dili_expert(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the RECAM crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
