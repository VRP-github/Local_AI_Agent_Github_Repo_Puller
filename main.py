import typer
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

from tools import scrape_website, search_tool
from database import init_db, add_repo, get_all_repos, RepoInfo

load_dotenv()

app = typer.Typer(
    name="GitHub Scout",
    help="An AI agent that finds top GitHub repositories for a given technology.",
    add_completion=False
)
console = Console()

class RepoInfoList(BaseModel):
    repositories: list[RepoInfo]

@app.command()
def find(
    topic: str = typer.Option("Machine Learning", help="The technology topic to search for."),
    custom_prompt: str = typer.Option(None, "--custom-prompt", help="A specific, custom prompt to guide the agent's search."),
    display_only: bool = typer.Option(False, "--display-only", help="Only display existing repos from the database.")
):
    """
    Finds and analyzes the top 5 GitHub repositories for a specific topic.
    """
    init_db()

    if not display_only:
        console.print(f"[bold green]Running GitHub Scout Agent for topic: {topic}...[/bold green]")
        
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
        parser = PydanticOutputParser(pydantic_object=RepoInfoList)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are an expert-level Technical Analyst. Your mission is to find and qualify the 5 best GitHub repositories related to the user's request.

            **Your Goal:** Fulfill the user's specific query. If they provide a detailed prompt, prioritize their instructions. If their query is simple (e.g., just a topic), follow the default process below.

            **Default Process (if no specific instructions are given):**
            - Find the 5 most popular and relevant repositories for the topic.
            - Prioritize relevance, star count, and quality of documentation.

            **Mandatory Execution Steps:**
            1.  **Search:** Use the `search_tool` to find potential repositories or curated lists.
            2.  **Scrape & Analyze:** For each promising URL, use `scrape_website` to extract information like stars, language, and description.
            3.  **Format:** Compile the 5 best repositories into the required JSON format. This is your only valid final output.

            Your final answer MUST BE ONLY the JSON object. Do not have a conversation.
            Return the output in this format: {format_instructions}
            """),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]).partial(format_instructions=parser.get_format_instructions())
        
        tools = [scrape_website, search_tool]
        agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=40)

        if custom_prompt:
            console.print(f"[yellow]Using custom prompt:[/yellow] {custom_prompt}")
            query = custom_prompt
        else:
            query = f"Find the top 5 GitHub repositories for the topic: {topic}."
        
        raw_response = agent_executor.invoke({
            "query": query,
            "topic": topic 
        })

        try:
            structured_response = parser.parse(raw_response.get('output'))
            for repo in structured_response.repositories:
                add_repo(repo)
            console.print("\n[bold green]Agent finished. Repositories saved to database.[/bold green]")
        except Exception as e:
            console.print(f"\n[bold red]Error parsing or saving response: {e}[/bold red]")
            console.print("Raw Response from Agent:", raw_response)
            raise typer.Exit()

    console.print("\n[bold blue]Displaying Repositories from Database...[/bold blue]")
    repos_df = get_all_repos()

    if not repos_df.empty:
        table = Table(title=f"Top GitHub Repositories", show_header=True, header_style="bold magenta")
        table.add_column("Repository", style="cyan", no_wrap=True)
        table.add_column("Stars", justify="right", style="green")
        table.add_column("Language", style="yellow")
        table.add_column("Description", style="dim", max_width=60)

        for index, row in repos_df.iterrows():
            table.add_row(
                row['repo_name'],
                str(row['stars']),
                row['primary_language'],
                row['description']
            )
        
        console.print(table)
    else:
        console.print("[yellow]No repositories found in the database.[/yellow]")

if __name__ == "__main__":
    app()

