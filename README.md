# 🏛️ AI Board of Directors — CrewAI

A multi-agent AI board powered by CrewAI, featuring Claude as Chairman and four specialist board members.

## Board Members

| Role | Model | Provider |
|------|-------|----------|
| 👑 Chairman | Claude Opus | Anthropic |
| 📊 Chief Data Analyst | GPT-4o | OpenAI |
| 🔬 Chief Research Officer | DeepSeek Chat | DeepSeek |
| 🎨 Chief Creative Officer | Gemini 1.5 Pro | Google |
| 🎬 Chief Video Producer | Seedance (via tool) | ByteDance |

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-board.git
cd ai-board
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API keys
```bash
cp .env.example .env
# Edit .env and add your actual API keys
```

### 4. Run the board
```bash
python main.py
```

## Customizing Tasks

Edit the task descriptions in `main.py` to change what the board works on:
```python
task_research = Task(
    description="Research the latest trends in [YOUR TOPIC HERE]...",
    ...
)
```

## Getting API Keys

- **Anthropic (Claude):** https://console.anthropic.com
- **OpenAI (GPT-4o):** https://platform.openai.com
- **Google (Gemini):** https://aistudio.google.com
- **DeepSeek:** https://platform.deepseek.com
- **Seedance:** https://seedance.ai (or ByteDance PixVerse API)

## ⚠️ Important
Never commit your `.env` file. It's in `.gitignore` for your protection.
