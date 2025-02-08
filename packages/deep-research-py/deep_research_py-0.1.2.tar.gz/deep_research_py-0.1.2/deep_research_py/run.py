import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
import asyncio
from prompt_toolkit import PromptSession

from deep_research_py.deep_research import deep_research, write_final_report
from deep_research_py.feedback import generate_feedback

app = typer.Typer()
console = Console()
session = PromptSession()

async def async_prompt(message: str, default: str = "") -> str:
    """Async wrapper for prompt_toolkit."""
    return await session.prompt_async(message)

@app.command()
async def main():
    """Deep Research CLI"""
    
    console.print(Panel.fit(
        "[bold blue]Deep Research Assistant[/bold blue]\n"
        "[dim]An AI-powered research tool[/dim]"
    ))
    
    # Get initial inputs with clear formatting
    query = await async_prompt("\n🔍 What would you like to research? ")
    console.print()
    
    breadth_prompt = f"📊 Research breadth (recommended 2-10) [4]: "
    breadth = int((await async_prompt(breadth_prompt)) or "4")
    console.print()
    
    depth_prompt = f"🔍 Research depth (recommended 1-5) [2]: "
    depth = int((await async_prompt(depth_prompt)) or "2")
    console.print()

    # First show progress for research plan
    console.print("\n[yellow]Creating research plan...[/yellow]")
    follow_up_questions = await generate_feedback(query)
    
    # Then collect answers separately from progress display
    console.print("\n[bold yellow]Follow-up Questions:[/bold yellow]")
    answers = []
    for i, question in enumerate(follow_up_questions, 1):
        console.print(f"\n[bold blue]Q{i}:[/bold blue] {question}")
        answer = await async_prompt("➤ Your answer: ")
        answers.append(answer)
        console.print()

    # Combine information
    combined_query = f"""
    Initial Query: {query}
    Follow-up Questions and Answers:
    {chr(10).join(f"Q: {q} A: {a}" for q, a in zip(follow_up_questions, answers))}
    """
    
    # Now use Progress for the research phase
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Do research
        task = progress.add_task("[yellow]Researching your topic...[/yellow]", total=None)
        research_results = await deep_research(
            query=combined_query,
            breadth=breadth,
            depth=depth
        )
        progress.remove_task(task)
        
        # Show learnings
        console.print("\n[yellow]Learnings:[/yellow]")
        for learning in research_results["learnings"]:
            rprint(f"• {learning}")
        
        # Generate report
        task = progress.add_task("Writing final report...", total=None)
        report = await write_final_report(
            prompt=combined_query,
            learnings=research_results["learnings"],
            visited_urls=research_results["visited_urls"]
        )
        progress.remove_task(task)
        
        # Show results
        console.print("\n[bold green]Research Complete![/bold green]")
        console.print("\n[yellow]Final Report:[/yellow]")
        console.print(Panel(report, title="Research Report"))
        
        # Show sources
        console.print("\n[yellow]Sources:[/yellow]")
        for url in research_results["visited_urls"]:
            rprint(f"• {url}")
        
        # Save report
        with open("output.md", "w") as f:
            f.write(report)
        console.print("\n[dim]Report has been saved to output.md[/dim]")


def run():
    """Synchronous entry point for the CLI tool."""
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main()) 