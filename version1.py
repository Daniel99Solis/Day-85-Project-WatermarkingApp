from tkinter import *
from tkinter.ttk import *  # Add styling to elements by creating style objects
from tkinter import filedialog as fd  # Create a file dialog object to select files from directory
from tkinter.messagebox import showinfo  # To show messagebox
from PIL import Image, ImageTk  # Library to manipulate images
import math

# Global variables to update the image in different functions
im = Image.open("static/image_default.png")
normal_width = 0
normal_height = 0
modify_width = 300
modify_height = 300
x_cor = 0
y_cor = 0
path_logo = "static/default_logo.png"
auxiliary_path_logo = ""
logo = ""
logo_width = 300
logo_height = 250


def drag(event):
    """Funtion to call when an element is drag with the left button of the mouse"""
    global f_img, logo_img, x_cor, y_cor, path_logo, auxiliary_path_logo
    x_cor = event.x
    y_cor = event.y
    l1.config(text='Position x : ' + str(event.x) + ", y : " + str(event.y))

    if auxiliary_path_logo == "":
        f_img = PhotoImage(file=path_logo)
    else:
        f_img = PhotoImage(file=auxiliary_path_logo)

    logo_img = canvas.create_image(event.x, event.y, image=f_img)


def select_file():
    """Function to select an image from a desire directory"""
    global im, normal_width, normal_height, modify_height, modify_width, img_to_edit, im_edit
    filetypes = (('png files', '*.png'), ('All files', '*.*'))

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    try:
        im = Image.open(filename)
    except AttributeError:
        print("No image was selected")
    else:
        normal_width = im.size[0]
        normal_height = im.size[1]
        modify_width = normal_width
        modify_height = normal_height
        while modify_width > 600:
            modify_width = round(modify_width / 2)
            modify_height = round(modify_height / 2)

        im = im.resize((modify_width, modify_height))

        # After selecting the image to update, we change the layout of the app
        label_app.pack_forget()
        label_description.pack_forget()
        select_file_button.pack_forget()

        label_app.grid(row=0, column=0, columnspan=2)
        label_description.config(text="This app allows you to add logos, images, \n "
                                      "etc to a current image and then \n save it inside a folder")
        label_description.grid(row=1, column=0, columnspan=2)
        select_file_button.grid(row=2, column=0, pady=5, columnspan=2)
        add_file_button.grid(row=3, column=0, pady=5, columnspan=2)
        save_button.grid(row=4, column=0, pady=5, columnspan=2)

        l1.grid(row=0, column=2)
        canvas.config(width=modify_width, height=modify_height)
        canvas.grid(row=1, column=2, rowspan=7)

        # With this we center the image the user pick inside the canvas
        x = math.floor(modify_width/2)
        y = math.floor(modify_height/2)
        img_to_edit = ImageTk.PhotoImage(im)
        im_edit = canvas.create_image(x, y, image=img_to_edit, anchor=CENTER)


def add_file():
    """Function to add files like images or logo to the image the user wants to edit"""
    global path_logo, auxiliary_path_logo, f_img, logo_img, logo_height, logo_width, x_cor, y_cor
    filetypes = (
        ('png files', '*.png'),
        ('All files', '*.*')
    )

    path_logo = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    print(path_logo)
    if path_logo == "":
        path_logo = "static/default_logo.png"
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

        # Here we initialize the scale for size of the logo image
        label_width_logo.config(text=f"Size: {logo_width} x {logo_height}")
        label_width_logo.grid(row=5, column=1)
        radiobutton_size.grid(row=6, column=0)
        scale_width.config(from_=50, to=logo_width, length=200, value=logo_width)
        scale_width.grid(row=6, column=1)

        # We also add the radio button for Dimensions (width and height) and the scale for it
        radiobutton_dim.grid(row=8, column=0)
        scale_height.config(from_=50, to=logo_height, length=200, value=logo_height)


def save_image():
    """Function to save image after the logo has been added"""
    global im, modify_height, modify_height, x_cor, y_cor, path_logo, logo, logo_width, logo_height
    global im_edit, img_to_edit

    # Open Logo to paste into the image to edit
    logo = Image.open(path_logo)
    logo = logo.resize((logo_width, logo_height))

    # Then we need to check if the logo has transparency in that case we need to converse it to RGBA
    logo.convert("RGBA")

    # Then we paste the logo in the image with the coordinates we get after dragging the logo
    # We need to do a little bit of calculations to have the logo where the user dragged it
    print(f"the new logo is {logo.size[0]} x {logo.size[1]}")
    center_width = round(logo.size[0]/2)
    center_height = round(logo.size[1]/2)
    im.paste(logo, (x_cor-center_width, y_cor-center_height))

    filetypes = (('png files', '*.png'), ('All Files', "*.*"))

    directory_to_save = fd.asksaveasfilename(
        title="Choose a directory and name to save",
        defaultextension=".png",
        filetypes=filetypes
    )

    try:
        im.save(directory_to_save)
    except ValueError:
        print("The operation was cancelled")
    else:
        showinfo(
            title='Saved Image',
            message=f'Your image has been successfully saved in {directory_to_save}'
        )

        # We also show the new image with the added logo in the canvas
        x = math.floor(modify_width / 2)
        y = math.floor(modify_height / 2)
        img_to_edit = PhotoImage(file=directory_to_save)
        im_edit = canvas.create_image(x, y, image=img_to_edit)


def adjust_width(value):
    """Function to adjust the width or the size of the logo image"""
    global logo_width,  logo_height, logo, path_logo, auxiliary_path_logo, f_img, logo_img
    logo_width = round(float(value))
    print(logo_width)

    # Creating the logo image from the path the user select to change size or dimensions
    logo = Image.open(path_logo)

    if radio_state.get() == "Size":
        # Adjusting the height base on the vale of the width
        factor = logo.size[0] / logo.size[1]
        diff = (logo.size[0] - logo_width)/factor
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
    """Function to adjust the height of the logo image"""
    global logo_width,  logo_height, logo, path_logo, auxiliary_path_logo, f_img, logo_img
    logo_height = round(float(value))
    print(logo_height)

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
        label_height_logo.grid(row=7, column=1)
        radiobutton_dim.grid(row=8, column=0)
        scale_height.config(value=logo_height)
        scale_height.grid(row=8, column=1)


# ------------------------ All of the application elements ------------------------------------- #
# Window
window = Tk()
window.title("Marky")
window.minsize(width=500, height=400)
window.maxsize(width=1000, height=800)
window.config(bg="black", padx=15, pady=15)

# Name App Label
label_app = Label(text="Marky", font=("Arial", 24, "italic"),
                  background="black", foreground="#4E4FEB", justify="center")
label_app.pack()

# Description Label
label_description = Label(text="This app allows you to add logos, images, etc  \n"
                               "to a current image and then save it inside a folder", font=("Arial", 12, "italic"),
                          background="black", foreground="#EEEEEE", justify="center", padding=15)
label_description.pack()

# Label to show the position when an element is drag inside the canvas
l1 = Label(window, text='Logo Position', background="black", foreground="white", font=30)

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

# This will create style object
style = Style()
style.configure('W.TButton', font=('calibri', 16, 'bold', 'underline'), foreground='#4E4FEB')

# Buttons to select, add and save
select_file_button = Button(window, text='Select File', style='W.TButton', command=select_file)
select_file_button.pack()

add_file_button = Button(window, text='Add Image', style='W.TButton', command=add_file)

save_button = Button(window, text='Save Image', style='W.TButton', command=save_image)

# Scale to modify width of the logo
label_width_logo = Label(window, text='Size: ', background="black", foreground="white", font=30)
radio_state = StringVar(value="Size")
style.configure("TRadiobutton", background="black",
                foreground="#4E4FEB", font=("arial", 14, "bold"))
radiobutton_size = Radiobutton(text="Size", value="Size", variable=radio_state, command=radio_used,
                               style="TRadiobutton")
scale_width = Scale(from_=0, to=100, command=adjust_width)

# Scale to modify height of the logo
label_height_logo = Label(window, text='Height: ', background="black", foreground="white", font=30)
radiobutton_dim = Radiobutton(text="Dim", value="Dim", variable=radio_state, command=radio_used)
scale_height = Scale(from_=0, to=100, command=adjust_height)

window.mainloop()
