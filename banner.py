from rich.console import Console
from rich.align import Align 
from rich.panel import Panel 
from pyfiglet import Figlet
from rich.text import Text 
from rich import print 

def format_text(inputed_text):
    """ Takes text and formats it with Rich and prints t0 console. """
    console = Console()
    console.print(Panel
                  (
                    Align
                    (
                        Text(inputed_text,justify="center", style = "white"), 
                        vertical="middle", align="center"
                    )
                   ), 
                   style= "white")
    

def project_banner():
    console = Console()
    #console.print("text", style = "bold")
    # create a banner 
    custom_fig = Figlet(font='epic')
    banner = (custom_fig.renderText('Cookbook'))
    # format banner 
    banner_text = Text(banner, justify="center", style="white")
    banner_align = Align((banner_text),vertical="middle", align="center")
    banner_panel = Panel(banner_align,  subtitle="by Jasmine Sidhu")
    console.print(banner_panel, style= "magenta")
    
def project_overview():
    """ Prints app overview to console. """
    console = Console()
    console.print(Panel
                  (
                    Align
                    (
                        Text("Welcome to Cookbook CLI!\n Store your favorite recipes, or search for new recipes in our database.",justify="center", style = "white"), 
                        vertical="middle", align="center"
                    )
                   ), 
                   style= "white")

def project_instructions():
    """ Prints app overview to console. """
    console = Console()
    console.print(Panel
                  (
                    Align
                    (
                        Text("Use UP and DOWN arrows to navigate, and ENTER to select option.",justify="center", style = "orchid1"), 
                        vertical="middle", align="center"
                    )
                   ), 
                   style= "white")
    
def exit_banner():
    """Displays a exit message and exits the program"""
    console = Console()
    # create a banner 
    custom_fig = Figlet(font='epic')
    banner = (custom_fig.renderText('Goodbye'))
    # format banner 
    banner_text = Text(banner, justify="center", style="white")
    banner_align = Align((banner_text),vertical="middle", align="center")
    banner_panel = Panel(banner_align,  subtitle="Till next time!")
    console.print(banner_panel, style= "magenta")
    exit()
    