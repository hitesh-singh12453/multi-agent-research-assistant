# Multi-Agent Research Assistant

An AI-powered research assistant built with **LangChain, Groq, Tavily, and Streamlit**. It uses multiple specialized agents to search the web, extract detailed information, generate structured research reports, and review the final output.

## Features

- **Search Agent:** Finds relevant information from the web using Tavily Search.
- **Reader Agent:** Selects relevant URLs and extracts webpage content using BeautifulSoup.
- **Research Writer:** Generates a structured research report using an LLM.
- **Critic:** Reviews the generated report and provides feedback.
- **Streamlit UI:** Provides an interactive interface for conducting research.
- **Report Download:** Allows users to download the generated report.

## Architecture

The project follows a sequential multi-agent workflow:

1. User enters a research topic.
2. Search Agent retrieves relevant web information.
3. Reader Agent scrapes selected webpages for deeper content.
4. Research Writer combines the collected information into a report.
5. Critic reviews the generated report.
6. The application displays the results.

## Tech Stack

- Python
- LangChain
- Groq API
- Tavily Search API
- BeautifulSoup
- Requests
- Streamlit
- python-dotenv

## Project Structure

```text
multi_agent_research_project/
│
├── agents.py           # Search and Reader agents, Writer and Critic chains
├── tools.py            # Web search and webpage scraping tools
├── pipeline.py         # Sequential research pipeline
├── app.py              # Streamlit application
├── requirements.txt    # Project dependencies
├── .env                # API keys (not committed)
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/hitesh-singh12453/multi-agent-research-assistant.git
```

### 2. Navigate to the project directory

```bash
cd multi-agent-research-assistant
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get your API keys:

- Groq: https://console.groq.com/
- Tavily: https://tavily.com/

**Important:** Never commit your `.env` file or expose your API keys.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## How It Works

The application uses specialized agents and processing chains to divide the research task into smaller steps.

- The Search Agent gathers relevant web information.
- The Reader Agent extracts additional information from selected webpages.
- The Writer generates the research report.
- The Critic evaluates the report and provides feedback.

This separation of responsibilities makes the research workflow modular and easier to maintain.

## Future Improvements

- Better source selection and URL extraction.
- Improved error handling and retry mechanisms.
- More robust research verification.
- Live progress updates for individual agents.
- Deployment and accessibility improvements.

## Author

**Hitesh Singh**

GitHub: [hitesh-singh12453](https://github.com/hitesh-singh12453)