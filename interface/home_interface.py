import os.path
from interface.code_interface import *
from pathlib import Path
from matplotlib import font_manager


class App:

    def __init__(self, isRefreshing=False, isFromAnotherWindow=False):

        """ Window For File Explorer """

        # Update Font, FontSize, And Color Theme
        if isRefreshing:
            settings.fontSize, settings.font, settings.colorTheme, settings.most_recently_open_folder = get_settings()
            settings.themeColors = get_theme()

        self.window = CTk()
        self.window.title("IDEDecode")
        self.window.geometry(f"{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()}")
        self.window.config(bg=settings.colorTheme)
        self.window.eval('tk::PlaceWindow . center')
        self.window.propagate(True)
        self.window.resizable(False, False)
        # Useful Variables
        self.start, self.stop = 0, limit
        self.filepath_contents = None
        self.file_absolute_path = None

        # Mother Frame 1
        self.mother_frame_1 = CTkFrame(self.window, fg_color=settings.themeColors[1])
        self.mother_frame_1.pack(side="left")

        # Decode
        label_1 = CTkLabel(self.mother_frame_1, text="Decode", fg_color=settings.themeColors[1], text_color="black" if settings.colorTheme == "black" else "white",
                         font=(settings.font, settings.fontSize))
        label_1.pack(expand=True, padx=10, pady=1)
        # IDEDecode
        label_2 = CTkLabel(self.mother_frame_1, text="IDEDecode", fg_color=settings.themeColors[1], text_color="black" if settings.colorTheme == "black" else "white",
                           font=(settings.font, settings.fontSize + 20, settings.fontStyle))
        label_2.pack(expand=True, padx=10, pady=1)
        # Frame For Settings And New File Buttons
        self.mother_frame_2 = CTkFrame(self.mother_frame_1, fg_color=settings.themeColors[1])
        self.mother_frame_2.pack(expand=True, padx=10, pady=1, fill=BOTH)
        # Settings
        self.settings_button = CTkButton(self.mother_frame_2, text="Settings", fg_color=settings.colorTheme, text_color=settings.themeColors[1],
                                    hover_color=settings.colorTheme, corner_radius=settings.corner, font=(settings.font, settings.fontSize),
                                    command=lambda: self.show_settings())
        self.settings_button.pack(expand=True, padx=10, pady=10, fill=BOTH)
        # New File
        new_file_button = CTkButton(self.mother_frame_2, text="New File", fg_color=settings.colorTheme, text_color=settings.themeColors[1],
                                    hover_color=settings.colorTheme, corner_radius=settings.corner, font=(settings.font, settings.fontSize),
                                    command=lambda: self.create_newfile())
        new_file_button.pack(expand=True, padx=10, pady=10, fill=BOTH)

        # Mother Frame 2
        self.mother_frame_3 = CTkFrame(self.window, fg_color=settings.colorTheme)
        self.mother_frame_3.pack(expand=True, fill="both", side="right")

        # Subframe
        self.subframe_1 = CTkFrame(self.mother_frame_3, fg_color=settings.colorTheme)
        self.subframe_1.pack(fill=X, pady=5)
        # Entry
        self.entry_1 = CTkEntry(self.subframe_1, fg_color=settings.colorTheme, placeholder_text="Enter Absolute Filepath",
                              placeholder_text_color="white" if settings.colorTheme == "black" else "black",
                              text_color=settings.themeColors[3], font=(settings.font, settings.fontSize), border_width=settings.border, corner_radius=settings.corner, height=80)
        self.entry_1.pack(side="left", fill=BOTH, expand=True)
        # Button
        self.button_1 = CTkButton(self.subframe_1, text="List", fg_color=settings.colorTheme, font=(settings.font, settings.fontSize), text_color=settings.themeColors[3],
                                  hover_color=settings.themeColors[2], corner_radius=settings.corner, height=80, command=lambda: self.manage_filepath_contents(isFromAnotherWindow=False))
        self.button_1.pack(expand=True, padx=5)
        # Sub Frame For Navigation Buttons
        self.sub_sub_frame_1 = CTkFrame(self.mother_frame_3, fg_color=settings.colorTheme)
        self.sub_sub_frame_1.pack(fill=X, pady=5)
        # Tracker Label For Navigation
        self.tracker_label = CTkLabel(self.sub_sub_frame_1, text="", font=(settings.font, settings.fontSize - 5), text_color=settings.themeColors[1], fg_color=settings.colorTheme)
        # Navigation Buttons
        self.navigate_left = CTkButton(self.sub_sub_frame_1, text="<", font=(settings.font, settings.fontSize - 5), text_color=settings.themeColors[3], fg_color=settings.colorTheme,
                                  hover_color=settings.colorTheme, command=lambda: self.button_manager("show left"))
        self.navigate_left.pack(side='left')
        self.tracker_label.place(relx=0.5, rely=0.45, anchor="center")
        self.navigate_right = CTkButton(self.sub_sub_frame_1, text=">", font=(settings.font, settings.fontSize - 5), text_color=settings.themeColors[3],
                                  fg_color=settings.colorTheme,hover_color=settings.colorTheme, command=lambda: self.button_manager("show right"))
        self.navigate_right.pack(side='right')

        # Frame Showcasing Filepath Contents
        self.sub_sub_frame_2 = CTkFrame(self.mother_frame_3, fg_color=settings.themeColors[2])
        self.sub_sub_frame_2.pack(fill=BOTH, expand=True, pady=10, padx=10)

        if isFromAnotherWindow:
            self.window.after_idle(lambda: self.manage_filepath_contents(isFromAnotherWindow))
        self.window.mainloop()


    def create_newfile(self):

        """ Creates A New File """

        # If Not Absolute Filepath Is Received Then The File Creation Will Be Done In The Current Working Directory

        # Get The Absolute Filepath Expected To Have Filename Too
        absolute_filepath = str(self.entry_1.get())

        if os.path.exists(absolute_filepath):
            # Show Error
            error_label = CTkLabel(self.sub_sub_frame_2, text="File Already Exists", font=(settings.font, settings.fontSize),
                                   text_color=settings.themeColors[0], fg_color=settings.themeColors[2], corner_radius=settings.corner)
            error_label.pack(fill=BOTH, expand=True)
            self.window.after(1000, error_label.destroy)
        else:
            try:
                with open(absolute_filepath, "w") as _:
                    pass
                # Show Success
                success_label = CTkLabel(self.sub_sub_frame_2, text="File Created", font=(settings.font, settings.fontSize),
                                   text_color=settings.themeColors[3], fg_color=settings.themeColors[2], corner_radius=settings.corner)
                success_label.pack(fill=BOTH, expand=True)
                self.window.after(1000, lambda: (success_label.destroy(), self.manage_filepath_contents(isFromAnotherWindow=True)))
            except Exception:
                # Show Error
                error_label = CTkLabel(self.sub_sub_frame_2, text="Error Creating File", font=(settings.font, settings.fontSize),
                                       text_color=settings.themeColors[0], fg_color=settings.themeColors[2], corner_radius=settings.corner)
                error_label.pack(fill=BOTH, expand=True)
                self.window.after(1000, error_label.destroy)


    def show_settings(self):

        """ Shows Settings """

        # Disable Settings Button
        self.settings_button.configure(state="disabled")

        # Open info.txt To Get Settings
        temp_fontSize, temp_font, temp_colorTheme, temp_most_recently_open_folder = get_settings()

        # Frame For info.txt Settings
        self.sub_frame_1 = CTkFrame(self.mother_frame_2, fg_color=settings.themeColors[1])
        self.sub_frame_1.pack(fill=BOTH, expand=True, pady=10)

        self.font_entry = CTkEntry(self.sub_frame_1, fg_color=settings.colorTheme, placeholder_text=f"{str(temp_font)}", placeholder_text_color="white" if settings.colorTheme == "black" else "black",
                              text_color=settings.themeColors[3], font=(settings.font, settings.fontSize), border_width=settings.border, corner_radius=settings.corner)
        self.font_entry.pack(fill=BOTH, expand=True, pady=10)

        self.font_size_entry = CTkEntry(self.sub_frame_1, fg_color=settings.colorTheme, placeholder_text=f"{str(temp_fontSize)}", placeholder_text_color="white" if settings.colorTheme == "black" else "black",
                                   text_color=settings.themeColors[3], font=(settings.font, settings.fontSize), border_width=settings.border, corner_radius=settings.corner)
        self.font_size_entry.pack(fill=BOTH, expand=True, pady=10)

        self.color_theme_entry = CTkEntry(self.sub_frame_1, fg_color=settings.colorTheme, placeholder_text=f"{str(temp_colorTheme)}", placeholder_text_color="white" if settings.colorTheme == "black" else "black",
                                     text_color=settings.themeColors[3], font=(settings.font, settings.fontSize), border_width=settings.border, corner_radius=settings.corner)
        self.color_theme_entry.pack(fill=BOTH, expand=True, pady=10)

        save_button = CTkButton(self.sub_frame_1, text="Save", font=(settings.font, settings.fontSize - 5), text_color=settings.themeColors[3],
                                fg_color=settings.themeColors[2], hover_color=settings.themeColors[2], height=80, command=self.save_settings)
        save_button.pack(fill=BOTH, expand=True, pady=10)

        cancel_button = CTkButton(self.sub_frame_1, text="Cancel", font=(settings.font, settings.fontSize - 5), text_color=settings.themeColors[3],
                                  fg_color=settings.themeColors[2], hover_color=settings.themeColors[2], height=80, command=self.remove_settings)
        cancel_button.pack(fill=BOTH, expand=True, pady=10)


    def remove_settings(self):

        """ Removes Settings """

        # Hide self.sub_frame_1
        self.sub_frame_1.destroy()

        # Enable self.settings_button
        self.settings_button.configure(state="normal")


    def get_filepath_contents(self, isFromAnotherWindow=False):

        """ Returns Filepath Contents """

        # Try Getting Absolute Path From info.txt
        temp_fontSize, temp_font, temp_colorTheme, temp_most_recently_open_folder = get_settings()
        temp_absolute_filepath = temp_most_recently_open_folder
        if temp_absolute_filepath != "0" and isFromAnotherWindow:
            absolute_filepath = temp_absolute_filepath
        else:
            # Get Absolute Path
            absolute_filepath = str(self.entry_1.get())

        # Error Checking
        if os.path.isdir(absolute_filepath):
            # Make Global self.file_absolute_path "Know" This
            self.file_absolute_path = absolute_filepath
            # Update info.txt
            write_file("../files/info.txt", f"{temp_fontSize},{temp_font},{temp_colorTheme},{str(absolute_filepath)}")
            return list(os.listdir(absolute_filepath))
        else:
            return None


    def manage_filepath_contents(self, isFromAnotherWindow=False):

        """ Manages The Showcase Of File Contents """

        self.filepath_contents = self.get_filepath_contents(isFromAnotherWindow)

        # Reset Limits
        self.start, self.stop = 0, limit

        if self.filepath_contents is not None:
            # Sort The List
            self.filepath_contents = sorted(self.filepath_contents)
            # Get Absolute Path
            if isFromAnotherWindow:
                pass
            else:
                self.file_absolute_path = str(self.entry_1.get())
            # Clear self.sub_sub_frame_2
            if self.sub_sub_frame_2.winfo_exists():
                for widget in self.sub_sub_frame_2.winfo_children():
                    widget.destroy()
            else:
                return
            # Show Absolute Filepath Files
            for file in self.filepath_contents[self.start:self.stop]:
                # File Name
                CTkButton(self.sub_sub_frame_2, text=str(file) if len(str(file)) <= limit * 5 else f"{str(file)[:limit * 5]}...",
                font=(settings.font, settings.fontSize + 10), text_color=settings.themeColors[3], fg_color=settings.themeColors[2], corner_radius=settings.corner,
                hover_color=settings.themeColors[1], command=lambda temp_file = file: self.handle_file(Path(self.file_absolute_path) / temp_file)).pack(anchor='w', pady=5, padx=5)
                # File Absolute Path
                CTkLabel(self.sub_sub_frame_2, text=self.file_absolute_path if len(self.file_absolute_path) <= limit * 10 else f"{self.file_absolute_path[:limit * 10]}...",
                         font=(settings.font, settings.fontSize - 10), text_color=settings.themeColors[0], fg_color=settings.themeColors[1], corner_radius=settings.corner).pack(anchor='w', pady=1, padx=10)
                # File Bytes
                try:
                    file_bytes = str(os.path.getsize(Path(self.file_absolute_path) / file)) if os.path.isfile(Path(self.file_absolute_path) / file) else None
                    if file_bytes is not None:
                        CTkLabel(self.sub_sub_frame_2, text=file_bytes + " bytes" if len(file_bytes) <= limit * 4 else f"{file_bytes[:limit * 4]}... bytes",
                             font=(settings.font, settings.fontSize - 10), text_color=settings.themeColors[0], fg_color=settings.themeColors[1],
                             corner_radius=settings.corner).pack(anchor='w', pady=1, padx=10)
                except Exception:
                    # FileNotFoundError, OSError And Other Exceptions Cause No Bytes At All
                    CTkLabel(self.sub_sub_frame_2, text="Bytes Not Found",font=(settings.font, settings.fontSize - 10), text_color=settings.themeColors[0], fg_color=settings.themeColors[1],
                             corner_radius=settings.corner).pack(anchor='w', pady=1, padx=10)
            # Update self.tracker_label
            self.manage_tracker_label()
        else:
            if self.sub_sub_frame_2.winfo_exists():
                # Clear self.sub_sub_frame_2
                for widget in self.sub_sub_frame_2.winfo_children():
                    widget.destroy()
            else:
                return
            # Show Error
            error_label = CTkLabel(self.sub_sub_frame_2, text="Filepath Error", font=(settings.font, settings.fontSize), text_color=settings.themeColors[0],
                     fg_color=settings.themeColors[2], corner_radius=settings.corner)
            error_label.pack(fill=BOTH, expand=True)
            self.window.after(1000, error_label.destroy)
            # Update self.tracker_label
            self.manage_tracker_label()


    def manage_tracker_label(self):

        """ Shows Page In self.filepath_contents """

        # Does self.tracker_label Exist
        if not self.tracker_label.winfo_exists():
            return

        if self.filepath_contents is None or self.file_absolute_path is None:
            self.tracker_label.configure(text=f"")
            return
        self.tracker_label.configure(text=f"{self.stop // limit}/{len(self.filepath_contents) // limit}" if len(self.filepath_contents) % limit == 0
                                     else f"{self.stop // limit}/{len(self.filepath_contents) // limit + 1}")


    def button_manager(self, button):

        """ Manages Buttons On Screen """

        if button == "show left":
            if self.filepath_contents is None or self.file_absolute_path is None:
                return
            if self.start >= limit:
                self.start = self.start - limit
                self.stop = self.stop - limit
                if self.sub_sub_frame_2.winfo_exists():
                    # Clear self.sub_sub_frame_2
                    for widget in self.sub_sub_frame_2.winfo_children():
                        widget.destroy()
                else:
                    return
                # Show Absolute Filepath Files
                for file in self.filepath_contents[self.start:self.stop]:
                    # File Name
                    CTkButton(self.sub_sub_frame_2,text=str(file) if len(str(file)) <= limit * 5 else f"{str(file)[:limit * 5]}...",
                              font=(settings.font, settings.fontSize + 10), text_color=settings.themeColors[3], fg_color=settings.themeColors[2], corner_radius=settings.corner,
                              hover_color=settings.themeColors[1], command=lambda temp_file=file: self.handle_file(Path(self.file_absolute_path) / temp_file)).pack(anchor='w', pady=5, padx=5)
                    # File Absolute Path
                    CTkLabel(self.sub_sub_frame_2, text=self.file_absolute_path if len(self.file_absolute_path) <= limit * 10 else f"{self.file_absolute_path[:limit * 10]}...",
                             font=(settings.font, settings.fontSize - 10), text_color=settings.themeColors[0], fg_color=settings.themeColors[1], corner_radius=settings.corner).pack(anchor='w', pady=1, padx=10)
                    # File Bytes
                    try:
                        file_bytes = str(os.path.getsize(Path(self.file_absolute_path) / file)) if os.path.isfile(Path(self.file_absolute_path) / file) else None
                        if file_bytes is not None:
                            CTkLabel(self.sub_sub_frame_2, text=file_bytes + " bytes" if len(file_bytes) <= limit * 4 else f"{file_bytes[:limit * 4]}... bytes",
                                     font=(settings.font, settings.fontSize - 10), text_color=settings.themeColors[0], fg_color=settings.themeColors[1], corner_radius=settings.corner).pack(anchor='w', pady=1, padx=10)
                    except Exception:
                        # FileNotFoundError, OSError And Other Exceptions Cause No Bytes At All
                        CTkLabel(self.sub_sub_frame_2, text="Bytes Not Found", font=(settings.font, settings.fontSize - 10),
                                 text_color=settings.themeColors[0], fg_color=settings.themeColors[1],
                                 corner_radius=settings.corner).pack(anchor='w', pady=1, padx=10)
                # Update self.tracker_label
                self.manage_tracker_label()
        elif button == "show right":
            if self.filepath_contents is None or self.file_absolute_path is None:
                return
            if self.stop < len(self.filepath_contents):
                self.start = self.start + limit
                self.stop = self.stop + limit
                if self.sub_sub_frame_2.winfo_exists():
                    # Clear self.sub_sub_frame_2
                    for widget in self.sub_sub_frame_2.winfo_children():
                        widget.destroy()
                else:
                    return
                # Show Absolute Filepath Files
                for file in self.filepath_contents[self.start:self.stop]:
                    # File Name
                    CTkButton(self.sub_sub_frame_2, text=str(file) if len(str(file)) <= limit * 5 else f"{str(file)[:limit * 5]}...",
                              font=(settings.font, settings.fontSize + 10), text_color=settings.themeColors[3], fg_color=settings.themeColors[2], corner_radius=settings.corner,
                              hover_color=settings.themeColors[1], command=lambda temp_file=file: self.handle_file(Path(self.file_absolute_path) / temp_file)).pack(anchor='w', pady=5, padx=5)
                    # File Absolute Path
                    CTkLabel(self.sub_sub_frame_2, text=self.file_absolute_path if len(self.file_absolute_path) <= limit * 10 else f"{self.file_absolute_path[:limit * 10]}...",
                             font=(settings.font, settings.fontSize - 10), text_color=settings.themeColors[0], fg_color=settings.themeColors[1],
                             corner_radius=settings.corner).pack(anchor='w', pady=1, padx=10)
                    # File Bytes
                    try:
                        file_bytes = str(os.path.getsize(Path(self.file_absolute_path) / file)) if os.path.isfile(
                            Path(self.file_absolute_path) / file) else None
                        if file_bytes is not None:
                            CTkLabel(self.sub_sub_frame_2, text=file_bytes + " bytes" if len(file_bytes) <= limit * 4 else f"{file_bytes[:limit * 4]}... bytes",
                                     font=(settings.font, settings.fontSize - 10), text_color=settings.themeColors[0], fg_color=settings.themeColors[1], corner_radius=settings.corner).pack(anchor='w', pady=1, padx=10)
                    except Exception:
                        # FileNotFoundError, OSError And Other Exceptions Cause No Bytes At All
                        CTkLabel(self.sub_sub_frame_2, text="Bytes Not Found", font=(settings.font, settings.fontSize - 10), text_color=settings.themeColors[0], fg_color=settings.themeColors[1],
                                 corner_radius=settings.corner).pack(anchor='w', pady=1, padx=10)
                # Update self.tracker_label
                self.manage_tracker_label()


    def handle_file(self, filename):

        """ Handles Validation, Closing Window, Opening Code Editor Window """

        if self.validate_file(filename):
            # Destroy Window
            self.window.destroy() if self.window.winfo_exists() else None
            # Call Next Window If All Is Good
            Code_Interface(filename, App)
        else:
            # Show Error
            error_label = CTkLabel(self.sub_sub_frame_2, text="Invalid File Format", font=(settings.font, settings.fontSize),
                     text_color=settings.themeColors[0], fg_color=settings.themeColors[1], corner_radius=settings.corner)
            error_label.place(relx=0.5, rely=0.95, anchor="center")
            self.window.after(1000, error_label.destroy)


    def save_settings(self):

        """ Saves A Setting To info.txt """

        # Get Old Settings
        x_fontSize, x_font, x_colorTheme, x_most_recently_open_folder = get_settings()

        temp_font = str(self.font_entry.get())
        temp_font_size = str(self.font_size_entry.get())
        temp_color_theme = str(self.color_theme_entry.get())
        _ = x_most_recently_open_folder

        if len(temp_font) > 0 and temp_font in sorted(font_manager.get_font_names()):
            write_file("../files/info.txt", f"{x_fontSize},{temp_font},{x_colorTheme},{x_most_recently_open_folder}")
        else:
            write_file("../files/info.txt", f"{x_fontSize},Menlo,{x_colorTheme},{x_most_recently_open_folder}")

        # Re-get Old Settings
        x_fontSize, x_font, x_colorTheme, x_most_recently_open_folder = get_settings()

        if len(temp_font_size) > 0:
            try:
                x = int(temp_font_size)
                if 25 <= x <= 30:
                    write_file("../files/info.txt", f"{x},{x_font},{x_colorTheme},{x_most_recently_open_folder}")
                else:
                    write_file("../files/info.txt", f"30,{x_font},{x_colorTheme},{x_most_recently_open_folder}")
            except ValueError:
                write_file("../files/info.txt", f"30,{x_font},{x_colorTheme},{x_most_recently_open_folder}")

        # Re-get Old Settings
        x_fontSize, x_font, x_colorTheme, x_most_recently_open_folder = get_settings()

        if len(temp_color_theme) > 0:
            if temp_color_theme == "black" or temp_color_theme == "white":
                write_file("../files/info.txt", f"{x_fontSize},{x_font},{temp_color_theme},{x_most_recently_open_folder}")
            else:
                write_file("../files/info.txt", f"{x_fontSize},{x_font},black,{x_most_recently_open_folder}")

        self.window.destroy() if self.window.winfo_exists() else None

        App(isRefreshing=True, isFromAnotherWindow=True)


    @staticmethod
    def validate_file(filename):

        """ Validates A File If "extension" File """

        filename = str(filename)
        if os.path.isfile(filename) and settings.extension in filename:
            try:
                with open(filename, "r") as file:
                    # Read Line By Line
                    for line in file:
                        temp = line.strip()
                        if not temp:
                            continue
                        temp_line = temp.split(" ")
                        # Checking The "Command" Only
                        if temp_line[0] not in settings.commands and temp_line[0] != "":
                            return False
                    return True
            except Exception:
                return False
        return False


if __name__ == "__main__":
    App()