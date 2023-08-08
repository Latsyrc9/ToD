import logging as log
import tkinter as tk

from .truth_or_dare import TruthOrDare
from .operations import Files

DATA_FOLDER_PATH = "data"

class GUI:
    def __init__(self, root):
        data_folder = Files(DATA_FOLDER_PATH)
        options = data_folder.get_csv_files_from_folder()

        # Init Dropdown Menu
        self.selected_option = tk.StringVar()
        self.selected_option.set(options[0])
        # Create Dropdown Menu
        self.dropdown_menu = tk.OptionMenu(root, self.selected_option, *options)

        self.root = root
        self.tod = TruthOrDare()

    def load_start_screen(self):
        # Create the main window
        self.root.title("Truth or Dare Game")
        self.root.geometry("400x300")

        # Create widgets
        self.start_label = tk.Label(self.root, text="", wraplength=300, justify="center", font=("Helvetica", 14))
        self.start_button = tk.Button(self.root, text="START GAME", command=self.start_button_clicked)

        # Place widgets in the window
        self.start_label.pack(pady=20)
        self.start_button.pack(pady=10)
        self.dropdown_menu.pack()

    def start_button_clicked(self):
        # Clean Up
        self.clear_window()

        self.button_frame = tk.Frame(self.root)

        self.summary_label = tk.Label(self.root, text="", wraplength=300, justify="center", font=("Helvetica", 14))
        self.details_label = tk.Label(self.root, text="Details TODO", wraplength=300, justify="center", font=("Helvetica", 14))
        self.truth_button = tk.Button(self.button_frame, text="Get Truth", command=self.truth_button_clicked)
        self.dare_button = tk.Button(self.button_frame, text="Get Dare", command=self.dare_button_clicked)

        self.truth_button.pack(side='left', padx=10)
        self.dare_button.pack(side='left', padx=10)
        self.button_frame.pack(side='bottom', anchor='s')
        self.summary_label.pack(side='top', pady=20)
        self.details_label.pack(side='bottom', pady=20)

        self.tod.get_data(self.selected_option.get())

    def truth_button_clicked(self):
        log.info('Truth Button Clicked')
        # Clean Up
        self.clear_window()

        question = self.tod.get_truth()
        self.summary_label.config(text=question)

    def dare_button_clicked(self):
        log.info('Dare Button Clicked')
        # Clean Up
        self.clear_window()

        action = self.tod.get_dare()
        self.summary_label.config(text=action)

    def clear_window(self):
        # Clean Up
        self.start_label.pack_forget()
        self.start_button.pack_forget()
        self.dropdown_menu.pack_forget()
        try:
            self.details_label.config(text="")
            self.summary_label.config(text="")
        except Exception as error:
            log.warning(error)
        

class SimpleUI:

    def __init__(self):
        self.root = tk.Tk()
    
    def run(self):
        App = GUI(self.root)
        App.load_start_screen()

        # Start the main event loop
        try:
            log.info('Starting Main Loop')
            self.root.mainloop()
        except Exception as error:
            log.error(error)