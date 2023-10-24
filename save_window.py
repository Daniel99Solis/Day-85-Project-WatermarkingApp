from tkinter import *
from tkinter.ttk import *  # Add styling to elements by creating style objects
from tkinter import filedialog as fd  # Create a file dialog object to select files from directory
from tkinter.messagebox import showinfo  # To show messagebox
from PIL import Image  # Library to manipulate images
import math
import os

actual_version = ""
width_normal = 0
height_normal = 0
width_modify = 0
height_modify = 0


class SaveWindow(Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Settings")
        self.minsize(width=500, height=400)
        self.maxsize(width=1000, height=800)
        self.config(bg="black", padx=15, pady=15)
        self.image_edited = ""
        self.drop_photo = ""
        self.user_selection = ""

    def create_image_objects(self, current_version):
        """Function that creates images objects because they need to be initialized"""
        self.image_edited = PhotoImage(file=f"back-versions/version{current_version}.png")
        self.drop_photo = PhotoImage(file="static/arrow-drop.png")

    def create_init_layout(self, version, widthN, heightN, widthM, heightM, styleT):
        """Function to create the initial Layout of the Save Window"""
        global actual_version, width_modify, height_modify, height_normal, width_normal
        actual_version = version
        width_normal = widthN
        height_normal = heightN
        width_modify = widthM
        height_modify = heightM

        def select(value):
            """Function that change the layout of saveWindow based on the user's choice"""
            global width_normal, height_normal, width_modify, height_modify
            self.user_selection = value
            label_image_width.grid_forget()
            label_image_height.grid_forget()
            entry_width.grid_forget()
            entry_height.grid_forget()
            width_modify = width_normal
            height_modify = height_normal
            entry_width.config(from_=50, to=1920)
            if value == "Do not resize":
                label_inst.config(text="Your image will be saved \n with its original dimensions.")
                label_current_width.config(text=f"Width: {width_modify} px")
                label_current_height.config(text=f"Height: {height_modify} px")
            elif value == "Exact width":
                width_value.set(width_modify)
                label_inst.config(text="Select the width and the height \n will be set automatically.")
                label_image_width.config(text="Width: ")
                label_image_width.grid(row=4, column=0, columnspan=2, sticky=W)
                entry_width.grid(row=5, column=0, columnspan=2)
            elif value == "Exact height":
                height_value.set(height_modify)
                label_inst.config(text="Select the height and the width \n will be set automatically.")
                label_image_height.grid(row=4, column=0, columnspan=2, sticky=W)
                entry_height.grid(row=5, column=0, columnspan=2)
            elif value == "Exact width and height":
                width_value.set(width_modify)
                height_value.set(height_modify)
                label_inst.config(text="Select both height and width.")
                label_image_width.config(text="Width: ")
                label_image_width.grid(row=4, column=0, sticky=W)
                label_image_height.grid(row=4, column=1, sticky=W)
                entry_width.grid(row=5, column=0)
                entry_height.grid(row=5, column=1)
            else:
                width_value.set(100)
                label_inst.config(text="Select a percentage value of \n the original dimensions")
                label_image_width.config(text="Percentage: ")
                entry_width.config(from_=0, to=100)
                label_image_width.grid(row=4, column=0, columnspan=2, sticky=W)
                entry_width.grid(row=5, column=0, columnspan=2)

        def select_folder_fun():
            """Function that allows to select a folder and a name to save the image"""
            global width_modify, height_modify
            im = Image.open(f"back-versions/version{version}.png")
            im_to_save = im.resize((width_modify, height_modify))

            filetypes = (('png files', '*.png'), ('All Files', "*.*"))

            directory_to_save = fd.asksaveasfilename(title="Choose a directory and name to save",
                                                     defaultextension=".png", filetypes=filetypes)
            try:
                im_to_save.save(directory_to_save)
            except ValueError:
                print("The operation was cancelled")
            else:
                showinfo(title='Saved Image', message=f'Your image has been successfully saved in {directory_to_save}')
                path = os.path.realpath(directory_to_save)
                os.startfile(path)

        # Label of the title of the New window
        label_save_window = Label(self, text="Settings", font=("Arial", 24, "italic"),
                                  background="black", foreground="#4E4FEB", justify="center", padding=5)
        label_save_window.grid(row=0, column=0, columnspan=2)

        # Label Resize Image
        label_resize = Label(self, text="Resize Image: ", style="M.TLabel")
        label_resize.grid(row=1, column=0, sticky=W)

        # Drop Down Menu to show the options
        style_drop = Style()
        style_drop.configure('TButton', font=('calibri', 16, 'bold'), foreground='#4E4FEB')
        options = ["", "Do not resize", "Exact width", "Exact height", "Exact width and height", "Percentage"]
        # datatype of menu text
        clicked = StringVar(value="Do not resize")
        # Create Dropdown menu
        drop = OptionMenu(self, clicked, *options, command=select, style="TButton")
        drop.config(image=self.drop_photo, compound=RIGHT)
        drop["menu"].configure(font=('calibri', 16, 'bold'), foreground='#4E4FEB')
        drop.grid(row=2, column=0, columnspan=2, padx=10)

        # Label to show the instructions to the user base on her or his choice
        label_inst = Label(self, text="Your image will be saved \n with its original dimensions",
                           font=("Arial", 12, "italic"),
                           background="black", foreground="#EEEEEE", justify="left", anchor="w", padding=5)
        label_inst.grid(row=3, column=0, columnspan=2)

        # Label and entries to show to the user base on her or his choice
        label_image_width = Label(self, text="Width: ", font=("Arial", 12, "italic"),
                                  background="black", foreground="#EEEEEE", justify="left", anchor="w", padding=5)
        label_image_height = Label(self, text="Height: ", font=("Arial", 12, "italic"),
                                   background="black", foreground="#EEEEEE", justify="left", anchor="w", padding=5)

        def spinbox_width():
            """Function to modify the width or percentage of the image"""
            global width_modify, height_modify, width_normal, height_normal
            value = int(entry_width.get())
            if self.user_selection == "Exact width":
                width_modify = value
                factor = width_normal / height_normal
                diff = (width_normal - value) / factor
                height_modify = int(height_normal - diff)
            elif self.user_selection == "Percentage":
                width_modify = math.floor((width_normal * value) / 100)
                height_modify = math.floor((height_normal * value) / 100)
            else:
                width_modify = value
            label_current_width.config(text=f"Width: {width_modify} px")
            label_current_height.config(text=f"Height: {height_modify} px")

        width_value = IntVar(self)
        entry_width = Spinbox(self, from_=50, to=1920, width=5, command=spinbox_width, textvariable=width_value,
                              font=("Arial", 12, "italic"),
                              background="black", foreground="black", justify="left")

        def spinbox_height():
            """Function to modify the width of the image"""
            global height_modify, width_modify, height_normal, width_normal
            value = int(entry_height.get())
            if self.user_selection == "Exact height":
                height_modify = value
                factor = height_normal / width_normal
                diff = (height_normal - value) / factor
                width_modify = int(width_normal - diff)
            else:
                height_modify = value

            label_current_width.config(text=f"Width: {width_modify} px")
            label_current_height.config(text=f"Height: {height_modify} px")

        height_value = IntVar(self)
        entry_height = Spinbox(self, from_=50, to=1080, width=5, command=spinbox_height, textvariable=height_value,
                               font=("Arial", 12, "italic"),
                               background="black", foreground="black", justify="left")

        # Button to select the folder where the image will be saved
        select_folder_button = Button(self, text="Select Folder", style='W.TButton', command=select_folder_fun)
        select_folder_button.grid(row=6, column=0, columnspan=2, pady=5)

        # Label to show a message to the user base on its current choice
        label_message = Label(self, text="Your image will be saved with the next dimensions", style="M.TLabel")
        label_message.grid(row=0, column=2)

        # Canvas to show the image
        canvas_save = Canvas(self, width=width_modify, height=height_modify, background="white",
                             highlightthickness=0)
        x_pos_im = math.floor(width_modify / 2)
        y_pos_im = math.floor(height_modify / 2)
        label_image = canvas_save.create_image(x_pos_im, y_pos_im, image=self.image_edited, anchor=CENTER)
        canvas_save.grid(row=1, column=2, rowspan=6)

        # Labels to show the values of the edited image
        label_current_width = Label(self, text=f"Width: {width_normal} px", style="M.TLabel")
        label_current_width.grid(row=7, column=2)
        label_current_height = Label(self, text=f"Height: {height_normal} px", style="M.TLabel")
        label_current_height.grid(row=1, column=3, rowspan=6)

        # Copyright Label
        label_copy_savewindow = Label(self, text="Copyright © Daniel Solis", style="M.TLabel")
        label_copy_savewindow.grid(row=8, column=0, columnspan=4)

        # We set the initial width and height with the values of the real image
        width_modify = width_normal
        height_modify = height_normal
