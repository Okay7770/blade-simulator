import random
import time
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

console = Console()

SWORD_ART = r"""
          /\
         /  \
        |    |
        |    |
        |    |
        |    |
        |    |
        |    |
      __|____|__
     [__________]
         |  |
         |  |
         |__|
         (  )
          \/
"""


def build_status_table(target: str, threads: int, completed: int, bandwidth_mbps: float) -> Table:
    table = Table(
        title="[bold bright_cyan]⚔️ LIVE TRAFFIC INJECTION SIMULATOR ⚔️[/bold bright_cyan]",
        expand=True,
        border_style="cyan",
        header_style="bold gold1",
    )
    table.add_column("TELEMETRY", style="bold bright_cyan")
    table.add_column("METRIC DATA", style="bold yellow")

    table.add_row("🎯 TARGET NODE", f"[bold white]{target}[/bold white]")
    table.add_row("⚙️ SIMULATED THREADS", f"[bold white]{threads}[/bold white]")
    table.add_row("📦 COMPLETED PACKETS", f"[bold green]{completed}[/bold green] / [bold white]{threads}[/bold white]")
    table.add_row("📊 BANDWIDTH SIMULATED", f"[bold bright_cyan]{bandwidth_mbps:.2f} Mbps[/bold bright_cyan]")
    table.add_row("🛡️ STATUS", "[bold blink gold1]INJECTING... (0 REAL PACKETS)[/bold blink gold1]")
    return table


def main():
    console.clear()

    sword_text = Text(SWORD_ART, style="bold bright_cyan", justify="center")
    title_text = Text("BLADE // TERMINAL SIMULATOR\n", style="bold gold1", justify="center")
    subtitle_text = Text("SAFE SYSTEM STRESS SIMULATOR | VERSION 2.5", style="dim white", justify="center")

    header_group = Group(sword_text, title_text, subtitle_text)
    console.print(
        Panel(
            header_group,
            border_style="bright_cyan",
            subtitle="[bold white]BLADE ENGINE[/bold white]",
            subtitle_align="center",
            padding=(1, 2),
        )
    )

    console.print()
    target = console.input("[bold bright_cyan]❯ Enter target IP / Hostname [localhost]: [/bold bright_cyan]").strip()
    if not target:
        target = "localhost"

    try:
        threads_input = int(console.input("[bold bright_cyan]❯ Enter simulated threads (0 - 10000): [/bold bright_cyan]"))
        threads = max(0, min(10000, threads_input))
    except ValueError:
        console.print("[bold yellow]⚠ Invalid input. Defaulting to 100 threads.[/bold yellow]")
        threads = 100

    if threads == 0:
        console.print("[bold red]❌ 0 threads selected. Operation aborted.[/bold red]")
        return

    progress = Progress(
        SpinnerColumn("aesthetic", style="bold bright_cyan"),
        TextColumn("[bold gold1]{task.description}"),
        BarColumn(bar_width=None, complete_style="bold green", finished_style="bold bright_green"),
        TextColumn("[bold yellow]{task.percentage:>3.0f}%"),
        TextColumn("[bold cyan]({task.completed}/{task.total})"),
    )
    task_id = progress.add_task("Injecting payloads...", total=threads)

    completed = 0
    simulated_mbps = 0.0

    with Live(refresh_per_second=15) as live:
        with ThreadPoolExecutor(max_workers=min(threads, 250)) as executor:

            def fake_worker(i):
                nonlocal completed, simulated_mbps
                time.sleep(random.uniform(0.001, 0.006))
                completed += 1
                simulated_mbps = random.uniform(250.0, 990.0)

                progress.update(task_id, advance=1)

                table = build_status_table(target, threads, completed, simulated_mbps)
                panel_group = Panel(
                    Group(table, progress),
                    title="[bold bright_green]● ONLINE[/bold bright_green]",
                    border_style="bright_cyan",
                    padding=(1, 2),
                )
                live.update(panel_group)

            futures = [executor.submit(fake_worker, i) for i in range(threads)]
            for future in futures:
                future.result()

    console.print()
    console.print(
        Panel(
            Text("✔ ATTACK SUCCESSFUL\n", style="bold bright_green", justify="center")
            + Text("Session completed successfully. 0 network packets were generated.", style="dim white", justify="center"),
            border_style="bold green",
            padding=(1, 4),
        )
    )


if __name__ == "__main__":
    main()