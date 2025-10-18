#!/usr/bin/env python3
"""
Test Pinterest GIF downloader with various GIF-specific queries
"""

from pinterest_gif_downloader import search_and_download_gifs
from rich.console import Console

console = Console()

# Test queries that should find ACTUAL GIFs
test_queries = [
    "animated gif loop",
    "motion graphics gif",
    "animated illustration gif",
    "gif art animation",
    "illustration animation gif",
]

console.print("\n[bold cyan]🧪 TESTING GIF DOWNLOADER WITH MULTIPLE QUERIES[/bold cyan]\n")

all_results = []

for i, query in enumerate(test_queries, 1):
    console.print(f"\n[bold]━━━ Test {i}/{len(test_queries)}: {query} ━━━[/bold]\n")
    
    try:
        results = search_and_download_gifs(
            query=query,
            num_gifs=3,  # Just 3 per query for testing
            convert_videos=True
        )
        
        all_results.extend(results)
        
        console.print(f"\n[green]✅ Test {i} complete: {len(results)} GIFs downloaded[/green]\n")
        
    except Exception as e:
        console.print(f"\n[red]❌ Test {i} failed: {str(e)[:100]}[/red]\n")

# Final summary
console.print("\n[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]")
console.print(f"\n[bold]📊 FINAL RESULTS[/bold]\n")
console.print(f"[green]Total GIFs downloaded: {len(all_results)}[/green]")
console.print(f"[cyan]Queries tested: {len(test_queries)}[/cyan]\n")

if all_results:
    console.print("[bold]✅ Downloaded files:[/bold]")
    for i, result in enumerate(all_results, 1):
        console.print(f"  {i}. {result['local_path']}")
        console.print(f"     Type: {result['media_type']} | Size: {result['size_mb']:.1f}MB")
else:
    console.print("[yellow]⚠️  No GIFs found in any query[/yellow]")

console.print("\n[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]\n")
