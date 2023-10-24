import tkinter  # This library was just useful to add background to a Frame
from tkinter import *  # This library is to use all the elements inside the library
from tkinter.ttk import *  # Add styling to elements by creating style objects
from tkinter import filedialog as fd  # Create a file dialog object to select files from directory
from tkinter.messagebox import showinfo, askyesnocancel, showwarning  # To show messagebox
from PIL import Image, ImageTk  # Library to manipulate images
import math  # Library to round the pixels
# Created libraries
from clean import clean_folder, delete_files  # Library to delete files from a folder
from save_window import SaveWindow  # Library to create the save window

# Variables
im = Image.open("static/image_default.png")  # Default image to edit
normal_width = 0  # Normal width of the selected image to edit
normal_height = 0  # Normal height of the selected image to edit
modify_width = 0  # Modify width to fit the image to edit in the screen
modify_height = 0  # Modify width to fit the image to edit in the screen
x_cor = 0  # X coordinate of the logo over the image to edit
y_cor = 0  # Y coordinate of the logo over the image to edit
path_logo = ""  # Default logo Path
auxiliary_path_logo = "static/default_logo.png"  # Auxiliary logo Path to show it to the user
logo = ""  # Image object to edit logo with Pillow
logo_width = 0  # Logo width
logo_height = 0  # Logo height
current_version = 0  # Variable to keep track the current version
max_num_version = 0  # Variable to keep track of the maximum number of versions created by the user


# --------------- Definition of event for the buttons or actions with the mouse ---------------- #
def drag(event):
    """Funtion to call when an element is drag with the left button of the mouse"""
    global f_img, logo_img, x_cor, y_cor, path_logo, auxiliary_path_logo
    x_cor = event.x
    y_cor = event.y
    l1.config(text='Logo position x : ' + str(event.x) + ", y : " + str(event.y))

    if auxiliary_path_logo == "":
        f_img = PhotoImage(file=path_logo)
    else:
        f_img = PhotoImage(file=auxiliary_path_logo)

    logo_img = canvas.create_image(event.x, event.y, image=f_img)


def select_file():
    """Function to select an image to be edited"""
    global im, normal_width, normal_height, modify_height, modify_width, img_to_edit, im_edit
    global current_version, max_num_version, path_logo

    filetypes = (('png files', '*.png'), ('All files', '*.*'))

    filename = fd.askopenfilename(title='Select Image to Edit', initialdir='/', filetypes=filetypes)

    try:
        im = Image.open(filename)
    except AttributeError:
        print("No image was selected")
    else:
        normal_width = im.size[0]
        normal_height = im.size[1]
        modify_width = normal_width
        modify_height = normal_height
        # We resize the image if it is too big to edit
        while modify_width > 600:
            modify_width = round(modify_width / 2)
            modify_height = round(modify_height / 2)

        # Here we clean the "back-versions" in case there will be from previous editions
        clean_folder()

        current_version = 0  # We also reinitialized the current version
        max_num_version = 0  # We also reinitialized the max number of versions
        im = im.resize((modify_width, modify_height))
        im.save(f"back-versions/version{current_version}.png")

        # After selecting the image to update, we change the layout of the app
        label_app.pack_forget()
        label_description.pack_forget()
        select_file_button.pack_forget()
        label_copyright.pack_forget()

        # New layout with grid
        label_app.grid(row=0, column=0, columnspan=2, rowspan=2)
        Top.grid(row=0, column=2, columnspan=3, sticky=NSEW)
        label_inst.config(text="Click the button 'Add Image' to add a logo or any image you want. If no image is \n "
                               "selected the default will be placed. You can hold the left click inside your \n"
                               "image to move the logo.")
        label_inst.grid(row=1, column=2, columnspan=3)
        canvas.config(width=modify_width, height=modify_height)
        canvas.grid(row=2, column=2, columnspan=3, rowspan=9)

        label_description.config(text="This app allows you to add logos, images, \n "
                                      "etc to a current image and then \n save it inside a folder")
        label_description.grid(row=2, column=0, columnspan=2)
        select_file_button.grid(row=3, column=0, pady=5, columnspan=2)
        add_file_button.grid(row=4, column=0, pady=5, columnspan=2)
        apply_changes_button.grid(row=5, column=0, pady=5, columnspan=2)
        save_button.grid(row=6, column=0, pady=5, columnspan=2)

        img_label_width.config(text=f"Width: {modify_width} px")
        img_label_width.grid(row=11, column=2, columnspan=3)
        img_label_height.config(text=f"Height: {modify_height} px")
        img_label_height.grid(row=2, column=5, rowspan=9)

        label_copyright.grid(row=12, column=0, columnspan=6)

        # We disable the apply button if the logo is the default by the app
        if path_logo == "static/default_logo.png":
            apply_changes_button["state"] = "disabled"

        # We always disable the save_button when a new image is selected
        save_button["state"] = "disabled"

        # With this we center the image the user pick inside the canvas
        x = math.floor(modify_width / 2)
        y = math.floor(modify_height / 2)
        img_to_edit = ImageTk.PhotoImage(im)
        im_edit = canvas.create_image(x, y, image=img_to_edit, anchor=CENTER)


def add_file():
    """Function to add files like images or logo to the image the user wants to edit"""
    global path_logo, auxiliary_path_logo, f_img, logo_img, logo_height, logo_width, x_cor, y_cor

    filetypes = (('png files', '*.png'), ('All files', '*.*'))

    path_logo = fd.askopenfilename(title='Select an Image to Add', initialdir='/', filetypes=filetypes)

    if path_logo == "":
        path_logo = auxiliary_path_logo
    else:
        auxiliary_path_logo = path_logo

    # This auxiliary is to add the intervals to the scales depending on the dimension of the logo
    try:
        auxiliary_logo = Image.open(path_logo)
    except AttributeError:
        print("No image or logo was selected")
    else:
        f_img = PhotoImage(file=path_logo)
        logo_img = canvas.create_image(x_cor, y_cor, image=f_img)

        # Here we initialize the initial dimensions of the logo
        logo_width = auxiliary_logo.size[0]
        logo_height = auxiliary_logo.size[1]

        # We change the label instructions message
        label_inst.config(text="Once you set the dimensions and position of the logo, you can apply the changes \n"
                               "with the 'Apply Button'")

        # We enable the Apply Button
        apply_changes_button["state"] = "normal"

        # Here we initialize the scale for size of the logo image
        label_width_logo.config(text=f"Size: {logo_width} x {logo_height}")
        label_width_logo.grid(row=7, column=1, pady=3)
        radiobutton_size.grid(row=8, column=0)
        scale_width.config(from_=50, to=logo_width * 2, length=200, value=logo_width)
        scale_width.grid(row=8, column=1)

        # We also add the radio button for Dimensions (width and height) and the scale for it
        radiobutton_dim.grid(row=10, column=0)
        scale_height.config(from_=50, to=logo_height * 2, length=200, value=logo_height)


def apply():
    """Function to apply change after a logo has been added"""
    global im, modify_height, modify_height, x_cor, y_cor, path_logo, logo, logo_width, logo_height
    global im_edit, img_to_edit, current_version, max_num_version

    apply_change = askyesnocancel(title="Apply Changes", message="Are you sure you want to apply the change?")

    if apply_change:
        # Open Logo to paste into the image to edit
        logo = Image.open(path_logo)
        logo = logo.resize((logo_width, logo_height))

        # Then we need to check if the logo has transparency in that case we need to converse it to RGBA
        logo = logo.convert("RGBA")

        # Then we paste the logo in the image with the coordinates we get after dragging the logo
        # We need to do a little bit of calculations to have the logo where the user dragged it
        print(f"the new logo is {logo.size[0]} x {logo.size[1]}")
        center_width = round(logo.size[0] / 2)
        center_height = round(logo.size[1] / 2)
        im.paste(logo, (x_cor - center_width, y_cor - center_height), logo)

        # We update the new version and also the max number of versions
        current_version += 1
        if max_num_version >= current_version:
            delete_files(from_=max_num_version, to_=current_version)
            # We initialized the max_num_version if the user decides to make changes from a specific version
            max_num_version = current_version
        else:
            max_num_version += 1
        im.save(f"back-versions/version{current_version}.png")

        # We also show the new image with the added logo in the canvas
        x = math.floor(modify_width / 2)
        y = math.floor(modify_height / 2)
        img_to_edit = PhotoImage(file=f"back-versions/version{current_version}.png")
        im_edit = canvas.create_image(x, y, image=img_to_edit)

        # We change the text to show in the instructions label
        label_inst.config(text="You can undo or redo changes with the top buttons or 'Save' the edited image \n"
                               "with the name and inside the folder of your choice")

        # We show a feedback message that the change has been applied
        showinfo(
            title='Change Applied',
            message=f'The change has been applied you can add more images or undo changes if you want.'
        )

        # Now that we have a new version we enable the undo and redo buttons
        undo_button["state"] = "normal"
        redo_button["state"] = "normal"
        save_button["state"] = "normal"


def adjust_width(value):
    """Functions to adjust the size or width of the logo image"""
    global logo_width, logo_height, logo, path_logo, auxiliary_path_logo, f_img, logo_img
    logo_width = round(float(value))

    # Creating the logo image from the path the user select to change size or dimensions
    logo = Image.open(path_logo)

    if radio_state.get() == "Size":
        # Adjusting the height base on the vale of the width
        factor = logo.size[0] / logo.size[1]
        diff = (logo.size[0] - logo_width) / factor
        logo_height = int(logo.size[1] - diff)
        adjust_logo = logo.resize((logo_width, logo_height))
        # Showing the dimensions of the logo
        label_width_logo.config(text=f"Size: {logo_width} x {logo_height}")
    else:
        adjust_logo = logo.resize((logo_width, logo_height))
        label_width_logo.config(text=f"Width: {logo_width}")
        label_height_logo.config(text=f"Height: {logo_height}")

    # Saving the logo in a new path to just show it to the user
    adjust_logo.save("static/auxiliary_logo.png")
    auxiliary_path_logo = "static/auxiliary_logo.png"

    # Show the new image to the user
    f_img = PhotoImage(file=auxiliary_path_logo)
    logo_img = canvas.create_image(x_cor, y_cor, image=f_img)


def adjust_height(value):
    """Functions to adjust the height of the logo image"""
    global logo_width, logo_height, logo, path_logo, auxiliary_path_logo, f_img, logo_img
    logo_height = round(float(value))

    if radio_state.get() == "Dim":
        logo = Image.open(path_logo)
        adjust_logo = logo.resize((logo_width, logo_height))
        label_width_logo.config(text=f"Width: {logo_width}")
        label_height_logo.config(text=f"Height: {logo_height}")
        adjust_logo.save("static/auxiliary_logo.png")
        auxiliary_path_logo = "static/auxiliary_logo.png"

    f_img = PhotoImage(file=auxiliary_path_logo)
    logo_img = canvas.create_image(x_cor, y_cor, image=f_img)


def radio_used():
    """Function to select modify size or dimensions of the logo image"""
    global logo_width, logo_height
    print(radio_state.get())
    if radio_state.get() == "Size":
        label_height_logo.grid_forget()
        scale_height.grid_forget()
        label_width_logo.config(text=f"Size: {logo_width} x {logo_height}")
    else:
        # show scale to adjust height logo image
        label_width_logo.config(text=f"Width: {logo_width}")
        label_height_logo.config(text=f"Height: {logo_height}")
        label_height_logo.grid(row=9, column=1, pady=3)
        radiobutton_dim.grid(row=10, column=0)
        scale_height.config(value=logo_height)
        scale_height.grid(row=10, column=1)


def undo():
    """Function to undo changes that has been added to the image"""
    global current_version, img_to_edit, im_edit, modify_height, modify_width, im

    if current_version > 0:
        print("Undo operation")
        current_version -= 1
        x = math.floor(modify_width / 2)
        y = math.floor(modify_height / 2)
        img_to_edit = PhotoImage(file=f"back-versions/version{current_version}.png")
        im = Image.open(f"back-versions/version{current_version}.png")
        im_edit = canvas.create_image(x, y, image=img_to_edit)
    else:
        showwarning(
            title='No previous',
            message=f'There are no more previous versions! Please, '
                    f'"Apply" your current change or continue with the edition'
        )


def redo():
    """Function to redo changes that has been added to the image"""
    global current_version, max_num_version, im, img_to_edit, im_edit, modify_height, modify_width, im

    if current_version < max_num_version:
        print("Redo operation")
        current_version += 1
        x = math.floor(modify_width / 2)
        y = math.floor(modify_height / 2)
        img_to_edit = PhotoImage(file=f"back-versions/version{current_version}.png")
        im = Image.open(f"back-versions/version{current_version}.png")
        im_edit = canvas.create_image(x, y, image=img_to_edit)
    else:
        showwarning(
            title='No previous',
            message=f'There are no more further versions! Please, "Apply" more changes or save your image.'
        )


def save_window():
    """Function that opens a new window to add the Settings to the image to be saved"""
    window_save = SaveWindow(window)
    window_save.create_image_objects(current_version=current_version)
    window_save.create_init_layout(version=current_version,
                                   widthN=normal_width,
                                   heightN=normal_height,
                                   widthM=modify_width, heightM=modify_height, styleT=style)
    window_save.grab_set()
    window_save.mainloop()


# ------------------------ All of the application elements ------------------------------------- #
# Window
window = Tk()
window.title("Marky")
window.minsize(width=500, height=400)
window.maxsize(width=1200, height=900)
window.config(bg="black", padx=15, pady=15)

# Styles to the elements
style = Style()
style.configure("M.TLabel", font=("Arial", 12, "italic"), background="black", foreground="#EEEEEE", justify="center",
                padding=5)
style.configure("S.TLabel", background="black", foreground="white", font=30, justify="center")
style.configure('W.TButton', font=('calibri', 16, 'bold', 'underline'), foreground='#4E4FEB')
style.configure("TRadiobutton", background="black", foreground="#4E4FEB", font=("arial", 14, "bold"))

# Name App Label
label_app = Label(text="Marky", font=("Arial", 24, "italic"), background="black", foreground="#4E4FEB",
                  justify="center")
label_app.pack()

# Frame to put inside the undo, redo y logo position widgets with better style
Top = tkinter.Frame(window, background="black")
Top.grid_columnconfigure(0, weight=0)
Top.grid_columnconfigure(1, weight=0)
Top.grid_columnconfigure(2, weight=1)
# Button undo to delete changes
image_undo = PhotoImage(file="static/undo-symbol.png")
undo_button = Button(Top, text="undo", image=image_undo, command=undo)
undo_button["state"] = "disabled"
undo_button.grid(row=0, column=0, padx=5, sticky=NSEW)
# Button redo to apply again the change
image_redo = PhotoImage(file="static/redo-symbol.png")
redo_button = Button(Top, text="redo", image=image_redo, command=redo)
redo_button["state"] = "disabled"
redo_button.grid(row=0, column=1, padx=5, sticky=NSEW)
# Label to show the position when an element is drag inside the canvas
l1 = Label(Top, text='Logo Position', style="S.TLabel")
l1.grid(row=0, column=2, sticky=NS)

# Label Instructions
label_inst = Label(text="Instructions to use the app", style="M.TLabel")

# Description Label
label_description = Label(text="This app allows you to add logos, images, etc  \n"
                               "to a current image and then save it inside a folder", style="M.TLabel")
label_description.pack()

# Canvas where the images will be drag
canvas = Canvas(window, width=modify_width, height=modify_height, background="white", highlightthickness=0)
# Default image to edit in the canvas
img_to_edit = PhotoImage(file="static/image_default.png")
im_edit = canvas.create_image(0, 0, image=img_to_edit)  # Here we specify the position in X and Y
# Default logo or image to add to user's image
f_img = PhotoImage(file=path_logo)
logo_img = canvas.create_image(0, 0, image=f_img)
# Adding event when the left click of the mouse is press and drag
canvas.bind('<B1-Motion>', drag)

# Label to show the height of the image
img_label_height = Label(text="Height: ", style="M.TLabel")

# Buttons to select, add, apply and save
select_file_button = Button(window, text='Select File', style='W.TButton', command=select_file)
select_file_button.pack()
add_file_button = Button(window, text='Add Image', style='W.TButton', command=add_file)
apply_changes_button = Button(window, text='Apply', style='W.TButton', command=apply)
save_button = Button(window, text='Save Image', style='W.TButton', command=save_window)

# Scale to modify width of the logo
radio_state = StringVar(value="Size")
label_width_logo = Label(window, text='Size: ', style="S.TLabel")
radiobutton_size = Radiobutton(text="Size", value="Size", variable=radio_state, command=radio_used,
                               style="TRadiobutton")
scale_width = Scale(from_=0, to=100, command=adjust_width)

# Scale to modify height of the logo
label_height_logo = Label(window, text='Height: ', style="S.TLabel")
radiobutton_dim = Radiobutton(text="Dim", value="Dim", variable=radio_state, command=radio_used)
scale_height = Scale(from_=0, to=100, command=adjust_height)

# Label to show the width of the image
img_label_width = Label(text="Width: ", style="M.TLabel")

# Copyright Label
label_copyright = Label(text="Copyright © Daniel Solis", style="M.TLabel")
label_copyright.pack()

window.mainloop()
