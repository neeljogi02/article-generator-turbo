import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from app.core.search import FreeResearcher
from app.core.outliner import FreeOutliner
from app.core.drafter import FreeDrafter
from app.core.media import FreeMediaFetcher

console = Console()

def main():
    topic = "How Agentic AI Workflows Are Replacing Traditional RPA"
    audience = "Software Engineers & Tech Leaders"

    console.print(f"[bold cyan]🔍 1. Gathering Live Research...[/bold cyan]")
    researcher = FreeResearcher(max_results=4)
    sources = researcher.search_topic(topic)
    research_text = researcher.format_sources_for_prompt(sources)
    console.print(f"[green]✔ Retrieved {len(sources)} verified sources.[/green]")

    console.print(f"[bold cyan]🧠 2. Synthesizing SEO Blueprint...[/bold cyan]")
    outliner = FreeOutliner()
    plan = outliner.generate_plan(topic, audience, sources, research_text)
    console.print(f"[bold yellow]Title:[/bold yellow] {plan.seo_title}")

    drafter = FreeDrafter()
    media = FreeMediaFetcher()

    markdown_parts = []
    markdown_parts.append(f"# {plan.seo_title}\n\n")
    markdown_parts.append(f"> **Meta Description:** {plan.meta_description}\n\n---\n\n")

    context_accumulator = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[yellow]Drafting sections and generating visuals...", total=len(plan.sections))

        for idx, sec in enumerate(plan.sections, 1):
            progress.update(task, description=f"[cyan]Writing Section {idx}/{len(plan.sections)}: {sec.heading}...")
            
            # Fetch Image
            img_url = media.get_image_url(sec.image_prompt)
            
            # Draft Section
            summary_context = " ".join(context_accumulator[-2:])
            content = drafter.draft_section(sec, summary_context, research_text)
            context_accumulator.append(sec.heading)

            # Assemble Markdown
            markdown_parts.append(f"## {sec.heading}\n\n")
            markdown_parts.append(f"![{sec.heading}]({img_url})\n\n")
            markdown_parts.append(f"{content}\n\n---\n\n")

            progress.advance(task)

    # Append Sources & References
    markdown_parts.append("## References & Key Sources\n\n")
    for s in plan.sources:
        markdown_parts.append(f"- [{s.title}]({s.url})\n")

    full_article = "".join(markdown_parts)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "article.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_article)

    console.print(f"\n[bold green]🎉 Article successfully generated and saved to: {output_file}[/bold green]")
    console.print(f"[dim]Total word count: ~{len(full_article.split())} words.[/dim]")

if __name__ == "__main__":
    main()
