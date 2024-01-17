# Import modules and libraries
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import subprocess

# Define path
OUTPUT_PATH = Path(__file__).parent
ASSETS_LOC = OUTPUT_PATH / Path(r"assets\about_page")

# Function to get full path for assets
def assets_path(path: str) -> Path:
    return ASSETS_LOC / Path(path)

# Function to open a new page and close the current window
def open_page(file_path: str):
    window.destroy()  # Close the current Tkinter window
    subprocess.run(['python', file_path], check=True)

# Create the main Tkinter window
window = Tk()
window.configure(bg="white")
window.geometry("1240x824")
window.title("About")

# Create a canvas for placing elements
canvas = Canvas(
    window,
    bg="white",
    height=824,
    width=1240,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Load background images and other elements
bg_back = PhotoImage(file=assets_path("bg_back.png"))
canvas.create_image(
    619.0,
    425.0,
    image=bg_back
)

bg_design = PhotoImage(file=assets_path("bg_design.png"))
canvas.create_image(
    707.0,
    299.0,
    image=bg_design
)

menubar = PhotoImage(file=assets_path("menubar.png"))
canvas.create_image(
    620.0,
    50.0,
    image=menubar
)

# Create buttons for different pages with associated images and actions
search_btn = PhotoImage(file=assets_path("search_btn.png"))
Button(
    image=search_btn,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_page("search_page.py"),
    relief="flat"
).place(
    x=1001.6,
    y=25.75,
    width=118.75,
    height=75
)

about_btn = PhotoImage(file=assets_path("about_btn.png"))
Button(
    image=about_btn,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_page("about_page.py"),
    relief="flat"
).place(
    x=1120.4,
    y=25.75,
    width=119.6,
    height=75
)

home_btn = PhotoImage(file=assets_path("home_btn.png"))
Button(
    image=home_btn,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_page("home_page.py"),
    relief="flat"
).place(
    x=882.9,
    y=25.75,
    width=118.75,
    height=75
)

canvas.create_rectangle(
    533.0,
    214.0,
    708.0,
    259.0,
    fill="white",
    outline=""
)

subtitle = PhotoImage(file=assets_path("subtitle.png"))
canvas.create_image(
    620.0,
    221.0,
    image=subtitle
)

canvas.create_text(
    274.0,
    699.0,
    anchor="nw",
    text="Created by:\t\t\t\t\tWith the help of:         ",
    fill="#152D6E",
    font=("Segoe UI Bold", 18 * -1)
)

canvas.create_text(
    274.0,
    699.0,
    anchor="nw",
    text="\t     Pauline Villahermosa, BSU BsC Year 2 Group 2 | \t              PokeAPI ",
    fill="#152D6E",
    font=("Segoe UI", 18 * -1)
)

canvas.create_text(
    178.0,
    256.0,
    anchor="nw",
    text="\tThis application is a Pokémon database which mimics the Pokédex, a gadget in\nthe Pokémon world that offers extensive information about creatures featured in there.\nOn the main list pages, you can view three Pokémon at a time. Clicking on the view more \n button beside a Pokémon will lead you to a detailed page containing Pokédex data, \n descriptions from the latest Pokémon game, its latest front sprite, information, and \n additional details—it does not include the move list of a Pokémon as an actual Pokédex\n would not.",
    fill="#152D6E",
    font=("Segoe UI Semibold", 22 * -1)
)

canvas.create_text(
    179.0,
    476.0,
    anchor="nw",
    text="\tFeel free to use the search bar to find a particular Pokémon by entering either its\nNational ID number or its name. It is not possible to search for a Pokémon with just a\nfew letters of its name. Alternatively, you can explore Pokémon directly from the initial\npage, where the three Pokémon are displayed each, and navigate through them using the\narrows. You might also find it intriguing to explore randomly selected Pokémon through\nthe shuffle button!",
    fill="#152D6E",
    font=("Segoe UI Semibold", 22 * -1)
)

# Starts the main loop
window.resizable(False, False)
window.mainloop()