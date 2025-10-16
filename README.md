# Local AI Agent: GitHub Repo Puller

An autonomous CLI agent powered by Google's Gemini Pro and LangChain that acts as a personal technical analyst. It finds, scrapes, and analyzes top GitHub repositories for any given technology topic based on natural language queries.

## About The Project

This project was built to solve a common developer problem: finding the most relevant and popular open-source projects for a new technology. Instead of manually searching, this AI agent automates the entire process. It understands user intent, browses the web, scrapes repository data, and presents a qualified, ranked list directly in the terminal.

What started as a simple script evolved into a complete, resume-worthy application demonstrating skills in AI engineering, agentic workflows, and professional developer tooling.

## Key Features

- **AI-Powered Analysis**: Utilizes Google's Gemini Pro model via LangChain to understand prompts, reason, and make decisions.
- **Autonomous Web Research**: Employs DuckDuckGoSearch and BeautifulSoup tools to autonomously find and scrape data from GitHub.
- **Polished Command-Line Interface (CLI)**: Built with Typer and Rich to provide a professional, user-friendly experience with clear commands and beautifully formatted table outputs.
- **Customizable Queries**: Supports both simple topic searches (e.g., "Machine Learning") and highly specific, custom prompts to guide the agent's research.
- **Persistent Storage**: Saves all findings in a local SQLite database to prevent duplicate work and allow for quick data retrieval.

## Built With

- Python
- LangChain for the agentic framework
- Google Gemini Pro as the core reasoning engine
- Typer for the CLI application structure
- Rich for beautiful terminal output
- Pydantic for robust data structuring
- SQLite for local database storage
- BeautifulSoup for web scraping

## Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

- Python 3.10 or higher
- A Google Gemini API Key. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Installation

1. Clone the repository:
- git clone ```https://github.com/your-username/Local_AI_Agent_Github_Repo_Puller.git
cd Local_AI_Agent_Github_Repo_Puller```



2. Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```


3. Install the required packages:
```
pip install -r requirements.txt
```

4. Set up your environment variables:
- Create a new file named `.env` in the root of the project.
- Add your API key to this file:
  ```
  GOOGLE_API_KEY="YOUR_API_KEY_HERE"
  ```

## Usage

The application is run from the command line with several available options.

### 1. Find Repositories for a Topic

This command will run the agent and save the results to the database.
```
python3 main.py --topic "Data Visualization"
```

### 2. Use a Custom, Specific Prompt

For more targeted research, provide a detailed prompt.
```
python3 main.py --topic "Python" --custom-prompt "Find the top 5 GitHub repositories for beginners learning Python, focusing on interactive tutorials."
```

### 3. Display Previously Found Repositories

This command retrieves and displays all data from the database without running the agent.
```
python3 main.py --display-only
```
