import threading
from customtkinter import *
from interface.settings import *
from DecodeLanguage.decode import *


class Code_Interface:

    def __init__(self, filename, menu_window):

        """ Creates Code Window """

        # filename Is An Absolute Filepath

        self.window = CTk()
        self.window.title("Decode Editor")
        self.window.config(background=settings.colorTheme)
        self.window.geometry(f"{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()}")
        self.window.eval('tk::PlaceWindow . center')
        self.window.propagate(True)
        self.window.resizable(False, False)
        # Useful Variables
        self.menu_window = menu_window
        self.isDebug_mode = False
        self.stop_code = True
        self.isCodeEditorLocked = False
        self.action_stack = []
        self.action_stack_index = -1

        # Mother Frame For Warning And Run Button
        mother_frame_1 = CTkFrame(self.window, fg_color=settings.colorTheme)
        mother_frame_1.pack(fill=BOTH, padx=5, pady=5)

        # Holds Filename, Stop, And Run
        sub_frame_1 = CTkFrame(mother_frame_1, fg_color=settings.colorTheme)
        sub_frame_1.pack(side="left")
        filename_label = CTkLabel(sub_frame_1, text=f"{str(filename)}" if len(str(filename)) <= settings.limit * 10 else f"{str(filename)[:settings.limit * 10]}...", font=(settings.font, settings.fontSize), fg_color=settings.themeColors[1],
                                       text_color=settings.colorTheme, corner_radius=settings.corner)
        filename_label.pack(fill=BOTH, padx=5, pady=1)
        # Frame For Stop And Run Buttons
        frame_1 = CTkFrame(mother_frame_1, fg_color=settings.colorTheme)
        frame_1.pack(side='right', padx=5, pady=5)
        self.stop_code_button = CTkButton(frame_1, text="Stop", fg_color=settings.colorTheme, text_color=settings.themeColors[3], hover_color=settings.themeColors[2],
                                          corner_radius=settings.corner, font=(settings.font, settings.fontSize), command=lambda: self.stop_code_function())
        self.stop_code_button.pack(side="left", padx=5, pady=5)
        self.run_code_button = CTkButton(frame_1, text="Run", fg_color=settings.colorTheme, text_color=settings.themeColors[3], hover_color=settings.colorTheme,
                                    corner_radius=settings.corner, font=(settings.font, settings.fontSize), command=lambda: self.start_code(filename))
        self.run_code_button.pack(side="right", padx=5, pady=1)

        # Holds Line Label, Column Label, Lock, Undo, And Redo
        sub_frame_2 = CTkFrame(sub_frame_1, fg_color=settings.colorTheme, height=50)
        sub_frame_2.pack(anchor="w")

        sub_sub_frame_1 = CTkFrame(sub_frame_2, fg_color=settings.colorTheme)
        sub_sub_frame_1.pack(fill=BOTH, side="left")
        self.position_label = CTkLabel(sub_sub_frame_1, text="L - C - ", fg_color=settings.colorTheme, font=(settings.font, settings.fontSize),
                                  text_color=settings.themeColors[1])
        self.position_label.pack(side="left", padx=5, pady=1)
        self.lock_button = CTkButton(sub_sub_frame_1, text="Lock", fg_color=settings.themeColors[2], hover_color=settings.themeColors[2], font=(settings.font, settings.fontSize),
                                corner_radius=settings.corner, text_color=settings.themeColors[3], command=self.handle_code_editor_lock)
        self.lock_button.pack(side="right", padx=5, pady=5)

        sub_sub_frame_2 = CTkFrame(sub_frame_2, fg_color=settings.colorTheme)
        sub_sub_frame_2.pack(fill=BOTH, side="right")
        self.undo_button = CTkButton(sub_sub_frame_2, text="Undo", fg_color=settings.colorTheme, hover_color=settings.colorTheme, font=(settings.font, settings.fontSize),
                                text_color=settings.themeColors[3], command=self.undo_action_code_editor)
        self.undo_button.pack(side="left", padx=5, pady=5)
        self.redo_button = CTkButton(sub_sub_frame_2, text="Redo", fg_color=settings.colorTheme, hover_color=settings.colorTheme, font=(settings.font, settings.fontSize),
                                text_color=settings.themeColors[3], command=self.redo_action_code_editor)
        self.redo_button.pack(side="right", padx=5, pady=5)


        # Mother Frame For Results
        self.mother_frame_2 = CTkFrame(self.window, fg_color=settings.colorTheme)
        self.mother_frame_2.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Frame 1
        self.frame_1 = CTkFrame(self.mother_frame_2, fg_color=settings.colorTheme)
        self.frame_1.pack(fill=BOTH, padx=5, pady=5, expand=True)

        # Mother Frame For Code Editor
        self.code_editor = CTkTextbox(self.frame_1, fg_color=settings.colorTheme, text_color=settings.themeColors[1],
                                      border_color=settings.themeColors[3], border_width=settings.border, font=(settings.font, settings.fontSize))
        self.code_editor.pack(fill=BOTH, expand=True, padx=5, pady=5, side="left")
        # Creating Tags
        self.code_editor.tag_config("command", foreground="orange")
        self.code_editor.tag_config("variable", foreground="yellow")
        self.code_editor.tag_config("comment", foreground="grey")
        self.code_editor.tag_config("arguments", foreground="green")
        self.code_editor.tag_config("debugging", background=settings.themeColors[1])
        # Insert Text Into Text Box
        code = self.open_file(filename)
        self.window.after_idle(lambda: self.code_editor.insert("1.0", code if code is not None else ""))
        self.window.after_idle(self.highlight_code)

        # Results Frame
        self.result_frame = CTkTextbox(self.frame_1, fg_color="black", font=(settings.font, settings.fontSize),
                                       border_color=settings.themeColors[2], border_width=settings.border)
        self.result_frame.configure(state='disabled')
        # Creating Tags For This Text Box
        self.result_frame.tag_config("normal_text", foreground="cyan")
        self.result_frame.tag_config("warning_text", foreground=settings.themeColors[0])
        self.result_frame.pack(side="right", fill=BOTH, expand=True, padx=5, pady=5)

        # Mother Frame For Bottom Buttons
        mother_frame_3 = CTkFrame(self.window, fg_color=settings.colorTheme, height=80)
        mother_frame_3.pack(fill="both")
        # Save Button, Menu Button, Run Button
        self.save_button = CTkButton(mother_frame_3, text="Save", fg_color=settings.colorTheme, text_color=settings.themeColors[3],
                                hover_color=settings.themeColors[2], font=(settings.font, settings.fontSize), corner_radius=settings.corner,
                                command=lambda: self.write_file(filename))
        self.save_button.place(relx=0.02, rely=0.0)
        self.menu_button = CTkButton(mother_frame_3, text="Menu", fg_color=settings.colorTheme, text_color=settings.themeColors[3],
                                hover_color=settings.themeColors[2], font=(settings.font, settings.fontSize), corner_radius=settings.corner,
                                command=lambda: self.call_menu(filename))
        self.menu_button.place(relx=0.30, rely=0.0)
        self.set_mode_button = CTkButton(mother_frame_3, text="Set Debug", fg_color=settings.colorTheme, text_color=settings.themeColors[3],
                               hover_color=settings.themeColors[2],font=(settings.font, settings.fontSize), corner_radius=settings.corner,
                               command=lambda: self.toggle_modes())
        self.set_mode_button.place(relx=0.60, rely=0.0)
        self.isDebug_label = CTkLabel(mother_frame_3, text=f"Debug\n{self.isDebug_mode}", fg_color=settings.colorTheme, text_color=settings.themeColors[1],
                                      font=(settings.font, settings.fontSize + 5, fontStyle))
        self.isDebug_label.place(relx=0.9, rely=0.0)

        self.code_editor.bind("<KeyRelease>", self.highlight_code)
        self.code_editor.bind("<KeyRelease>", self.update_code_position)
        self.code_editor.bind("<ButtonRelease>", self.update_code_position)
        self.code_editor.bind("<KeyRelease>", self.save_action_stack)
        self.window.mainloop()


    def get_user_code(self):

        """ Returns User Code """

        code = list()
        lineCode = ""
        for char in self.code_editor.get("1.0", END):
            if char != "\n":
                lineCode += char
            else:
                code.append(lineCode)
                # Reset lineCode
                lineCode = ""
        return code


    @ staticmethod
    def open_file(filename):

        """ Opens File And Return Text """

        try:
            with open(filename, "r") as file:
                return str(file.read())
        except Exception:
            # Show Error
            return None


    def write_file(self, filename):

        """ Writes To File """

        text = self.code_editor.get("1.0", END)
        if text:
            try:
                with open(filename, "w") as file:
                    # Remove Trailing Newline
                    file.write(text.strip())
            except Exception:
                # Show Error
                return
        else:
            # Show Error
            return


    def call_menu(self, filename):

        """ Calls Menu Window """

        # Save This File's Contents
        self.write_file(filename)

        self.window.destroy()
        self.menu_window(isFromAnotherWindow=True)


    def highlight_code(self, _event=None):

        """ Highlights Code """

        # Remove Old Tags
        for tag in self.code_editor.tag_names():
            self.code_editor.tag_delete(tag)

        # Creating New Tags
        self.code_editor.tag_config("command", foreground="orange")
        self.code_editor.tag_config("variable", foreground="yellow")
        self.code_editor.tag_config("comment", foreground="grey")
        self.code_editor.tag_config("arguments", foreground="green")
        self.code_editor.tag_config("debugging", background=settings.themeColors[1])

        # Check Code While Updating Foreground
        temp_line = str()
        position = 1
        for char in self.code_editor.get("1.0", END):
            # Accumulate temp_line
            if char != "\n":
                temp_line += char
            else:
                # Check temp_line For Commands
                commands = temp_line.split(" ")
                # Checking For Different Commands To Apply Respective Foreground
                match commands[0]:
                    case "//": self.code_editor.tag_add("comment", f"{position}.0", f"{position}.end")
                    case "printr":
                        self.code_editor.tag_add("command", f"{position}.0", f"{position}.{len(commands[0])}")
                        self.code_editor.tag_add("arguments", f"{position}.{len(commands[0]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1])}") if len(commands) == 2 else None
                    case "set":
                        self.code_editor.tag_add("command", f"{position}.0", f"{position}.{len(commands[0])}")
                        self.code_editor.tag_add("variable", f"{position}.{len(commands[0]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1])}") if len(commands) > 1 else None
                        self.code_editor.tag_add("arguments", f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2])}") if len(commands) == 3 else None
                    case "add":
                        self.code_editor.tag_add("command", f"{position}.0", f"{position}.{len(commands[0])}")
                        self.code_editor.tag_add("variable", f"{position}.{len(commands[0]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1])}") if len(commands) > 1 else None
                        self.code_editor.tag_add("arguments", f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2])}") if len(commands) > 2 else None
                        self.code_editor.tag_add("arguments",f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2]) + 1}",f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2]) + 1 + len(commands[3])}") if len(commands) == 4 else None
                    case "sub":
                        self.code_editor.tag_add("command", f"{position}.0", f"{position}.{len(commands[0])}")
                        self.code_editor.tag_add("variable", f"{position}.{len(commands[0]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1])}") if len(commands) > 1 else None
                        self.code_editor.tag_add("arguments", f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2])}") if len(commands) > 2 else None
                        self.code_editor.tag_add("arguments",f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2]) + 1}",f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2]) + 1 + len(commands[3])}") if len(commands) == 4 else None
                    case "mul":
                        self.code_editor.tag_add("command", f"{position}.0", f"{position}.{len(commands[0])}")
                        self.code_editor.tag_add("variable", f"{position}.{len(commands[0]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1])}") if len(commands) > 1 else None
                        self.code_editor.tag_add("arguments", f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2])}") if len(commands) > 2 else None
                        self.code_editor.tag_add("arguments",f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2]) + 1}",f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2]) + 1 + len(commands[3])}") if len(commands) == 4 else None
                    case "div":
                        self.code_editor.tag_add("command", f"{position}.0", f"{position}.{len(commands[0])}")
                        self.code_editor.tag_add("variable", f"{position}.{len(commands[0]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1])}") if len(commands) > 1 else None
                        self.code_editor.tag_add("arguments", f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2])}") if len(commands) > 2 else None
                        self.code_editor.tag_add("arguments",f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2]) + 1}",f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2]) + 1 + len(commands[3])}") if len(commands) == 4 else None
                    case "when":
                        self.code_editor.tag_add("command", f"{position}.0", f"{position}.{len(commands[0])}")
                        self.code_editor.tag_add("arguments", f"{position}.{len(commands[0]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1])}") if len(commands) == 2 else None
                    case "end":
                        self.code_editor.tag_add("command", f"{position}.0", f"{position}.{len(commands[0])}")
                    case "if":
                        self.code_editor.tag_add("command", f"{position}.0", f"{position}.{len(commands[0])}")
                        self.code_editor.tag_add("arguments", f"{position}.{len(commands[0]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1])}") if len(commands) > 1 else None
                        self.code_editor.tag_add("arguments", f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1]) + 1 + len(commands[2])}") if len(commands) == 3 else None
                    case "done": self.code_editor.tag_add("command", f"{position}.0", f"{position}.{len(commands[0])}")
                    case "branch":
                        self.code_editor.tag_add("command", f"{position}.0", f"{position}.{len(commands[0])}")
                        self.code_editor.tag_add("arguments", f"{position}.{len(commands[0]) + 1}", f"{position}.{len(commands[0]) + 1 + len(commands[1])}") if len(commands) == 2 else None
                    case "stop": self.code_editor.tag_add("command", f"{position}.0", f"{position}.{len(commands[0])}")
                position += 1
                temp_line = ""


    def toggle_modes(self):

        """ Switches Between Debug Mode And Normal Mode """

        if self.isDebug_mode:
            # Lock Editing
            self.code_editor.configure(state="normal")

            self.isDebug_mode = False
            # Remove Debugging Window
            self.textBox_debug.destroy() if self.textBox_debug.winfo_exists() else None
            # Clear Old Debugging Tags In Editor
            self.code_editor.tag_remove("debugging", "1.0", "end")
            # Clear Results Widget
            self.result_frame.delete("1.0", "end")

            # Toggle Mode Label
            self.isDebug_label.configure(text=f"Debug\n{self.isDebug_mode}")
        else:
            # Lock Editing
            self.code_editor.configure(state="disabled")

            self.isDebug_mode = True
            # Text Box For Debugged Variables And Their Values
            self.textBox_debug = CTkTextbox(self.mother_frame_2, fg_color=settings.colorTheme, font=(settings.font, settings.fontSize), text_color=settings.themeColors[1],
                                            border_color=settings.themeColors[1], border_width=settings.border, height=300)
            self.textBox_debug.configure(state="disabled")
            # Clear Old Debugging Tags In Editor
            self.code_editor.tag_remove("debugging", "1.0", "end")
            # Clear Results Widget
            self.result_frame.configure(state="normal")
            self.result_frame.delete("1.0", "end")
            self.result_frame.configure(state="disabled")

            # Toggle Mode Label
            self.isDebug_label.configure(text=f"Debug\n{self.isDebug_mode}")

            # All These Variables Are Global And Only Debug Function Must Edit Them
            # Reset Some Labels
            # Remove Background Tags
            self.code_editor.tag_remove("debugging", "1.0", "end")
            self.window.update_idletasks()

            # Get Code
            self.code = self.get_user_code()
            if not self.code:
                # Enable Disabled Buttons
                self.run_code_button.configure(state="normal")
                self.set_mode_button.configure(state="normal")
                self.menu_button.configure(state="normal")
                self.save_button.configure(state="normal")
                self.lock_button.configure(state="normal")
                self.undo_button.configure(state="normal")
                self.redo_button.configure(state="normal")
                self.window.update_idletasks()
                return

            # Error Flags
            self.error_flags = {"out_of_bounds": 0,       # Indexing Out Of Bounds
                           "not_integer": 0,              # Not Using Integers
                           "zero_division": 0,            # Dividing By Zero
                           "bad_command": 0,              # Invalid Command
                           "argument_error": 0,           # Not Enough Arguments Or Error In Arguments To Function Call
                           "internal_error": 0,           # Indicates OS Or Python Has A Problem
                           "no_errors": True              # Global Status Flag
                           }
            # Shows Index Where We Are In Showing Output
            self.output_position = 1

            self.vars = dict()
            # Flag For If Statements
            self.IF_FLAG: int = 1
            # Remembers Temporary Value For when
            self.tempValue: str = ""
            # Remembers Temporary Index For when
            self.tempIndex: int = 0
            # Program Counter
            self.execCounter: int = 0


    def stop_code_function(self):

        """ Stops Code In Another Thread """

        self.stop_code = True


    def start_code(self, filename):

        """ Starts Code In Another Thread """

        # Save File's Contents
        self.write_file(filename)

        threading.Thread(target=self.run_normal_mode, daemon=True).start()


    def run_normal_mode(self):

        """ Runs Normal Mode """

        # All Variable In THis Function Are Meant To Run Once And Never Used Outside This Function

        # Lock Editing
        self.code_editor.configure(state="disabled")

        # Call Debugger If Debug Mode
        if self.isDebug_mode:
            self.textBox_debug.pack(fill=BOTH, padx=5, pady=5) if self.textBox_debug.winfo_exists() else None
            self.run_debug_mode()
            return

        # Indicate That Code Has Started Running
        self.stop_code = False

        # Reset Some Labels And Variables
        self.run_code_button.configure(state="disabled")
        self.set_mode_button.configure(state="disabled")
        self.menu_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.lock_button.configure(text="Lock")
        self.lock_button.configure(state="disabled")
        self.undo_button.configure(state="disabled")
        self.redo_button.configure(state="disabled")
        # Remove Background Tags
        self.code_editor.tag_remove("debugging", "1.0", "end")
        # Clear Results Widget
        self.result_frame.configure(state="normal")
        self.result_frame.delete("1.0", "end")
        self.result_frame.configure(state="disabled")

        self.window.update_idletasks()

        # Get Code
        code = self.get_user_code()
        if not code:
            # Enable Disabled Buttons
            self.run_code_button.configure(state="normal")
            self.set_mode_button.configure(state="normal")
            self.menu_button.configure(state="normal")
            self.save_button.configure(state="normal")
            self.lock_button.configure(state="normal")
            self.undo_button.configure(state="normal")
            self.redo_button.configure(state="normal")
            self.window.update_idletasks()
            return

        # Error Flags
        error_flags = {"out_of_bounds": 0,      # Indexing Out Of Bounds
                       "not_integer": 0,        # Not Using Integers
                       "zero_division": 0,      # Dividing By Zero
                       "bad_command": 0,        # Invalid Command
                       "argument_error": 0,     # Not Enough Arguments Or Error In Arguments To Function Call
                       "internal_error": 0,     # Indicates OS Or Python Has A Problem
                       "no_errors": True        # Global Status Flag
                       }

        # Shows Index Where We Are In Showing Output
        output_position = 1

        vars = dict()
        # Flag For If Statements
        IF_FLAG: int = 1
        # Remembers Temporary Value For when
        tempValue: str = ""
        # Remembers Temporary Index For when
        tempIndex: int = 0
        # Program Counter
        execCounter: int = 0
        while len(code) > execCounter >= 0 and error_flags["no_errors"] and not self.isDebug_mode and not self.stop_code:
            try:
                vars, error_flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position = executeLine(code[execCounter], vars, error_flags, execCounter, tempIndex, tempValue, IF_FLAG, len(code), output_position, self.result_frame)
            except IndexError:
                # User Did Not Give Full Arguments On A Function Call
                error_flags["argument_error"] = 1
                error_flags["no_errors"] = False
            except Exception:
                # Imagine Python Or The OS Run Into Problems Like User Doing An Infinite Loop, Stack Overflow
                error_flags["internal_error"] = 1
                error_flags["no_errors"] = False
            execCounter += 1

        # Show Errors
        if not error_flags["no_errors"]:
            # Get Error
            for index, value in enumerate(list(error_flags.values())):
                if value == 1:
                    # Show Error Information
                    self.result_frame.configure(state="normal")
                    self.result_frame.insert("end", f"Line: {str(execCounter)}\n" if len(str(execCounter)) <= settings.limit * 3 else f"Line: {str(execCounter)[:settings.limit * 3]}...\n")
                    self.result_frame.tag_add("warning_text", f"{output_position}.0", f"{output_position}.end")
                    output_position += 1
                    self.result_frame.insert("end", f"Content: {str(code[execCounter - 1])}\n" if len(str(code[execCounter - 1])) <= settings.limit * 3 else f"Content: {str(code[execCounter - 1])[:settings.limit * 3]}...\n")
                    self.result_frame.tag_add("warning_text", f"{output_position}.0", f"{output_position}.end")
                    output_position += 1
                    self.result_frame.insert("end", f"Error: {list(error_flags.keys())[index]}")
                    self.result_frame.tag_add("warning_text", f"{output_position}.0", f"{output_position}.end")
                    output_position += 1
                    self.result_frame.configure(state="disabled")
                    # In Order To Show One Error At A Time
                    break

        # Enable Disabled Buttons
        self.run_code_button.configure(state="normal")
        self.set_mode_button.configure(state="normal")
        self.menu_button.configure(state="normal")
        self.save_button.configure(state="normal")
        self.code_editor.configure(state="normal")
        self.lock_button.configure(state="normal")
        self.undo_button.configure(state="normal")
        self.redo_button.configure(state="normal")
        self.window.update_idletasks()


    def run_debug_mode(self):

        """ Runs Debug Mode """

        if len(self.code) > self.execCounter >= 0 and self.error_flags["no_errors"] and self.isDebug_mode:
            # Highlight Codeline Currently Running To Show User Where System Is Running Code
            self.highlight_code_line(self.execCounter + 1)
            try:
                self.vars, self.error_flags, self.execCounter, self.tempIndex, self.tempValue, self.IF_FLAG, self.output_position = executeLine(self.code[self.execCounter], self.vars, self.error_flags, self.execCounter, self.tempIndex, self.tempValue, self.IF_FLAG, len(self.code), self.output_position, self.result_frame)
            except IndexError:
                # User Did Not Give Full Arguments On A Function Call
                self.error_flags["argument_error"] = 1
                self.error_flags["no_errors"] = False
            except Exception:
                # Imagine Python Or The OS Run Into Problems Like User Doing An Infinite Loop, Stack Overflow
                self.error_flags["internal_error"] = 1
                self.error_flags["no_errors"] = False
            self.execCounter += 1

            # Show Errors
            if not self.error_flags["no_errors"]:
                # Get Error
                for index, value in enumerate(list(self.error_flags.values())):
                    if value == 1:
                        # Shows Error Information
                        self.result_frame.configure(state="normal")
                        self.result_frame.insert("end", f"Line: {str(self.execCounter)}\n" if len(str(self.execCounter)) <= limit * 3 else f"Line: {str(self.execCounter)[:settings.limit * 3]}...\n")
                        self.result_frame.tag_add("warning_text", f"{self.output_position}.0", f"{self.output_position}.end")
                        self.output_position += 1
                        self.result_frame.insert("end", f"Content: {str(self.code[self.execCounter - 1])}\n" if len(str(self.code[self.execCounter - 1])) <= limit * 3 else f"Content: {str(self.code[self.execCounter - 1])[:settings.limit * 3]}...\n")
                        self.result_frame.tag_add("warning_text", f"{self.output_position}.0", f"{self.output_position}.end")
                        self.output_position += 1
                        self.result_frame.insert("end", f"Error: {list(self.error_flags.keys())[index]}")
                        self.result_frame.tag_add("warning_text", f"{self.output_position}.0", f"{self.output_position}.end")
                        self.output_position += 1
                        self.run_code_button.configure(state="disabled")
                        # In Order To Show One Error At A Time
                        break

            # Enable Disabled Buttons
            self.run_code_button.configure(state="normal")
            self.set_mode_button.configure(state="normal")
            self.menu_button.configure(state="normal")
            self.save_button.configure(state="normal")
            self.lock_button.configure(state="normal")
            self.undo_button.configure(state="normal")
            self.redo_button.configure(state="normal")

            # Update Window
            self.update_variable_window_debug_mode()
            self.window.update_idletasks()


    def highlight_code_line(self, position: int):

        """ Highlights A Line Of Code """

        self.code_editor.tag_remove("debugging", "1.0", "end")
        self.code_editor.tag_config("debugging", background=settings.themeColors[1])

        start = f"{position}.0"
        end = f"{position}.end"

        self.code_editor.tag_add("debugging", start, end)
        self.code_editor.see(start)


    def update_variable_window_debug_mode(self):

        """ Updates Variable Window In Debug Mode """

        # Clear Window
        self.textBox_debug.configure(state="normal")
        self.textBox_debug.delete("1.0", "end")

        # Get The Variables And Their Values From Debugging Code
        for index, (key, value) in enumerate(self.vars.items()):
            if len(str(key)) <= settings.limit * 12 and len(str(value)) <= settings.limit * 12:
                self.textBox_debug.insert("end", f"{key}::{value}") if index == 0 else self.textBox_debug.insert("end", f"\n{key}::{value}")
            elif len(str(key)) > settings.limit * 12 and len(str(value)) > settings.limit * 12:
                self.textBox_debug.insert("end", f"{str(key)[:settings.limit * 12]}...::{str(value)[:settings.limit * 12]}...") if index == 0 else self.textBox_debug.insert("end", f"\n{str(key)[:settings.limit * 12]}...::{str(value)[:settings.limit * 12]}...")
            elif len(str(value)) > limit * 12:
                self.textBox_debug.insert("end", f"{key}::{str(value)[:settings.limit * 12]}...") if index == 0 else self.textBox_debug.insert("end", f"\n{key}::{str(value)[:settings.limit * 12]}...")
            elif len(str(key)) > limit * 12:
                self.textBox_debug.insert("end", f"{str(key)[:settings.limit * 12]}...::{value}") if index == 0 else self.textBox_debug.insert("end", f"\n{str(key)[:settings.limit * 12]}...::{value}")
        self.textBox_debug.configure(state="disabled")


    def update_code_position(self, _event):

        """ Updates The Current Line Of Code And Column """

        line, column = self.code_editor.index("insert").split(".")
        if len(str(line)) > settings.limit:
            self.position_label.configure(text=f"L - {str(line)[:settings.limit]}... C - {column}")
        elif len(str(column)) > settings.limit:
            self.position_label.configure(text=f"L - {line} C - {str(column)[:settings.limit]}...")
        elif len(str(line)) > settings.limit and len(str(column)) > settings.limit:
            self.position_label.configure(text=f"L - {str(line)[:settings.limit]}... C - {str(column)[:settings.limit]}...")
        else:
            self.position_label.configure(text=f"L - {line} C - {column}")


    def handle_code_editor_lock(self):

        """ Locks And Unlocks Code Editor """

        if self.isDebug_mode:
            return

        if self.isCodeEditorLocked:
            self.isCodeEditorLocked = False
            self.code_editor.configure(state="normal")
            self.lock_button.configure(text="Unlocked")
        else:
            self.isCodeEditorLocked = True
            self.code_editor.configure(state="disabled")
            self.lock_button.configure(text="Locked")


    def save_action_stack(self, _event):

        """ Saves To Action Stack """

        self.action_stack = self.action_stack[:self.action_stack_index + 1]

        try:
            self.action_stack.append(self.code_editor.get("1.0", "end"))
        except IndexError:
            return
        # If Memory Is DOne Or Any Other Exception Then Do Not Append Anything
        except Exception:
            return
        self.action_stack_index += 1


    def redo_action_code_editor(self):

        """ Redoes Action In Code Editor """

        if self.action_stack_index >= len(self.action_stack) - 1:
            return

        self.action_stack_index += 1

        # Clear The Code Editor
        self.code_editor.delete("1.0", "end")

        # Insert New Code From Stack
        self.code_editor.insert("1.0", str(self.action_stack[self.action_stack_index]).strip())

        # Highlight Code
        self.highlight_code()


    def undo_action_code_editor(self):

        """ Undoes Action In Code Editor """

        if self.action_stack_index <= 0:
            return

        self.action_stack_index -= 1

        # Clear The Code Editor
        self.code_editor.delete("1.0", "end")

        # Insert New Code From Stack
        self.code_editor.insert("1.0", str(self.action_stack[self.action_stack_index]).strip())

        # Highlight Code
        self.highlight_code()