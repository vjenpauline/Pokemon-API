# Import modules and libraries
from PIL import ImageTk, Image
from io import BytesIO
from pathlib import Path
from tkinter import Canvas, PhotoImage
import requests

# Define path
OUTPUT_PATH = Path(__file__).parent
ASSETS_LOC = OUTPUT_PATH / Path(r"assets\info_page")

# Function to get full path for assets
def assets_path(path: str) -> Path:
    return ASSETS_LOC / Path(path)

# Function to get Pokemon data from PokeAPI
def get_pokemon_data(offset, limit):
    url = f"https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    return data["results"]

# Function to get information about a Pokemon from PokeAPI
def get_pokemon_info(url):
    response = requests.get(url)
    data = response.json()
    name = data["name"]
    id_number = data["id"]
    front_sprite_url = data["sprites"]["front_default"]
    types = [t["type"]["name"] for t in data["types"]]

    base_stats = {
        "hp": data["stats"][0]["base_stat"],
        "attack": data["stats"][1]["base_stat"],
        "defense": data["stats"][2]["base_stat"],
        "sp_atk": data["stats"][3]["base_stat"],
        "sp_def": data["stats"][4]["base_stat"],
        "spd": data["stats"][5]["base_stat"],
        "total": sum(stat["base_stat"] for stat in data["stats"]),
    }

    species_url = data["species"]["url"]
    gender_info = get_gender_info(species_url)
    desc = get_pokemon_description(species_url).replace('\n', ' ').replace('\f', ' ')

    get_abilities = "\n".join([ability["ability"]["name"] for ability in data["abilities"]])

    profile = {
        "height": data["height"],
        "weight": data["weight"],
        "exp": data["base_experience"],
        "gender": gender_info,
        "abilities": get_abilities.title(),
    }

    return id_number, name, front_sprite_url, types, base_stats, profile, desc

# Function to get gender of a Pokemon
def get_gender_info(url):
    response = requests.get(url)
    data = response.json()

    if data["gender_rate"] == -1:
        return "Genderless\n"
    
    male_percentage = data["gender_rate"] * 12.5
    female_percentage = (8 - data["gender_rate"]) * 12.5
    return f"Male: {male_percentage}%\nFemale: {female_percentage}%"

# Function to get Pokemon description
def get_pokemon_description(url):
    response = requests.get(url)
    data = response.json()
     
    for entry in data["flavor_text_entries"]:
        if entry["language"]["name"] == "en": # Assumes the description is in English
            return entry["flavor_text"]
        
    # If there is no English flavor text or no text in general, return a default message
    return "There are no Pokédex entries available for this Pokemon."

# Class to represent the information page of a Pokemon
class InfoPage:
    def __init__(self, master, pokemon_data):
        self.master = master
        self.pokemon_data = pokemon_data

        # Calls function that creates widgets
        self.create_widgets()

    def create_widgets(self):
        # Extracts relevant information from pokemon_data
        id_number, name, front_sprite_url, types, base_stats, profile, desc = get_pokemon_info(self.pokemon_data["url"])

        global first_type, second_type
        first_type = types[0] if types else "unknown"
        second_type = types[1] if len(types) > 1 else "unknown"

        # Create a canvas for placing elements
        canvas = Canvas(
            self.master,
            bg = "white",
            height = 824,
            width = 1240,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.place(x = 0, y = 0)

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
        
        bg_img1 = PhotoImage(file=assets_path("bg_img1.png"))
        canvas.create_image(
            598.0,
            616.0,
            image=bg_img1
        )

        type1 = PhotoImage(file=assets_path(f"{first_type}-iconbig.png"))
        canvas.create_image(
            497.1,
            317.4,
            anchor="w",
            image=type1
        )

        # Checks if Pokemon has a second type to show 
        if second_type != "unknown":
            type2 = PhotoImage(file=assets_path(f"{second_type}-iconbig.png"))
            canvas.create_image(
                700.08349609375,
                317.37109375,
                image=type2
            )

        bg_img2 = PhotoImage(file=assets_path("bg_img2.png"))
        canvas.create_image(
            922.3, 
            616.3,
            image=bg_img2
        )
        canvas.create_text(
            498.26,
            225.3,
            anchor="nw",
            text=f"{name.title()}",
            fill="#091D51",
            font=("Segoe UI Bold", 48 * -1)
        )
        canvas.create_text(
            498.26,
            203.4,
            anchor="nw",
            text=f"#{id_number}",
            fill="#152D6E",
            font=("Segoe UI", 26 * -1)
        )
        canvas.create_text(
            498.26,
            360.4,
            anchor="nw",
            text=f"{desc}",
            width=600,
            fill="#152D6E",
            font=("Segoe UI", 16 * -1)
        )
        canvas.create_text(
            1075.0,
            517.0,
            anchor="ne",
            justify="right",
            text=f"{profile['height']}\n{profile['weight']}\n{profile['exp']}\n{profile['gender']}\n{profile['abilities']}\n",
            fill="#152D6E",
            font=("Segoe UI", 16 * -1)
        )
        canvas.create_text(
            768.0,
            517.0,
            anchor="nw",
            text="Height\nWeight\nExperience\nGender Ratio\n\nAbilities ",
            fill="#152D6E",
            font=("Segoe UI Bold", 16 * -1)
        )
        canvas.create_text(
            748.2,
            454.2,
            anchor="nw",
            text="Profile",
            fill="#152D6E",
            font=("Segoe UI Bold", 20 * -1)
        )
        canvas.create_text(
            524.0,
            517.0,
            anchor="nw",
            text="HP\nAttack\nDefense\nSp. Atk\nSp. Def\nSpeed\nTotal",
            fill="#152D6E",
            font=("Segoe UI Bold", 16 * -1)
        )
        canvas.create_text(
            670,
            517,
            anchor="ne",
            justify="right",
            text=f"{base_stats['hp']}\n{base_stats['attack']}\n{base_stats['defense']}\n{base_stats['sp_atk']}\n{base_stats['sp_def']}\n{base_stats['spd']}\n{base_stats['total']}",
            fill="#152D6E",
            font=("Segoe UI", 16 * -1)
        )
        canvas.create_text(
            498.0,
            454.0,
            anchor="nw",
            text="Base Stats",
            fill="#152D6E",
            font=("Segoe UI Bold", 20 * -1)
        )

        response = requests.get(front_sprite_url)
        image_data = response.content

        # Create a PIL Image object and resize it
        sprite_image = Image.open(BytesIO(image_data))
        # Enlarges sprite size from PokeAPI Database
        resized_sprite = sprite_image.resize((sprite_image.width * 5, sprite_image.height * 5))

        photo = ImageTk.PhotoImage(resized_sprite)

        canvas.create_image(
            275.930908203125,
            420.8599853515625,
            image=photo
        )

        img_back_btn = PhotoImage(file=assets_path("back_btn.png"))
        back_btn = canvas.create_image(
            1094.39111328125,
            203.129638671875,
            image=img_back_btn,
            anchor="nw" 
        )
        # Bind a function to the button click event
        canvas.tag_bind(back_btn, '<Button-1>', lambda event: self.back_click())
        
        self.master.mainloop()

    # Function to close the window
    def back_click(self):
        self.master.destroy()