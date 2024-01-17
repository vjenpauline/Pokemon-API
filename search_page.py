# Import modules and libraries
from PIL import ImageTk
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, IntVar, Frame, Label, Toplevel, messagebox
from info_page import InfoPage, get_pokemon_data, get_pokemon_info  # Imports functions from info_page.py file
import subprocess
import requests
import random

# Define path
OUTPUT_PATH = Path(__file__).parent
ASSETS_LOC = OUTPUT_PATH / Path(r"assets\search_page")

# Function to get full path for assets
def assets_path(path: str) -> Path:
    return ASSETS_LOC / Path(path)

# Function to open a new page and close the current window
def open_page(file_path: str):
    window.destroy()  # Close the current Tkinter window
    subprocess.run(['python', file_path], check=True)

# Function to display detailed information about a Pokemon
def show_pokemon_info(pokemon_data):
    info_window = Toplevel(window)
    info_window.configure(bg="white")
    info_window.geometry("1240x824")
    info_window.resizable(False, False)
    info_window.title(f"{pokemon_data['name'].title()} Information")

    # Use the InfoPage class to display
    InfoPage(info_window, pokemon_data)

# Function to display Pokemon on the main frame
def show_pokemon(page, frame):
    clear_labels(frame)
    offset = (page - 1) * 3
    limit = 3
    pokemon_data = get_pokemon_data(offset, limit)

    # Color mapping for Pokemon types
    type_color_mapping = {
        "bug": "#8bd674",
        "dark": "#6f6e78",
        "dragon": "#7383b9",
        "electric": "#f2cb55",
        "fairy": "#eba8c3",
        "fighting": "#eb4971",
        "fire": "#ffa756",
        "flying": "#83a2e3",
        "ghost": "#8571be",
        "grass": "#8bbe8a",
        "ground": "#f78551",
        "ice": "#91d8df",
        "normal": "#b5b9c4",
        "poison": "#9f6e97",
        "psychic": "#ff6568",
        "rock": "#d4c294",
        "steel": "#4c91b2",
        "water": "#58abf6",
    }

    for i, pokemon in enumerate(pokemon_data):
        id_number, name, front_sprite_url, types, base_stats, profile, desc = get_pokemon_info(pokemon["url"])
        
        global first_type, second_type
        first_type = types[0] if types else "unknown"
        second_type = types[1] if len(types) > 1 else "unknown"
        bg_color = type_color_mapping.get(first_type, "white")
        
        # Create labels, buttons, and images for each Pokemon
        label_id = Label(frame, text=f"#{id_number}", bg=bg_color, fg="#423E36", font=("Segoe UI Bold", 12 * -1))
        label_name = Label(frame, text=name.title(), bg=bg_color, fg="white", font=("Segoe UI Bold", 30 * -1))
        label_types = Label(frame, text=", ".join(types).title(), bg=bg_color, fg="#423E36", font=("Segoe UI Semibold", 18 * -1))
        view_button = Button(frame, image=img_view_button, bg=bg_color, activebackground=bg_color, borderwidth=0, highlightthickness=0, command=lambda p=pokemon: show_pokemon_info(p))

        # Download and display the front sprite image
        response = requests.get(front_sprite_url)
        image_data = response.content
        photo = ImageTk.PhotoImage(data=image_data)

        label_sprite = Label(frame, image=photo, bg=bg_color)
        label_sprite.photo = photo

        # Change background image based on the first type
        background_photo = PhotoImage(file=assets_path((f"{first_type.lower()}-bg.png")))

        label_background = Label(frame, image=background_photo)
        label_background.photo = background_photo

        # Positions elements
        label_id.grid(row=i, column=0, padx=10, pady=5)
        label_name.grid(row=i, column=1, padx=10, pady=5)
        label_types.grid(row=i, column=2, padx=10, pady=5)
        label_sprite.grid(row=i, column=3, padx=10, pady=5)
        view_button.grid(row=i, column=4, padx=10, pady=5)
        label_background.grid(row=i, column=0, columnspan=5, padx=10, pady=5)
        label_background.lower()
        
    frame.update()

# Function to clear labels on the frame
def clear_labels(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Function to move to the next page
def next_page():
    if current_page.get() == 342: 
        current_page.set(1) # If at the last page, the next page will be the 1st page
    else:
        current_page.set(current_page.get() + 1)
    show_pokemon(current_page.get(), main_frame)

# Function to move to the previous page
def prev_page():
    if current_page.get() == 1: # If at the first page, the previous page will be the last page
        current_page.set(342)
    else:
        current_page.set(current_page.get() - 1)
    show_pokemon(current_page.get(), main_frame)

# Function to search for a Pokemon by name or ID
def search_pokemon():
    search_text = search_pkmn.get().lower()  # Get the entered text from the entry field

    # Check if the entered text is a valid integer to search by DID
    try:
        search_id = int(search_text)
    except ValueError:
        search_id = None

    # Search for the Pokemon by name or ID
    if search_id is not None:
        # If it's a valid integer, search by ID
        pokemon_data = get_pokemon_data(search_id - 1, 1) 
    else:
        # If it's not a valid integer, search by name
        pokemon_data_list = get_pokemon_data(0, 1025)  # Searchs from list IDs 0-1025
        matching_pokemon = None

        for pokemon_data in pokemon_data_list:
            # Check if the entered name matches the name in the list
            if pokemon_data["name"] == search_text:
                matching_pokemon = pokemon_data
                break

        if matching_pokemon:
            # If a matching Pokemon is found by name, use its ID to open detailed information
            url = matching_pokemon["url"]
            response = requests.get(url)
            matching_pokemon_data = response.json()
            search_id = matching_pokemon_data["id"]

            pokemon_data = get_pokemon_data(search_id - 1, 1)
        else:
            # If no matching Pokemon is found, display an error message
            messagebox.showinfo("Not Found", f"No Pokemon found with the name or ID: {search_text}")
            return

    # Checks if any Pokemon is found
    if pokemon_data:
        show_pokemon_info(pokemon_data[0])  # Display the information for the first result
    else: # If no matching Pokemon is found, display an error message
        messagebox.showinfo("Not Found", f"No Pokemon found with the name or ID: {search_text}")

# Function to randomize Pokemon displayed
def randomize_pokemon():
    # Finds a random Pokemon
    random_pokemon_id = random.randint(0, 1025)
    random_pokemon_data = get_pokemon_data(random_pokemon_id - 1, 1)[0]

    # Displays information
    show_pokemon_info(random_pokemon_data)

# Create the main Tkinter window
window = Tk()

# Configure properties
window.configure(bg="white")
window.geometry("1240x824")
window.title("Pokédex Search")

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

# Load button image
img_view_button = PhotoImage(file=assets_path("view_button.png"))

# Load background images and elements
bg_back = PhotoImage(file=assets_path("bg_back.png"))
canvas.create_image(
    619.0,
    425.0,
    image=bg_back
)

# Title
pokedex_title = PhotoImage(file=assets_path("pokedex_title.png"))
canvas.create_image(
    620.0,
    210.0,
    image=pokedex_title
)

# Search Bar Image
search_bg = PhotoImage(file=assets_path("search_bg.png"))
canvas.create_image(
    568.7,
    328.3,
    image=search_bg
)

# Menu Bar
menubar = PhotoImage(file=assets_path("menubar.png"))
canvas.create_image(
    620.0,
    50.0,
    image=menubar
)

# Place entry for searching Pokemon
search_pkmn = Entry( 
    bd=0,
    bg="#F2F2F2",
    fg="#797979",
    font=("Segoe UI", 24 * -1),
    highlightthickness=0
)
search_pkmn.place(
    x=234.9,
    y=299.3,
    width=734.88,
    height=56.75
)
search_pkmn.bind("<Return>", lambda event: search_pokemon())

# Shuffle Button
shuffle = PhotoImage(file=assets_path("shuffle.png"))
shuffle_btn = Button(
    image=shuffle,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: randomize_pokemon(),
    relief="flat"
).place(
    x=1009.38,
    y=299.34,
    width=74.0,
    height=58.75
)

# Menu: Search Button
search_btn = PhotoImage(file=assets_path("search_btn.png"))
Button(
    image=search_btn,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_page("search_page.py"),
    relief="flat"
).place(
    x=1001.64,
    y=25.75,
    width=118.75,
    height=75
)

# Menu: About Button
about_btn = PhotoImage(file=assets_path("about_btn.png"))
Button(
    image=about_btn,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_page("about_page.py"),
    relief="flat"
).place(
    x=1120.39,
    y=25.75,
    width=119.6,
    height=75
)

# Menu: Home Button
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

# Next Page Button
next_btn = PhotoImage(file=assets_path("next_btn.png"))
Button(
    image=next_btn,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: next_page(),
            relief="flat",
        ).place(
            x=1050,
            y=585.8,
            width=26.6,
            height=27.3
        )

# Back Page Button
back_btn = PhotoImage(file=assets_path("back_btn.png"))
Button(
    image=back_btn,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: prev_page(),
            relief="flat",
        ).place(
            x=1050,
            y=538.3,
            width=26.7,
            height=27.4
        )

# Set the current page value
current_page = IntVar(value=1)

# Create a main frame for displaying Pokemon
main_frame = Frame(window, bg="white")
main_frame.place(x=160, y=380, width=866, height=387)

# Displays first page
show_pokemon(current_page.get(), main_frame)

# Starts the main loop
window.resizable(False, False)
window.mainloop()