"""
AI Board of Directors - CrewAI Implementation
Chairman: Claude | Members: GPT-4o, DeepSeek, Gemini, Seedance (Video)
"""

import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
import anthropic
import requests


# ============================================================
# ENVIRONMENT VARIABLES (set these in your .env file)
# ============================================================
# ANTHROPIC_API_KEY=your_key
# OPENAI_API_KEY=your_key
# GEMINI_API_KEY=your_key
# DEEPSEEK_API_KEY=your_key
# SEEDANCE_API_KEY=your_key (ByteDance / Seedance API)


# ============================================================
# CUSTOM TOOL: Seedance Video Generation
# ============================================================
@tool("Seedance Video Generator")
def generate_video(prompt: str) -> str:
    """
    Generates a short video using the Seedance (ByteDance) API.
    Input: A text prompt describing the video to generate.
    Output: A URL or file path to the generated video.
    """
    api_key = os.getenv("SEEDANCE_API_KEY")
    if not api_key:
        return "Error: SEEDANCE_API_KEY not set in environment variables."

    # Seedance / PixVerse / ByteDance video gen endpoint (update URL as needed)
    url = "https://api.seedance.ai/v1/video/generate"  # Replace with actual endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "duration": 5,       # seconds
        "resolution": "720p",
        "style": "cinematic"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        video_url = result.get("video_url", "No URL returned")
        return f"Video generated successfully! URL: {video_url}"
    except requests.exceptions.RequestException as e:
        return f"Video generation failed: {str(e)}"


# ============================================================
# AGENT DEFINITIONS
# ============================================================

# 👑 CHAIRMAN — Claude (Anthropic)
chairman = Agent(
    role="Chairman of the AI Board",
    goal=(
        "Lead the board of AI directors with strategic vision. "
        "Synthesize insights from all board members, make final decisions, "
        "and ensure all outputs align with the overarching mission."
    ),
    backstory=(
        "You are Claude, an AI by Anthropic renowned for nuanced reasoning, "
        "ethical judgment, and clear communication. As Chairman, you facilitate "
        "board discussions, assign tasks to the right members, and deliver "
        "the final unified recommendation."
    ),
    llm="claude-opus-4-5",  # Uses ANTHROPIC_API_KEY automatically
    verbose=True,
    allow_delegation=True,   # Chairman can delegate to other agents
)


# 📊 BOARD MEMBER 1 — GPT-4o (OpenAI)
analyst = Agent(
    role="Chief Data Analyst",
    goal=(
        "Analyze data, produce structured reports, and provide evidence-based "
        "insights. Specializes in quantitative analysis and business intelligence."
    ),
    backstory=(
        "You are GPT-4o, OpenAI's flagship model. You excel at structured "
        "reasoning, data interpretation, and producing clear, formatted outputs. "
        "You support the board with hard numbers and actionable analysis."
    ),
    llm="gpt-4o",            # Uses OPENAI_API_KEY automatically
    verbose=True,
    allow_delegation=False,
)


# 🔬 BOARD MEMBER 2 — DeepSeek
researcher = Agent(
    role="Chief Research Officer",
    goal=(
        "Conduct deep technical and scientific research. Specializes in coding, "
        "mathematics, and cutting-edge academic findings."
    ),
    backstory=(
        "You are DeepSeek, a powerful open-source AI known for exceptional "
        "performance on technical benchmarks. You dive deep into complex topics "
        "and provide the board with rigorous, well-sourced research."
    ),
    llm="deepseek/deepseek-chat",  # Routed via LiteLLM using DEEPSEEK_API_KEY
    verbose=True,
    allow_delegation=False,
)


# 🎨 BOARD MEMBER 3 — Gemini 1.5 Pro (Google)
creative_director = Agent(
    role="Chief Creative Officer",
    goal=(
        "Lead creative strategy, multimodal content planning, and visual "
        "storytelling. Evaluates ideas from a creative and audience-focused lens."
    ),
    backstory=(
        "You are Gemini 1.5 Pro, Google's multimodal AI. You think visually, "
        "understand context across text and images, and bring creative flair "
        "to the board's decisions. You champion innovative approaches."
    ),
    llm="gemini/gemini-1.5-pro",   # Routed via LiteLLM using GEMINI_API_KEY
    verbose=True,
    allow_delegation=False,
)


# 🎬 BOARD MEMBER 4 — Seedance Video Producer
video_producer = Agent(
    role="Chief Video Production Officer",
    goal=(
        "Produce compelling video content based on the board's creative direction. "
        "Translates strategies and narratives into video prompts and manages "
        "video generation via the Seedance API."
    ),
    backstory=(
        "You are a specialist AI Video Producer powered by Seedance, ByteDance's "
        "state-of-the-art video generation model. You craft precise video prompts "
        "and generate high-quality short-form video content for the board's campaigns."
    ),
    llm="gpt-4o",                  # Uses GPT-4o as reasoning backbone for this agent
    tools=[generate_video],        # Equipped with the Seedance video tool
    verbose=True,
    allow_delegation=False,
)


# ============================================================
# TASK DEFINITIONS (customize these for your use case)
# ============================================================

task_research = Task(
    description=(
        "Research the latest trends in [YOUR TOPIC HERE]. "
        "Provide a technical summary with key findings, statistics, and sources."
    ),
    expected_output="A structured research report with bullet points and citations.",
    agent=researcher,
)

task_analysis = Task(
    description=(
        "Analyze the research findings provided and produce a data-driven "
        "business case. Include risk assessment and opportunity scoring."
    ),
    expected_output="A business analysis report with data insights and recommendations.",
    agent=analyst,
    context=[task_research],       # Receives output from researcher
)

task_creative = Task(
    description=(
        "Based on the research and analysis, develop a creative campaign concept. "
        "Include messaging, visual themes, and audience targeting strategy."
    ),
    expected_output="A creative brief with campaign concept, tagline, and visual direction.",
    agent=creative_director,
    context=[task_research, task_analysis],
)

task_video = Task(
    description=(
        "Using the creative brief, generate a short promotional video. "
        "Craft a detailed video prompt and use the Seedance Video Generator tool."
    ),
    expected_output="A generated video URL and a description of the video content.",
    agent=video_producer,
    context=[task_creative],
)

task_chairman_summary = Task(
    description=(
        "As Chairman, review all board members' outputs: research, analysis, "
        "creative direction, and video production. Synthesize a final executive "
        "summary and strategic recommendation for the board."
    ),
    expected_output=(
        "An executive summary (500-700 words) covering: key findings, strategic "
        "recommendation, next steps, and any dissenting considerations."
    ),
    agent=chairman,
    context=[task_research, task_analysis, task_creative, task_video],
)


# ============================================================
# CREW SETUP
# ============================================================

board = Crew(
    agents=[chairman, researcher, analyst, creative_director, video_producer],
    tasks=[
        task_research,
        task_analysis,
        task_creative,
        task_video,
        task_chairman_summary,
    ],
    process=Process.sequential,   # Tasks run in order (chairman goes last)
    verbose=True,
    memory=True,                  # Agents share memory across tasks
    max_rpm=10,                   # Rate limit: max 10 requests/min across agents
)


# ============================================================
# RUN THE BOARD
# ============================================================

if __name__ == "__main__":
    print("🏛️  AI Board of Directors — Session Starting...\n")
    print("=" * 60)
    result = board.kickoff()
    print("\n" + "=" * 60)
    print("📋 FINAL BOARD RESOLUTION:\n")
    print(result)
