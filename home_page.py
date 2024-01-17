# Import modules and libraries
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import subprocess

# Define path
OUTPUT_PATH = Path(__file__).parent
ASSETS_LOC = OUTPUT_PATH / Path(r"assets\home_page")

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
window.title("Home")

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
    620.0,
    412.0,
    image=bg_back
)

bg_front = PhotoImage(file=assets_path("bg_front.png"))
canvas.create_image(
    619.0,
    412.0,
    image=bg_front
)

bg_design = PhotoImage(file=assets_path("bg_design.png"))
canvas.create_image(
    620.0,
    527.0,
    image=bg_design
)

title = PhotoImage(file=assets_path("title.png"))
canvas.create_image(
    619.7,
    333.05,
    image=title
)

# Create buttons for different pages with associated images and actions
about_btn = PhotoImage(file=assets_path("about_btn.png"))
Button(
    image=about_btn,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_page("about_page.py"),
    relief="flat"
).place(
    x=477.0,
    y=605.0,
    width=286.0,
    height=57.0
)

pokedex_btn = PhotoImage(file=assets_path("pokedex_btn.png"))
Button(
    image=pokedex_btn,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_page("search_page.py"),
    relief="flat"
).place(
    x=477.0,
    y=528.0,
    width=286.0,
    height=57.0
)

# Starts the main loop
window.resizable(False, False)
window.mainloop()