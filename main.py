import typer
import pyfiglet
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from src.agent.core import initialize_agent

app = typer.Typer()
console = Console()

def print_banner():
    """Imprime el banner estilo retro-hacker."""
    console.clear()
    
    # Generar Arte ASCII
    ascii_art = pyfiglet.figlet_format("BELFORT", font="slant")
    title = Text(ascii_art, style="bold cyan")
    
    subtitle = "Financial Risk Intelligence System v1.0"
    border = Panel(
        Align.center(title + "\n" + subtitle),
        border_style="bold blue",
        title="[bold green]● ONLINE[/bold green]",
        title_align="right",
        subtitle="[dim]Created by Diego Ortiz[/dim]",
        padding=(1, 2)
    )
    
    console.print(border)
    console.print("\n")

@app.command()
def start():
    """Inicia la terminal de BELFORT."""
    print_banner()
    console.print("[dim]Initialising neural engines...[/dim]")
    
    chat_session = None

    # BLOQUE 1: Carga e Inicialización (El spinner solo vive aquí)
    with console.status("[bold blue]Connecting to Institutional Radar DB...[/bold blue]", spinner="dots"):
        try:
            chat_session = initialize_agent()
        except Exception as e:
            console.print(f"[bold red]Critical Boot Error:[/bold red] {e}")
            return # Detener si falla la carga

    # Una vez fuera del 'with', el spinner desaparece.
    console.print("[bold green]✓ System Connected. Secure Channel Established.[/bold green]\n")
    
    # Mensaje de bienvenida
    console.print(Panel(
        Markdown("Soy **BELFORT**. Tu GPS de riesgo financiero está activo. ¿Qué auditamos hoy?"),
        title="🤖 Agent Output",
        border_style="cyan"
    ))
    console.print("\n")

    # BLOQUE 2: Bucle de Conversación (Ya sin spinner de carga inicial)
    while True:
        try:
            user_input = console.input("[bold yellow]USER >> [/bold yellow]")
            
            if user_input.lower() in ["exit", "salir", "quit"]:
                console.print("\n[bold red]Shutting down...[/bold red]")
                break
            
            console.print() # Espacio visual
            
            # Spinner secundario SOLO para procesar la respuesta
            with console.status("[bold cyan]Processing Market Data...[/bold cyan]", spinner="earth"):
                response = chat_session.send_message(user_input)
                
            # Mostrar respuesta
            console.print(Panel(
                Markdown(response.text),
                title="🐺 BELFORT ANALYSIS",
                border_style="bold white",
                expand=False
            ))
            console.print("\n")
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Force Close detected.[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]Runtime Error:[/bold red] {e}")

if __name__ == "__main__":
    app()