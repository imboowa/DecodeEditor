import os.path

from matplotlib import font_manager

# Font Style
fontStyle = "bold"

# Limit
limit = 5

# Corner Radius
corner = 5

# Border Radius
border = 5

# Useful Variables
commands = ["printr", "set", "//", "add", "sub", "mul", "div", "when", "end", "if", "done", "branch", "stop"]
extension = ".ggh"

def open_file(absolute_filepath):
    try:
        with open(absolute_filepath, "r") as file:
            return file.read().split(",")
    except FileNotFoundError:
        return ["30","Menlo","black","0"]

def write_file(absolute_filepath, text):
    try:
        with open(absolute_filepath, "w") as file:
            file.write(text)
    except FileNotFoundError:
        file.write("30,Menlo,black,0")
    except Exception:
        file.write("30,Menlo,black,0")

def get_settings():
    temp_settings = open_file("../files/info.txt")

    try:
        temp_font_size = temp_settings[0]
        temp_font = temp_settings[1]
        temp_color_theme = temp_settings[2]
        temp_most_recently_opened_folder = temp_settings[3]
    except Exception:
        temp_font_size = 30
        temp_font = "Menlo"
        temp_color_theme = "black"
        temp_most_recently_opened_folder = "0"

    correct_font_size = 30
    correct_font = "Menlo"
    correct_color_theme = "black"
    correct_most_recently_opened_folder = "0"

    # Check Font
    if temp_font in sorted(font_manager.get_font_names()):
        correct_font = temp_font

    # Check Font Size
    try:
        x = int(temp_font_size)
        if 25 <= x <= 30:
            correct_font_size = x
    except ValueError:
        pass

    # Check Color Theme
    if temp_color_theme == "black" or temp_color_theme == "white":
        correct_color_theme = temp_color_theme

    # Check Folder Path
    if os.path.isdir(temp_most_recently_opened_folder):
        correct_most_recently_opened_folder = temp_most_recently_opened_folder

    return correct_font_size, correct_font, correct_color_theme, correct_most_recently_opened_folder

# Get info.txt Settings
fontSize, font, colorTheme, most_recently_open_folder = get_settings()

# Dark Theme Colors
darkThemeColors = ["red", "white", "yellow", "blue"]

# Light Theme Colors
lightThemeColors = ["brown", "black", "green", "orange"]

def get_theme():
    temp_themeColors = ["", "", "", ""]
    if colorTheme == "black":
        for i in range(len(darkThemeColors)):
            temp_themeColors[i] = darkThemeColors[i]
    elif colorTheme == "white":
        for i in range(len(lightThemeColors)):
            temp_themeColors[i] = lightThemeColors[i]
    return temp_themeColors

# Theme Colors
themeColors = get_theme()